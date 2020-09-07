import sys
from polygon_rest.models import Dot, Rectangle, FRectangle, MAX_COUNT_C, MAX_COUNT

eps = sys.float_info.epsilon * 10000000000


def create_dot(x, y, desc='Пустая точка'):
    dot = Dot()
    dot.desc = desc
    dot.x = x
    dot.y = y
    return dot


temp_dots_list = {}
cache_count = 19


def paste(to, dot):
    """ Paste dot in rectangle """

    if to not in temp_dots_list.keys():
        temp_dots_list[to] = [dot]
    else:
        temp_dots_list[to].append(dot)
    if len(temp_dots_list[to]) > cache_count:
        dots_list = []
        for dot in temp_dots_list[to]:
            dot.save()
            dots_list.append(dot)
            to.frectangle.dots.add(*dots_list)
            temp_dots_list.clear()
    return True


def create_rectangle(dots):
    (d0, d1, d2, d3) = dots
    if all([d0.y == d1.y, d0.x == d3.x, d1.x == d2.x, d2.y == d3.y]):
        if d0.x < d1.x and d0.y > d2.y:
            d0.save()
            d1.save()
            d2.save()
            d3.save()
            rectangle = Rectangle.objects.create(d0=d0, d1=d1, d2=d2, d3=d3)
            return rectangle
        else:
            raise Exception('Bad rectangle')
    else:
        raise Exception('Bad rectangle')


def create_Frectangle(dots):
    (d0, d1, d2, d3) = dots
    # print(d0.info(), d1.info(), d2.info(), d3.info())
    if all([d0.y == d1.y, d0.x == d3.x, d1.x == d2.x, d2.y == d3.y]):
        if d0.x < d1.x and d0.y > d2.y:
            dt0 = create_dot(d0.x, d0.y)
            dt0.save()
            dt1 = create_dot(d1.x, d1.y)
            dt1.save()
            dt2 = create_dot(d2.x, d2.y)
            dt2.save()
            dt3 = create_dot(d3.x, d3.y)
            dt3.save()
            frectangle = FRectangle.objects.create(d0=dt0, d1=dt1, d2=dt2, d3=dt3)
            frectangle.save()  # dots in rectangle
            return frectangle
        else:
            print('не правильный порядок вершин f', (d0, d1, d2, d3))
    else:
        print('это не прямоугольник F')


def get_eps_dots(dot, number):
    if number == 0:
        dot0 = create_dot(x=dot.x, y=dot.y)
        dot1 = create_dot(dot.x + eps, dot.y)
        dot2 = create_dot(dot.x + eps, dot.y - eps)
        dot3 = create_dot(dot.x, dot.y - eps)
        return dot0, dot1, dot2, dot3

    if number == 1:
        dot1 = create_dot(x=dot.x, y=dot.y)
        dot0 = create_dot(dot.x - eps, dot.y)
        dot2 = create_dot(dot.x, dot.y - eps)
        dot3 = create_dot(dot.x - eps, dot.y - eps)
        return dot0, dot1, dot2, dot3

    if number == 2:
        dot2 = create_dot(x=dot.x, y=dot.y)
        dot1 = create_dot(dot.x, dot.y + eps)
        dot0 = create_dot(dot.x - eps, dot.y + eps)
        dot3 = create_dot(dot.x - eps, dot.y)
        return dot0, dot1, dot2, dot3

    if number == 3:
        dot3 = create_dot(x=dot.x, y=dot.y)
        dot0 = create_dot(dot.x, dot.y + eps)
        dot2 = create_dot(dot.x + eps, dot.y)
        dot1 = create_dot(dot.x + eps, dot.y + eps)
        return dot0, dot1, dot2, dot3


def search_of_four(rect):
    middle_x = (rect.d1.x + rect.d0.x) / 2
    middle_y = (rect.d3.y + rect.d0.y) / 2
    dot0 = create_dot(x=middle_x, y=middle_y)
    dot1 = create_dot(x=middle_x + eps / 2, y=middle_y)
    dot2 = create_dot(x=middle_x + eps / 2, y=middle_y - eps / 2)
    dot3 = create_dot(x=middle_x, y=middle_y - eps / 2)

    return dot0, dot1, dot2, dot3


def check_is_not_f(rect):
    try:
        type(rect.frectangle)
    except:
        return True
    return False


def check_count(node, rect):
    """ check frectangle count """
    if rect.frectangle.dots.count() > MAX_COUNT:
        (d0, d1, d2, d3) = rect.get_dots()
        lu, ru, rd, ld = search_of_four(rect)

        temp_lu = create_Frectangle(dots=(d0, create_dot(x=lu.x, y=d0.y),
                                          lu, create_dot(x=d0.x, y=lu.y)))

        temp_ru = create_Frectangle(dots=(create_dot(x=ru.x, y=d0.y),
                                          d1, create_dot(x=d1.x, y=ru.y), ru))

        temp_rd = create_Frectangle(dots=(rd, create_dot(x=d2.x, y=rd.y),
                                          d2, create_dot(x=rd.x, y=d2.y)))

        temp_ld = create_Frectangle(dots=(create_dot(x=d3.x, y=ld.y), ld,
                                          create_dot(x=ld.x, y=d3.y), d3))

        for i in rect.frectangle.dots.all():
            if i.dot_in(rect=temp_lu):
                paste(to=temp_lu, dot=i)
            elif i.dot_in(rect=temp_ru):
                paste(to=temp_ru, dot=i)
            elif i.dot_in(rect=temp_rd):
                paste(to=temp_rd, dot=i)
            else:
                paste(to=temp_ld, dot=i)
        rect.frectangle.dots.clear()
        rect.delete()
        node.children.add(temp_lu, temp_ru, temp_rd, temp_ld)

        return True
    else:
        return False


def check_children(node, temp_children, dot):
    for rect in temp_children:
        if dot.dot_in(rect):
            if not insert_in(rect, dot):
                return False
            if not check_is_not_f(rect):
                if check_count(node=node, rect=rect):
                    count = 0
                    for fre in node.children.all():
                        if not check_is_not_f(fre):
                            count += 1
                        if count > MAX_COUNT_C:
                            future_list = []
                            for child in node.children.all():
                                (d0, d1, d2, d3) = child.get_dots()
                                temp = create_rectangle(dots=(d0, d1, d2, d3))
                                node.children.remove(child)
                                temp.children.add(child)
                                future_list.append(temp)
                            node.children.add(*future_list)
                            break
            return True


def insert_in(node, dot):
    if check_is_not_f(node):
        if node.children.count() != 0:
            temp_children = node.children.all()
            if check_children(node=node, temp_children=temp_children, dot=dot):
                return True
            distances = [dot.distance(child)[0] for child in temp_children]
            numb_min = distances.index(min(distances))
            temp_dist, numb_dot = dot.distance(temp_children[numb_min])
            temp_children[numb_min].expand(dot=dot, number=numb_dot)
            insert_in(temp_children[numb_min], dot)
            return True

        else:
            if create_dot(x=(dot.x + eps), y=(dot.y + eps)).dot_in(rect=node):
                node.children.add(create_Frectangle(dots=get_eps_dots(dot, 3)))
                paste(node.children.all()[0].frectangle, dot=dot)
                return True
            elif create_dot(x=dot.x - eps, y=dot.y - eps).dot_in(rect=node):
                node.children.add(create_Frectangle(dots=get_eps_dots(dot, 1)))
                paste(node.children.all()[0].frectangle, dot=dot)
                return True
            elif create_dot(x=dot.x - eps, y=dot.y + eps).dot_in(rect=node):
                node.children.add(create_Frectangle(dots=get_eps_dots(dot, 2)))
                paste(node.children.all()[0].frectangle, dot=dot)
                return True
            elif create_dot(x=dot.x + eps, y=dot.y - eps).dot_in(rect=node):
                node.children.add(create_Frectangle(dots=get_eps_dots(dot, 0)))
                paste(to=node.children.all()[0].frectangle, dot=dot)
                return True
            else:
                raise Exception('bad dot', 'bad dot')
    else:
        paste(to=node, dot=dot)
        return True


temp_res = []


def search(node, dot, R, K):
    if check_is_not_f(node):
        if node.rect_in_circ(c=dot, r=R):
            for child in node.children.select_related('children_a').all():
                if len(temp_res) >= K:
                    search(child, dot, R=temp_res[-1][0], K=K)
                else:
                    search(child, dot, R, K=K)
    elif node.rect_in_circ(c=dot, r=R):
        for elem in node.frectangle.dots.all():
            if elem.dot_in_circ(c=dot, r=R):
                if len(temp_res) < K:
                    temp_res.append([elem.dot_distance(dot=dot), elem.x])
                    temp_res.sort()
                else:
                    if temp_res[-1][0] > elem.dot_distance(dot):
                        temp_res.pop(K - 1)
                        temp_res.append([elem.dot_distance(dot), elem])
                        temp_res.sort()

import sys
import asyncio
from polygon_rest.models import Dot, Rectangle, FRectangle, MAX_COUNT_C, MAX_COUNT, MIN_COUNT

# Functions
eps = sys.float_info.epsilon * 10000000000


def create_dot(x, y, desc='Пустая точка'):
    dot = Dot()
    dot.desc = desc
    dot.x = x
    dot.y = y
    return dot


temp_dots_list = {}


def paste(to, dot):
    """ Paste dot in rectangle """

    if to not in temp_dots_list.keys():
        temp_dots_list[to] = [dot]
    else:
        temp_dots_list[to].append(dot)
    if len(temp_dots_list[to]) > 19:
        dots_list = []
        for dot in temp_dots_list[to]:
            dot.save()
            dots_list.append(dot)
            # return True
            to.frectangle.dots.add(*dots_list)
            temp_dots_list.clear()

    return True

    # if type(dot) == Dot:
    # print('вставка точки')
    # dot.save()  # собственно сохранение
    # to.frectangle.dots.add(dot)

    # print('ошибка в paste', dot.info())
    # return False

    # else:
    #   pass
    # print('это не точка')


def create_rectangle(dots):
    (d0, d1, d2, d3) = dots
    if all([d0.y == d1.y, d0.x == d3.x, d1.x == d2.x, d2.y == d3.y]):
        if d0.x < d1.x and d0.y > d2.y:

            # Dot.objects.bulk_create(
            #    objs=[d0, d1, d2, d3]
            # )

            d0.save()
            d1.save()
            d2.save()
            d3.save()
            rectangle = Rectangle.objects.create(d0=d0, d1=d1, d2=d2, d3=d3)
            # rectangle.children.set([])
            # rectangle.save()  # промежуточные вершины
            return rectangle
        else:
            print('не правильный порядок вершин', (d0, d1, d2, d3))
    else:
        print('это не прямоугольник')


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
        # need separation
        (d0, d1, d2, d3) = rect.get_dots()
        # if not all([d0.y == d1.y, d0.x == d3.x, d1.x == d2.x, d2.y == d3.y]):
        #    print('сломан до check_count')
        lu, ru, rd, ld = search_of_four(rect)

        # print(l, r, d0, d1, d2, d3)
        # print('11')
        # print(lu.info(), ru.info(), rd.info(), ld.info())
        # print(lu.info(), ru.info(), rd.info(), ld.info())
        # print(d0.info(), d1.info(), d2.info(), d3.info())
        temp_lu = create_Frectangle(dots=(d0, create_dot(x=lu.x, y=d0.y),
                                          lu, create_dot(x=d0.x, y=lu.y)))

        # print('12')
        temp_ru = create_Frectangle(dots=(create_dot(x=ru.x, y=d0.y),
                                          d1, create_dot(x=d1.x, y=ru.y), ru))

        # print('13')
        temp_rd = create_Frectangle(dots=(rd, create_dot(x=d2.x, y=rd.y),
                                          d2, create_dot(x=rd.x, y=d2.y)))
        # print('14')
        temp_ld = create_Frectangle(dots=(create_dot(x=d3.x, y=ld.y), ld,
                                          create_dot(x=ld.x, y=d3.y), d3))
        # print('15')

        for i in rect.frectangle.dots.all():
            if i.dot_in(rect=temp_lu):
                paste(to=temp_lu, dot=i)
            elif i.dot_in(rect=temp_ru):
                paste(to=temp_ru, dot=i)
            elif i.dot_in(rect=temp_rd):
                paste(to=temp_rd, dot=i)
            else:
                paste(to=temp_ld, dot=i)
        # node.children.all()[number].delete()
        rect.frectangle.dots.clear()
        # rect.frectangle.delete()
        rect.delete()
        # node.children.remove(rect)
        node.children.add(temp_lu, temp_ru, temp_rd, temp_ld)
        # node.children.add(temp_ru)
        # node.children.add(temp_rd)
        # node.children.add(temp_ld)

        # print('после разделения frectangle', node.children.count())
        return True
    else:
        return False


def insert_in(node, dot):
    # print('дети:', node.children.count())
    if check_is_not_f(node):
        # if node - rectangle
        if node.children.count() != 0:

            temp_children = node.children.all()  #####

            for rect in temp_children:

                # (dt0,dt1,dt2,dt3)=rect.get_dots()
                # if not all([dt0.y == dt1.y, dt0.x == dt3.x, dt1.x == dt2.x, dt2.y == dt3.y]):
                #    print('тут 2', check_is_not_f(rect))

                if dot.dot_in(rect):
                    if not insert_in(rect, dot):
                        return False

                    if not check_is_not_f(rect):
                        if check_count(node=node, rect=rect):
                            count = 0
                            for fre in node.children.all():
                                # for fre in temp_children:
                                if not check_is_not_f(fre):
                                    count += 1
                                if count > MAX_COUNT_C:
                                    # print(node.children.count(), 'до увеличения rectangle')
                                    future_list = []
                                    # for child in temp_children:
                                    for child in node.children.all():
                                        (d0, d1, d2, d3) = child.get_dots()

                                        temp = create_rectangle(dots=(d0, d1, d2, d3))
                                        # if not all([d0.y == d1.y, d0.x == d3.x, d1.x == d2.x, d2.y == d3.y]):
                                        #    print('сломан там где f->r')
                                        node.children.remove(child)
                                        temp.children.add(child)
                                        future_list.append(temp)

                                    # for child in future_list:
                                    node.children.add(*future_list)

                                    # print(node.children.count(), 'после увеличеня')
                                    break
                    return True
            # temp_children = node.children.all()
            distances = [dot.distance(child)[0] for child in temp_children]
            numb_min = distances.index(min(distances))
            # (de0, de1, de2, de3) = temp_children[numb_min].get_dots()
            # print(de0.info(), de1.info(), de2.info(), de3.info())
            temp_dist, numb_dot = dot.distance(temp_children[numb_min])

            # (dt0, dt1, dt2, dt3) = temp_children[numb_min].get_dots()
            # if not all([dt0.y == dt1.y, dt0.x == dt3.x, dt1.x == dt2.x, dt2.y == dt3.y]):
            #    print('тут 1')
            temp_children[numb_min].expand(dot=dot, number=numb_dot)
            # (de0, de1, de2, de3) = temp_children[numb_min].get_dots()
            # print(de0.info(), de1.info(), de2.info(), de3.info())
            # print(dot.dot_in(rect=temp_children[numb_min]))
            insert_in(temp_children[numb_min], dot)
            # check_count(number=numb_min, rect=temp_children[numb_min], node=node)
            return True

        else:
            print('добавление первого frectangle')
            if create_dot(x=(dot.x + eps), y=(dot.y + eps)).dot_in(rect=node):
                node.children.add(create_Frectangle(dots=get_eps_dots(dot, 3)))
                # print('после создания', node.children.count())
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
                print('точка не должна здесь быть')

    # if not check_is_not_f(node):
    else:

        # в том случае если попали в финальный прямоугольник
        # if dot not in node.frectangle.dots.all():
        # if dot.dot_in(rect=node):
        paste(to=node, dot=dot)
        return True
        # else:
        # return False
        # else:
        # return False  # дубль


temp_res = []


def search(node, dot, R, K):
    if check_is_not_f(node):
        if node.rect_in_circ(c=dot, r=R):
            for child in node.children.all():
                 search(child, dot, R, K=K)
    elif node.rect_in_circ(c=dot, r=R):
        for elem in node.frectangle.dots.all():
            if elem.dot_in_circ(c=dot, r=R):
                if len(temp_res) < K:
                    temp_res.append([elem.dot_distance(dot=dot), elem])
                    temp_res.sort()
                else:
                    dist = elem.dot_distance(dot=dot)
                    if temp_res[-1][0] > dist:
                        temp_res.pop(K - 1)
                        temp_res.append([dist, elem])
                        temp_res.sort()

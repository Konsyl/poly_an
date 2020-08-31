import sys
from polygon_rest.models import Dot, Rectangle, FRectangle, MAX_COUNT_C, MAX_COUNT, MIN_COUNT

# Functions
eps = sys.float_info.epsilon * 1000000000000


def create_dot(x, y, desc='Пустая точка'):
    dot = Dot()
    dot.desc = desc
    dot.x = x
    dot.y = y
    return dot


def paste(to, dot):
    """ Paste dot in rectangle """

    if type(dot) == Dot:
        if dot.dot_in(to):
            dot.save()  # собственно сохранение
            to.frectangle.dots.add(dot)
            print('YES')
        else:
            print('ошибка в paste', dot.info())
            return False

    else:
        print('это не точка')


def create_rectangle(dots):
    (d0, d1, d2, d3) = dots
    if d0.y == d1.y and d0.x == d3.x and d1.x == d2.x and d2.y == d3.y:
        if d0.x < d1.x and d0.y > d2.y:
            d0.save()
            d1.save()
            d2.save()
            d3.save()
            rectangle = Rectangle.objects.create(d0=d0, d1=d1, d2=d2, d3=d3)
            # rectangle.d0 = d0
            # rectangle.d1 = d1
            # rectangle.d2 = d2
            # rectangle.d3 = d3
            rectangle.children.set([])
            rectangle.save()  # промежуточные вершины
            return rectangle
        else:
            print('не правильный порядок вершин')
    else:
        print('это не прямоугольник')


def create_Frectangle(dots):
    (d0, d1, d2, d3) = dots
    if d0.y == d1.y and d0.x == d3.x and d1.x == d2.x and d2.y == d3.y:
        if d0.x < d1.x and d0.y > d2.y:
            d0.save()
            d1.save()
            d2.save()
            d3.save()
            frectangle = FRectangle.objects.create(d0=d0, d1=d1, d2=d2, d3=d3)
            # frectangle.d0 = d0
            # frectangle.d1 = d1
            # frectangle.d2 = d2
            # frectangle.d3 = d3
            # frectangle.save()
            frectangle.dots.set([])
            frectangle.save()  # dots in rectangle
            return frectangle
        else:
            print('не правильный порядок вершин')
    else:
        print('это не прямоугольник')


def get_eps_dots(dot, number):
    if number == 0:
        dot0 = dot
        dot1 = create_dot(dot.x + eps, dot.y)
        dot2 = create_dot(dot.x + eps, dot.y - eps)
        dot3 = create_dot(dot.x, dot.y - eps)
        return dot0, dot1, dot2, dot3

    if number == 1:
        dot1 = dot
        dot0 = create_dot(dot.x - eps, dot.y)
        dot2 = create_dot(dot.x, dot.y - eps)
        dot3 = create_dot(dot.x - eps, dot.y - eps)
        return dot0, dot1, dot2, dot3

    if number == 2:
        dot2 = dot
        dot1 = create_dot(dot.x, dot.y + eps)
        dot0 = create_dot(dot.x - eps, dot.y + eps)
        dot3 = create_dot(dot.x - eps, dot.y)
        return dot0, dot1, dot2, dot3

    if number == 3:
        dot3 = dot
        dot0 = create_dot(dot.x, dot.y + eps)
        dot2 = create_dot(dot.x + eps, dot.y)
        dot1 = create_dot(dot.x + eps, dot.y + eps)
        return dot0, dot1, dot2, dot3


def search_of_pair(rect):
    max_left = rect.d0.x
    x_left = None
    max_right = rect.d1.x
    x_right = None
    middle = (rect.d1.x + rect.d0.x) / 2

    for i in rect.frectangle.dots.all():
        if i.x >= max_left and i.x <= middle:
            max_left = i.x
            x_left = i.x
        if i.x <= max_right and i.x > middle:
            max_right = i.x
            x_right = i.x

    return x_left, x_right

def check_is_not_f(rect):
    is_not_fr = False
    try:
        type(rect.frectangle)
    except:
        is_not_fr = True
    return is_not_fr

def check_count(number,node,rect):
    print('проверка')
    # проверяем финальный
    if rect.frectangle.dots.count() > MAX_COUNT:
        print('деление финального')
        # Если в измененном прямоугольнике стало больше максимума точек
        # необходимо разделение
        (d0, d1, d2, d3) = rect.get_dots()

        l, r = search_of_pair(rect)

        print(l,r,d0,d1,d2,d3)
        temp1 = create_Frectangle(dots=(d0, create_dot(x=l, y=d0.y),
                                        create_dot(x=l, y=d3.y), d3))

        temp2 = create_Frectangle(dots=(create_dot(x=r, y=d0.y),
                                        d1, d2, create_dot(x=r, y=d2.y)))

        for i in rect.frectangle.dots.all():
            if i.dot_in(rect=temp1):
                paste(to=temp1,dot=i)
            else:
                paste(to=temp2,dot=i)

        lsch = [node.children.all()]
        lsch[number].delete()
        node.children.add(temp1)
        node.children.add(temp2)


def insert_in(node, dot):
    # если node - промежуточная вершина

    if check_is_not_f(node):
        if node.children.count() != 0:
            for (number, rect) in enumerate(node.children.all()):
                if dot.dot_in(rect):
                    # найден подходящий прямоугольник - переходим в него
                    if not insert_in(rect, dot):
                        return False  # дубль
                    print('удачно')

                    if not check_is_not_f(rect):
                        check_count(number=number, node=node, rect=rect)
                    else:
                        # проверяем промежуточный
                        if rect.children.count() > MAX_COUNT_C:

                            (d0, d1, d2, d3) = rect.get_dots()

                            l, r = search_of_pair(rect)

                            temp1 = create_rectangle(dots=(d0, create_dot(x=l, y=d0.y),
                                                           create_dot(l, d3.y), d3))

                            temp2 = create_rectangle(dots=(create_dot(x=r, y=d0.y), d1,
                                                           d2, create_dot(x=r, y=d2.y)))

                            l = rect.children.count() // 2
                            rect.children.all()

                            for i in range(l // 2):
                                temp_ch = rect.children.all()[i]
                                rect.children.all()[i].delete()
                                temp1.children.add(temp_ch)

                            for i in range(l // 2, l):
                                temp_ch = rect.children.all()[i]
                                rect.children.all()[i].delete()
                                temp2.children.add(temp_ch)
                            temp1.save()
                            temp2.save()
                            rect.children.add(temp1, temp2)
                    return True
                    #
            # не нашли подходящего - иницируем расширение ближайшего
            distances = [dot.distance(child)[0] for child in node.children.all()]  # ближайший прямоугольник
            numb_min = distances.index(min(distances))  # номер ближайшего прямоугольника

            temp_dist, numb_dot = dot.distance(node.children.all()[numb_min])  # ближайшая вершина
            node.children.all()[numb_min].expand(dot=dot, number=numb_dot)  # инициируем расширение

            insert_in(node.children.all()[numb_min], dot)  # вставка точки в получившийся прямогугольник
            check_count(number=numb_min, rect=node.children.all()[numb_min], node=node)
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
                print('точка не должна здесь быть')

    if not check_is_not_f(node):
        # в том случае если попали в финальный прямоугольник
        if dot not in node.frectangle.dots.all():

            paste(to=node, dot=dot)
            return True
        else:
            return False  # дубль


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
                    temp_res.append([elem.dot_distance(dot=dot), elem])
                    temp_res.sort()
                    temp_res.pop(K)

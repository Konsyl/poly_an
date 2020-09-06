from django.test import TestCase
from django.test import Client
from polygon_rest.models import Dot, Rectangle
import random
import datetime


# Create your tests here.
class DotTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        size = 32000000
        d0 = Dot.objects.create(x=0, y=size)  # 0
        d1 = Dot.objects.create(x=size, y=size)  # 1
        d2 = Dot.objects.create(x=size, y=0)  # 2
        d3 = Dot.objects.create(x=0, y=0)  # 3
        Rectangle.objects.create(d0=d0, d1=d1, d2=d2, d3=d3)

    def test_dot_add(self):
        c = Client()
        sq = 40
        # sq=25

        t = 0
        countz = 0
        wall = sq-10
        ls1=list(range(sq, 2, -1))
        random.shuffle(ls1)
        ls2 = list(range(sq, 2, -1))
        random.shuffle(ls2)
        for i in ls1:
            countz+=1
            #print(countz, 'тут')
            #count = 0
            for j in ls2:
                x, y = (random.uniform(i - 0.5, i), random.uniform(j - 0.5, j))
                # t = datetime.datetime.now()
                #count += 1

                if countz % 10 ==0:
                    t = datetime.datetime.now()
                response = c.post(path='/poligon/dots/', data={'x': x, 'y': y, 'desc': 'dot ({0},{1})'.format(x, y)})
                if countz % 10 ==0:
                    t = datetime.datetime.now() - t
                    print(countz, t)
                if response.status_code != 200:
                    print('fail')
                    break

        t = datetime.datetime.now()
        response = c.post(path='/poligon/dotfromR/',
                          data={'x': random.uniform(sq/2, sq), 'y': random.uniform(sq/2, sq), 'R': 50, 'K': 5})
        t = datetime.datetime.now() - t
        print(t)
        print(response)


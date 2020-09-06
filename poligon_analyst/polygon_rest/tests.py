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

    def test_dot_update(self):
        c = Client()
        for i in range(25):
            c.post(path='/poligon/dots/', data={'x': i, 'y': i, 'desc': 'dot ({0},{1})'.format(i, i)})
        response = c.put(path='/poligon/dot/24', body={'x': 20, 'y': 20, 'desc': 'dot ({0},{1})'.format(20, 20)})
        self.assertEqual(response.status_code, 200)

    def test_dot_delete(self):
        c = Client()
        for i in range(25):
            c.post(path='/poligon/dots/', data={'x': i, 'y': i, 'desc': 'dot ({0},{1})'.format(i, i)})
        response = c.delete(path='/poligon/dot/24')
        self.assertEqual(response.status_code, 200)

    def test_dots_add(self):
        c = Client()
        number_of_dots = 30
        ls1 = list(range(number_of_dots, 2, -1))
        random.shuffle(ls1)
        ls2 = list(range(number_of_dots, 2, -1))
        random.shuffle(ls2)
        for i in ls1:
            for j in ls2:
                x, y = (random.uniform(i - 0.5, i), random.uniform(j - 0.5, j))
                response = c.post(path='/poligon/dots/', data={'x': x, 'y': y, 'desc': 'dot ({0},{1})'.format(x, y)})
                self.assertEqual(response.status_code, 200)

        c = Client()
        t = datetime.datetime.now()

        c.post(path='/poligon/dotfromR/',
               data={'x': random.uniform(number_of_dots / 2, number_of_dots),
                     'y': random.uniform(number_of_dots / 2, number_of_dots),
                     'R': 50, 'K': 5})
        t = datetime.datetime.now() - t
        print(t)

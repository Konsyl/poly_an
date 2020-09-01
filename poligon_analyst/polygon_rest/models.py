import math

from django.db import models

# Create your models here.

MAX_COUNT = 8  # maximum of number dots in rectangle
MAX_COUNT_C = 8  # rectangles in rectangle
MIN_COUNT = 1  # minimum of number dots in rectangle


class Dot(models.Model):
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    desc = models.CharField(max_length=255, default='Пустая точка')
    frectangle = models.ForeignKey('FRectangle', on_delete=models.CASCADE, related_name='dots', null=True, blank=True)

    def info(self):
        """ output of information """
        return self.x, self.y, self.desc

    def __eq__(self, other):
        if isinstance(other, Dot):
            return self.x == other.x and self.y == other.y
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y, self.desc))

    def dot_in(self, rect):
        """check of affiliation"""
        if self.x <= rect.d1.x and self.x >= rect.d0.x and self.y <= rect.d0.y and self.y >= rect.d3.y:
            return True
        else:
            return False

    def distance(self, rect):
        """distance to the corner of the rectangle"""
        if not self.dot_in(rect):
            temp = [math.fabs(self.x - dot.x) + math.fabs(self.y - dot.y)
                    for dot in rect.get_dots()]
            minim = min(temp)
            number = temp.index(minim)
            return minim, number

    def dot_distance(self, dot):
        return math.sqrt((self.x - dot.x) ** 2 + (self.y - dot.y) ** 2)

    def dot_in_circ(self, c, r):
        if ((self.x - c.x) ** 2 + (self.y - c.y) ** 2) <= r ** 2:
            return True


class Rectangle(models.Model):
    children_a = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    d0 = models.ForeignKey(Dot, on_delete=models.CASCADE, related_name='d0')
    d1 = models.ForeignKey(Dot, on_delete=models.CASCADE, related_name='d1')
    d2 = models.ForeignKey(Dot, on_delete=models.CASCADE, related_name='d2')
    d3 = models.ForeignKey(Dot, on_delete=models.CASCADE, related_name='d3')

    def info(self):
        return self.d0.info(), self.d1.info(), self.d2.info(), self.d3.info()

    def get_dots(self):

        return [self.d0, self.d1, self.d2, self.d3]

    def expand(self, dot, number):

        t_d = self.get_dots()[number]
        t_d.x = max(dot.x, self.get_dots()[number].x)
        t_d.save()

        t_d = self.get_dots()[number]
        t_d.y = max(dot.y, self.get_dots()[number].y)
        t_d.save()
        if number % 2 == 0:

            t_d = self.get_dots()[(number - 1) % 4]
            t_d.x = max(dot.x, self.get_dots()[(number - 1) % 4].x)
            t_d.save()
            t_d = self.get_dots()[(number + 1) % 4]
            t_d.y = max(dot.y, self.get_dots()[(number + 1) % 4].y)
            t_d.save()
        else:

            t_d = self.get_dots()[(number - 1) % 4]
            t_d.y = max(dot.y, self.get_dots()[(number - 1) % 4].y)
            t_d.save()
            t_d = self.get_dots()[(number + 1) % 4]
            t_d.x = max(dot.x, self.get_dots()[(number + 1) % 4].x)
            t_d.save()

    def rect_in_circ(self, c, r):
        # in rectangle
        if c.dot_in(rect=self):
            return True
        # angle
        elif c.x <= self.d0.x and c.y >= self.d0.y:
            if self.d0.dot_in_circ(c=c, r=r):
                return True
        elif c.x >= self.d1.x and c.y >= self.d1.y:
            if self.d1.dot_in_circ(c=c, r=r):
                return True
        elif c.x >= self.d2.x and c.y <= self.d2.y:
            if self.d2.dot_in_circ(c=c, r=r):
                return True
        elif c.x <= self.d3.x and c.y <= self.d3.y:
            if self.d3.dot_in_circ(c=c, r=r):
                return True
        # sides
        elif math.fabs(c.x - self.d0.x) <= r or math.fabs(c.x - self.d1.x) <= r:
            return True
        elif math.fabs(c.y - self.d0.y) <= r or math.fabs(c.y - self.d3.y) <= r:
            return True
        return False


class FRectangle(Rectangle):
    pass

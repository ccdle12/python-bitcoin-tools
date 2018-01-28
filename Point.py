from unittest import TestCase
from ecc import ECC

class Point:

    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b

        if self.y**2 != self.x ** 3 + self.a * self.x + self.b:
            raise RuntimeError("Points not on the curve")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return self.x != other.x and self.y != other.y and self.a != other.a and self.b != other.b

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise RuntimeError("Points are using different curves")

        # Calculate if self.x != other.x
        if self.x != other.x:
            slope = (self.y - other.y) / (self.x - other.x)

            # x3 = s**2 -x1 -x2
            x3 = slope**2 - self.x - other.x

            # y3 = slope * (x1 - x3) - y1
            y3 = slope * (self.x - x3) - self.y

            return self.__class__(x3, y3, self.a, self.b)
        else:
            # Point Doubling because x is the same value
            # Slope = (3* x1 ** 2 +a) / (2 * y1)
            slope = (3*self.x**2 + self.a) / (2*self.y)

            #x3 = slope**2 - 2*x1
            x3 = slope**2 - 2*self.x

            #y3 = slope * (x1 - x3) - y1
            y3 = slope*(self.x-x3) - self.y

            print("X3 and Y3: {0}, {1}".format(x3, y3))
            return self.__class__(x3, y3, self.a, self.b)

class PointTest(TestCase):
    def test_points_on_curve(self):
        with self.assertRaises(RuntimeError):
            Point(x=2, y=7, a=5, b=7)

        # Comparing for equality
        p1 = Point(18, 77, 5, 7)
        p2 = Point(18, 77, 5, 7)
        self.assertEqual(p1, p2)

        # Adding two points
        p1 = Point(x=3, y=7, a=5, b=7)
        p2 = Point(x=-1, y=-1, a=5, b=7)
        self.assertEqual(p1 + p2, Point(x=2, y=-5, a=5, b=7))

        # Adding two points by point doubling
        a = Point(x=-1, y=1, a=5, b=7)
        self.assertEqual(a + a, Point(x=18, y=-77, a=5, b=7))


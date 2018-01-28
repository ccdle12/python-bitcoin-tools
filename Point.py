from unittest import TestCase
from FieldElement import FieldElement
from ecc import ECC


class Point:

    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b

        if self.x is None and self.y is None:
            return

        if self.y ** 2 != self.x ** 3 + self.a * self.x + self.b:
            raise RuntimeError("Points not on the curve")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and \
               self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or \
               self.a != other.a or self.b != other.b

    def __repr__(self):
        if self.x is None:
            return 'Point(infinity)'
        else:
            return 'Point({},{})'.format(self.x, self.y)

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise RuntimeError("Points are using different curves")

        if self.x is None:
            return other

        if other.x is None:
            return self

        # Check for reaching point at infinity
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        # Calculate if self.x != other.x
        if self.x != other.x:
            slope = (self.y - other.y) / (self.x - other.x)

            # x3 = s**2 -x1 -x2
            x3 = slope ** 2 - self.x - other.x

            # y3 = slope * (x1 - x3) - y1
            y3 = slope * (self.x - x3) - self.y

            return self.__class__(x3, y3, self.a, self.b)
        else:
            # Point Doubling because x is the same value
            # Slope = (3* x1 ** 2 +a) / (2 * y1)
            slope = (3 * self.x ** 2 + self.a) / (2 * self.y)

            # x3 = slope**2 - 2*x1
            x3 = slope ** 2 - 2 * self.x

            # y3 = slope * (x1 - x3) - y1
            y3 = slope * (self.x - x3) - self.y

            return self.__class__(x3, y3, self.a, self.b)

    def __rmul__(self, scalar):
        product = self.__class__(None, None, self.a, self.b)

        for _ in range(scalar):
            product += self

        return product


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

    def test_rmul(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        multiplications = (
            (2, 192, 105, 49, 71),
            (2, 143, 98, 64, 168),
            (2, 47, 71, 36, 111),
            (4, 47, 71, 194, 51),
            (8, 47, 71, 116, 55),
            (21, 47, 71, None, None),
        )

        # iterate over the multiplications
        for coefficient, _x1, _y1, _x2, _y2 in multiplications:
            x1 = FieldElement(_x1, prime)
            y1 = FieldElement(_y1, prime)
            p1 = Point(x1, y1, a, b)

            # initialize the second point based on whether it's the point at infinity
            if _x2 is None:
                p2 = Point(None, None, a, b)
            else:
                x2 = FieldElement(_x2, prime)
                y2 = FieldElement(_y2, prime)
                p2 = Point(x2, y2, a, b)

            # check that the product is equal to the expected point
            self.assertEqual(coefficient * p1, p2)

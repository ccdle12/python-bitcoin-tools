from unittest import TestCase
from ecc import ECC

class Point():

    def __init__(self, x, y):
        if x is None or y is None:
            raise RuntimeError("x or y is None")

        if not ECC().is_on_curve(x, y):
            raise RuntimeError("x and y are not on the curve: {0}, {1}".format(x, y))

        self.x = x
        self.y = y


class Point_Tests(TestCase):
    def test_creating_point(self):
        point = Point(4009715469895962904302745416817721540571577912364644137838095050706137667860,
                      32025336288095498019218993550383068707359510270784983226210884843871535451292)

        print("Should create a point and retrieve the x value and should be valid on the curve")
        self.assertEqual(4009715469895962904302745416817721540571577912364644137838095050706137667860,
                         point.x)

    def test_should_fail_passing_None(self):
        print("Should raise error that None is not an acceptable point")
        with self.assertRaises(RuntimeError):
            point = Point(12, None)

    def test_should_fail_since_x_y_not_on_ecc(self):
        print("Should raise error that the points are not on the EC")
        with self.assertRaises(RuntimeError):
            point = Point(5, 5)

    def test_creating_G_point(self):
        G = Point(55066263022277343669578718895168534326250603453777594175500187360389116729240,
                  32670510020758816978083085130507043184471273380659243275938904335757337482424)

        print("Should create the generator point and retrieve y")
        self.assertEqual(32670510020758816978083085130507043184471273380659243275938904335757337482424, G.y)

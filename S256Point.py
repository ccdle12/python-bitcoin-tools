from FieldElement import FieldElement
from Point import Point
from unittest import TestCase
from binascii import hexlify

P = 2 ** 256 - 2 ** 32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
A = 0
B = 7


class S256Field(FieldElement):

    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=P)

    def hex(self):
        return '{:x}'.format(self.num).zfill(64)

    def __repr__(self):
        return self.hex()


class S256Point(Point):
    bits = 256

    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(A), S256Field(B)

        if x is None:
            super().__init__(x=None, y=None, a=a, b=b)
        elif type(x) == int:
            super().__init__(S256Field(x), S256Field(y), a=a, b=b)
        else:
            super().__init__(x=x, y=y, a=a, b=b)

    def __repr__(self):
        if self.x is None:
            return 'Point(infinity)'
        else:
            return 'Point({},{})'.format(self.x, self.y)

    def __rmul__(self, scalar):
        print("DOING RMUL!!")
        # Binary Expansion on current
        current = self

        result = S256Point(None, None)

        for _ in range(self.bits):
            # Bitwise AND, if bit is 1
            if scalar & 1:
                result += current

            current += current

            # Shifting bits to the right by 1
            scalar >>= 1
            # print("Current: {0}".format(current))

        # print("Result: {0}, {1}".format(result.x, result.y))
        print("Rmul product in S256: {0}".format(result))
        return result


G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)


class S256Test(TestCase):

    def test_point_at_infinity(self):
        print("N: {0}".format(N))
        print("Should return None since point of infinity")
        point = N*G
        # print(50 & 20)
        # print(50 ^ 20)
        # print(50 >> 1)
        # print(240 >> 1)
        # print(16 >> 1)
        # print(240 >> 2)
        # print(16 << 1)
        # print(240 << 1)
        print(point.x)
        self.assertIsNone(point.x)

    def test_generating_pub_key(self):
        secret = 999
        point = secret*G
        print("Secret multiply G should return the following points")
        self.assertEqual(hexlify(point.x.num.to_bytes(32, 'big')).decode('ascii'), "9680241112d370b56da22eb535745d9e314380e568229e09f7241066003bc471")
        self.assertEqual(hexlify(point.y.num.to_bytes(32, 'big')).decode('ascii'), "ddac2d377f03c201ffa0419d6596d10327d6c70313bb492ff495f946285d8f38")

    def test_pubpoint(self):
        # write a test that tests the public point for the following
        print("Should return true for generating public points from secret")
        points = (
            # secret, x, y
            (7, 0x5cbdf0646e5db4eaa398f365f2ea7a0e3d419b7e0330e39ce92bddedcac4f9bc,
             0x6aebca40ba255960a3178d6d861a54dba813d0b813fde7b5a5082628087264da),
            (1485, 0xc982196a7466fbbbb0e27a940b6af926c1a74d5ad07128c82824a11b5398afda,
             0x7a91f9eae64438afb9ce6448a1c133db2d8fb9254e4546b6f001637d50901f55),
            (2 ** 128, 0x8f68b9d2f63b5f339239c1ad981f162ee88c5678723ea3351b7b444c9ec4c0da,
             0x662a9f2dba063986de1d90c2b6be215dbbea2cfe95510bfdf23cbf79501fff82),
            (2 ** 240 + 2 ** 31, 0x9577ff57c8234558f293df502ca4f09cbc65a6572c842b39b366f21717945116,
             0x10b49c67fa9365ad7b90dab070be339a1daf9052373ec30ffae4f72d5e66d053),
        )

        # iterate over points
        for secret, _x, _y in points:
            # initialize the secp256k1 point (S256Point)
            p = S256Point(_x, _y)

            # check that the secret*G is the same as the point
            self.assertEqual(secret * G, p)

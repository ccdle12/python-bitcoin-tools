import secrets
from Signature import Signature
from S256Point import G, N, P, A, B
from unittest import TestCase

class ECC:
    def generate_priv_key(self):
        return secrets.randbelow(N)

    def generate_pub_key(self, priv_key):
        return priv_key * G

    def is_on_curve(self, x, y):
        return (y ** 2) % P == (x ** 3 + A + B) % P

    # TODO: Examine and review
    def generate_signature(self, priv_key):
        z = secrets.randbelow(2 ** 256)
        k = secrets.randbelow(2 ** 256)
        r = (k * G).x.num

        sig = (z + r * priv_key) * pow(k, N - 2, N) % N

        return Signature(z, r, sig)

class ECCTests(TestCase):
    def test_P(self):
        print("First test, should show ECC.P equal to Prime Number Field")
        self.assertEqual(P, 2 ** 256 - 2 ** 32 - 977)

    # # # # # # # # # # # # # # # # # # # # # # #
    # Test Generating Private and Public Keys   #
    # # # # # # # # # # # # # # # # # # # # # # #
    def test_generate_priv_key(self):
        priv_key = ECC().generate_priv_key()
        print("Private key generated should be above 0 and below ECC.N")
        self.assertTrue(0 < priv_key < N)

    def test_duplicate_priv_key(self):

        prev_gen_priv_keys = {}

        # 2.2 GHz Intel Core i7
        # 16 GB 1600 MHz DDR3
        # Takes about 9 - 10 seconds to run this test
        for _ in range(1000000):
            priv_key = ECC().generate_priv_key()

            assert 0 < priv_key < N

            if priv_key in prev_gen_priv_keys:
                raise RuntimeError('Randomly generated number, has been generated before')

            prev_gen_priv_keys[priv_key] = priv_key

        print("There should be no duplicates after creating 1000000 private keys")

    def test_generate_pub_key(self):
        priv_key = ECC().generate_priv_key()
        pub_key = ECC().generate_pub_key(priv_key)
        print("There should be a x val of pub_key > 0")
        self.assertTrue(0 < pub_key.x.num)

    def test_point_at_infinity(self):
        point_at_infinity = N * G
        print("Point at Infinity, should return None for both x and y")
        self.assertEqual(None, point_at_infinity.x)
        self.assertEqual(None, point_at_infinity.y)

    def test_pub_key_is_on_curve(self):
        priv_key = ECC().generate_priv_key()
        pub_key = ECC().generate_pub_key(priv_key)
        print(pub_key.x, pub_key.y)
        print("Both x and y should be on the curve, checking if pub_key is on curve")
        self.assertEqual(True, ECC().is_on_curve(pub_key.x.num, pub_key.y.num))

    def test_pub_key_is_not_on_curve(self):
        pub_key = (20700948478913772076119439904629995041653958252327787830786676775719940102654,
                   5554562626338682950266833423860784775451683510376504490669758056891525878098)
        print("Should return false, y has been tampered with, so it is not a valid point on the curve")
        self.assertEqual(False, ECC().is_on_curve(pub_key[0], pub_key[1]))


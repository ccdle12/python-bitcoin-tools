from unittest import TestCase
import secrets
from pycoin.ecdsa import generator_secp256k1 as G

class ECC:
    P = 2**256 - 2**32 - 977
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    A = 0
    B = 7

    def generate_priv_key(self):
        return secrets.randbelow(self.N)

    def generate_pub_key(self, priv_key):
        return priv_key * G

    def is_on_curve(self, x, y):
        return (y ** 2) % self.P == (x ** 3 + self.A + self.B) % self.P


class ECC_Tests(TestCase):
    def test_P(self):
        self.assertEqual(ECC.P, 2**256 - 2**32 - 977)

    def test_generate_priv_key(self):
        priv_key = ECC().generate_priv_key()
        self.assertTrue(0 < priv_key < ECC.N)

    def test_duplicate_priv_key(self):

        prev_gen_priv_keys = {}

        # 2.2 GHz Intel Core i7
        # 16 GB 1600 MHz DDR3
        # Takes about 9 - 10 seconds to run this test
        for _ in range(1000000):
            priv_key = ECC().generate_priv_key()

            assert 0 < priv_key < ECC.N

            if priv_key in prev_gen_priv_keys:
                raise RuntimeError('Randomly generated number, has been generated before')

            prev_gen_priv_keys[priv_key] = priv_key


    def test_generate_pub_key(self):
        priv_key = ECC().generate_priv_key()
        pub_key = ECC().generate_pub_key(priv_key)

        self.assertTrue(0 < pub_key.x())

    def test_point_at_infinity(self):
        point_at_infinity = ECC().N * G
        self.assertEqual(None, point_at_infinity.x())
        self.assertEqual(None, point_at_infinity.y())

    def test_pub_key_is_on_curve(self):
        priv_key = ECC().generate_priv_key()
        pub_key = ECC().generate_pub_key(priv_key)
        print(pub_key.x(), pub_key.y())

        self.assertEqual(True, ECC().is_on_curve(pub_key.x(), pub_key.y()))

    def test_pub_key_is_not_on_curve(self):
        pub_key = (20700948478913772076119439904629995041653958252327787830786676775719940102654, 5554562626338682950266833423860784775451683510376504490669758056891525878098)

        self.assertEqual(False, ECC().is_on_curve(pub_key[0], pub_key[1]))
from unittest import TestCase
import ecc
from S256Point import N, G


class Signature:
    def __init__(self, z, r, sig):
        if type(z) is not int:
            raise RuntimeError("z is not in int format")

        if type(r) is not int:
            raise RuntimeError("r is not in int format")

        if type(sig) is not int:
            raise RuntimeError("sig is not int format")

        self.z = z
        self.r = r
        self.sig = sig

    def verify(self, pub_key):
        u = self.z * pow(self.sig, N - 2, N) % N
        v = self.r * pow(self.sig, N - 2, N) % N

        return (u * G + v * pub_key).x.num == self.r


class SignatureTest(TestCase):
    def test_generating_signature(self):
        print("------------------------------------------------")
        priv_key = ecc.ECC().generate_priv_key()
        pub_key = ecc.ECC().generate_pub_key(priv_key)
        signature = ecc.ECC().generate_signature(priv_key)

        print("------------------------------------------------")
        print("Should assert z,r,sig as NOT none")
        self.assertIsNotNone(signature.z)
        self.assertIsNotNone(signature.r)
        self.assertIsNotNone(signature.sig)

        print("------------------------------------------------")
        print("Should verify signature as True")
        self.assertTrue(signature.verify(pub_key))

        print("------------------------------------------------")
        print("Should verify signature as False, since we are trying to verify signature 2 with the first pub_key")
        priv_key2 = ecc.ECC().generate_priv_key()
        signature2 = ecc.ECC().generate_signature(priv_key2)

        self.assertFalse(signature2.verify(pub_key))

        print("------------------------------------------------")
        print("Should verify signature as True, since we are using signature 2 and pub_key2")
        priv_key2 = ecc.ECC().generate_priv_key()
        pub_key2 = ecc.ECC().generate_pub_key(priv_key2)
        signature2 = ecc.ECC().generate_signature(priv_key2)

        self.assertTrue(signature2.verify(pub_key2))

        print("------------------------------------------------")
        print("Should verify signature as False, since we are using signature 2 and pub_key3")
        priv_key3 = ecc.ECC().generate_priv_key()
        pub_key3 = ecc.ECC().generate_pub_key(priv_key3)
        signature3 = ecc.ECC().generate_signature(priv_key2)

        self.assertFalse(signature2.verify(pub_key3))

        print("------------------------------------------------")
        print("Should verify signature as True, since we are using signature 4 and pub_key4")
        priv_key4 = ecc.ECC().generate_priv_key()
        pub_key4 = ecc.ECC().generate_pub_key(priv_key4)
        signature4 = ecc.ECC().generate_signature(priv_key4)

        self.assertTrue(signature4.verify(pub_key4))

        print("------------------------------------------------")
        print("Should verify signature as False, since we are using signature 4 and pub_key1")
        self.assertFalse(signature4.verify(pub_key))

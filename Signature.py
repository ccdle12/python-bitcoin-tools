from unittest import TestCase
import ecc
from S256Point import N, G
from io import BytesIO
from binascii import hexlify


class Signature:
    def __init__(self, r, s):
        if type(s) is not int:
            raise RuntimeError("s is not in int format")

        if type(r) is not int:
            raise RuntimeError("r is not in int format")

        self.s = s
        self.r = r

    @classmethod
    def parse(cls, signature_bin):
        s = BytesIO(signature_bin)

        compound = s.read(1)[0]

        if compound != 0x30:
            raise RuntimeError("Bad Signature")

        length = s.read(1)[0]
        if length + 2 != len(signature_bin):
            raise RuntimeError("Bad Signature Length")

        marker = s.read(1)[0]
        if marker != 0x02:
            raise RuntimeError("Bad Signature")

        rlength = s.read(1)[0]
        r = int(hexlify(s.read(rlength)), 16)
        marker = s.read(1)[0]
        if marker != 0x02:
            raise RuntimeError("Bad Signature")

        slength = s.read(1)[0]
        s = int(hexlify(s.read(slength)), 16)
        if len(signature_bin) != 6 + rlength + slength:
            raise RuntimeError("Signature too long")

        return cls(r, s)

    def der(self):
        rbin = self.r.to_bytes(32, byteorder='big')

        # if rbin has a high bit, add a 00
        if rbin[0] > 128:
            rbin = b'\x00' + rbin

        result = bytes([2, len(rbin)]) + rbin
        sbin = self.s.to_bytes(32, byteorder='big')

        # if sbin has a high bit, add a 00
        if sbin[0] > 128:
            sbin = b'\x00' + sbin

        result += bytes([2, len(sbin)]) + sbin
        return bytes([0x30, len(result)]) + result


class SignatureTest(TestCase):
    def test_generating_signature(self):
        print("------------------------------------------------")
        priv_key = ecc.ECC().generate_priv_key()
        pub_key = ecc.ECC().generate_pub_key(priv_key)
        signature = ecc.ECC().generate_signature(priv_key)

        print("------------------------------------------------")
        print("Should assert r, s as NOT none")
        self.assertIsNotNone(signature.s)
        self.assertIsNotNone(signature.r)
        # # self.assertIsNotNone(signature.sig)
        #
        # print("------------------------------------------------")
        # print("Should verify signature as True")
        # self.assertTrue(signature.verify(pub_key))
        #
        # print("------------------------------------------------")
        # print("Should verify signature as False, since we are trying to verify signature 2 with the first pub_key")
        # priv_key2 = ecc.ECC().generate_priv_key()
        # signature2 = ecc.ECC().generate_signature(priv_key2)
        #
        # self.assertFalse(signature2.verify(pub_key))
        #
        # print("------------------------------------------------")
        # print("Should verify signature as True, since we are using signature 2 and pub_key2")
        # priv_key2 = ecc.ECC().generate_priv_key()
        # pub_key2 = ecc.ECC().generate_pub_key(priv_key2)
        # signature2 = ecc.ECC().generate_signature(priv_key2)
        #
        # self.assertTrue(signature2.verify(pub_key2))
        #
        # print("------------------------------------------------")
        # print("Should verify signature as False, since we are using signature 2 and pub_key3")
        # priv_key3 = ecc.ECC().generate_priv_key()
        # pub_key3 = ecc.ECC().generate_pub_key(priv_key3)
        # signature3 = ecc.ECC().generate_signature(priv_key2)
        #
        # self.assertFalse(signature2.verify(pub_key3))
        #
        # print("------------------------------------------------")
        # print("Should verify signature as True, since we are using signature 4 and pub_key4")
        # priv_key4 = ecc.ECC().generate_priv_key()
        # pub_key4 = ecc.ECC().generate_pub_key(priv_key4)
        # signature4 = ecc.ECC().generate_signature(priv_key4)
        #
        # self.assertTrue(signature4.verify(pub_key4))
        #
        # print("------------------------------------------------")
        # print("Should verify signature as False, since we are using signature 4 and pub_key1")
        # self.assertFalse(signature4.verify(pub_key))

from unittest import TestCase
from io import BytesIO
from binascii import hexlify, unhexlify


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

        # if the length of the signature is into equal to the 6 byte markers, plus r and s, then sig is too long
        if len(signature_bin) != 6 + rlength + slength:
            raise RuntimeError("Signature too long")

        return cls(r, s)

    def der(self):
        # Return r, s in Der Format (serializing)
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

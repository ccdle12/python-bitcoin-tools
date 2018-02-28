from bitcoin_tools.FieldElement import FieldElement
from bitcoin_tools.Point import Point
from bitcoin_tools.helper import sha256_ripemd160, double_sha256, encode_base58
from unittest import TestCase
from binascii import hexlify, unhexlify
import math

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

    def sqrt(self):
        return self ** ((P + 1) // 4)


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
        # Binary Expansion on current
        current = self

        result = S256Point(None, None)

        # Iterating in range of 256 and doubling each time ->
        # when there is a 1 at the end of the binary number ->
        # add to result
        for _ in range(self.bits):
            # If last bit is 1, add current to self (adding -> p1 + p2 = p3)
            if scalar & 1:
                # Calling super class (Point) to calculate the next point on the curve  ->
                # adding result(x,y) + current (x,y)
                result += current

            # Calling super class (Point) to point double current(x,y) * current(x,y)
            current += current

            # Shifting bits of scalar to the right by 1 and assigning new value
            # Decrementing scalar by /2
            scalar >>= 1

        return result

    def get_sec(self, compressed=True):

        if self.x is None or self.y is None:
            raise RuntimeError("x is None")

        x = self.x.num.to_bytes(32, 'big')
        y = self.y.num.to_bytes(32, 'big')

        if compressed:
            if self.y.num % 2 == 0:
                prefix = b'\x02'
            else:
                prefix = b'\x03'

            sec = prefix + x

        else:
            prefix = b'\x04'

            sec = prefix + x + y

        return hexlify(sec)

    def get_address(self, sec, mainnet=False):

        if type(sec) is not bytes:
            raise RuntimeError("sec must be passed as bytes format")

        # Need to turn sec into bytes before hashing
        sec_bytes = unhexlify(sec)

        if mainnet:
            prefix = b'\x00'
        else:
            prefix = b'\x6f'


        # SHA256 -> RIMPEMD160
        hashed_sec_bytes = sha256_ripemd160(sec_bytes)

        # Concatenate prefix and hashed sec bytes
        raw = prefix + hashed_sec_bytes

        # Double SHA256 raw and take the first 4 bytes as checksum
        checksum = double_sha256(raw)[:4]

        # Encode Base58 raw and checksum to generate accepted address
        address = encode_base58(raw + checksum)

        return address.decode('ascii')

    @classmethod
    def parse(cls, sec_bin):
        '''returns a Point object from a compressed sec binary (not hex)
        '''
        # Uncompressed SEC
        if sec_bin[0] == 4:
            x = int(hexlify(sec_bin[1:33]), 16)
            y = int(hexlify(sec_bin[33:65]), 16)
            return S256Point(x=x, y=y)

        # Comprssed SEC
        is_even = sec_bin[0] == 2
        x = S256Field(int(hexlify(sec_bin[1:]), 16))

        # right side of the equation y^2 = x^3 + 7
        alpha = x ** 3 + S256Field(B)
        # solve for left side
        beta = alpha.sqrt()

        if beta.num % 2 == 0:
            even_beta = beta
            odd_beta = S256Field(P - beta.num)
        else:
            even_beta = S256Field(P - beta.num)
            odd_beta = beta
        if is_even:
            return S256Point(x, even_beta)
        else:
            return S256Point(x, odd_beta)

    def verify(self, z, sig):
        # remember sig.r and sig.s are the main things we're checking
        # remember 1/s = pow(s, N-2, N)
        s_inv = pow(sig.s, N - 2, N)
        # u = z / s
        u = z * s_inv % N
        # v = r / s
        v = sig.r * s_inv % N
        # u*G + v*P should have as the x coordinate, r
        total = u * G + v * self
        return total.x.num == sig.r


G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)


from bitcoin_tools.S256Point import N, G, B, P, A
from bitcoin_tools.helper import encode_base58_checksum
from bitcoin_tools.Signature import Signature
from random import randint
import secrets

class PrivateKey:
    def __init__(self, secret=None):

        if secret is None:
            self.secret = secrets.randbelow(N)
        else:
            self.secret = secret

        self.public_key = self.secret * G

        if self.is_on_curve() is False:
            raise RuntimeError("Generated Public Point is not on Curve, do not use this private key")

    def is_on_curve(self):
        return (self.public_key.y.num ** 2) % P == (self.public_key.x.num ** 3 + A + B) % P

    def get_WIF(self, compressed=True, mainnet=True):

        if mainnet:
            prefix = b'\x80'
        else:
            prefix = b'\xef'

        s = self.secret.to_bytes(32, 'big')

        wif = prefix + s

        if compressed:
            wif = wif + b'\x01'

        return encode_base58_checksum(wif)

    @classmethod
    def import_private_key(cls, secret):
        return cls(secret)

    def sign(self, z):

        k = randint(0,  2**256)
        r = (k * G).x.num

        s = (z + r * self.secret) * pow(k, N - 2, N) % N

        if s > N // 2:
            s = N - s

        return Signature(r, s)

import secrets
from S256Point import G, N, P, A, B
from pycoin.ecdsa.secp256k1 import Point
from binascii import hexlify, unhexlify
from helper import encode_base58, double_sha256, sha256_ripemd160


class ECC:
    def generate_priv_key(self):
        return secrets.randbelow(N)

    def generate_pub_key(self, priv_key):
        return priv_key * G

    def is_on_curve(self, x, y):
        return (y ** 2) % P == (x ** 3 + A + B) % P

    def generate_uncompressed_SEC(self, x_int, y_int):

        if x_int == None or y_int == None:
            raise RuntimeError("X or Y is None")

        if x_int == 0 or y_int == 0:
            raise RuntimeError("X or Y is 0")

        if not self.is_on_curve(x_int, y_int):
            raise RuntimeError("x,y provided is not on the secp256k1 curve")

        prefix = b'\x04'

        x_bytes = x_int.to_bytes(32, 'big')
        y_bytes = y_int.to_bytes(32, 'big')

        uncompressed_SEC_bytes = prefix + x_bytes + y_bytes

        return hexlify(uncompressed_SEC_bytes)

    def generate_compressed_SEC(self, x_int, y_int):

        if x_int == None or y_int == None:
            raise RuntimeError("X or Y is None")

        if x_int == 0 or y_int == 0:
            raise RuntimeError("X or Y is equal to 0")

        if not self.is_on_curve(x_int, y_int):
            raise RuntimeError("x,y provided is not on the secp256k1 curve")

        if y_int % 2 == 0:
            prefix = b'\x02'
        else:
            prefix = b'\x03'

        x_bytes = x_int.to_bytes(32, 'big')

        compressed_SEC_bytes = prefix + x_bytes

        return hexlify(compressed_SEC_bytes)


    # TODO: Examine and review
    def generate_signature(self, priv_key):
        z = secrets.randbelow(2 ** 256)
        k = secrets.randbelow(2 ** 256)
        r = (k * self.G).x()

        signature = (z + r * priv_key) * pow(k, self.N - 2, self.N) % self.N

        return z, r, signature

    # TODO: Verify_signature is failing with unsupported operand type
    def verify_signature(self, z, r, s, pub_key):
        u = z * pow(s, self.N - 2, self.N) % self.N
        print("U: {0}".format(u))
        v = r * pow(s, self.N - 2, self.N) % self.N
        print("V: {0}".format(v))
        point = Point(pub_key[0], pub_key[1], (self.P, self.A, self.B, self.N))

        return (u * self.G + v * point).x() == r


if __name__ == '__main__':
    priv_key = ECC().generate_priv_key()
    print("-----------------------------------")
    print("Private Key: {0}".format(priv_key))
    print("-----------------------------------")
    pub_key = ECC().generate_pub_key(priv_key)
    print("Public Key: {0}".format(pub_key))
    print("-----------------------------------")
    uncompressed_sec = ECC().generate_uncompressed_SEC(pub_key.x(), pub_key.y())
    print("Uncompressed SEC: {0}".format(uncompressed_sec))
    print("-----------------------------------")
    compressed_sec = ECC().generate_compressed_SEC(pub_key.x(), pub_key.y())
    print("Compressed SEC: {0}".format(compressed_sec))
    print("-----------------------------------")

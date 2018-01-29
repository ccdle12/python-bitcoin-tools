import secrets
from S256Point import G, N, P, A, B
import Signature

#TODO: TURN THIS INTO MAIN
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

        return Signature.Signature(z, r, sig)


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

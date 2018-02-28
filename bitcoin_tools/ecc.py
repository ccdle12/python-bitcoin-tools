import secrets
from bitcoin_tools.Signature import Signature
from bitcoin_tools.S256Point import G, N, P, A, B

class ECC:
    def generate_priv_key(self):
        return secrets.randbelow(N)

    def generate_pub_key(self, priv_key):
        return priv_key * G

    def is_on_curve(self, x, y):
        return (y ** 2) % P == (x ** 3 + A + B) % P

    # TODO: Examine and review
    # TODO: K needs to have higher entropy, use tx as seed
    def generate_signature(self, priv_key):
        z = secrets.randbelow(2 ** 256)
        k = secrets.randbelow(2 ** 256)
        r = (k * G).x.num

        sig = (z + r * priv_key) * pow(k, N - 2, N) % N

        return Signature(z, r, sig)




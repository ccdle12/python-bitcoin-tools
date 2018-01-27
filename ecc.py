import secrets
from pycoin.ecdsa import generator_secp256k1 as G
from binascii import hexlify
import hashlib

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


    def generate_uncompressed_SEC(self, x_int , y_int):

        if x_int == None or y_int == None:
            raise RuntimeError("X or Y is None")

        if x_int == 0 or y_int == 0:
            raise RuntimeError("X or Y is 0")

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

        if y_int % 2 == 0:
            prefix = b'\x02'
        else:
            prefix = b'\x03'

        x_bytes = x_int.to_bytes(32, 'big')

        compressed_SEC_bytes = prefix + x_bytes

        return hexlify(compressed_SEC_bytes)


    def generate_testnet_address(self, hex_SEC):

        if type(hex_SEC) != bytes:
            raise RuntimeError("Argument should be in bytes")

        prefix = b'\x6f'

        hashed_bytes = hashlib.new('ripemd160', hashlib.sha256(hex_SEC).digest()).digest()

        testnet_raw = prefix + hashed_bytes




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
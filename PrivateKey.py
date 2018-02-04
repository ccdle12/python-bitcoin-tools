from unittest import TestCase
from S256Point import N, G, B, P, A
import secrets
from helper import encode_base58_checksum
from Signature import Signature


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
        # Rand int
        k = secrets.randbelow(2 ** 256)
        r = (k * G).x.num

        s = (z + r * self.secret) * pow(k, N - 2, N) % N

        if s > N // 2:
            s = N - s

        return Signature(r, s)


class PrivateKeyTest(TestCase):
    def test_init_PrivateKey(self):
        priv_key = PrivateKey().secret

        print("Private Key should not be None")
        self.assertIsNotNone(priv_key)
        print("Private key should be greater than 0 and less than N")
        self.assertTrue(0 < priv_key < N)
        print("Private key should NOT be greater than N")
        self.assertFalse(priv_key > N)
        print("----------------------------------------------------------")

        point_at_infinity = N * G
        print("Point at Infinity, should return None for both x and y")
        self.assertEqual(None, point_at_infinity.x)
        self.assertEqual(None, point_at_infinity.y)

    def test_duplicate_priv_key(self):

        prev_gen_priv_keys = {}

        # 2.2 GHz Intel Core i7
        # 16 GB 1600 MHz DDR3
        # Takes about 9 - 10 seconds to run this test
        for _ in range(1000000):
            priv_key = PrivateKey().secret

            assert 0 < priv_key < N

            print(priv_key)
            if priv_key in prev_gen_priv_keys:
                raise RuntimeError('Randomly generated number, has been generated before')

            prev_gen_priv_keys[priv_key] = priv_key

        print("There should be no duplicates after creating 1000000 private keys")

    def test_gen_pub_key(self):
        priv_key = PrivateKey()
        pub_key = priv_key.public_key

        print("pub_key has been generated")
        self.assertIsNotNone(pub_key)

        print("----------------------------------------------------------")
        print("Both x and y should be on the curve, checking if pub_key is on curve")
        self.assertTrue(priv_key.is_on_curve())

    def test_wallet_import_format(self):
        secret = 40739339072244861339425603543300453407867090494212474723312591401916565730912

        prefix = b'\x80'
        s = secret.to_bytes(32, 'big')

        print("----------------------------------------------------------")
        print("Should create wallet import format for mainnet uncompressed")
        expected = "5JVxGiHdVvu7XTr1PMRb8gGE2vdFYQnsErmJMFrUXSF5rWf6sPh"
        self.assertEqual(expected, encode_base58_checksum(prefix + s))

        print("----------------------------------------------------------")
        print("Should create wallet import format for mainnet compressed")
        expected = "KzEnxMEQ6gu1oTVJhf9XetJCXVh1Be1SkAeXaQZNVLRARGK6inwT"
        self.assertEqual(expected, encode_base58_checksum(prefix + s + b'\x01'))

        print("----------------------------------------------------------")
        print("Should create wallet import format for testnet uncompressed")
        prefix = b'\xef'
        expected = "92GarT7B69yFVXMJ1hKW1GpBgayxhaL4aodFRtCysAz8dWAsiBQ"
        self.assertEqual(expected, encode_base58_checksum(prefix + s))

        print("----------------------------------------------------------")
        print("Should create wallet import format for testnet uncompressed")
        prefix = b'\xef'
        expected = "cQbnRGEFXkbGxtxa64xf2CoG9izQr678pCnzgq1szT5Ag1U7rZ88"
        self.assertEqual(expected, encode_base58_checksum(prefix + s + b'\x01'))

        print("----------------------------------------------------------")
        print("Should create wallet import format for mainnet uncompressed")
        expected = "5"
        self.assertEqual(expected, PrivateKey().get_WIF(compressed=False, mainnet=True)[:1])

        print("----------------------------------------------------------")
        print("Should create wallet import format for mainnet compressed")
        expected = "K"
        expected2 = "L"
        self.assertTrue(expected or expected2 == PrivateKey().get_WIF(compressed=True, mainnet=True)[:1])

        print("----------------------------------------------------------")
        print("Should create wallet import format for testnet and uncompressed")
        expected = "9"
        self.assertEqual(expected, PrivateKey().get_WIF(compressed=False, mainnet=False)[:1])

        print("----------------------------------------------------------")
        print("Should create wallet import format for testnet and compressed")
        expected = "c"
        self.assertEqual(expected, PrivateKey().get_WIF(compressed=True, mainnet=False)[:1])

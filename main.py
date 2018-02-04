from unittest import TestCase
import PrivateKey


class Main:
    def __init__(self, secret=None):

        if secret is None:
            self.keys = PrivateKey.PrivateKey()
        else:
            self.keys = PrivateKey.PrivateKey.import_private_key(secret)

        self.sec = self.keys.public_key.get_sec(compressed=True)

    def get_private_key(self):
        return self.keys.get_WIF(mainnet=False)

    def is_public_key_valid(self):
        return self.keys.is_on_curve()

    def get_address(self, mainnet=False):
        return self.keys.public_key.get_address(self.sec, mainnet)

    @classmethod
    def import_private_key(cls, secret):
        return cls(secret)


class MainTest(TestCase):

    def test_private_key_generated(self):
        print("Should generate a private key on construction")
        wallet = Main()
        self.assertIsNotNone(wallet.get_private_key())

        print("-------------------------------------------------------------")
        print("Should generate a valid public key on the secp256k1 curve")
        self.assertTrue(wallet.is_public_key_valid())

        print("-------------------------------------------------------------")
        print("Should generate a valid address on the testnet")
        testnet_address = wallet.get_address(mainnet=False)
        print(testnet_address)
        self.assertTrue(testnet_address[0] != '1')

        print("-------------------------------------------------------------")
        print("Import a private key, temp method, will change this to a cleaner way of importing secrets using WIF")
        wallet = Main().import_private_key(
            100897809677138163174856952607694300238573305027534078569886890414323321447504)
        self.assertEqual('cV4KeBeyuaHct1fzoiXkjEjaNGGiVXwwhfRbUdJYqVLqArQk6UBb', wallet.get_private_key())

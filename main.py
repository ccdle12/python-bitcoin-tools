from unittest import TestCase
import PrivateKey

class Main:
    def __init__(self):
        self.private_key = PrivateKey.PrivateKey()


    def get_private_key(self):
        return self.private_key.get_WIF(mainnet=False)


class Main(TestCase):

    def test_private_key_generated(self):
        print("Should generate a private key on construction")
        wallet = Main.Main();
        self.assertIsNotNone(wallet.get_private_key())
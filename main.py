from unittest import TestCase
from binascii import unhexlify
from Tx import TxIn, TxOut, Tx
from helper import decode_base58
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

    def send_transaction(self, prev_tx, target_addr, amount, change_amount):
        # Initialize Inputs
        tx_inputs = []

        # Create a tx input for transaction
        tx_inputs.append(TxIn
                         (prev_hash=prev_tx,
                          prev_index=1,
                          script_sig=b'',
                          sequence=0xffffffff
                        ))


        # Initialize Outputs for transaction
        tx_outputs = []

        # decode the hash160 from the target address, this is to create the p2pkh script (LOCKING SCRIPT) on the output ->
        # to the target address
        target_addr_h160 = decode_base58(target_addr)

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

        print("-------------------------------------------------------------")
        print("Should create a valid transaction to another address")

        # First step is to create the transaction and send the hex
        # Next steps are to cache available UTXO's as TX objects


        ## This will is the address that is generated by the private key when Wallet() was initialized
        sending_address = "mfke2PVhGePAy1GfZNotr6LeXfQ5nwnZTa"

        target_address = "mwM7hxtkequUMuTJATjHisfp6VACgNgcfv"

        target_amount = 0.5
        change_amount = 1.055

        wallet = Main().import_private_key(
            100897809677138163174856952607694300238573305027534078569886890414323321447504)

        self.assertEqual(200, wallet.send_transaction(
            prev_tx = unhexlify('fea5cbf4efc220a5512d394279778f75937c253cac32c43047cadffc9ee4d85c'),
            target_addr=target_address,
            amount=target_amount,
            change_amount=change_amount))

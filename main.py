from unittest import TestCase
from binascii import unhexlify, hexlify
from Tx import TxIn, TxOut, Tx
from Script import Script
from helper import decode_base58, p2pkh_script, bitcoin_to_satoshi, SIGHASH_ALL
import blockchain_explorer_helper
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

    def generate_p2pkh_pub_key(self, address):
        h160 = decode_base58(address)
        print("Decoded Address: {}".format(hexlify(h160)))
        print("Script: {}".format(hexlify(p2pkh_script(h160))))
        return p2pkh_script(h160)

    def send_transaction(self, prev_tx, prev_index, target_addr, amount, change_amount):
        # Initialize Inputs
        tx_inputs = []

        # Create a tx input for transaction
        tx_inputs.append(TxIn
                         (prev_hash=prev_tx,
                          prev_index=prev_index,
                          script_sig=b'',
                          sequence=0xffffffff
                          ))

        # Initialize Outputs for transaction
        tx_outputs = []

        # decode the hash160 from the target address, to be used in the p2pkh (LOCKING SCRIPT) on this output
        # Use the target_addr_h160 in create the p2pkh (LOCKING SCRIPT) on this output
        target_output_p2pkh = self.generate_p2pkh_pub_key(target_addr)

        # Convert the target output amount to satoshis
        output_amount_in_satoshis = bitcoin_to_satoshi(amount)

        # Create the TX OUTPUT, pass in the amount and the LOCKING SCRIPT
        tx_outputs.append(TxOut
                          (amount=output_amount_in_satoshis,
                           script_pub_key=target_output_p2pkh
                           ))

        # decode the hash160 for the change address (Sending coins back to sender)
        # Create the p2pkh (LOCKING SCRIPT) for the change output (sending back to sender)
        change_output_p2pkh = self.generate_p2pkh_pub_key(self.get_address(mainnet=False))

        # Convert the change amount output to satoshis
        change_amount_in_satoshis = bitcoin_to_satoshi(change_amount)

        # Create a tx output for the change transaction
        tx_outputs.append(TxOut
            (
            amount=change_amount_in_satoshis,
            script_pub_key=change_output_p2pkh
        ))

        # sign with tx object with SIGHASH_ALL
        sig_hash = SIGHASH_ALL

        # Create the Tx object with all the inputs and outputs created above
        transaction = Tx(version=1,
                         tx_ins=tx_inputs,
                         tx_outs=tx_outputs,
                         locktime=0,
                         testnet=True)

        # Hash of the message to sign
        z = transaction.sig_hash(0, sig_hash)

        # Sign z with the private key
        der = self.keys.sign(z).der()

        # Add the sighash to the der signature
        sig = der + bytes([sig_hash])

        # Input a new Script sig to unlock the input
        transaction.tx_ins[0].script_sig = Script([sig, self.sec])

        # Create a block explorer instance and serialize t
        block_explorer = blockchain_explorer_helper.BlockchainExplorer()
        raw_tx = hexlify(transaction.serialize()).decode('ascii')

        print(raw_tx)

        # return raw_tx
        return block_explorer.send_tx(raw_tx)


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
        print("Should return this address as an address generated by private key")
        expected = "mfke2PVhGePAy1GfZNotr6LeXfQ5nwnZTa"
        self.assertEqual(expected, wallet.get_address(mainnet=False))

        print("-------------------------------------------------------------")
        print("Should create a valid transaction and broadcast to the network")

        # First step is to create the transaction and send the hex
        # Next steps are to cache available UTXO's as TX objects

        ## This will is the address that is generated by the private key when Wallet() was initialized
        sending_address = "mwM7hxtkequUMuTJATjHisfp6VACgNgcfv"

        target_address = "mfke2PVhGePAy1GfZNotr6LeXfQ5nwnZTa"

        target_amount = 0.02
        change_amount = 0.017

        wallet2 = Main().import_private_key(
            53543775883506703906499148469479904297172220131041556152219913425601595776857)

        response = wallet2.send_transaction(
            prev_tx=unhexlify('6061273f139ad7dbb00d455a05c646f6019fd3ec932c537c75e6f210efdb378d'),
            prev_index=1,
            target_addr=target_address,
            amount=target_amount,
            change_amount=change_amount)

        expected = "010000000199ab3f377992df2ccad0af99dc846af032fbd982f916d72715d2eb0f2828342d010000006b483045022100ac3e55420a7b9897f0da43ff7a076895d0ead13fda49926041124aca00c5d6070220245aaefc7047563e42baa350cc7424efcb03ef7e70e596c28b5eca7223fa663f01210275bdc1759e7ffb5fb1f07655d5572cec8219b28250acdbc7f936396884d196f2ffffffff0280841e00000000001976a914029692862d60b5f84ba706b37939d074b6c5808588acc0fb3900000000001976a914ada5b5ba34eb8774388d0ac30c5bc3c8e8afae0388ac00000000"
        print("RESPONSE: {}".format(response))
        print("EXPECTED: {}".format(expected))
        self.assertEqual(expected, response)

    def test_p2pkh_generation(self):
        wallet = Main().import_private_key(
            53543775883506703906499148469479904297172220131041556152219913425601595776857)

        print("-------------------------------------------------------------")
        print("Should generate this adderss: 'mwM7hxtkequUMuTJATjHisfp6VACgNgcfv'")
        expected = "mwM7hxtkequUMuTJATjHisfp6VACgNgcfv"

        self.assertEqual(expected, wallet.get_address(mainnet=False))

        print("-------------------------------------------------------------")
        print("Should generate a p2pkh")
        expected = b'76a914029692862d60b5f84ba706b37939d074b6c5808588ac'

        self.assertEqual(expected, hexlify(wallet.generate_p2pkh_pub_key("mfke2PVhGePAy1GfZNotr6LeXfQ5nwnZTa")))

        print("-------------------------------------------------------------")
        print("Should generate a p2pkh for the change output")
        expected = b'76a914ada5b5ba34eb8774388d0ac30c5bc3c8e8afae0388ac'

        self.assertEqual(expected, hexlify(wallet.generate_p2pkh_pub_key(wallet.get_address(mainnet=False))))

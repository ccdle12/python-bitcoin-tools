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

    def send_transaction(self, prev_tx, prev_indx, target_addr, amount, change_amount):
        # Initialize Inputs
        tx_inputs = []

        # Create a tx input for transaction
        tx_inputs.append(TxIn
                         (prev_hash=prev_tx,
                          prev_index=prev_indx,
                          script_sig=b'',
                          sequence=0xffffffff
                          ))

        # Initialize Outputs for transaction
        tx_outputs = []

        # decode the hash160 from the target address, to be used in the p2pkh (LOCKING SCRIPT) on this output
        target_addr_h160 = decode_base58(target_addr)

        # Use the target_addr_h160 in create the p2pkh (LOCKING SCRIPT) on this output
        target_output_p2pkh_script = p2pkh_script(target_addr_h160)

        # Convert the target output amount to satoshis
        output_amount_in_satoshis = bitcoin_to_satoshi(amount)

        # Create the TX OUTPUT, pass in the amount and the LOCKING SCRIPT
        tx_outputs.append(TxOut
                          (amount=output_amount_in_satoshis,
                           script_pub_key=target_output_p2pkh_script
                           ))

        # decode the hash160 for the change address (Sending coins back to sender)
        change_addr_h160 = decode_base58(self.get_address(mainnet=False))
        print(self.get_address(mainnet=False))

        # Create the p2pkh (LOCKING SCRIPT) for the change output (sending back to sender)
        change_output_p2pkh_script = p2pkh_script(change_addr_h160)

        # Convert the change amount output to satoshis
        change_amount_in_satoshis = bitcoin_to_satoshi(change_amount)

        # Create a tx output for the change transaction
        tx_outputs.append(TxOut
                          (
                            amount=change_amount_in_satoshis,
                            script_pub_key=change_output_p2pkh_script
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
        transaction.tx_ins[0].script_sig = Script([self.sec, sig])

        # Create a block explorer instance and serialize t
        block_explorer = blockchain_explorer_helper.BlockchainExplorer()
        raw_tx = hexlify(transaction.serialize()).decode('ascii')

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

        response = wallet.send_transaction(
            prev_tx=unhexlify('fea5cbf4efc220a5512d394279778f75937c253cac32c43047cadffc9ee4d85c'),
            prev_indx=1,
            target_addr=target_address,
            amount=target_amount,
            change_amount=change_amount)

        print(response)
        self.assertEqual(200, response)



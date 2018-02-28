from unittest import TestCase
from binascii import unhexlify, hexlify
from Tx import TxIn, TxOut, Tx
from Script import Script
from helper import decode_base58, encode_base58_checksum, encode_base58, double_sha256, p2pkh_script, p2sh_script, bitcoin_to_satoshi, SIGHASH_ALL, sha256_ripemd160, generate_reedemScript, generate_p2sh_address, generate_p2pkh_pub_key, generate_p2sh_pub_key, satoshi_to_bitcoin
import blockchain_explorer_helper as BlockExplorer
import PrivateKey
from io import BytesIO
import json
from UTXO import UTXO

class Main:
    def __init__(self, secret=None):

        if secret is None:
            self.keys = PrivateKey.PrivateKey()
        else:
            self.keys = PrivateKey.PrivateKey.import_private_key(secret)

        self.sec = self.keys.public_key.get_sec(compressed=True)

        # Retrieve all existing UTXO's for this wallet (if any)
        self.get_UTXOs()

    def get_private_key(self):
        return self.keys.get_WIF(mainnet=False)

    def is_public_key_valid(self):
        return self.keys.is_on_curve()

    def get_address(self, mainnet=False):
        return self.keys.public_key.get_address(self.sec, mainnet)

    def get_balance(self, mainnet=False):
        response = BlockExplorer.request_balance(self.get_address())

        json_response = response.json()

        return json_response["balance"]


    def get_UTXOs(self, mainnet=False):
        response = BlockExplorer.request_UTXOs(self.get_address())
        json_response = response[0].json()

        UTXOs = []
        if response[1] == 'block_cypher':
            if 'txrefs' in json_response:
                print("TX_REFS: {}".format(json_response.get('txrefs')))
                tx_refs = json_response.get('txrefs')

                if len(tx_refs) > 0:
                    filtered = list(filter(lambda x: 'spent' in x and x.get('spent') is False, tx_refs))
                    UTXOs = list(map(lambda x: UTXO.parse(x), filtered))


        self.UTXOs = UTXOs
        return self.UTXOs

    @classmethod
    def import_private_key(cls, secret):
        return cls(secret)
 
    def send_transaction(self, prev_tx, prev_index, target_addr, amount, change_amount, redeem_script=None, p2sh=False):
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
        print("Target Address: {}".format(target_addr))

        # if p2sh:
            # print("Creating p2sh pubkey:")
            # target_output_script_pub_key = generate_p2sh_pub_key(target_addr)
            # print("P2SH CREATED: {}".format(target_output_script_pub_key))
        # else:    
        target_output_script_pub_key = generate_p2pkh_pub_key(target_addr)

        print("Target Output: {}".format(hexlify(target_output_script_pub_key)))

        # Convert the target output amount to satoshis
        output_amount_in_satoshis = bitcoin_to_satoshi(amount)

        # Create the TX OUTPUT, pass in the amount and the LOCKING SCRIPT
        tx_outputs.append(TxOut
                          (amount=output_amount_in_satoshis,
                           script_pub_key=target_output_script_pub_key
                           ))

        # decode the hash160 for the change address (Sending coins back to sender)
        # Create the p2pkh (LOCKING SCRIPT) for the change output (sending back to sender)

        #TODO: CHECK CHANGE ADDRESS TYPE TO GENERATE THE CORRECT SCRIPT PUB KEY
        change_output_p2pkh = generate_p2pkh_pub_key(self.get_address(mainnet=False))

        # Convert the change amount output to satoshis
        change_amount_in_satoshis = bitcoin_to_satoshi(change_amount)

        # Create a tx output for the change transaction
        tx_outputs.append(TxOut
            (
            amount=change_amount_in_satoshis,
            script_pub_key=change_output_p2pkh
        ))

        # sign with tx object with SIGHASH_ALL, sender is signing all the inputs and outputs
        sig_hash = SIGHASH_ALL

        # Create the Tx object with all the inputs and outputs created above
        transaction = Tx(version=1,
                         tx_ins=tx_inputs,
                         tx_outs=tx_outputs,
                         locktime=0,
                         testnet=True)

        # Hash of the message to sign
        # if p2sh:
            # z = transaction.sig_hash(0, sig_hash, redeem_script)
        # else:
        z = transaction.sig_hash(0, sig_hash)

        # Sign z with the private key
        der = self.keys.sign(z).der()

        # Add the sighash to the der signature
        sig = der + bytes([sig_hash])

        # Input a new Script sig to unlock the input
        sec = unhexlify(self.keys.public_key.get_sec(compressed=True))

        # Creating the p2pkh script sig to UNLOCK the input at index 0
        unlocking_script = Script([sig, sec])
        transaction.tx_ins[0].script_sig = unlocking_script

        # Create a block explorer instance and serialize transaction
        raw_tx = hexlify(transaction.serialize()).decode('ascii')
        print(raw_tx)

        # print("RAW TX: {}".format(raw_tx))
        return BlockExplorer.send_tx(raw_tx)



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

        target_amount = 0.002
        change_amount = 0.014

        wallet2 = Main().import_private_key(
            53543775883506703906499148469479904297172220131041556152219913425601595776857)


        expected = "010000000199ab3f377992df2ccad0af99dc846af032fbd982f916d72715d2eb0f2828342d010000006b483045022100ac3e55420a7b9897f0da43ff7a076895d0ead13fda49926041124aca00c5d6070220245aaefc7047563e42baa350cc7424efcb03ef7e70e596c28b5eca7223fa663f01210275bdc1759e7ffb5fb1f07655d5572cec8219b28250acdbc7f936396884d196f2ffffffff0280841e00000000001976a914029692862d60b5f84ba706b37939d074b6c5808588acc0fb3900000000001976a914ada5b5ba34eb8774388d0ac30c5bc3c8e8afae0388ac00000000"

        print("Should raise run time error since the input used has been spent")
        with self.assertRaises(RuntimeError):
            response = wallet2.send_transaction(
                prev_tx=unhexlify('1b562bc7c059af8a61bec721bae5c8f47d929389049b38525045e6330ac7acf2'),
                prev_index=1,
                target_addr=target_address,
                amount=target_amount,
                change_amount=change_amount)

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

        self.assertEqual(expected, hexlify(generate_p2pkh_pub_key("mfke2PVhGePAy1GfZNotr6LeXfQ5nwnZTa")))

        print("-------------------------------------------------------------")
        print("Should generate a p2pkh for the change output")
        expected = b'76a914ada5b5ba34eb8774388d0ac30c5bc3c8e8afae0388ac'

        self.assertEqual(expected, hexlify(generate_p2pkh_pub_key(wallet.get_address(mainnet=False))))

    
    def test_p2sh_generation(self):
        print("Should genrate a P2SH using wallet1 and wallet2")
        
        # Wallet 1
        wallet1 = Main().import_private_key(
            53543775883506703906499148469479904297172220131041556152219913425601595776857)

        # Wallet 2
        wallet2 = Main().import_private_key(
            100897809677138163174856952607694300238573305027534078569886890414323321447504)

        print("p2sh reedem script is generated")
        p2sh_reedemScript = generate_reedemScript(wallet1.sec, [unhexlify(wallet2.sec)])
        self.assertIsNotNone(p2sh_reedemScript)

        print("p2sh redeem script generated is valid")
        expected = b'52210275bdc1759e7ffb5fb1f07655d5572cec8219b28250acdbc7f936396884d196f221035fb3daf8558881ab26e0955e96eec75937c513d730c5ef5866b4a2a0bd52206052ae'
        self.assertEqual(expected, hexlify(p2sh_reedemScript))

        print("Should throw run time error, when passing empty list of pub keys")
        with self.assertRaises(RuntimeError):
            p2sh_reedemScript = generate_reedemScript(wallet1.sec, [])

        print("Should generate an address for reedeem script")
        print(hexlify(p2sh_reedemScript))

        p2sh_address = generate_p2sh_address(p2sh_reedemScript, mainnet=False)
        print("p2sh_address: {}".format(p2sh_address))
        self.assertIsNotNone(p2sh_address)

    def test_send_tx_to_p2sh(self):
        # Address: mhpzxr92VHqCXy3Zpat41vGgQuv9YcKzt7
        # SEC: b'02d0b55a1e551abfa7123d3e2130325b5cc77103108a84b91c05add554dfbebebf'

        # P2SH Address: 2N3gQkVbrV8Kam9Zv1G4QwuCt7oF2skpCPE
        # Redeem Script: 52210275bdc1759e7ffb5fb1f07655d5572cec8219b28250acdbc7f936396884d196f221035fb3daf8558881ab26e0955e96eec75937c513d730c5ef5866b4a2a0bd52206052ae

        wallet1 = Main().import_private_key(
            12196958284001970079242031404833655250066517166607428365484251744560960260904)

        print("Should hash160 correctly")
        print("----------------------------------------------------------------------------------------------------------------------------")
        redeem_script = b'52210275bdc1759e7ffb5fb1f07655d5572cec8219b28250acdbc7f936396884d196f221035fb3daf8558881ab26e0955e96eec75937c513d730c5ef5866b4a2a0bd52206052ae'
        redeem_script = unhexlify(redeem_script)
        h160 = hexlify(sha256_ripemd160(redeem_script)).decode('ascii')
        expected = b'7274a4081f8e7f7fd9b4d1f048e853e96c6352c5'.decode('ascii')

        self.assertEqual(expected, h160)


        # target_address = "2N3gQkVbrV8Kam9Zv1G4QwuCt7oF2skpCPE"
        print("Should generate correct address")
        print("----------------------------------------------------------------------------------------------------------------------------")
        target_address = generate_p2sh_address(redeem_script)
        expected = '2N3gQkVbrV8Kam9Zv1G4QwuCt7oF2skpCPE'
        print("Target address: {}".format(target_address))
        self.assertEqual(expected, target_address)
        
        # response = wallet1.send_transaction(
        #     prev_tx = unhexlify('7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20'), 
        #     prev_index = 0, 
        #     target_addr = 'mhpzxr92VHqCXy3Zpat41vGgQuv9YcKzt7', 
        #     amount = 0.019,
        #     change_amount = 0.001,
        #     redeem_script=unhexlify(b'52210275bdc1759e7ffb5fb1f07655d5572cec8219b28250acdbc7f936396884d196f221035fb3daf8558881ab26e0955e96eec75937c513d730c5ef5866b4a2a0bd52206052ae'),
        #     p2sh=False)
        
        # self.assertEqual(201, response)

        print("P2SH should contain the same hashed redeem script")
        print("----------------------------------------------------------------------------------------------------------------------------")
        p2sh_scriptPubKey = generate_p2sh_pub_key(target_address)
        print(p2sh_scriptPubKey)

        # Extracting p2sh from scriptPubKey
        stream = BytesIO(p2sh_scriptPubKey)
        current = stream.read(1)

        for i in range(2):
            current = stream.read(1)
            
        p2sh_addr_hash160 = b''
        while current != b'\x87':
            p2sh_addr_hash160 += current
            current = stream.read(1)

        p2sh_from_scriptPubKey = hexlify(p2sh_addr_hash160)
        reedeem_script_hash160 = hexlify(sha256_ripemd160(redeem_script))

        print("Hexed p2sh addr: {}".format(p2sh_from_scriptPubKey))
        print("Redeem Script hashed: {}".format(hexlify(sha256_ripemd160(redeem_script))))
        
        #Expecting: 7274a4081f8e7f7fd9b4d1f048e853e96c6352c5
        self.assertEqual(p2sh_from_scriptPubKey, reedeem_script_hash160)

        print("Should now take hash160 from script pub key and create address")
        print("----------------------------------------------------------------------------------------------------------------------------")
        expected = '2LSKzp4QheQU5VR1Zuaj91Q7jbnDFzPAZ1V'
        prefix = b'\xc0'
        print("P2SH from scriptPubKey: {}".format(p2sh_from_scriptPubKey))
        address = encode_base58_checksum(prefix + unhexlify(p2sh_from_scriptPubKey))

        self.assertEqual(expected, address)


        print("Should take address and decode base58 to get hash160")
        print("----------------------------------------------------------------------------------------------------------------------------")
        #7274a4081f8e7f7fd9b4d1f048e853e96c6352c5
        expected = b'7274a4081f8e7f7fd9b4d1f048e853e96c6352c5'
        hash160 = decode_base58(address)

        self.assertEqual(expected, hexlify(hash160))

        print("Address from Block Cypher is decoded to the same h160, what does this mean?")
        print("----------------------------------------------------------------------------------------------------------------------------")
        #7274a4081f8e7f7fd9b4d1f048e853e96c6352c5
        expected = b'7274a4081f8e7f7fd9b4d1f048e853e96c6352c5'
        h160 = decode_base58('2N3gQkVbrV8Kam9Zv1G4QwuCt7oF2skpCPE')
        
        self.assertEqual(expected, hexlify(h160))

    def test_get_balance(self):
        wallet1 = Main().import_private_key(
            12196958284001970079242031404833655250066517166607428365484251744560960260904)

        print("Should return a the balance of wallet1 address")
        expected = satoshi_to_bitcoin(104900000)
        balance = satoshi_to_bitcoin(wallet1.get_balance())

        self.assertEqual(expected, balance)

    def test_get_UTXOs(self):
        wallet1 = Main().import_private_key(
            12196958284001970079242031404833655250066517166607428365484251744560960260904)

        print("Should return a list of UTXOs greater than 0")
        print("----------------------------------------------------------------------------------------------------------------------------")
        UTXOs = wallet1.get_UTXOs()

        self.assertTrue(len(UTXOs) > 0)
        print(len(UTXOs))

        for x in UTXOs:
            print(x)

        print("Should get a prev tx of a UTXO")
        print("----------------------------------------------------------------------------------------------------------------------------")
        expected = "7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20"
        self.assertEqual(expected, UTXOs[0].tx_hash)

        print("Should only return a list of UTXO's of length 4")
        print("----------------------------------------------------------------------------------------------------------------------------")
        expected = 1
        print(UTXOs)

        self.assertEqual(expected, len(UTXOs))

        print("Should cache UTXOs in list in wallet object")
        print("----------------------------------------------------------------------------------------------------------------------------")

        self.assertIsNotNone(wallet1.UTXOs)

    def test_send_tx(self):
        # Address of wallet1: mhpzxr92VHqCXy3Zpat41vGgQuv9YcKzt7
        wallet1 = Main().import_private_key(
            12196958284001970079242031404833655250066517166607428365484251744560960260904)

        print("Address: {}".format(wallet1.get_address()))

        # def send_transaction(self, prev_tx, prev_index, target_addr, amount, change_amount, redeem_script=None, p2sh=False):
        response = wallet1.send_transaction(unhexlify('7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20'), 1, 'n1adMtYYKT72d3NKjbFiE7Wv4tHSpiEC9M', 1.039, 0.01)

        self.assertEqual(409, response.status_code)

        print("Should find the optimum inputs according to target output amount")
        wallet2 = Main().import_private_key(11721815747117917583098828363610524599463178642721196404024595875870538950423)
        print("Printing UTXOs: {}".format(wallet2.UTXOs))
        print("Printing Addres: {}".format(wallet2.get_address()))
        




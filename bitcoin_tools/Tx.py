from bitcoin_tools.helper import little_endian_to_int, read_varint, satoshi_to_bitcoin, int_to_little_endian, encode_varint, double_sha256, SIGHASH_ALL, decode_base58
from bitcoin_tools.Signature import Signature
from bitcoin_tools.Script import Script
from bitcoin_tools.S256Point import S256Point
import requests
from io import BytesIO
from binascii import unhexlify, hexlify


class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=True):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.testnet = testnet

    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'

        tx_outs = ''
        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'

        return 'version: {}\ntx_ins:\n{}\ntx_outs:\n{}\nlocktime: {}\n'.format(
            self.version,
            tx_ins,
            tx_outs,
            self.locktime,
        )

    # Allows method to be called without instantiating class, cls points to the class not the object instance
    # MUST pass in RAW BYTES
    @classmethod
    def parse(cls, transaction_bytes):
        if type(transaction_bytes) is str:
            transaction_bytes = unhexlify(transaction_bytes)

        # Create a stream of bytes
        stream = BytesIO(transaction_bytes)

        # Retrieve the version as int
        # Read the first 4 bytes of the stream, interpret as int, little endian architecture
        version = little_endian_to_int(stream.read(4))

        # Number of inputs is a varint
        num_inputs = read_varint(stream)

        inputs = []
        for _ in range(num_inputs):
            inputs.append(TxIn.parse(stream))

        # Reads number of outputs as a varint to int
        num_outputs = read_varint(stream)
        outputs = []
        for _ in range(num_outputs):
            outputs.append(TxOut.parse(stream))

        # Read the locktime as int, little endian
        locktime = little_endian_to_int(stream.read(4))

        return cls(version, inputs, outputs, locktime)

    # TODO: Serializes data in object and returns as bytes
    def serialize(self):
        result = int_to_little_endian(self.version, 4)

        result += encode_varint(len(self.tx_ins))

        for tx_in in self.tx_ins:
            result += tx_in.serialize()

        result += encode_varint(len(self.tx_outs))

        for tx_out in self.tx_outs:
            result += tx_out.serialize()

        result += int_to_little_endian(self.locktime, 4)

        return result

    def calculate_fee(self):
        input_amount = 0
        output_amount = 0

        for tx_in in self.tx_ins:
            input_amount += tx_in.value()

        for tx_out in self.tx_outs:
            output_amount += tx_out.amount

        return input_amount - output_amount

    def sig_hash(self, input_index, hash_type):
        '''Returns the integer representation of the hash that needs to get
        signed for index input_index'''
        # create a new set of tx_ins (alt_tx_ins)
        alt_tx_ins = []

        # iterate over self.tx_ins
        for tx_in in self.tx_ins:
            # create a new TxIn that has a blank script_sig (b'') and add to alt_tx_ins
            print("Prev Transaction of input: {}".format(hexlify(tx_in.prev_hash)))
            alt_tx_ins.append(TxIn(
                prev_hash=tx_in.prev_hash,
                prev_index=tx_in.prev_index,
                script_sig=b'',
                sequence=tx_in.sequence,
            ))

        # grab the input at the input_index
        # "1b562bc7c059af8a61bec721bae5c8f47d929389049b38525045e6330ac7acf2:1"
        signing_input = alt_tx_ins[input_index]
        print("SIGNING INPUT: {}".format(signing_input))

        # grab the script_pubkey of the input
        script_pubkey = signing_input.script_pubkey(self.testnet)
        print("Script pubkey: {}".format(script_pubkey))

        # Check the sig type
        sig_type = script_pubkey.type()

        if sig_type == 'p2pkh':
            signing_input.script_sig = script_pubkey
        elif sig_type == 'p2sh':
            # Get the tx input at index passed of the tx_object
            current_input = self.tx_ins[input_index]
            # current_input.script_sig = Script.parse(redeem_script)
            # print("REDEEM SCRIPT Sig Passed: {}".format(current_input.redeem_script()))

            # signing_input.script_sig = Script.parse(current_input.redeem_script())
        else:
            raise RuntimeError('no valid sig_type')

        # create an alternate transaction with the modified tx_ins
        alt_tx = self.__class__(
            version=self.version,
            tx_ins=alt_tx_ins,
            tx_outs=self.tx_outs,
            locktime=self.locktime)

        # add the hash_type int 4 bytes, little endian
        result = alt_tx.serialize() + int_to_little_endian(hash_type, 4)

        # get the double_sha256 of the tx serialization
        s256 = double_sha256(result)

        # convert this to a big-endian integer using int.from_bytes(x, 'big')
        return int.from_bytes(s256, 'big')

    def validate_signature(self, index_pos):
        # Parse the transaction

        # Get the input at index_pos provided
        tx_in = self.tx_ins[index_pos]

        # Get the der signature and hash type
        der, hash_type = tx_in.der_signature()

        # Parse the der signature
        signature = Signature.parse(der)

        # Get the sec pub key of the input
        sec = tx_in.sec_pubkey()

        # Parse the sec_pubkey to return x,y points
        point = S256Point.parse(sec)

        # Use sig_has method on transaction to turn transaction into z
        sig_hash = self.sig_hash(index_pos, hash_type)

        # Verify both x co-ordinates are the same in signed hash and signature
        return point.verify(sig_hash, signature)


class TxIn:
    cache = {}

    def __init__(self, prev_hash, prev_index, script_sig, sequence):
        self.prev_hash = prev_hash
        self.prev_index = prev_index
        self.script_sig = Script.parse(script_sig)
        self.sequence = sequence

    def __repr__(self):
        return '{}:{}'.format(
            hexlify(self.prev_hash).decode('ascii'),
            self.prev_index,
        )

    @classmethod
    def parse(cls, stream):
        # Read prev_hash 32 bytes little endian
        prev_hash = stream.read(32)[::-1]

        # Read the prev_index 4 bytes, little endian as int
        prev_index = little_endian_to_int(stream.read(4))

        # Script sig is variable length, use varint to find out its length
        # The first byte signifies the length
        script_sig_length = read_varint(stream)
        script_sig = stream.read(script_sig_length)

        # Read sequence 4 bytes, little endian as int
        sequence = little_endian_to_int(stream.read(4))

        return cls(prev_hash, prev_index, script_sig, sequence)

    def serialize(self):
        result = self.prev_hash[::-1]

        result += int_to_little_endian(self.prev_index, 4)

        script_sig = self.script_sig.serialize()

        result += encode_varint(len(script_sig))

        result += script_sig

        result += int_to_little_endian(self.sequence, 4)

        return result

    @classmethod
    def get_url(self, testnet=True):
        if testnet:
            return 'https://testnet.blockexplorer.com/api'
        else:
            return 'https://btc-bitcore3.trezor.io/api'

    # Fetches Raw TX of the input and creates a Tx Object
    def fetch_tx(self, testnet=True):
        if self.prev_hash not in self.cache:
            url = self.get_url(testnet) + '/rawtx/{}'.format(hexlify(self.prev_hash).decode('ascii'))
            response = requests.get(url)

            if response.status_code == 404:
                raise RuntimeError("404 error received, usually a bad prex_tx hash")

            js_response = response.json()

            if 'rawtx' not in js_response:
                raise RuntimeError('Did not receive expected response: {}'.format(js_response))

            raw = unhexlify(js_response['rawtx'])
            tx = Tx.parse(raw)
            self.cache[self.prev_hash] = tx

        return self.cache[self.prev_hash]

    def value(self, testnet=True):
        tx = self.fetch_tx()

        return tx.tx_outs[self.prev_index].amount

    def der_signature(self, index=0):

        signature = self.script_sig.der_signature(index=index)
        print("Signature in der_signature: {}".format(hexlify(signature)))

        # last byte is the hash_type, rest is the signature
        return signature[:-1], signature[-1]

    def sec_pubkey(self, index=0):
        return self.script_sig.sec_pubkey(index=index)

    # Fetches the script_pub key of this tx input (LOCKING SCRIPT)
    def script_pubkey(self, testnet=True):
        '''Get the scriptPubKey by looking up the tx hash on block explorer server
        Returns the binary scriptpubkey (LOCKING SCRIPT)
        '''
        tx = self.fetch_tx(testnet=testnet)

        return tx.tx_outs[self.prev_index].script_pub_key

    def redeem_script(self):
        ''' Returns a redeem script if there is one '''
        return self.script_sig.redeem_script()



class TxOut:
    def __init__(self, amount, script_pub_key):
        self.amount = amount
        self.script_pub_key = Script.parse(script_pub_key)

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_pub_key)

    @classmethod
    def parse(cls, stream):
        # Read amount of the output, Little Endian, 8 bytes as int?
        amount = little_endian_to_int(stream.read(8))

        # Retrieve script_pub_key, variable, read varint for length
        script_pub_key_length = read_varint(stream)
        script_pub_key = stream.read(script_pub_key_length)

        return cls(amount, script_pub_key)

    def serialize(self):
        result = int_to_little_endian(self.amount, 8)

        scriptPubKey = self.script_pub_key.serialize()

        result += encode_varint(len(scriptPubKey))

        result += scriptPubKey

        return result
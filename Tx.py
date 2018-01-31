from unittest import TestCase
from io import BytesIO
from binascii import unhexlify, hexlify
from helper import little_endian_to_int, read_varint, satoshi_to_bitcoin, int_to_little_endian, encode_varint
from Script import Script


class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime

    # Allows method to be called without instantiating class, cls points to the class not the object instance
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

    #TODO: Serializes data in object and returns as bytes
    def serialize(self):
        # TODO: 1. RETURN THE VERSION SERIALIZED, LITTLE ENDIAN 4 BYTES
        result = int_to_little_endian(self.version, 4)

        # TODO: 2. RETURN THE NUMBER OF INPUTS AS A VARINT, USE LEN(SELF.TX_INS)
        result += encode_varint(len(self.tx_ins))

        # TODO: 3. RETURN EACH TX_IN AS BYTE, FOR LOOP OVER TX_INS AND CALL EACH TX_IN TO SERIALIZE AND ADD THE BYTES TO RESULT
        for tx_in in self.tx_ins:
            # TODO: 4. CREATE SERIALIZE() IN TX_IN
            result += tx_in.serialize()


        #TODO 5. Retrun number of Outputs as a varint, len(self.tx_outs)
        result += encode_varint(len(self.tx_outs))

        #TODO 6. Return each tx_out as a byte, for loop over tx_outs and call each tx_out to serialize()
        for tx_out in self.tx_outs:
            result += tx_out.serialize()

        result += int_to_little_endian(self.locktime, 4)

        return result

class TxIn:
    def __init__(self, prev_hash, prev_index, script_sig, sequence):
        self.prev_hash = prev_hash
        self.prev_index = prev_index
        self.script_sig = Script.parse(script_sig)
        self.sequence = sequence

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


class TxOut:
    def __init__(self, amount, script_pub_key):
        self.amount = amount
        self.script_pub_key = Script.parse(script_pub_key)

    @classmethod
    def parse(cls, stream):
        # Read amount of the output, Little Endian, 8 bytes as int?
        amount = little_endian_to_int(stream.read(8))

        # Retrieve script_pub_key, variable, read varint for length
        script_pub_key_length = read_varint(stream)
        script_pub_key = stream.read(script_pub_key_length)

        return cls(amount, script_pub_key)

    def serialize(self):
        #TODO: Return th value/amount, 8 bytes, little endian
        result = int_to_little_endian(self.amount, 8)

        #todo: Return the scriptPubKey, variable length
        scriptPubKey = self.script_pub_key.serialize()

        result += encode_varint(len(scriptPubKey))

        result += scriptPubKey

        return result


class TxTest(TestCase):
    def test_parse_transaction(self):
        transaction = '010000000456919960ac691763688d3d3bcea9ad6ecaf875df5339e148a1fc61c6ed7a069e010000006a47304402204585bcdef85e6b1c6af5c2669d4830ff86e42dd205c0e089bc2a821657e951c002201024a10366077f87d6bce1f7100ad8cfa8a064b39d4e8fe4ea13a7b71aa8180f012102f0da57e85eec2934a82a585ea337ce2f4998b50ae699dd79f5880e253dafafb7feffffffeb8f51f4038dc17e6313cf831d4f02281c2a468bde0fafd37f1bf882729e7fd3000000006a47304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a7160121035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937feffffff567bf40595119d1bb8a3037c356efd56170b64cbcc160fb028fa10704b45d775000000006a47304402204c7c7818424c7f7911da6cddc59655a70af1cb5eaf17c69dadbfc74ffa0b662f02207599e08bc8023693ad4e9527dc42c34210f7a7d1d1ddfc8492b654a11e7620a0012102158b46fbdff65d0172b7989aec8850aa0dae49abfb84c81ae6e5b251a58ace5cfeffffffd63a5e6c16e620f86f375925b21cabaf736c779f88fd04dcad51d26690f7f345010000006a47304402200633ea0d3314bea0d95b3cd8dadb2ef79ea8331ffe1e61f762c0f6daea0fabde022029f23b3e9c30f080446150b23852028751635dcee2be669c2a1686a4b5edf304012103ffd6f4a67e94aba353a00882e563ff2722eb4cff0ad6006e86ee20dfe7520d55feffffff0251430f00000000001976a914ab0c0b2e98b1ab6dbf67d4750b0a56244948a87988ac005a6202000000001976a9143c82d7df364eb6c75be8c80df2b3eda8db57397088ac46430600'
        parsed_tx = Tx.parse(transaction)
        script_sig = "47304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a7160121035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937"

        print("Should return the script sig of the second input")
        self.assertEqual(script_sig, hexlify(parsed_tx.tx_ins[1].script_sig).decode('ascii'))

        print("-------------------------------------------------------------------------------------------")
        print("Amount of inputs should be 4")
        self.assertEqual(4, len(parsed_tx.tx_ins))

        print("-------------------------------------------------------------------------------------------")
        print("Previous hash/transaction should be 32 bytes in length")
        self.assertEqual(32 * 2, len(hexlify(parsed_tx.tx_ins[0].prev_hash).decode('ascii')))

        print("-------------------------------------------------------------------------------------------")
        print("First output amount should be 100273 Satoshis ")
        self.assertEqual(1000273, parsed_tx.tx_outs[0].amount)

        print("-------------------------------------------------------------------------------------------")
        print("First output amount should be 0.01000273 Bitcoin")
        self.assertEqual(0.01000273, satoshi_to_bitcoin(parsed_tx.tx_outs[0].amount))

    def test_serialization(self):
        raw_tx = unhexlify(
            '0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')

        tx = Tx.parse(raw_tx)
        expected_version = 1
        print("-------------------------------------------------------------------------------------------")
        print("Should return unserialized version number as int")
        self.assertEqual(expected_version, tx.version)


        print("-------------------------------------------------------------------------------------------")
        print("Should return the exact same byte values as tx_raw, since we are serializing the data held in the Tx Object")

        tx_serialized = tx.serialize()
        self.assertEqual(tx_serialized, raw_tx)

    def test_fee_calculation(self):
        print("Should return teh fee amount in satoshis")
        hex_tx = '010000000456919960ac691763688d3d3bcea9ad6ecaf875df5339e148a1fc61c6ed7a069e010000006a47304402204585bcdef85e6b1c6af5c2669d4830ff86e42dd205c0e089bc2a821657e951c002201024a10366077f87d6bce1f7100ad8cfa8a064b39d4e8fe4ea13a7b71aa8180f012102f0da57e85eec2934a82a585ea337ce2f4998b50ae699dd79f5880e253dafafb7feffffffeb8f51f4038dc17e6313cf831d4f02281c2a468bde0fafd37f1bf882729e7fd3000000006a47304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a7160121035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937feffffff567bf40595119d1bb8a3037c356efd56170b64cbcc160fb028fa10704b45d775000000006a47304402204c7c7818424c7f7911da6cddc59655a70af1cb5eaf17c69dadbfc74ffa0b662f02207599e08bc8023693ad4e9527dc42c34210f7a7d1d1ddfc8492b654a11e7620a0012102158b46fbdff65d0172b7989aec8850aa0dae49abfb84c81ae6e5b251a58ace5cfeffffffd63a5e6c16e620f86f375925b21cabaf736c779f88fd04dcad51d26690f7f345010000006a47304402200633ea0d3314bea0d95b3cd8dadb2ef79ea8331ffe1e61f762c0f6daea0fabde022029f23b3e9c30f080446150b23852028751635dcee2be669c2a1686a4b5edf304012103ffd6f4a67e94aba353a00882e563ff2722eb4cff0ad6006e86ee20dfe7520d55feffffff0251430f00000000001976a914ab0c0b2e98b1ab6dbf67d4750b0a56244948a87988ac005a6202000000001976a9143c82d7df364eb6c75be8c80df2b3eda8db57397088ac46430600'
        tx = Tx.parse(hex_tx)
        expected = 140500
        self.assertEqual(expected, tx.calculate_fee())
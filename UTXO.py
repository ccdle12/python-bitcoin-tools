from unittest import TestCase

class UTXO:
    def __init__(self, tx_hash, block_height, tx_output, value, confirmations, confirmed, double_spend):
        self.tx_hash = tx_hash
        self.block_height = block_height
        self.tx_output = tx_output
        self.value = value
        self.confirmations = confirmations
        self.confirmed = confirmed
        self.double_spend = double_spend

    @staticmethod
    def schema_type(raw_utxo):
        if type(raw_utxo) is dict:
            if ('tx_hash' in raw_utxo
                and 'block_height' in raw_utxo  
                and 'tx_input_n' in raw_utxo 
                and 'value' in raw_utxo 
                and 'ref_balance' in raw_utxo 
                and 'spent' in raw_utxo 
                and 'confirmations' in raw_utxo 
                and 'confirmed' in raw_utxo 
                and 'double_spend' in raw_utxo):
                return 'block_cypher'

        raise RuntimeError('Unknown Schema Type') 

    @classmethod
    def parse(cls, raw_utxo):
        schema_type = UTXO.schema_type(raw_utxo)

        if schema_type == 'block_cypher':
            return cls(tx_hash=raw_utxo.get('tx_hash'), 
                    block_height=raw_utxo.get('block_height'), 
                    tx_output=raw_utxo.get('tx_output'),
                    value=raw_utxo.get('value'), 
                    confirmations=raw_utxo.get('confirmations'),
                    confirmed=raw_utxo.get('confirmed'), 
                    double_spend=raw_utxo.get('double_spend'))

   


class UTXOTest(TestCase):
    def test_can_init(self):
        print("Can Init a UTXO object")
        UTXOObj = UTXO(tx_hash='7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20',
                                  block_height=1283283,   
                                  tx_output=1,
                                  value=104900000,
                                  confirmations=3322,
                                  confirmed="2018-02-17T19:10:32Z",
                                  double_spend=False)

        self.assertIsNotNone(UTXOObj)

    def test_can_parse(self):
        print("Should parse response and init object")
        utxo_object = UTXO.parse({'tx_hash': '7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20', 'block_height': 1283283, 'tx_input_n': -1, 'tx_output_n': 1, 'value': 104900000, 'ref_balance': 211900000, 'spent': False, 'confirmations': 3326, 'confirmed': '2018-02-17T19:10:32Z', 'double_spend': False})

        self.assertEqual('7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20', utxo_object.tx_hash)

    def test_should_return_block_cypher_schema(self):
        print("Should return 'block_cypher'")
        utxo_object = UTXO.parse({'tx_hash': '7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20', 'block_height': 1283283, 'tx_input_n': -1, 'tx_output_n': 1, 'value': 104900000, 'ref_balance': 211900000, 'spent': False, 'confirmations': 3326, 'confirmed': '2018-02-17T19:10:32Z', 'double_spend': False})

        schema_type = utxo_object.schema_type({'tx_hash': '7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20', 'block_height': 1283283, 'tx_input_n': -1, 'tx_output_n': 1, 'value': 104900000, 'ref_balance': 211900000, 'spent': False, 'confirmations': 3326, 'confirmed': '2018-02-17T19:10:32Z', 'double_spend': False})

        self.assertEqual('block_cypher', schema_type)

    def test_should_return_run_time_error(self):
        print("Should return Run Time Error Unknown Schema Type")
        utxo_object = UTXO.parse({'tx_hash': '7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20', 'block_height': 1283283, 'tx_input_n': -1, 'tx_output_n': 1, 'value': 104900000, 'ref_balance': 211900000, 'spent': False, 'confirmations': 3326, 'confirmed': '2018-02-17T19:10:32Z', 'double_spend': False})

        with self.assertRaises(RuntimeError):
            schema_type = utxo_object.schema_type({'block_height': 1283283, 'tx_input_n': -1, 'tx_output_n': 1, 'value': 104900000, 'ref_balance': 211900000, 'spent': False, 'confirmations': 3326, 'confirmed': '2018-02-17T19:10:32Z', 'double_spend': False})

        print("Should return Run Time Error Unknown Schema Type")
        with self.assertRaises(RuntimeError):
            utxo_object = UTXO.parse({'block_height': 1283283, 'tx_input_n': -1, 'tx_output_n': 1, 'value': 104900000, 'ref_balance': 211900000, 'spent': False, 'confirmations': 3326, 'confirmed': '2018-02-17T19:10:32Z', 'double_spend': False})

        
        
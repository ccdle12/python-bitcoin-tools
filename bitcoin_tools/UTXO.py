class UTXO:
    def __init__(self, tx_hash, block_height, tx_index, value, confirmations, confirmed, double_spend):
        self.tx_hash = tx_hash
        self.block_height = block_height
        self.tx_index = tx_index
        self.value = value
        self.confirmations = confirmations
        self.confirmed = confirmed
        self.double_spend = double_spend

    def __repr__(self):
        return "\nUTXO: \ntx_hash: {}\nblock_height:{}\ntx_index:{}\nvalue:{}\nconfirmations:{}\nconfirmed:{}\ndouble_spend:{}\n".format(
            self.tx_hash,
            self.block_height,
            self.tx_index,
            self.value,
            self.confirmations,
            self.confirmed,
            self.double_spend
        )

    @staticmethod
    def schema_type(raw_utxo):
        if type(raw_utxo) is dict:
            if ('tx_hash' in raw_utxo
                and 'block_height' in raw_utxo  
                and 'tx_input_n' in raw_utxo 
                and 'tx_output_n' in raw_utxo
                and 'value' in raw_utxo 
                and 'ref_balance' in raw_utxo 
                and 'spent' in raw_utxo 
                and 'confirmations' in raw_utxo 
                and 'confirmed' in raw_utxo 
                and 'double_spend' in raw_utxo):
                return 'block_cypher'

        if type(raw_utxo) is dict:
            # ({'hash': 'fea5cbf4efc220a5512d394279778f75937c253cac32c43047cadffc9ee4d85c', 'time': '2018-02-04T12:29:01+0000', 'confirmations': 12468, 'is_coinbase': False, 'value': 156000000, 'index': 1, 'address': 'mfke2PVhGePAy1GfZNotr6LeXfQ5nwnZTa', 'type': 'pubkeyhash', 'multisig': None, 'script': 'OP_DUP OP_HASH160 029692862d60b5f84ba706b37939d074b6c58085 OP_EQUALVERIFY OP_CHECKSIG', 'script_hex': '76a914029692862d60b5f84ba706b37939d074b6c5808588ac'})
            if ('hash' in raw_utxo
                and 'time' in raw_utxo
                and 'confirmations' in raw_utxo
                and 'is_coinbase' in raw_utxo
                and 'value' in raw_utxo
                and 'index' in raw_utxo
                and 'address' in raw_utxo
                and 'type' in raw_utxo
                and 'multisig' in raw_utxo
                and 'script' in raw_utxo
                and 'script_hex' in raw_utxo):
                return 'block_trail'

        raise RuntimeError('Unknown Schema Type') 

    @classmethod
    def parse(cls, raw_utxo):
        schema_type = UTXO.schema_type(raw_utxo)

        # utxo_object = UTXO.parse({'tx_hash': '7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20', 'block_height': 1283283, 'tx_input_n': -1, 'tx_output_n': 1, 'value': 104900000, 'ref_balance': 211900000, 'spent': False, 'confirmations': 3326, 'confirmed': '2018-02-17T19:10:32Z', 'double_spend': False})
        if schema_type == 'block_cypher':
            return cls(tx_hash=raw_utxo.get('tx_hash'), 
                    block_height=raw_utxo.get('block_height'), 
                    tx_index=raw_utxo.get('tx_output_n'),
                    value=raw_utxo.get('value'), 
                    confirmations=raw_utxo.get('confirmations'),
                    confirmed=raw_utxo.get('confirmed'), 
                    double_spend=raw_utxo.get('double_spend'))

        # uxto_object = UTXO.parse({'hash': 'fea5cbf4efc220a5512d394279778f75937c253cac32c43047cadffc9ee4d85c', 'time': '2018-02-04T12:29:01+0000', 'confirmations': 12468, 'is_coinbase': False, 'value': 156000000, 'index': 1, 'address': 'mfke2PVhGePAy1GfZNotr6LeXfQ5nwnZTa', 'type': 'pubkeyhash', 'multisig': None, 'script': 'OP_DUP OP_HASH160 029692862d60b5f84ba706b37939d074b6c58085 OP_EQUALVERIFY OP_CHECKSIG', 'script_hex': '76a914029692862d60b5f84ba706b37939d074b6c5808588ac'})
        if schema_type == 'block_trail':
            return cls(tx_hash=raw_utxo.get('hash'),
                    block_height=None,
                    tx_index=raw_utxo.get('index'),
                    value=raw_utxo.get('value'),
                    confirmations=raw_utxo.get('confirmations'),
                    confirmed=raw_utxo.get('time'),
                    double_spend=None)        
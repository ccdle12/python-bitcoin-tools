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

        raise RuntimeError('Unknown Schema Type') 

    @classmethod
    def parse(cls, raw_utxo):
        schema_type = UTXO.schema_type(raw_utxo)

        if schema_type == 'block_cypher':
            return cls(tx_hash=raw_utxo.get('tx_hash'), 
                    block_height=raw_utxo.get('block_height'), 
                    tx_index=raw_utxo.get('tx_output_n'),
                    value=raw_utxo.get('value'), 
                    confirmations=raw_utxo.get('confirmations'),
                    confirmed=raw_utxo.get('confirmed'), 
                    double_spend=raw_utxo.get('double_spend'))        
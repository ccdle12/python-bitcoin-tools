from binascii import unhexlify, hexlify
from io import BytesIO
from bitcoin_tools.PrivateKey import PrivateKey
from bitcoin_tools.helper import decode_base58, p2pkh_script, SIGHASH_ALL

OP_CODES = {
    0: 'OP_0',
    76: 'OP_PUSHDATA1',
    77: 'OP_PUSHDATA2',
    78: 'OP_PUSHDATA4',
    79: 'OP_1NEGATE',
    80: 'OP_RESERVED',
    81: 'OP_1',
    82: 'OP_2',
    83: 'OP_3',
    84: 'OP_4',
    85: 'OP_5',
    86: 'OP_6',
    87: 'OP_7',
    88: 'OP_8',
    89: 'OP_9',
    90: 'OP_10',
    91: 'OP_11',
    92: 'OP_12',
    93: 'OP_13',
    94: 'OP_14',
    95: 'OP_15',
    96: 'OP_16',
    97: 'OP_NOP',
    98: 'OP_VER',
    99: 'OP_IF',
    100: 'OP_NOTIF',
    101: 'OP_VERIF',
    102: 'OP_VERNOTIF',
    103: 'OP_ELSE',
    104: 'OP_ENDIF',
    105: 'OP_VERIFY',
    106: 'OP_RETURN',
    107: 'OP_TOALTSTACK',
    108: 'OP_FROMALTSTACK',
    109: 'OP_2DROP',
    110: 'OP_2DUP',
    111: 'OP_3DUP',
    112: 'OP_2OVER',
    113: 'OP_2ROT',
    114: 'OP_2SWAP',
    115: 'OP_IFDUP',
    116: 'OP_DEPTH',
    117: 'OP_DROP',
    118: 'OP_DUP',
    119: 'OP_NIP',
    120: 'OP_OVER',
    121: 'OP_PICK',
    122: 'OP_ROLL',
    123: 'OP_ROT',
    124: 'OP_SWAP',
    125: 'OP_TUCK',
    126: 'OP_CAT',
    127: 'OP_SUBSTR',
    128: 'OP_LEFT',
    129: 'OP_RIGHT',
    130: 'OP_SIZE',
    131: 'OP_INVERT',
    132: 'OP_AND',
    133: 'OP_OR',
    134: 'OP_XOR',
    135: 'OP_EQUAL',
    136: 'OP_EQUALVERIFY',
    137: 'OP_RESERVED1',
    138: 'OP_RESERVED2',
    139: 'OP_1ADD',
    140: 'OP_1SUB',
    141: 'OP_2MUL',
    142: 'OP_2DIV',
    143: 'OP_NEGATE',
    144: 'OP_ABS',
    145: 'OP_NOT',
    146: 'OP_0NOTEQUAL',
    147: 'OP_ADD',
    148: 'OP_SUB',
    149: 'OP_MUL',
    150: 'OP_DIV',
    151: 'OP_MOD',
    152: 'OP_LSHIFT',
    153: 'OP_RSHIFT',
    154: 'OP_BOOLAND',
    155: 'OP_BOOLOR',
    156: 'OP_NUMEQUAL',
    157: 'OP_NUMEQUALVERIFY',
    158: 'OP_NUMNOTEQUAL',
    159: 'OP_LESSTHAN',
    160: 'OP_GREATERTHAN',
    161: 'OP_LESSTHANOREQUAL',
    162: 'OP_GREATERTHANOREQUAL',
    163: 'OP_MIN',
    164: 'OP_MAX',
    165: 'OP_WITHIN',
    166: 'OP_RIPEMD160',
    167: 'OP_SHA1',
    168: 'OP_SHA256',
    169: 'OP_HASH160',
    170: 'OP_HASH256',
    171: 'OP_CODESEPARATOR',
    172: 'OP_CHECKSIG',
    173: 'OP_CHECKSIGVERIFY',
    174: 'OP_CHECKMULTISIG',
    175: 'OP_CHECKMULTISIGVERIFY',
    176: 'OP_NOP1',
    177: 'OP_NOP2',
    177: 'OP_CHECKLOCKTIMEVERIFY',
    178: 'OP_NOP3',
    178: 'OP_CHECKSEQUENCEVERIFY',
    179: 'OP_NOP4',
    180: 'OP_NOP5',
    181: 'OP_NOP6',
    182: 'OP_NOP7',
    183: 'OP_NOP8',
    184: 'OP_NOP9',
    185: 'OP_NOP10',
    252: 'OP_NULLDATA',
    253: 'OP_PUBKEYHASH',
    254: 'OP_PUBKEY',
    255: 'OP_INVALIDOPCODE',
}


class Script:
    def __init__(self, elements):
        self.elements = elements

    @classmethod
    def parse(cls, raw):
        stream = BytesIO(raw)

        elements = []

        current = stream.read(1)

        while current != b'':
            # Read the int representation of the byte
            op_code = current[0]

            if 0 < op_code <= 75:
                # Read the next set of bytes as the length of the op_code
                # which should be the length of the pub key hash and add it to the list
                elements.append(stream.read(op_code))
            else:
                elements.append(op_code)

            current = stream.read(1)
        return cls(elements)

    # Returns a print format for the object
    def __repr__(self):
        result = ''
        for element in self.elements:
            if type(element) == int:
                result += '{} '.format(OP_CODES[element])
            else:
                result += '{} '.format(hexlify(element))
        return result

    def type(self):
        if len(self.elements) == 0:
            return 'blank'
        elif self.elements[0] == 0x76 \
                and self.elements[1] == 0xa9 \
                and type(self.elements[2]) == bytes \
                and len(self.elements[2]) == 0x14 \
                and self.elements[3] == 0x88 \
                and self.elements[4] == 0xac:

            # hex/int
            # script_pubkey = <76/118 : OP_DUP> <a9/169 : OP_HASH160> <14/20 : Length of hash> <88/136 : OP_EQUAL_VERIFY> <ac/172 : OP_CHECKSIG>
            return 'p2pkh'
        elif self.elements[0] == 0xa9 \
                and type(self.elements[1]) is bytes \
                and len(self.elements[1]) == 0x14 \
                and self.elements[2] == 0x87:

            # <a9 : OP_HASH16-> <14 : Length of hash> < hash > <87 : OP_EQUAL>
            return 'p2sh'
        elif type(self.elements[0]) == bytes \
                and len(self.elements[0]) in (0x47, 0x48, 0x49) \
                and type(self.elements[1]) == bytes \
                and len(self.elements[1]) in (0x21, 0x41):
            # p2pkh scriptSig:
            # <signature> <pubkey>
            return 'p2pkh sig'
        elif len(self.elements) > 1 \
                and type(self.elements[1]) == bytes \
                and len(self.elements[1]) in (0x47, 0x48, 0x49) \
                and self.elements[-1][-1] == 0xae:
            # HACK: assumes p2sh is a multisig
            # p2sh multisig:
            # <x> <sig1> ... <sigm> <redeemscript ends with OP_CHECKMULTISIG>
            return 'p2sh sig'

    def serialize(self):
        result = b''
        for each_element in self.elements:
            # if element is an int, it's an OP_CODEgit
            if type(each_element) == int:
                result += bytes([each_element])
            else:
                # Element is the hash160 of the sec pub key, prefix it with the length of bytes and then the h160
                result += bytes([len(each_element)]) + each_element

        return result

    def der_signature(self, index=0):
        '''index isn't used for p2pkh, for p2sh, means one of m sigs'''
        sig_type = self.type()
        if sig_type == 'p2pkh sig':
            return self.elements[0]
        elif sig_type == 'p2sh sig':
            return self.elements[index + 1]
        else:
            raise RuntimeError('script type needs to be p2pkh sig or p2sh sig')

    def sec_pubkey(self, index=0):
        '''index isn't used for p2pkh, for p2sh, means one of n pubkeys'''
        sig_type = self.type()
        if sig_type == 'p2pkh sig':
            # Returns the Pub Key (A SEC public key)
            return self.elements[1]
        elif sig_type == 'p2sh sig':
            # HACK: assumes p2sh is a multisig
            redeem_script = Script.parse(self.elements[-1])
            return redeem_script.elements[index + 1]

    def redeem_script(self):
        sig_type = self.type()
        #If the type is p2sh signature, return the last object which is the redeem script
        if sig_type == 'p2sh sig':
            return self.elements[-1]
        else:
            raise RuntimeError('script types needs to be p2sh sig')




from unittest import TestCase
from binascii import unhexlify
from io import BytesIO

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
    def __init__(self, element):
        self.element = element

    @classmethod
    def parse(cls, raw):
        stream = BytesIO(raw)

        elements = []

        current = stream.read(1)

        while current != b'':
            op_code = current[0]

            if 0 < op_code <= 75:
                elements.append(stream.read(op_code))
            else:
                elements.append(op_code)

            current = stream.read(1)
        return cls(elements)

    def type(self):
        if len(self.element) == 0:
            return 'blank'
        elif self.element[0] == 118 \
                and self.element[1] == 169 \
                and len(self.element[2]) == 20 \
                and self.element[3] == 136 \
                and self.element[4] == 172:

            # hex/int
            # script_pubkey = <76/118 : OP_DUP> <a9/169 : OP_HASH160> <14/20 : Length of hash> <88/136 : OP_EQUAL_VERIFY> <ac/172 : OP_CHECKSIG>
            return 'p2pkh'
        elif self.element[0] == 0xa9 \
            and type(self.element[1]) is bytes\
            and len(self.element[1]) == 0x14 \
            and self.element[2] == 0x87:

            #<a9 : OP_HASH16-> <14 : Length of hash> < hash > <87 : OP_EQUAL>
            return 'p2sh'
        elif type(self.element[0]) == bytes \
                and len(self.element[0]) in (0x47, 0x48, 0x49) \
                and type(self.element[1]) == bytes \
                and len(self.element[1]) in (0x21, 0x41):
            # p2pkh scriptSig:
            # <signature> <pubkey>
            return 'p2pkh sig'
        elif len(self.element) > 1 \
                and type(self.element[1]) == bytes \
                and len(self.element[1]) in (0x47, 0x48, 0x49) \
                and self.element[-1][-1] == 0xae:
            # HACK: assumes p2sh is a multisig
            # p2sh multisig:
            # <x> <sig1> ... <sigm> <redeemscript ends with OP_CHECKMULTISIG>
            return 'p2sh sig'

    def serialize(self):
        result = b''

        for each_element in self.element:
            if type(each_element) == int:
                result += bytes([each_element])
            else:
                result += bytes([len(each_element)]) + each_element

        return result

    def der_signature(self, index=0):
        '''index isn't used for p2pkh, for p2sh, means one of m sigs'''
        sig_type = self.type()
        if sig_type == 'p2pkh sig':
            return self.element[0]
        elif sig_type == 'p2sh sig':
            return self.element[index + 1]
        else:
            raise RuntimeError('script type needs to be p2pkh sig or p2sh sig')

    def sec_pubkey(self, index=0):
        '''index isn't used for p2pkh, for p2sh, means one of n pubkeys'''
        sig_type = self.type()
        if sig_type == 'p2pkh sig':
            return self.element[1]
        elif sig_type == 'p2sh sig':
            # HACK: assumes p2sh is a multisig
            redeem_script = Script.parse(self.element[-1])
            return redeem_script.element[index + 1]


class ScriptTest(TestCase):
    def test_script_type(self):
        print("Should return type p2pkh (pay to pub key hash)")
        # script_pubkey = <76 : OP_DUP> <a9 : OP_HASH160> <14 : Length of hash> <88 : OP_EQUAL_VERIFY> <ac : OP_CHECKSIG>
        script_pubkey_raw = unhexlify('76a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac')
        script_pubkey = Script.parse(script_pubkey_raw)
        self.assertEqual('p2pkh', script_pubkey.type())

        print("Should return type p2sh (pay to script hash)")
        # script_pubkey = <a9 : OP_HASH16-> <14 : Length of hash> < hash > <87 : OP_EQUAL>
        script_pubkey_raw = unhexlify('a91474d691da1574e6b3c192ecfb52cc8984ee7b6c5687')
        script_pubkey = Script.parse(script_pubkey_raw)
        self.assertEqual('p2sh', script_pubkey.type())


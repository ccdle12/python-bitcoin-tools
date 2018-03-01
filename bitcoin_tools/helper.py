import hashlib
from binascii import hexlify, unhexlify
from unittest import TestCase

SIGHASH_ALL = 1
SIGHASH_NONE = 2
SIGHASH_SINGLE = 3
BASE58_ALPHABET = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def encode_base58(s):
    # Find the amount of leading 0 bytes
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break

    # There are no 0's in base58,
    # Replace the leading 0's with 1's,
    # 1's represent 0's in base58
    prefix = b'1' * count

    # Convert hexadecimal value of s to base-16 integer
    num = int(hexlify(s), 16)

    # Mutable byte array from 0 to 256
    result = bytearray()

    # While the base 16 integer is greater than 0
    while num > 0:
        # divmod returns the quotient and remainder
        # Divide num by 58
        num, mod = divmod(num, 58)

        # Using mod as an index, retrieve corresponding letter/number
        # Insert this value at index 0 in result bytearray
        # Inserting at 0, doesn't override but shifts the the rest of the array by 1
        result.insert(0, BASE58_ALPHABET[mod])

    return prefix + bytes(result)


def encode_base58_checksum(s):
    return encode_base58(s + double_sha256(s)[:4]).decode('ascii')


def double_sha256(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def sha256_ripemd160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()


def little_endian_to_int(b):
    return int.from_bytes(b, 'little')


def int_to_little_endian(num, length):
    return int.to_bytes(num, length, 'little')


# TODO: NEED to understand varint types better
def encode_varint(i):
    # Encodes an integer to varint
    # if i is less than 253 (int)
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + int_to_little_endian(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(i, 8)
    else:
        raise RuntimeError('integer too large: {}'.format(i))


def read_varint(s):
    i = s.read(1)[0]

    if i == 0xfd:
        # 0xfd means the next two bytes are the number
        return little_endian_to_int(s.read(2))
    elif i == 0xfe:
        # 0xfe means that the next four bytes are the number
        return little_endian_to_int(s.read(4))
    elif i == 0xff:
        # 0xff means the next eight bytes are the number
        return little_endian_to_int(s.read(8))
    else:
        # i is just the number
        return i


def satoshi_to_bitcoin(satoshi):
    return float(satoshi / 100000000)


def bitcoin_to_satoshi(bitcoin):
    return int(bitcoin * 100000000)


def decode_base58(address):
    num = 0
    # Iterate over each string, in the address, c is the integer value of the ascii character
    for c in address.encode('ascii'):
        num *= 58
        num += BASE58_ALPHABET.index(c)

    combined = num.to_bytes(25, byteorder='big')
    checksum = combined[-4:]

    # Check that combined bytes, double_sha256() -> take the last 4 bytes of combined and then take the first 4 bytes
    # This should equal checksum
    if double_sha256(combined[:-4])[:4] != checksum:
        raise RuntimeError('malformed address: {} {}'.format(checksum, double_sha256(combined)[:4]))

    return combined[1:-4]


def p2pkh_script(h160):
    # Takes the h160 of an address and inserts it into the p2pkh scriptPubKey format
    return b'\x76\xa9\x14' + h160 + b'\x88\xac'

def p2sh_script(h160):
    # Takes the h160 of an address and inserts it into p2sh scriptPubKey format
    return b'\xa9\x14' + h160 + b'\x87'

def generate_reedemScript(owners_sec, list_of_pub_keys):
    if len(list_of_pub_keys) < 1:
        raise RuntimeError("No public keys passed")

    unhexed_sec = unhexlify(owners_sec)
    len_of_unhexed_sec = bytes([len(unhexed_sec)])

    result = b'\x52' + len_of_unhexed_sec + unhexed_sec

    for pub_key in list_of_pub_keys:
        result += bytes([len(pub_key)])
        result += pub_key

    result += b'\x52' + b'\xae'

    return result

def generate_p2sh_address(redeem_script, mainnet=False):
        if mainnet:
            prefix = b'\x05'
        else:
            prefix = b'\xc4'

        h160 = sha256_ripemd160(redeem_script)
        address = encode_base58_checksum(prefix + h160)

        return address

def generate_p2pkh_pub_key(address):
    h160 = decode_base58(address)

    return p2pkh_script(h160)

def generate_p2sh_pub_key(address):
    h160 = decode_base58(address)

    return p2sh_script(h160)


import hashlib
from binascii import hexlify

BASE58_ALPHABET = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def encode_base58(s):
    # Find the amount of leadings 0 bytes
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break

    prefix = b'1' * count

    num = int(hexlify(s), 16)
    result = bytearray()

    while num > 0:
        num, mod = divmod(num, 58)
        result.insert(0, BASE58_ALPHABET[mod])

    return prefix + bytes(result)


def double_sha256(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def sha256_ripemd160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()

import hashlib
from binascii import hexlify

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
    print("Count: {0}".format(count))
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

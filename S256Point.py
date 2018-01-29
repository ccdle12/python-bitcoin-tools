from FieldElement import FieldElement
from Point import Point
from unittest import TestCase
from binascii import hexlify, unhexlify
from helper import sha256_ripemd160, double_sha256, encode_base58

P = 2 ** 256 - 2 ** 32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
A = 0
B = 7


class S256Field(FieldElement):

    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=P)

    def hex(self):
        return '{:x}'.format(self.num).zfill(64)

    def __repr__(self):
        return self.hex()


class S256Point(Point):
    bits = 256

    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(A), S256Field(B)

        if x is None:
            super().__init__(x=None, y=None, a=a, b=b)
        elif type(x) == int:
            super().__init__(S256Field(x), S256Field(y), a=a, b=b)
        else:
            super().__init__(x=x, y=y, a=a, b=b)

    def __repr__(self):
        if self.x is None:
            return 'Point(infinity)'
        else:
            return 'Point({},{})'.format(self.x, self.y)

    # TODO: Review and run experiments to look into this function
    def __rmul__(self, scalar):
        # Binary Expansion on current
        current = self

        result = S256Point(None, None)

        for _ in range(self.bits):
            # Bitwise AND, if bit is 1
            if scalar & 1:
                result += current

            current += current

            # Shifting bits to the right by 1
            scalar >>= 1

        return result

    def get_sec(self, compressed=True):

        if self.x is None or self.y is None:
            raise RuntimeError("x is None")

        x = self.x.num.to_bytes(32, 'big')
        y = self.y.num.to_bytes(32, 'big')

        if compressed:
            if self.y.num % 2 == 0:
                prefix = b'\x02'
            else:
                prefix = b'\x03'

            sec = prefix + x

        else:
            prefix = b'\x04'

            sec = prefix + x + y

        return hexlify(sec)

    # TODO: Examine and Summarize helper hashing methods
    def get_address(self, sec, testnet=True):

        if type(sec) is not bytes:
            raise RuntimeError("sec must be passed as bytes format")

        # Need to turn sec into bytes before hashing
        sec_bytes = unhexlify(sec)

        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'

        # SHA256 -> RIMPEMD160
        hashed_sec_bytes = sha256_ripemd160(sec_bytes)

        # Concatenate prefix and hashed sec bytes
        raw = prefix + hashed_sec_bytes

        # Double SHA256 raw and take the first 4 bytes as checksum
        checksum = double_sha256(raw)[:4]

        # Encode Base58 raw and checksum to generate accepted address
        address = encode_base58(raw + checksum)

        return address.decode('ascii')


G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)


class S256Test(TestCase):

    def test_point_at_infinity(self):
        print("Should return None since point of infinity")
        point = N * G
        self.assertIsNone(point.x)

    def test_generating_pub_key(self):
        secret = 999
        point = secret * G
        print("Secret multiply G should return the following points")
        self.assertEqual(hexlify(point.x.num.to_bytes(32, 'big')).decode('ascii'),
                         "9680241112d370b56da22eb535745d9e314380e568229e09f7241066003bc471")
        self.assertEqual(hexlify(point.y.num.to_bytes(32, 'big')).decode('ascii'),
                         "ddac2d377f03c201ffa0419d6596d10327d6c70313bb492ff495f946285d8f38")

    def test_pubpoint(self):
        # write a test that tests the public point for the following
        print("Should return true for generating public points from secret")
        points = (
            # secret, x, y
            (7, 0x5cbdf0646e5db4eaa398f365f2ea7a0e3d419b7e0330e39ce92bddedcac4f9bc,
             0x6aebca40ba255960a3178d6d861a54dba813d0b813fde7b5a5082628087264da),
            (1485, 0xc982196a7466fbbbb0e27a940b6af926c1a74d5ad07128c82824a11b5398afda,
             0x7a91f9eae64438afb9ce6448a1c133db2d8fb9254e4546b6f001637d50901f55),
            (2 ** 128, 0x8f68b9d2f63b5f339239c1ad981f162ee88c5678723ea3351b7b444c9ec4c0da,
             0x662a9f2dba063986de1d90c2b6be215dbbea2cfe95510bfdf23cbf79501fff82),
            (2 ** 240 + 2 ** 31, 0x9577ff57c8234558f293df502ca4f09cbc65a6572c842b39b366f21717945116,
             0x10b49c67fa9365ad7b90dab070be339a1daf9052373ec30ffae4f72d5e66d053),
        )

        # iterate over points
        for secret, _x, _y in points:
            # initialize the secp256k1 point (S256Point)
            p = S256Point(_x, _y)

            # check that the secret*G is the same as the point
            self.assertEqual(secret * G, p)

    def test_generate_sec_pub_key(self):
        print("-------------------------------------------------------------------------------------------")
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = S256Point(4009715469895962904302745416817721540571577912364644137838095050706137667860,
                            32025336288095498019218993550383068707359510270784983226210884843871535451292)

        sec_x = pub_key.x.num.to_bytes(32, 'big')
        sec_y = pub_key.y.num.to_bytes(32, 'big')

        expected = hexlify(b'\x04' + sec_x + sec_y)

        print("Should generate an uncompressed public key")
        self.assertEqual(expected, pub_key.get_sec(compressed=False))

        print("-------------------------------------------------------------------------------------------")
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = S256Point(4009715469895962904302745416817721540571577912364644137838095050706137667860,
                            32025336288095498019218993550383068707359510270784983226210884843871535451292)

        print("There should be a true assertion that y in pub_key is EVEN")
        # We know the Y val of the pub_key is EVEN
        self.assertTrue(pub_key.y.num % 2 == 0)

        print("-------------------------------------------------------------------------------------------")
        priv_key = 52025986665857613263760395809269303684785643089926984150804307617991608511766
        pub_key = S256Point(43733605778270459583874364812384261459365992207657902102567152558096696733127,
                            64346778444748414606606796249150556060624935198788845168028978963277938956739)

        print("There should be a true assertion that y in pub_key is ODD")
        # We know the Y val of the pub_key is ODD
        self.assertFalse(pub_key.y.num % 2 == 0)

        print("-------------------------------------------------------------------------------------------")
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = S256Point(4009715469895962904302745416817721540571577912364644137838095050706137667860,
                            32025336288095498019218993550383068707359510270784983226210884843871535451292)

        sec_x = pub_key.x.num.to_bytes(32, 'big')
        sec_y = pub_key.y.num.to_bytes(32, 'big')

        expected = hexlify(b'\x02' + sec_x)
        print("Expected compressed EVEN: {0}".format(expected))
        print("There should be a valid EVEN compressed SEC format pub_key")
        self.assertEqual(expected, pub_key.get_sec(compressed=True))

        print("-------------------------------------------------------------------------------------------")
        priv_key = 52025986665857613263760395809269303684785643089926984150804307617991608511766
        pub_key = S256Point(43733605778270459583874364812384261459365992207657902102567152558096696733127,
                            64346778444748414606606796249150556060624935198788845168028978963277938956739)

        sec_x = pub_key.x.num.to_bytes(32, 'big')
        sec_y = pub_key.y.num.to_bytes(32, 'big')

        expected = hexlify(b'\x03' + sec_x)
        print("Expected Compressed ODD: {0}".format(expected))
        print("There should be a valid ODD compressed SEC format pub_key")
        self.assertEqual(expected, pub_key.get_sec(compressed=True))

        print("-------------------------------------------------------------------------------------------")
        # It should raise an error since we are passing None
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = S256Point(None,
                            32025336288095498019218993550383068707359510270784983226210884843871535451292)

        print("There should be a raised RuntimeError because None is passed as argument to SEC")
        with self.assertRaises(RuntimeError):
            pub_key.get_sec(compressed=True)

        print("-------------------------------------------------------------------------------------------")
        # It should raise an error since points not on curve
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497

        print("There should be a raised RuntimeError because None is passed as argument to SEC")
        with self.assertRaises(RuntimeError):
            pub_key = S256Point(43733605778270459583874364812384261459365992207657902102567152558096696,
                                32025336288095498019218993550383068707359510270784983226210884843871535451292)

    def test_generate_address(self):
        priv_key = 85766691447432562285107349766825790927431446373602486150911666480754112492464
        pub_key = S256Point(43651727216793576570341989570883305974491642311510342469928224726666590034225,
                            109857391791750504773247734335453148952192151977881622854599464318335318347795)

        compressed_sec = pub_key.get_sec(compressed=True)

        testnet_address = pub_key.get_address(compressed_sec, testnet=True)

        expected = "mo24iC138ffpdWiFsH8y7dq6v5CDD1UbiT"

        print("There should generate a compressed testnet address")

        self.assertEqual(expected, testnet_address)

        print("-------------------------------------------------------------------------------------------")
        priv_key = 85766691447432562285107349766825790927431446373602486150911666480754112492464
        pub_key = S256Point(43651727216793576570341989570883305974491642311510342469928224726666590034225,
                            109857391791750504773247734335453148952192151977881622854599464318335318347795)

        compressed_sec = pub_key.get_sec(compressed=True)
        print(type(compressed_sec))

        mainnet_address = pub_key.get_address(compressed_sec, testnet=False)

        expected = "18W7R8v4KeEZrQEe9iAbHicn45bWNn2QBe"

        print("It should return the mainnet address")
        self.assertEqual(expected, mainnet_address)

        print("-------------------------------------------------------------------------------------------")
        priv_key = 85766691447432562285107349766825790927431446373602486150911666480754112492464
        pub_key = S256Point(43651727216793576570341989570883305974491642311510342469928224726666590034225,
                            109857391791750504773247734335453148952192151977881622854599464318335318347795)

        # 0360820086ce7d8015b537abb9937805b49e178db9151cfe43d0aa529919481931
        compressed_sec = pub_key.get_sec(compressed=True)

        print("It should raise error as not passing bytes as argument")
        with self.assertRaises(RuntimeError):
            pub_key.get_address("0360820086ce7d8015b537abb9937805b49e178db9151cfe43d0aa529919481931", testnet=False)

        print("-------------------------------------------------------------------------------------------")
        priv_key = 85766691447432562285107349766825790927431446373602486150911666480754112492464
        pub_key = S256Point(43651727216793576570341989570883305974491642311510342469928224726666590034225,
                            109857391791750504773247734335453148952192151977881622854599464318335318347795)

        # 0360820086ce7d8015b537abb9937805b49e178db9151cfe43d0aa529919481931
        print("It should NOT raise error as passing bytes as argument")
        compressed_sec = pub_key.get_sec(compressed=True)
        mainnet_address = pub_key.get_address(b'0360820086ce7d8015b537abb9937805b49e178db9151cfe43d0aa529919481931',
                                              testnet=False)

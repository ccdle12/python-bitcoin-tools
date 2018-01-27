from unittest import TestCase
import secrets
from pycoin.ecdsa import generator_secp256k1 as G
from binascii import hexlify

class ECC:
    P = 2**256 - 2**32 - 977
    N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    A = 0
    B = 7

    def generate_priv_key(self):
        return secrets.randbelow(self.N)

    def generate_pub_key(self, priv_key):
        return priv_key * G

    def is_on_curve(self, x, y):
        return (y ** 2) % self.P == (x ** 3 + self.A + self.B) % self.P

    def generate_uncompressed_SEC(self, x_int , y_int):
        prefix = b'\x04'

        x_bytes = x_int.to_bytes(32, 'big')
        y_bytes = y_int.to_bytes(32, 'big')

        uncompressed_SEC_bytes = prefix + x_bytes + y_bytes

        return hexlify(uncompressed_SEC_bytes)

    def generate_compressed_SEC(self, x_int, y_int):

        if y_int % 2 == 0:
            prefix = b'\x02'
        else:
            prefix = b'\x03'

        x_bytes = x_int.to_bytes(32, 'big')

        compressed_SEC_bytes = prefix + x_bytes

        return hexlify(compressed_SEC_bytes)


class ECC_Tests(TestCase):
    def test_P(self):
        self.assertEqual(ECC.P, 2**256 - 2**32 - 977)

    def test_generate_priv_key(self):
        priv_key = ECC().generate_priv_key()
        self.assertTrue(0 < priv_key < ECC.N)

    def test_duplicate_priv_key(self):

        prev_gen_priv_keys = {}

        # 2.2 GHz Intel Core i7
        # 16 GB 1600 MHz DDR3
        # Takes about 9 - 10 seconds to run this test
        for _ in range(1000000):
            priv_key = ECC().generate_priv_key()

            assert 0 < priv_key < ECC.N

            if priv_key in prev_gen_priv_keys:
                raise RuntimeError('Randomly generated number, has been generated before')

            prev_gen_priv_keys[priv_key] = priv_key

    def test_generate_pub_key(self):
        priv_key = ECC().generate_priv_key()
        pub_key = ECC().generate_pub_key(priv_key)

        self.assertTrue(0 < pub_key.x())

    def test_point_at_infinity(self):
        point_at_infinity = ECC().N * G
        self.assertEqual(None, point_at_infinity.x())
        self.assertEqual(None, point_at_infinity.y())

    def test_pub_key_is_on_curve(self):
        priv_key = ECC().generate_priv_key()
        pub_key = ECC().generate_pub_key(priv_key)
        print(pub_key.x(), pub_key.y())

        self.assertEqual(True, ECC().is_on_curve(pub_key.x(), pub_key.y()))

    def test_pub_key_is_not_on_curve(self):
        pub_key = (20700948478913772076119439904629995041653958252327787830786676775719940102654,
                   5554562626338682950266833423860784775451683510376504490669758056891525878098)

        self.assertEqual(False, ECC().is_on_curve(pub_key[0], pub_key[1]))

    def test_uncompressed_SEC(self):
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = (4009715469895962904302745416817721540571577912364644137838095050706137667860,
                   32025336288095498019218993550383068707359510270784983226210884843871535451292)

        sec_x = pub_key[0].to_bytes(32, 'big')
        sec_y = pub_key[1].to_bytes(32, 'big')

        expected = hexlify(b'\x04' + sec_x + sec_y)

        print("Uncompressed SEC: {0}".format(ECC().generate_uncompressed_SEC(pub_key[0], pub_key[1])))

        self.assertEqual(expected, ECC().generate_uncompressed_SEC(pub_key[0], pub_key[1]))

    def test_compressed_SEC_1(self):
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = (4009715469895962904302745416817721540571577912364644137838095050706137667860,
                   32025336288095498019218993550383068707359510270784983226210884843871535451292)

        # We know the Y val of the pub_key is EVEN
        self.assertTrue(pub_key[1] % 2 == 0)


    def test_compressed_SEC_2(self):
        priv_key = 52025986665857613263760395809269303684785643089926984150804307617991608511766
        pub_key = (43733605778270459583874364812384261459365992207657902102567152558096696733127,
                   64346778444748414606606796249150556060624935198788845168028978963277938956739)


        # We know the Y val of the pub_key is ODD
        self.assertFalse(pub_key[1] % 2 == 0)

    def test_compressed_SEC_1_EVEN(self):
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = (4009715469895962904302745416817721540571577912364644137838095050706137667860,
                   32025336288095498019218993550383068707359510270784983226210884843871535451292)

        sec_x = pub_key[0].to_bytes(32, 'big')
        sec_y = pub_key[1].to_bytes(32, 'big')

        expected = hexlify(b'\x02' + sec_x)
        print("Expected compressed EVEN: {0}".format(expected))
        self.assertEqual(expected, ECC().generate_compressed_SEC(pub_key[0], pub_key[1]))

    def test_compressed_SEC_2_ODD(self):
        priv_key = 52025986665857613263760395809269303684785643089926984150804307617991608511766
        pub_key = (43733605778270459583874364812384261459365992207657902102567152558096696733127,
                   64346778444748414606606796249150556060624935198788845168028978963277938956739)

        sec_x = pub_key[0].to_bytes(32, 'big')
        sec_y = pub_key[1].to_bytes(32, 'big')

        expected = hexlify(b'\x03' + sec_x)
        print("Expected Compressed ODD: {0}".format(expected))
        self.assertEqual(expected, ECC().generate_compressed_SEC(pub_key[0], pub_key[1]))

if __name__ == '__main__':
    priv_key = ECC().generate_priv_key()
    print("-----------------------------------")
    print("Private Key: {0}".format(priv_key))
    print("-----------------------------------")
    pub_key = ECC().generate_pub_key(priv_key)
    print("Public Key: {0}".format(pub_key))
    print("-----------------------------------")
    uncompressed_sec = ECC().generate_uncompressed_SEC(pub_key.x(), pub_key.y())
    print("Uncompressed SEC: {0}".format(uncompressed_sec))
    print("-----------------------------------")
    compressed_sec = ECC().generate_compressed_SEC(pub_key.x(), pub_key.y())
    print("Compressed SEC: {0}".format(compressed_sec))
    print("-----------------------------------")
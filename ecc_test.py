from unittest import TestCase
from pycoin.ecdsa import generator_secp256k1 as G
from binascii import hexlify, unhexlify
from ecc import ECC

class ECC_Tests(TestCase):
    def test_P(self):
        print("First test, should show ECC.P equal to Prime Number Field")
        self.assertEqual(ECC.P, 2**256 - 2**32 - 977)

    # # # # # # # # # # # # # # # # # # # # # # #
    # Test Generating Private and Public Keys   #
    # # # # # # # # # # # # # # # # # # # # # # #
    def test_generate_priv_key(self):
        priv_key = ECC().generate_priv_key()
        print("Private key generated should be above 0 and below ECC.N")
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

        print("There should be no duplicates after creating 1000000 private keys")

    def test_generate_pub_key(self):
        priv_key = ECC().generate_priv_key()
        pub_key = ECC().generate_pub_key(priv_key)
        print("There should be a x val of pub_key > 0")
        self.assertTrue(0 < pub_key.x())

    def test_point_at_infinity(self):
        point_at_infinity = ECC().N * G
        print("Point at Infinity, should return None for both x and y")
        self.assertEqual(None, point_at_infinity.x())
        self.assertEqual(None, point_at_infinity.y())

    def test_pub_key_is_on_curve(self):
        priv_key = ECC().generate_priv_key()
        pub_key = ECC().generate_pub_key(priv_key)
        print(pub_key.x(), pub_key.y())
        print("Both x and y should be on the curve, checking if pub_key is on curve")
        self.assertEqual(True, ECC().is_on_curve(pub_key.x(), pub_key.y()))

    def test_pub_key_is_not_on_curve(self):
        pub_key = (20700948478913772076119439904629995041653958252327787830786676775719940102654,
                   5554562626338682950266833423860784775451683510376504490669758056891525878098)
        print("Should return false, y has been tampered with, so it is not a valid point on the curve")
        self.assertEqual(False, ECC().is_on_curve(pub_key[0], pub_key[1]))


    # # # # # # # # # # # # # # # # # # # # # #
    # Test Generating SEC Format Public Keys  #
    # # # # # # # # # # # # # # # # # # # # # #
    def test_uncompressed_SEC(self):
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = (4009715469895962904302745416817721540571577912364644137838095050706137667860,
                   32025336288095498019218993550383068707359510270784983226210884843871535451292)

        sec_x = pub_key[0].to_bytes(32, 'big')
        sec_y = pub_key[1].to_bytes(32, 'big')

        expected = hexlify(b'\x04' + sec_x + sec_y)

        print("Uncompressed SEC: {0}".format(ECC().generate_uncompressed_SEC(pub_key[0], pub_key[1])))
        print("There should be a valid uncompressed SEC Format pub_key")

        self.assertEqual(expected, ECC().generate_uncompressed_SEC(pub_key[0], pub_key[1]))

    def test_compressed_SEC_1(self):
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = (4009715469895962904302745416817721540571577912364644137838095050706137667860,
                   32025336288095498019218993550383068707359510270784983226210884843871535451292)

        print("There should be a true assertion that y in pub_key is EVEN")
        # We know the Y val of the pub_key is EVEN
        self.assertTrue(pub_key[1] % 2 == 0)


    def test_compressed_SEC_2(self):
        priv_key = 52025986665857613263760395809269303684785643089926984150804307617991608511766
        pub_key = (43733605778270459583874364812384261459365992207657902102567152558096696733127,
                   64346778444748414606606796249150556060624935198788845168028978963277938956739)

        print("There should be a true assertion that y in pub_key is ODD")
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
        print("There should be a valid EVEN compressed SEC format pub_key")
        self.assertEqual(expected, ECC().generate_compressed_SEC(pub_key[0], pub_key[1]))

    def test_compressed_SEC_2_ODD(self):
        priv_key = 52025986665857613263760395809269303684785643089926984150804307617991608511766
        pub_key = (43733605778270459583874364812384261459365992207657902102567152558096696733127,
                   64346778444748414606606796249150556060624935198788845168028978963277938956739)

        sec_x = pub_key[0].to_bytes(32, 'big')
        sec_y = pub_key[1].to_bytes(32, 'big')

        expected = hexlify(b'\x03' + sec_x)
        print("Expected Compressed ODD: {0}".format(expected))
        print("There should be a valid ODD compressed SEC format pub_key")
        self.assertEqual(expected, ECC().generate_compressed_SEC(pub_key[0], pub_key[1]))

    def test_uncompressed_SEC_should_raise_error_1(self):
        # It should raise an error since we are passing None
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = (4009715469895962904302745416817721540571577912364644137838095050706137667860,
                   32025336288095498019218993550383068707359510270784983226210884843871535451292)

        print("There should be a raised RuntimeError because None is passed as argument to generate uncompressed SEC 1")
        with self.assertRaises(RuntimeError):
            ECC().generate_uncompressed_SEC(None, pub_key[1])

    def test_uncompressed_SEC_should_raise_error_2(self):
        # It should raise an error since we are passing None
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = (4009715469895962904302745416817721540571577912364644137838095050706137667860,
                   32025336288095498019218993550383068707359510270784983226210884843871535451292)

        print("There should be a raised RuntimeError because None is passed as argument to generate uncompressed SEC 2")
        with self.assertRaises(RuntimeError):
            ECC().generate_uncompressed_SEC(pub_key[0], None)

    def test_uncompressed_SEC_should_raise_error_3(self):
        # It should raise an error since we are passing None
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = (4009715469895962904302745416817721540571577912364644137838095050706137667860,
                   32025336288095498019218993550383068707359510270784983226210884843871535451292)

        print("There should be a raised RuntimeError because None is passed as argument to generate uncompressed SEC 3")
        with self.assertRaises(RuntimeError):
            ECC().generate_uncompressed_SEC(None, None)

    def test_uncompressed_SEC_should_raise_error_4(self):
        # It should raise an error since we are passing None
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = (4009715469895962904302745416817721540571577912364644137838095050706137667860,
                   32025336288095498019218993550383068707359510270784983226210884843871535451292)

        print("There should be a raised RuntimeError because 0 is passed as argument to generate uncompressed SEC 4")
        with self.assertRaises(RuntimeError):
            ECC().generate_uncompressed_SEC(0, pub_key[1])

    def test_compressed_SEC_should_raise_error_1(self):
        # It should raise an error since we are passing None
        priv_key = 52025986665857613263760395809269303684785643089926984150804307617991608511766
        pub_key = (43733605778270459583874364812384261459365992207657902102567152558096696733127,
                   64346778444748414606606796249150556060624935198788845168028978963277938956739)

        print("There should be a raised RuntimeError because None is passed as argument to generate compressed SEC 1")
        with self.assertRaises(RuntimeError):
            ECC().generate_compressed_SEC(pub_key[0], None)

    def test_compressed_SEC_should_raise_error_2(self):
        # It should raise an error since we are passing None
        priv_key = 52025986665857613263760395809269303684785643089926984150804307617991608511766
        pub_key = (43733605778270459583874364812384261459365992207657902102567152558096696733127,
                   64346778444748414606606796249150556060624935198788845168028978963277938956739)

        print("There should be a raised RuntimeError because None is passed as argument to generate compressed SEC 2")
        with self.assertRaises(RuntimeError):
            ECC().generate_compressed_SEC(None, pub_key[1])

    def test_compressed_SEC_should_raise_error_3(self):
        # It should raise an error since we are passing None
        priv_key = 52025986665857613263760395809269303684785643089926984150804307617991608511766
        pub_key = (43733605778270459583874364812384261459365992207657902102567152558096696733127,
                   64346778444748414606606796249150556060624935198788845168028978963277938956739)

        print("There should be a raised RuntimeError because 0 is passed as argument to generate compressed SEC 3")
        with self.assertRaises(RuntimeError):
            ECC().generate_compressed_SEC(0, pub_key[1])

    # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Test Generating Main net and Test net Addresses #
    # # # # # # # # # # # # # # # # # # # # # # # # # #
    def test_generate_testnet_address_1(self):
        priv_key = 85766691447432562285107349766825790927431446373602486150911666480754112492464
        pub_key = (43651727216793576570341989570883305974491642311510342469928224726666590034225,
                   109857391791750504773247734335453148952192151977881622854599464318335318347795)

        print("There should an error raised because we are not passing in a bytes value")
        compressed_sec = ECC().generate_compressed_SEC(pub_key[0], pub_key[1])

        with self.assertRaises(RuntimeError):
            ECC().generate_address(False, pub_key[1])


    def test_generate_testnet_address_2(self):
        priv_key = 85766691447432562285107349766825790927431446373602486150911666480754112492464
        pub_key = (43651727216793576570341989570883305974491642311510342469928224726666590034225,
                   109857391791750504773247734335453148952192151977881622854599464318335318347795)

        compressed_sec = ECC().generate_compressed_SEC(pub_key[0], pub_key[1])

        #Need to pass the compressed sec in pure byte format -> unhexlify()
        testnet_address = ECC().generate_address(True, compressed_sec)

        expected = "mo24iC138ffpdWiFsH8y7dq6v5CDD1UbiT"

        print("There should be a generated testnet address")

        self.assertEqual(expected, testnet_address)



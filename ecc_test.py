from unittest import TestCase
from binascii import hexlify, unhexlify
from ecc import ECC
from S256Point import G, N, P, A, B

class ECC_Tests(TestCase):
    def test_P(self):
        print("First test, should show ECC.P equal to Prime Number Field")
        self.assertEqual(P, 2**256 - 2**32 - 977)

    # # # # # # # # # # # # # # # # # # # # # # #
    # Test Generating Private and Public Keys   #
    # # # # # # # # # # # # # # # # # # # # # # #
    def test_generate_priv_key(self):
        priv_key = ECC().generate_priv_key()
        print("Private key generated should be above 0 and below ECC.N")
        self.assertTrue(0 < priv_key < N)

    def test_duplicate_priv_key(self):

        prev_gen_priv_keys = {}

        # 2.2 GHz Intel Core i7
        # 16 GB 1600 MHz DDR3
        # Takes about 9 - 10 seconds to run this test
        for _ in range(1000000):
            priv_key = ECC().generate_priv_key()

            assert 0 < priv_key < N

            if priv_key in prev_gen_priv_keys:
                raise RuntimeError('Randomly generated number, has been generated before')

            prev_gen_priv_keys[priv_key] = priv_key

        print("There should be no duplicates after creating 1000000 private keys")

    def test_generate_pub_key(self):
        priv_key = ECC().generate_priv_key()
        pub_key = ECC().generate_pub_key(priv_key)
        print("There should be a x val of pub_key > 0")
        self.assertTrue(0 < pub_key.x.num)

    def test_point_at_infinity(self):
        point_at_infinity = N * G
        print("Point at Infinity, should return None for both x and y")
        self.assertEqual(None, point_at_infinity.x)
        self.assertEqual(None, point_at_infinity.y)

    def test_pub_key_is_on_curve(self):
        priv_key = ECC().generate_priv_key()
        pub_key = ECC().generate_pub_key(priv_key)
        print(pub_key.x, pub_key.y)
        print("Both x and y should be on the curve, checking if pub_key is on curve")
        self.assertEqual(True, ECC().is_on_curve(pub_key.x.num, pub_key.y.num))

    def test_pub_key_is_not_on_curve(self):
        pub_key = (20700948478913772076119439904629995041653958252327787830786676775719940102654,
                   5554562626338682950266833423860784775451683510376504490669758056891525878098)
        print("Should return false, y has been tampered with, so it is not a valid point on the curve")
        self.assertEqual(False, ECC().is_on_curve(pub_key[0], pub_key[1]))


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

        testnet_address = ECC().generate_address(True, compressed_sec)

        expected = "mo24iC138ffpdWiFsH8y7dq6v5CDD1UbiT"

        print("There should be a generated compressed testnet address")

        self.assertEqual(expected, testnet_address)

    def test_generate_testnet_address_uncompressed_3(self):
        priv_key = 85766691447432562285107349766825790927431446373602486150911666480754112492464
        pub_key = (43651727216793576570341989570883305974491642311510342469928224726666590034225,
                   109857391791750504773247734335453148952192151977881622854599464318335318347795)

        uncompressed_sec = ECC().generate_uncompressed_SEC(pub_key[0], pub_key[1])

        testnet_address = ECC().generate_address(True, uncompressed_sec)

        expected = "msfDb9z8hms8yBLwB5zkZCdqivbyvepL5k"

        print("There should be a generated uncompressed testnet address")

        self.assertEqual(expected, testnet_address)

    def test_generate_mainnet_address_uncompressed_4(self):
        priv_key = 85766691447432562285107349766825790927431446373602486150911666480754112492464
        pub_key = (43651727216793576570341989570883305974491642311510342469928224726666590034225,
                   109857391791750504773247734335453148952192151977881622854599464318335318347795)

        uncompressed_sec = ECC().generate_uncompressed_SEC(pub_key[0], pub_key[1])

        mainnet_address = ECC().generate_address(False, uncompressed_sec)

        expected = "1D9GJ6u9tkRtC4sKTX2NjHRWrw1H2xDgqJ"

        print("There should be a generated uncompressed mainnet address")

        self.assertEqual(expected, mainnet_address)

    def test_generate_mainnet_address_compressed_5(self):
        priv_key = 85766691447432562285107349766825790927431446373602486150911666480754112492464
        pub_key = (43651727216793576570341989570883305974491642311510342469928224726666590034225,
                   109857391791750504773247734335453148952192151977881622854599464318335318347795)

        compressed_sec = ECC().generate_compressed_SEC(pub_key[0], pub_key[1])

        mainnet_address = ECC().generate_address(False, compressed_sec)

        expected = "18W7R8v4KeEZrQEe9iAbHicn45bWNn2QBe"

        print("There should be a generated compressed mainnet address")

        self.assertEqual(expected, mainnet_address)

    # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Test Generating a Signature and Verifying       #
    # # # # # # # # # # # # # # # # # # # # # # # # # #
    def test_generating_signature(self):
        priv_key = 85766691447432562285107349766825790927431446373602486150911666480754112492464
        pub_key = (43651727216793576570341989570883305974491642311510342469928224726666590034225,
                   109857391791750504773247734335453148952192151977881622854599464318335318347795)

        z, r, s = ECC().generate_signature(priv_key)

        print("It should return true since we have the private key to verify signature")
        print("Z: {0}".format(z))
        print("R: {0}".format(r))
        print("S: {0}".format(s))

        verified = ECC().verify_signature(z, r, s, pub_key)
        self.assertTrue(verified)
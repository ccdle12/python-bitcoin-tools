import unittest
from bitcoin_tools import *

class FieldElementTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\n----------------------------------------------------------------------------------------")
        print("!!! Starting Field Element Tests !!!")
        print("----------------------------------------------------------------------------------------\n")

    def test_addition(self):
        p1 = FieldElement(9, 11)
        p2 = FieldElement(6, 11)
        self.assertEqual(p1 + p2, FieldElement(4, 11))

        p1 = FieldElement(10, 11)
        p2 = FieldElement(9, 11)
        self.assertEqual(p1 + p2, FieldElement(8, 11))

        # Since product of both nums are below the prime field, the answer is the normal addition
       
        print("Since product of both nums are below the prime field, the answer is the normal addition")
        p1 = FieldElement(2, 11)
        p2 = FieldElement(3, 11)
        self.assertEqual(p1 + p2, FieldElement(5, 11))

        p1 = FieldElement(6, 11)
        p2 = FieldElement(3, 11)
        self.assertEqual(p1 + p2, FieldElement(9, 11))

        # Should throw an error since passing two different primes
        print("Should throw an error since passing two different primes")
        with self.assertRaises(RuntimeError):
            p1 = FieldElement(2, 11)
            p2 = FieldElement(3, 7)
            p3 = p1 + p2

        # Should throw an error num is greater than prime number
        print("Should throw an error num is greater than prime number")
        with self.assertRaises(RuntimeError):
            p1 = FieldElement(12, 11)
            p2 = FieldElement(3, 11)
            p3 = p1 + p2

        with self.assertRaises(RuntimeError):
            p1 = FieldElement(2, 11)
            p2 = FieldElement(24, 11)
            p3 = p1 + p2

        # Should throw an error since num is less than 0, cannot have a member of the prime field below 0
        print("Should throw an error since num is less than 0")
        with self.assertRaises(RuntimeError):
            p1 = FieldElement(-1, 11)
            p2 = FieldElement(3, 11)
            p3 = p1 + p2

        with self.assertRaises(RuntimeError):
            p1 = FieldElement(2, 11)
            p2 = FieldElement(-24, 11)
            p3 = p1 + p2

    def test_subtraction(self):
        # Should throw an error since passing two different primes
        print("Should throw an error since passing two different primes")
        with self.assertRaises(RuntimeError):
            p1 = FieldElement(2, 11)
            p2 = FieldElement(3, 7)
            p3 = p1 - p2

        p1 = FieldElement(9, 11)
        p2 = FieldElement(6, 11)
        self.assertEqual(p1 - p2, FieldElement(3, 11))

        p1 = FieldElement(10, 11)
        p2 = FieldElement(1, 11)
        self.assertEqual(p1 - p2, FieldElement(9, 11))

        p1 = FieldElement(5, 11)
        p2 = FieldElement(10, 11)
        self.assertEqual(p1 - p2, FieldElement(6, 11))

        p1 = FieldElement(2, 11)
        p2 = FieldElement(4, 11)
        self.assertEqual(p1 - p2, FieldElement(9, 11))

        p1 = FieldElement(1, 11)
        p2 = FieldElement(10, 11)
        self.assertEqual(p1 - p2, FieldElement(2, 11))

    def test_multiplication(self):
        # Should throw an error since passing two different primes
        print("Should throw an error since passing two different primes")
        with self.assertRaises(RuntimeError):
            p1 = FieldElement(2, 11)
            p2 = FieldElement(3, 7)
            p3 = p1 * p2

        p1 = FieldElement(9, 11)
        p2 = FieldElement(6, 11)
        self.assertEqual(p1 * p2, FieldElement(10, 11))

        p1 = FieldElement(2, 11)
        p2 = FieldElement(3, 11)
        self.assertEqual(p1 * p2, FieldElement(6, 11))

        p1 = FieldElement(6, 11)
        p2 = FieldElement(6, 11)
        self.assertEqual(p1 * p2, FieldElement(3, 11))

        p1 = FieldElement(3, 11)
        p2 = FieldElement(5, 11)
        self.assertEqual(p1 * p2, FieldElement(4, 11))

    def test_powers(self):
        p1 = FieldElement(9, 11)
        self.assertEqual(p1 ** 2, FieldElement(4, 11))

        print( "Will perform powers with an exponent greater than the prime, it should wrap around and keep the product within the field of the prime number")
        p1 = FieldElement(2, 5)
        self.assertEqual(p1 ** 6, FieldElement(4, 5))

        # Prime: 7
        # Powers: 9
        # Num: 5
        # Power % (prime - 1) = 9 % (7-1) = 9 % 6 = 3
        # exponent = 3
        # result = num ^ exponent = 5**3 = 125
        # final result = 125 % 7
        p1 = FieldElement(5, 7)
        self.assertEqual(p1 ** 9, FieldElement(6, 7))

        # Prime: 5
        # Powers: 12
        # Num: 2
        # Exponent = Power % (prime - 1) = 12 % (5 - 1) = 12 % 4 = 8
        # Result = num ^ exponent = 2 ** 8 = 256
        # Final Result = result % prime = 256 % 5 = 1
        p1 = FieldElement(2, 5)
        self.assertEqual(p1 ** 12, FieldElement(1, 5))

        # Prime: 5
        # Powers: 9
        # Num: 3
        # Exponent = Powers % (prime - 1) = 9 % (5 - 1) = 9 % 4 = 5
        # Result = num ^ exponent = 3 ** 5 = 243
        # Final modulo operation keeps result within the prime field
        # Final Result = result % prime = 243 % 5 = 3
        p1 = FieldElement(3, 5)
        self.assertEqual(p1 ** 9, FieldElement(3, 5))

    def test_division(self):
        print("\nShould throw an error since passing two different primes")
        with self.assertRaises(RuntimeError):
            p1 = FieldElement(2, 11)
            p2 = FieldElement(3, 7)
            p3 = p1 / p2

        # Formula: (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
        # (2 * pow(3, (11-2), 11)) % 11
        # Calculate the pow equation: 3^9 == 19,683
        # exponent = 19,683 % 11 = 4
        # 2 * 4 = 8
        # 8 % 11 = 8
        p1 = FieldElement(2, 11)
        p2 = FieldElement(3, 11)
        print((p1 / p2).num)
        self.assertEqual(p1 / p2, FieldElement(8, 11))

        # Formula: (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
        # (4 * pow(3, (5-2), 5)) % 5
        # 3^3 == 27
        # exponent = 27 % 5 = 2
        # 4 * 2 = 8
        # 8 % 5 = 1
        p1 = FieldElement(4, 5)
        p2 = FieldElement(3, 5)
        self.assertEqual(p1 / p2, FieldElement(3, 5))

        # Formula: (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
        # (6 * pow(4, (7-2), 7)) % 7
        # 4^5 == 1024
        # exponent = 1024 % 7 = 2
        # 6 * 2 = 12
        # 12 % 7 = 5
        p1 = FieldElement(6, 7)
        p2 = FieldElement(4, 7)
        self.assertEqual(p1 / p2, FieldElement(5, 7))

    def test_rmul(self):
        p1 = FieldElement(5, 11)
        expected = p1 + p1
        scalar = 2
        self.assertEqual(scalar * p1, expected)

        p1 = FieldElement(5, 11)
        expected = p1 + p1 + p1
        scalar = 3
        self.assertEqual(scalar * p1, expected)

        p1 = FieldElement(5, 11)
        expected = p1 + p1 + p1 + p1 + p1
        scalar = 5
        self.assertEqual(scalar * p1, expected)



class PointTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n----------------------------------------------------------------------------------------")
        print("!!! Starting Point Tests !!!")
        print("----------------------------------------------------------------------------------------\n")

    def test_points_on_curve(self):
        with self.assertRaises(RuntimeError):
            Point(x=2, y=7, a=5, b=7)

        # Comparing for equality
        p1 = Point(18, 77, 5, 7)
        p2 = Point(18, 77, 5, 7)
        self.assertEqual(p1, p2)

        # Adding two points
        p1 = Point(x=3, y=7, a=5, b=7)
        p2 = Point(x=-1, y=-1, a=5, b=7)
        self.assertEqual(p1 + p2, Point(x=2, y=-5, a=5, b=7))

        # Adding two points by point doubling
        a = Point(x=-1, y=1, a=5, b=7)
        self.assertEqual(a + a, Point(x=18, y=-77, a=5, b=7))

    def test_rmul(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        multiplications = (
            (2, 192, 105, 49, 71),
            (2, 143, 98, 64, 168),
            (2, 47, 71, 36, 111),
            (4, 47, 71, 194, 51),
            (8, 47, 71, 116, 55),
            (21, 47, 71, None, None),
        )

        # iterate over the multiplications
        for coefficient, _x1, _y1, _x2, _y2 in multiplications:
            x1 = FieldElement(_x1, prime)
            y1 = FieldElement(_y1, prime)
            p1 = Point(x1, y1, a, b)

            # initialize the second point based on whether it's the point at infinity
            if _x2 is None:
                p2 = Point(None, None, a, b)
            else:
                x2 = FieldElement(_x2, prime)
                y2 = FieldElement(_y2, prime)
                p2 = Point(x2, y2, a, b)

            # check that the product is equal to the expected point
            self.assertEqual(coefficient * p1, p2)



class S256Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n----------------------------------------------------------------------------------------")
        print("!!! Starting S256 Tests !!!")
        print("----------------------------------------------------------------------------------------\n")
       
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
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = S256Point(4009715469895962904302745416817721540571577912364644137838095050706137667860,
                            32025336288095498019218993550383068707359510270784983226210884843871535451292)

        sec_x = pub_key.x.num.to_bytes(32, 'big')
        sec_y = pub_key.y.num.to_bytes(32, 'big')

        expected = hexlify(b'\x04' + sec_x + sec_y)

        print("Should generate an uncompressed public key")
        self.assertEqual(expected, pub_key.get_sec(compressed=False))

        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = S256Point(4009715469895962904302745416817721540571577912364644137838095050706137667860,
                            32025336288095498019218993550383068707359510270784983226210884843871535451292)

        print("There should be a true assertion that y in pub_key is EVEN")
        # We know the Y val of the pub_key is EVEN
        self.assertTrue(pub_key.y.num % 2 == 0)

        priv_key = 52025986665857613263760395809269303684785643089926984150804307617991608511766
        pub_key = S256Point(43733605778270459583874364812384261459365992207657902102567152558096696733127,
                            64346778444748414606606796249150556060624935198788845168028978963277938956739)

        print("There should be a true assertion that y in pub_key is ODD")
        # We know the Y val of the pub_key is ODD
        self.assertFalse(pub_key.y.num % 2 == 0)

        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = S256Point(4009715469895962904302745416817721540571577912364644137838095050706137667860,
                            32025336288095498019218993550383068707359510270784983226210884843871535451292)

        sec_x = pub_key.x.num.to_bytes(32, 'big')
        sec_y = pub_key.y.num.to_bytes(32, 'big')

        expected = hexlify(b'\x02' + sec_x)
        print("Expected compressed EVEN: {0}".format(expected))
        print("There should be a valid EVEN compressed SEC format pub_key")
        self.assertEqual(expected, pub_key.get_sec(compressed=True))

        priv_key = 52025986665857613263760395809269303684785643089926984150804307617991608511766
        pub_key = S256Point(43733605778270459583874364812384261459365992207657902102567152558096696733127,
                            64346778444748414606606796249150556060624935198788845168028978963277938956739)

        sec_x = pub_key.x.num.to_bytes(32, 'big')
        sec_y = pub_key.y.num.to_bytes(32, 'big')

        expected = hexlify(b'\x03' + sec_x)
        print("Expected Compressed ODD: {0}".format(expected))
        print("There should be a valid ODD compressed SEC format pub_key")
        self.assertEqual(expected, pub_key.get_sec(compressed=True))

        # It should raise an error since we are passing None
        priv_key = 111567339125642131892342490513530754499087578141730827863121284639663457832497
        pub_key = S256Point(None,
                            32025336288095498019218993550383068707359510270784983226210884843871535451292)

        print("There should be a raised RuntimeError because None is passed as argument to SEC")
        with self.assertRaises(RuntimeError):
            pub_key.get_sec(compressed=True)

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

        testnet_address = pub_key.get_address(compressed_sec, mainnet=False)

        expected = "mo24iC138ffpdWiFsH8y7dq6v5CDD1UbiT"

        print("There should generate a compressed testnet address")

        self.assertEqual(expected, testnet_address)

        priv_key = 85766691447432562285107349766825790927431446373602486150911666480754112492464
        pub_key = S256Point(43651727216793576570341989570883305974491642311510342469928224726666590034225,
                            109857391791750504773247734335453148952192151977881622854599464318335318347795)

        compressed_sec = pub_key.get_sec(compressed=True)
        print(type(compressed_sec))

        mainnet_address = pub_key.get_address(compressed_sec, mainnet=True)

        expected = "18W7R8v4KeEZrQEe9iAbHicn45bWNn2QBe"

        print("It should return the mainnet address")
        self.assertEqual(expected, mainnet_address)

        priv_key = 85766691447432562285107349766825790927431446373602486150911666480754112492464
        pub_key = S256Point(43651727216793576570341989570883305974491642311510342469928224726666590034225,
                            109857391791750504773247734335453148952192151977881622854599464318335318347795)

        # 0360820086ce7d8015b537abb9937805b49e178db9151cfe43d0aa529919481931
        compressed_sec = pub_key.get_sec(compressed=True)

        print("It should raise error as not passing bytes as argument")
        with self.assertRaises(RuntimeError):
            pub_key.get_address("0360820086ce7d8015b537abb9937805b49e178db9151cfe43d0aa529919481931", mainnet=True)

        priv_key = 85766691447432562285107349766825790927431446373602486150911666480754112492464
        pub_key = S256Point(43651727216793576570341989570883305974491642311510342469928224726666590034225,
                            109857391791750504773247734335453148952192151977881622854599464318335318347795)

        # 0360820086ce7d8015b537abb9937805b49e178db9151cfe43d0aa529919481931
        print("It should NOT raise error as passing bytes as argument")
        compressed_sec = pub_key.get_sec(compressed=True)
        mainnet_address = pub_key.get_address(b'0360820086ce7d8015b537abb9937805b49e178db9151cfe43d0aa529919481931',
                                              mainnet=True)

class BlockchainExplorerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n----------------------------------------------------------------------------------------")
        print("!!! Starting Blockchain Explorer Tests !!!")
        print("----------------------------------------------------------------------------------------\n")
        
    def test_request_to_block_cypher(self):
        print("Block cypher returns 200 and name of chain")
        expected = "BTC.test3"
        self.assertEqual(expected, ping().json()["name"])

        print("Should make request for the balance of the address passed")
        expected = 200
        self.assertEqual(expected, request_balance("mfke2PVhGePAy1GfZNotr6LeXfQ5nwnZTa").status_code)

        print("Should return an error since we haven't passed a valid address")
        with self.assertRaises(RuntimeError):
            request_balance("m2PVhGePAy1GfZNotr6LeXfQ5nw")

        print("Should make request for the balance of the address passed")
        expected = 200
        tx = get_transaction(
            "fea5cbf4efc220a5512d394279778f75937c253cac32c43047cadffc9ee4d85c").status_code
        self.assertEqual(expected, tx)

        print("Should return an error on request_UTXOs since we haven't passed a valid address")
        with self.assertRaises(RuntimeError):
            request_UTXOs("m2PVhGePAy1GfZNotr6LeXfQ5")

        # print("--------------------------------------------------------------")
        # print("Should decode transaction details and return the addresse of the sending address")
        # tx_to_decode = "01000000015cd8e49efcdfca4730c432ac3c257c93758f777942392d51a520c2eff4cba5fe010000008b4230333566623364616638353538383831616232366530393535653936656563373539333763353133643733306335656635383636623461326130626435323230363047304402203608e89b94feab1cc26f5350dfaaaa5a3d8feee8213e46305924e573e2cf19240220170415f4042ec1e9b3ee8edb51bb338277b5ded56595959289edb8d301bf782501ffffffff0280f0fa02000000001976a914ada5b5ba34eb8774388d0ac30c5bc3c8e8afae0388ac60cd4906000000001976a914029692862d60b5f84ba706b37939d074b6c5808588ac00000000"
        # response = BlockchainExplorer().decode_transaction(tx_to_decode).json()
        # expected = 'mfke2PVhGePAy1GfZNotr6LeXfQ5nwnZTa'
        # print(response)
        # self.assertEqual(expected, response['addresses'][1])

    # def test_request_block_trail(self):
    #     print("Should only test block trail API requests")
    #     response = request_balance("mfke2PVhGePAy1GfZNotr6LeXfQ5nwnZTa")
    #     status_code = response.status_code
    #     print(response.json())
    #     self.assertEqual(200, status_code)


class ECCTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n----------------------------------------------------------------------------------------")
        print("!!! Starting ECC Tests !!!")
        print("----------------------------------------------------------------------------------------\n")
        
    def test_P(self):
        print("First test, should show ECC.P equal to Prime Number Field")
        self.assertEqual(P, 2 ** 256 - 2 ** 32 - 977)

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

class HelperTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("!!! Starting Helper Tests !!!")

    def test_decode_base58(self):
        print("Should decode base 58")
        expected = b'029692862d60b5f84ba706b37939d074b6c58085'
        self.assertEqual(expected, hexlify(decode_base58("mfke2PVhGePAy1GfZNotr6LeXfQ5nwnZTa")))

    def test_bitcoin_to_satoshi(self):
        print("Should return bitcoin to satoshi")
        expected = 50000000
        self.assertEqual(expected, bitcoin_to_satoshi(0.5))

class PrivateKeyTest(TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n----------------------------------------------------------------------------------------")
        print("!!! Starting Private Key Tests !!!")
        print("----------------------------------------------------------------------------------------\n")
        
    def test_init_PrivateKey(self):
        priv_key = PrivateKey().secret

        print("Private Key should not be None")
        self.assertIsNotNone(priv_key)

        print("Private key should be greater than 0 and less than N")
        self.assertTrue(0 < priv_key < N)

        print("Private key should NOT be greater than N")
        self.assertFalse(priv_key > N)

        point_at_infinity = N * G
        print("Point at Infinity, should return None for both x and y")
        self.assertEqual(None, point_at_infinity.x)
        self.assertEqual(None, point_at_infinity.y)

    # def test_duplicate_priv_key(self):
    #     prev_gen_priv_keys = {}

    #     # 2.2 GHz Intel Core i7
    #     # 16 GB 1600 MHz DDR3
    #     # Takes about 9 - 10 seconds to run this test
    #     for _ in range(1000000):
    #         priv_key = PrivateKey().secret

    #         assert 0 < priv_key < N

    #         print(priv_key)
    #         if priv_key in prev_gen_priv_keys:
    #             raise RuntimeError('Randomly generated number, has been generated before')

    #         prev_gen_priv_keys[priv_key] = priv_key

    #     print("There should be no duplicates after creating 1000000 private keys")

    def test_gen_pub_key(self):
        priv_key = PrivateKey()
        pub_key = priv_key.public_key

        print("pub_key has been generated")
        self.assertIsNotNone(pub_key)

        print("Both x and y should be on the curve, checking if pub_key is on curve")
        self.assertTrue(priv_key.is_on_curve())

    def test_wallet_import_format(self):
        secret = 40739339072244861339425603543300453407867090494212474723312591401916565730912

        prefix = b'\x80'
        s = secret.to_bytes(32, 'big')

        print("Should create wallet import format for mainnet uncompressed")
        expected = "5JVxGiHdVvu7XTr1PMRb8gGE2vdFYQnsErmJMFrUXSF5rWf6sPh"
        self.assertEqual(expected, encode_base58_checksum(prefix + s))

        print("Should create wallet import format for mainnet compressed")
        expected = "KzEnxMEQ6gu1oTVJhf9XetJCXVh1Be1SkAeXaQZNVLRARGK6inwT"
        self.assertEqual(expected, encode_base58_checksum(prefix + s + b'\x01'))

        print("Should create wallet import format for testnet uncompressed")
        prefix = b'\xef'
        expected = "92GarT7B69yFVXMJ1hKW1GpBgayxhaL4aodFRtCysAz8dWAsiBQ"
        self.assertEqual(expected, encode_base58_checksum(prefix + s))

        print("Should create wallet import format for testnet uncompressed")
        prefix = b'\xef'
        expected = "cQbnRGEFXkbGxtxa64xf2CoG9izQr678pCnzgq1szT5Ag1U7rZ88"
        self.assertEqual(expected, encode_base58_checksum(prefix + s + b'\x01'))

        print("Should create wallet import format for mainnet uncompressed")
        expected = "5"
        self.assertEqual(expected, PrivateKey().get_WIF(compressed=False, mainnet=True)[:1])

        print("Should create wallet import format for mainnet compressed")
        expected = "K"
        expected2 = "L"
        self.assertTrue(expected or expected2 == PrivateKey().get_WIF(compressed=True, mainnet=True)[:1])

        print("Should create wallet import format for testnet and uncompressed")
        expected = "9"
        self.assertEqual(expected, PrivateKey().get_WIF(compressed=False, mainnet=False)[:1])

        print("Should create wallet import format for testnet and compressed")
        expected = "c"
        self.assertEqual(expected, PrivateKey().get_WIF(compressed=True, mainnet=False)[:1])

class ScriptTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n----------------------------------------------------------------------------------------")
        print("!!! Starting Script Tests !!!")
        print("----------------------------------------------------------------------------------------\n")
        
    def test_script_type(self):
        print("Should return type p2pkh (pay to pub key hash)")
        # script_pubkey = <76 : OP_DUP> <a9 : OP_HASH160> <14 : Length of hash> <88 : OP_EQUAL_VERIFY> <ac : OP_CHECKSIG>
        script_pubkey_raw = unhexlify('76a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac')
        print("Raw bytes pub key: {}".format(script_pubkey_raw))
        script_pubkey = Script.parse(script_pubkey_raw)
        self.assertEqual('p2pkh', script_pubkey.type())

        print("Should return type p2sh (pay to script hash)")
        # p2sh script_pubkey
        # script_pubkey = <a9 : OP_HASH16-> <14 : Length of hash> < hash > <87 : OP_EQUAL>
        script_pubkey_raw = unhexlify('a91474d691da1574e6b3c192ecfb52cc8984ee7b6c5687')
        script_pubkey = Script.parse(script_pubkey_raw)
        self.assertEqual('p2sh', script_pubkey.type())

        print("Should serialize the script and return the bytes in the pattern below")
        # p2sh script_pubkey
        result = hexlify(script_pubkey.serialize())
        self.assertEqual(b'a91474d691da1574e6b3c192ecfb52cc8984ee7b6c5687', result)

    # def test_p2sh(self):
    #     print("Should create a p2sh using the existing addresses")

    #     # Address 1
    #     wallet = main.Main().import_private_key(
    #         100897809677138163174856952607694300238573305027534078569886890414323321447504)

    #     # Address 2
    #     wallet2 = main.Main().import_private_key(
    #         53543775883506703906499148469479904297172220131041556152219913425601595776857)

class TxTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n----------------------------------------------------------------------------------------")
        print("!!! Starting TX Tests !!!")
        print("----------------------------------------------------------------------------------------\n")
        
    def test_parse_transaction(self):
        transaction = '010000000456919960ac691763688d3d3bcea9ad6ecaf875df5339e148a1fc61c6ed7a069e010000006a47304402204585bcdef85e6b1c6af5c2669d4830ff86e42dd205c0e089bc2a821657e951c002201024a10366077f87d6bce1f7100ad8cfa8a064b39d4e8fe4ea13a7b71aa8180f012102f0da57e85eec2934a82a585ea337ce2f4998b50ae699dd79f5880e253dafafb7feffffffeb8f51f4038dc17e6313cf831d4f02281c2a468bde0fafd37f1bf882729e7fd3000000006a47304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a7160121035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937feffffff567bf40595119d1bb8a3037c356efd56170b64cbcc160fb028fa10704b45d775000000006a47304402204c7c7818424c7f7911da6cddc59655a70af1cb5eaf17c69dadbfc74ffa0b662f02207599e08bc8023693ad4e9527dc42c34210f7a7d1d1ddfc8492b654a11e7620a0012102158b46fbdff65d0172b7989aec8850aa0dae49abfb84c81ae6e5b251a58ace5cfeffffffd63a5e6c16e620f86f375925b21cabaf736c779f88fd04dcad51d26690f7f345010000006a47304402200633ea0d3314bea0d95b3cd8dadb2ef79ea8331ffe1e61f762c0f6daea0fabde022029f23b3e9c30f080446150b23852028751635dcee2be669c2a1686a4b5edf304012103ffd6f4a67e94aba353a00882e563ff2722eb4cff0ad6006e86ee20dfe7520d55feffffff0251430f00000000001976a914ab0c0b2e98b1ab6dbf67d4750b0a56244948a87988ac005a6202000000001976a9143c82d7df364eb6c75be8c80df2b3eda8db57397088ac46430600'
        parsed_tx = Tx.parse(transaction)
        script_sig = "47304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a7160121035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937"

        print("Should return the script sig of the second input")
        self.assertEqual(script_sig, hexlify(parsed_tx.tx_ins[1].script_sig.serialize()).decode('ascii'))

        print("Amount of inputs should be 4")
        self.assertEqual(4, len(parsed_tx.tx_ins))

        print("Previous hash/transaction should be 32 bytes in length")
        self.assertEqual(32 * 2, len(hexlify(parsed_tx.tx_ins[0].prev_hash).decode('ascii')))

        print("First output amount should be 100273 Satoshis ")
        self.assertEqual(1000273, parsed_tx.tx_outs[0].amount)

        print("First output amount should be 0.01000273 Bitcoin")
        self.assertEqual(0.01000273, satoshi_to_bitcoin(parsed_tx.tx_outs[0].amount))

    def test_serialization(self):
        raw_tx = unhexlify(
            '0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')

        tx = Tx.parse(raw_tx)
        expected_version = 1
        print("Should return unserialized version number as int")
        self.assertEqual(expected_version, tx.version)

        print("Should return the exact same byte values as tx_raw, since we are serializing the data held in the Tx Object")
        tx_serialized = tx.serialize()
        self.assertEqual(tx_serialized, raw_tx)

    def test_fee_calculation(self):
        print("Should return the fee amount in satoshis")
        hex_tx = unhexlify('0100000001d98f39606b064b94e2f6542c7e3d308209543630b0325065394611db07704795000000006b21035fb3daf8558881ab26e0955e96eec75937c513d730c5ef5866b4a2a0bd522060483045022100e8e6dcecb724bfc880195e1bcd7ef40a3057a1fac2f54137edba303f3b007c16022026ec84a3aed8f0feb2c1920d91635fa5eff3e9541de09dfd287650c466d0c3cf01ffffffff0240420f00000000001976a914ada5b5ba34eb8774388d0ac30c5bc3c8e8afae0388acc0c62d00000000001976a914029692862d60b5f84ba706b37939d074b6c5808588ac00000000')
        tx = Tx.parse(hex_tx)
        expected = 1000000
        self.assertEqual(expected, tx.calculate_fee())

    def test_sig_hash(self):
        print("Should return signature hash of this transaction")
        raw_tx = unhexlify('0100000001d98f39606b064b94e2f6542c7e3d308209543630b0325065394611db07704795000000006b21035fb3daf8558881ab26e0955e96eec75937c513d730c5ef5866b4a2a0bd522060483045022100e8e6dcecb724bfc880195e1bcd7ef40a3057a1fac2f54137edba303f3b007c16022026ec84a3aed8f0feb2c1920d91635fa5eff3e9541de09dfd287650c466d0c3cf01ffffffff0240420f00000000001976a914ada5b5ba34eb8774388d0ac30c5bc3c8e8afae0388acc0c62d00000000001976a914029692862d60b5f84ba706b37939d074b6c5808588ac00000000')
        tx = Tx.parse(raw_tx)

        hash_type = SIGHASH_ALL

        # expected = int('27e0c5994dec7824e56dec6b2fcb342eb7cdb0d0957c2fce9882f715e85d81a6', 16)
        self.assertEqual(tx.sig_hash(0, hash_type), 77258308350076620367147655891627665071260816465761938366048897796088334202502)

    def test_validate_input_signature(self):
        print("Should return true for validating the signature of 0 index input")
        hex_tx = unhexlify('010000000199ab3f377992df2ccad0af99dc846af032fbd982f916d72715d2eb0f2828342d010000006b483045022100ac3e55420a7b9897f0da43ff7a076895d0ead13fda49926041124aca00c5d6070220245aaefc7047563e42baa350cc7424efcb03ef7e70e596c28b5eca7223fa663f01210275bdc1759e7ffb5fb1f07655d5572cec8219b28250acdbc7f936396884d196f2ffffffff0280841e00000000001976a914029692862d60b5f84ba706b37939d074b6c5808588acc0fb3900000000001976a914ada5b5ba34eb8774388d0ac30c5bc3c8e8afae0388ac00000000')
        index = 0

        tx = Tx.parse(hex_tx)

        self.assertTrue(tx.validate_signature(index))

class UTXOTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n----------------------------------------------------------------------------------------")
        print("!!! Starting UTXO Tests !!!")
        print("----------------------------------------------------------------------------------------\n")

    def test_can_init(self):
        print("Can Init a UTXO object")
        UTXOObj = UTXO(tx_hash='7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20',
                                  block_height=1283283,   
                                  tx_index=1,
                                  value=104900000,
                                  confirmations=3322,
                                  confirmed="2018-02-17T19:10:32Z",
                                  double_spend=False)

        self.assertIsNotNone(UTXOObj)

    def test_can_parse(self):
        print("Should parse response and init object")
        utxo_object = UTXO.parse({'tx_hash': '7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20', 'block_height': 1283283, 'tx_input_n': -1, 'tx_output_n': 1, 'value': 104900000, 'ref_balance': 211900000, 'spent': False, 'confirmations': 3326, 'confirmed': '2018-02-17T19:10:32Z', 'double_spend': False})

        self.assertEqual('7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20', utxo_object.tx_hash)

    def test_should_return_block_cypher_schema(self):
        print("Should return 'block_cypher'")
        utxo_object = UTXO.parse({'tx_hash': '7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20', 'block_height': 1283283, 'tx_input_n': -1, 'tx_output_n': 1, 'value': 104900000, 'ref_balance': 211900000, 'spent': False, 'confirmations': 3326, 'confirmed': '2018-02-17T19:10:32Z', 'double_spend': False})

        schema_type = utxo_object.schema_type({'tx_hash': '7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20', 'block_height': 1283283, 'tx_input_n': -1, 'tx_output_n': 1, 'value': 104900000, 'ref_balance': 211900000, 'spent': False, 'confirmations': 3326, 'confirmed': '2018-02-17T19:10:32Z', 'double_spend': False})

        self.assertEqual('block_cypher', schema_type)

    def test_should_return_run_time_error(self):
        print("Should return Run Time Error Unknown Schema Type")
        utxo_object = UTXO.parse({'tx_hash': '7c95996721bba829589a622d4bed06410ab455a8be932271d53ec9630b586c20', 'block_height': 1283283, 'tx_input_n': -1, 'tx_output_n': 1, 'value': 104900000, 'ref_balance': 211900000, 'spent': False, 'confirmations': 3326, 'confirmed': '2018-02-17T19:10:32Z', 'double_spend': False})

        with self.assertRaises(RuntimeError):
            schema_type = utxo_object.schema_type({'block_height': 1283283, 'tx_input_n': -1, 'tx_output_n': 1, 'value': 104900000, 'ref_balance': 211900000, 'spent': False, 'confirmations': 3326, 'confirmed': '2018-02-17T19:10:32Z', 'double_spend': False})

        print("Should return Run Time Error Unknown Schema Type")
        with self.assertRaises(RuntimeError):
            utxo_object = UTXO.parse({'block_height': 1283283, 'tx_input_n': -1, 'tx_output_n': 1, 'value': 104900000, 'ref_balance': 211900000, 'spent': False, 'confirmations': 3326, 'confirmed': '2018-02-17T19:10:32Z', 'double_spend': False})


class SignatureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n----------------------------------------------------------------------------------------")
        print("!!! Starting Signature Tests !!!")
        print("----------------------------------------------------------------------------------------\n")


    def test_generating_signature(self):
        print("Should pass as valid Signature object, test will assert sig IS NOT NONE")

        r = 65768643913645672968978426589689987237850374542483501912088659345491159391021
        s = 55618899300744280687710599871980893657541124572884031214465422719409044157728
        sig = Signature(r, s)

        self.assertIsNotNone(sig)
        self.assertEqual(sig.r, r)

        print("Should pass and return valid DER signature")
        expected = "30450221009167bbb944c67d650cab2f3d5cbd06c2391977de478832c50d4af00b0a2f9b2d02207af72e71cecf43022204cce257af9625f799d5a90ed904c42b903771dd217520"
        self.assertEqual(expected, hexlify(sig.der()).decode('ascii'))


        print("Should raise error length of signature is too short")
        with self.assertRaises(RuntimeError):
            sig = Signature.parse(unhexlify(
                "30450221009167bbb944c67d650cab2f3d5cbd06c2391977de478832c50d4af00b0a2f9b2d02207af72e71cecf43022204cce257af9625f799d5a90ed904c42b903771dd2175"))


        print("Should return bad signature")
        with self.assertRaises(RuntimeError):
            sig = Signature.parse(unhexlify(
                "20450221009167bbb944c67d650cab2f3d5cbd06c2391977de478832c50d4af00b0a2f9b2d02207af72e71cecf43022204cce257af9625f799d5a90ed904c42b903771dd2175"))


        sig.der()
if __name__ == '__main__':
    unittest.main()
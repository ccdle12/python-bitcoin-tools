import test_helper as helper
from ecc_test import ECC_Tests
from FieldElement import FieldElementTest
from Point import PointTest
from S256Point import S256Test
from Signature import SignatureTest
from PrivateKey import PrivateKeyTest


# # # # # # # # # # # # # # # # # # # # # #  #
#  Field Element Test                        #
# # # # # # # # # # # # # # # # # # # ## # # #
helper.run_test(FieldElementTest('test_addition'))
helper.run_test(FieldElementTest('test_subtraction'))
helper.run_test(FieldElementTest('test_multiplication'))
helper.run_test(FieldElementTest('test_powers'))
helper.run_test(FieldElementTest('test_division'))
helper.run_test(FieldElementTest('test_rmul'))


# # # # # # # # # # # # # # # # # # # #
#  Point Tests                        #
# # # # # # # # # # # # # # # # # # # #
helper.run_test(PointTest('test_points_on_curve'))
helper.run_test(PointTest('test_rmul'))


# # # # # # # # # # # # # # # # # # # #
#  S256 Point Tests                   #
# # # # # # # # # # # # # # # # # # # #
helper.run_test(S256Test('test_point_at_infinity'))
helper.run_test(S256Test('test_generating_pub_key'))
helper.run_test(S256Test('test_pubpoint'))
helper.run_test(S256Test('test_generate_sec_pub_key'))
helper.run_test(S256Test('test_generate_address'))


#//TODO: RENAME ECC_TESTS TO ECCTest
# # # # # # # # # # # # # # # # # # # #
#  ECC Tests                          #
# # # # # # # # # # # # # # # # # # # #

helper.run_test(ECC_Tests('test_P'))
helper.run_test(ECC_Tests('test_generate_priv_key'))
# # # Takes 9 - 10 seconds
# helper.run_test(ECC_Tests('test_duplicate_priv_key'))
helper.run_test(ECC_Tests('test_generate_pub_key'))
helper.run_test(ECC_Tests('test_point_at_infinity'))
helper.run_test(ECC_Tests('test_pub_key_is_on_curve'))
helper.run_test(ECC_Tests('test_pub_key_is_not_on_curve'))


# # # # # # # # # # # # # # # # # # # # #
#  Signature Test                       #
# # # # # # # # # # # # # # # # # # # # #
helper.run_test(SignatureTest('test_generating_signature'))


# # # # # # # # # # # # # # # # # # # # # #
#  Private Key Test                       #
# # # # # # # # # # # # # # # # # # # # # #
helper.run_test(PrivateKeyTest('test_init_PrivateKey'))
# # # Takes 9 - 10 seconds
# helper.run_test(PrivateKeyTest('test_duplicate_priv_key'))
helper.run_test(PrivateKeyTest('test_gen_pub_key'))
helper.run_test(PrivateKeyTest('test_wallet_import_format'))





# # # # # # # # # # # # # # # # # # # # # #
#  NOT BEING USED                         #
# # # # # # # # # # # # # # # # # # # # # #
# helper.run_test(ECC_Tests('test_uncompressed_SEC'))
# helper.run_test(ECC_Tests('test_compressed_SEC_1'))
# helper.run_test(ECC_Tests('test_compressed_SEC_2'))
# helper.run_test(ECC_Tests('test_compressed_SEC_1_EVEN'))
# helper.run_test(ECC_Tests('test_compressed_SEC_2_ODD'))
# helper.run_test(ECC_Tests('test_uncompressed_SEC_should_raise_error_1'))
# helper.run_test(ECC_Tests('test_uncompressed_SEC_should_raise_error_2'))
# helper.run_test(ECC_Tests('test_uncompressed_SEC_should_raise_error_3'))
# helper.run_test(ECC_Tests('test_uncompressed_SEC_should_raise_error_4'))
# helper.run_test(ECC_Tests('test_compressed_SEC_should_raise_error_1'))
# helper.run_test(ECC_Tests('test_compressed_SEC_should_raise_error_2'))
# helper.run_test(ECC_Tests('test_compressed_SEC_should_raise_error_3'))
# helper.run_test(ECC_Tests('test_generate_testnet_address_1'))
# helper.run_test(ECC_Tests('test_generate_testnet_address_2'))
# helper.run_test(ECC_Tests('test_generate_testnet_address_uncompressed_3'))
# helper.run_test(ECC_Tests('test_generate_mainnet_address_uncompressed_4'))
# helper.run_test(ECC_Tests('test_generate_mainnet_address_compressed_5'))
# helper.run_test(ECC_Tests('test_generating_signature'))



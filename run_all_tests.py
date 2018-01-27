import test_helper as helper
from ecc_test import ECC_Tests

# # # # # # # # # # # # # # # # # # # #
#  ECC Tests                          #
# # # # # # # # # # # # # # # # # # # #

#Tests
helper.run_test(ECC_Tests('test_P'))
helper.run_test(ECC_Tests('test_generate_priv_key'))

# Takes 9 - 10 seconds
# helper.run_test(ECC_Tests('test_duplicate_priv_key'))

helper.run_test(ECC_Tests('test_generate_pub_key'))
helper.run_test(ECC_Tests('test_point_at_infinity'))
helper.run_test(ECC_Tests('test_pub_key_is_on_curve'))
helper.run_test(ECC_Tests('test_pub_key_is_not_on_curve'))
helper.run_test(ECC_Tests('test_uncompressed_SEC'))
helper.run_test(ECC_Tests('test_compressed_SEC_1'))
helper.run_test(ECC_Tests('test_compressed_SEC_2'))
helper.run_test(ECC_Tests('test_compressed_SEC_1_EVEN'))
helper.run_test(ECC_Tests('test_compressed_SEC_2_ODD'))
helper.run_test(ECC_Tests('test_uncompressed_SEC_should_raise_error_1'))
helper.run_test(ECC_Tests('test_uncompressed_SEC_should_raise_error_2'))
helper.run_test(ECC_Tests('test_uncompressed_SEC_should_raise_error_3'))
helper.run_test(ECC_Tests('test_uncompressed_SEC_should_raise_error_4'))
helper.run_test(ECC_Tests('test_compressed_SEC_should_raise_error_1'))
helper.run_test(ECC_Tests('test_compressed_SEC_should_raise_error_2'))
helper.run_test(ECC_Tests('test_compressed_SEC_should_raise_error_3'))

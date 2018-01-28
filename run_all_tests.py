import test_helper as helper
from ecc_test import ECC_Tests
from FieldElement import FieldElementTest
from Point import PointTest


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
# helper.run_test(Point_Tests('test_creating_point'))
# helper.run_test(Point_Tests('test_should_fail_passing_None'))
# helper.run_test(Point_Tests('test_should_fail_since_x_y_not_on_ecc'))
# helper.run_test(Point_Tests('test_creating_G_point'))
# helper.run_test(Point_Tests('test_multiplying_a_tuple'))
# helper.run_test(Point_Tests('test_init_Point_object'))
# helper.run_test(Point_Tests('test_multiplying_points'))


# helper.run_test(Point_Tests('test_add_two_points'))





# # # # # # # # # # # # # # # # # # # #
#  ECC Tests                          #
# # # # # # # # # # # # # # # # # # # #

# helper.run_test(ECC_Tests('test_P'))
# helper.run_test(ECC_Tests('test_generate_priv_key'))
# # Takes 9 - 10 seconds
# # helper.run_test(ECC_Tests('test_duplicate_priv_key'))
# helper.run_test(ECC_Tests('test_generate_pub_key'))
# helper.run_test(ECC_Tests('test_point_at_infinity'))
# helper.run_test(ECC_Tests('test_pub_key_is_on_curve'))
# helper.run_test(ECC_Tests('test_pub_key_is_not_on_curve'))
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



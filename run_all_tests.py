import test_helper as helper
import ecc
from ecc import ECC_Tests

# # # # # # # # # # # # # # # # # # # #
#  ECC Tests                          #
# # # # # # # # # # # # # # # # # # # #

#Tests
helper.run_test(ecc.ECC_Tests('test_P'))
helper.run_test(ecc.ECC_Tests('test_generate_priv_key'))

# Takes 9 - 10 seconds
#helper.run_test(ecc.ECC_Tests('test_duplicate_priv_key'))

helper.run_test(ecc.ECC_Tests('test_generate_pub_key'))
helper.run_test(ecc.ECC_Tests('test_point_at_infinity'))
helper.run_test(ecc.ECC_Tests('test_pub_key_is_on_curve'))
helper.run_test(ecc.ECC_Tests('test_pub_key_is_not_on_curve'))
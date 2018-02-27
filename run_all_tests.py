import test_helper as helper
from ecc import ECCTests
from FieldElement import FieldElementTest
from Point import PointTest
from S256Point import S256Test
from Signature import SignatureTest
from PrivateKey import PrivateKeyTest
from Tx import TxTest
from Script import ScriptTest
from main import MainTest
from helper import HelperTest
from blockchain_explorer_helper import BlockchainExplorerTest
from UTXO import UTXOTest


# # # # # # # # # # # # # # # # # # # # # #  #
#  Field Element Test                        #
# # # # # # # # # # # # # # # # # # # ## # # #
# helper.run_test(FieldElementTest('test_addition'))
# helper.run_test(FieldElementTest('test_subtraction'))
# helper.run_test(FieldElementTest('test_multiplication'))
# helper.run_test(FieldElementTest('test_powers'))
# helper.run_test(FieldElementTest('test_division'))
# helper.run_test(FieldElementTest('test_rmul'))


# # # # # # # # # # # # # # # # # # # # # #
# # #  Point Tests                        #
# # # # # # # # # # # # # # # # # # # # # #
# helper.run_test(PointTest('test_points_on_curve'))
# helper.run_test(PointTest('test_rmul'))


# # # # # # # # # # # # # # # # # # # # #
# #  S256 Point Tests                   #
# # # # # # # # # # # # # # # # # # # # # #
# helper.run_test(S256Test('test_point_at_infinity'))
# helper.run_test(S256Test('test_generating_pub_key'))
# helper.run_test(S256Test('test_pubpoint'))
# helper.run_test(S256Test('test_generate_sec_pub_key'))
# helper.run_test(S256Test('test_generate_address'))


# # # # # # # # # # # # # # # # # # # # # #
# # #  ECC Tests                          #
# # # # # # # # # # # # # # # # # # # # # #
# helper.run_test(ECCTests('test_P'))
# helper.run_test(ECCTests('test_generate_priv_key'))

# # # # Takes 9 - 10 seconds
# # helper.run_test(ECC_Tests('test_duplicate_priv_key'))
# helper.run_test(ECCTests('test_generate_pub_key'))
# helper.run_test(ECCTests('test_point_at_infinity'))
# helper.run_test(ECCTests('test_pub_key_is_on_curve'))
# helper.run_test(ECCTests('test_pub_key_is_not_on_curve'))


# # # # # # # # # # # # # # # # # # # # # # #
# # #  Signature Test                       #
# # # # # # # # # # # # # # # # # # # # # # #
# helper.run_test(SignatureTest('test_generating_signature'))


# # # # # # # # # # # # # # # # # # # # # # # #
# # #  Private Key Test                       #
# # # # # # # # # # # # # # # # # # # # # # # #
# helper.run_test(PrivateKeyTest('test_init_PrivateKey'))
# # Takes 9 - 10 seconds
# helper.run_test(PrivateKeyTest('test_duplicate_priv_key'))
# helper.run_test(PrivateKeyTest('test_gen_pub_key'))
# helper.run_test(PrivateKeyTest('test_wallet_import_format'))

# # # # # # # # # # # # # # # # # # # # # # # # #
# #  Script Test                                #
# # # # # # # # # # # # # # # # # # # # # # # # #
# helper.run_test(ScriptTest('test_script_type'))
## helper.run_test(ScriptTest('test_p2sh'))

# # # # # # # # # # # # # # # # # # # # # # #
# #  Tx Test                                #
# # # # # # # # # # # # # # # # # # # # # # #
# helper.run_test(TxTest('test_parse_transaction'))
# helper.run_test(TxTest('test_serialization'))
# helper.run_test(TxTest('test_fee_calculation'))
# helper.run_test(TxTest('test_sig_hash'))
# helper.run_test(TxTest('test_validate_input_signature'))


# # # # # # # # # # # # # # # # # # # # # # # #
# # #  Helper Test                            #
# # # # # # # # # # # # # # # # # # # # # # # #
# helper.run_test(HelperTest('test_decode_base58'))
# helper.run_test(HelperTest('test_bitcoin_to_satoshi'))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # #  Blockchain Explorer Test  - HTTP Requests            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# helper.run_test(BlockchainExplorerTest('test_request_to_block_cypher'))

# # # # # # # # # # # # # # # # # # # # # # #
# #  Wallet Test                            #
# # # # # # # # # # # # # # # # # # # # # # #
# helper.run_test(MainTest('test_private_key_generated'))
# helper.run_test(MainTest('test_p2pkh_generation'))
# helper.run_test(MainTest('test_p2sh_generation'))
# helper.run_test(MainTest('test_send_tx_to_p2sh'))
# helper.run_test(MainTest('test_get_balance'))
# helper.run_test(MainTest('test_get_UTXOs'))
helper.run_test(MainTest('test_send_tx'))

# # # # # # # # # # # # # # # # # # # # # # #
# #  UTXO Test                              #
# # # # # # # # # # # # # # # # # # # # # # #
# helper.run_test(UTXOTest('test_can_init'))
# helper.run_test(UTXOTest('test_can_parse'))
# helper.run_test(UTXOTest('test_should_return_block_cypher_schema'))
# helper.run_test(UTXOTest('test_should_return_run_time_error'))



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



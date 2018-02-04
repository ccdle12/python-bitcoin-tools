from unittest import TestCase
import requests

class BlockchainExplorer:


class BlockchainExplorerTest(TestCase):
    def test_request_to_block_cypher(self):
        print("Block cypher returns 200")
        expected = "200"
        self.assertEqual(expected, BlockchainExplorer().get())
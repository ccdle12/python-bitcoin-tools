from unittest import TestCase
import requests


class BlockchainExplorer:
    def __init__(self):
        self.blockchain_cypher_url = "https://api.blockcypher.com/v1/btc/test3"

    def ping(self):
        return requests.get(self.blockchain_cypher_url)

    def get_balance(self, address):
        balance_url = "/addrs/{}/balance".format(address)
        response = requests.get(self.blockchain_cypher_url + balance_url)

        if response.status_code != 200:
            raise RuntimeError("The server returned an error: {}".format(response.json()))

        return response


class BlockchainExplorerTest(TestCase):
    def test_request_to_block_cypher(self):
        print("Block cypher returns 200 and name of chain")
        expected = "BTC.test3"
        self.assertEqual(expected, BlockchainExplorer().ping().json()["name"])

        print("--------------------------------------------------------------")
        print("Should make request for the balance of the address passed")
        expected = 200
        self.assertEqual(expected, BlockchainExplorer().get_balance("mfke2PVhGePAy1GfZNotr6LeXfQ5nwnZTa").status_code)

        print("--------------------------------------------------------------")
        print("Should return an error since we haven't passed a valid address")

        with self.assertRaises(RuntimeError):
            BlockchainExplorer().get_balance("m2PVhGePAy1GfZNotr6LeXfQ5nw")

        print("--------------------------------------------------------------")
        print("Should construct a transaction")

        # Blockchain Explorer should just pass the transaction as string to the api
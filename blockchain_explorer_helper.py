from unittest import TestCase
import json
import requests

blockchain_cypher_url = "https://api.blockcypher.com/v1/btc/test3"
token_url = "?token=5757068b376143b8aa5f7fc137dc2351"


def ping():
    return requests.get(blockchain_cypher_url)


def get_balance(address):
    balance_url = "/addrs/{}/balance".format(address)
    response = requests.get(blockchain_cypher_url + balance_url)

    if response.status_code != 200:
        raise RuntimeError("The server returned an error: {}".format(response.json()))

    return response


def send_tx(raw_tx):
    send_tx_url = "/txs/push"

    json_tx = create_json_tx(raw_tx)

    response = requests.post(blockchain_cypher_url + send_tx_url + token_url, data=json_tx)

    if response.status_code == 400:
        raise RuntimeError("Error sending the tx: {}".format(response.json()))

    return response


def get_transaction(transaction_hash):
    get_tx_url = "/txs/{}".format(transaction_hash)

    response = requests.get(blockchain_cypher_url + get_tx_url)

    return response


def decode_transaction(raw_tx):
    decode_tx_url = "/txs/decode"

    json_tx = create_json_tx(raw_tx)

    response = requests.post(blockchain_cypher_url + decode_tx_url + token_url, data=json_tx)

    return response


def create_json_tx(raw_tx):
    tx_object = {"tx": raw_tx}
    return json.dumps(tx_object)

def request_balance(address):
    request_balance_url = "/addrs/{}/balance".format(address)

    response = requests.get(blockchain_cypher_url + request_balance_url)

    if response.status_code != 200:
        raise RuntimeError("The server returned an error: {}".format(response.json()))

    return response


class BlockchainExplorerTest(TestCase):
    def test_request_to_block_cypher(self):
        print("Block cypher returns 200 and name of chain")
        expected = "BTC.test3"
        self.assertEqual(expected, ping().json()["name"])

        print("--------------------------------------------------------------")
        print("Should make request for the balance of the address passed")
        expected = 200
        self.assertEqual(expected, request_balance("mfke2PVhGePAy1GfZNotr6LeXfQ5nwnZTa").status_code)

        print("--------------------------------------------------------------")
        print("Should return an error since we haven't passed a valid address")
        with self.assertRaises(RuntimeError):
            request_balance("m2PVhGePAy1GfZNotr6LeXfQ5nw")

        print("--------------------------------------------------------------")
        print("Should make request for the balance of the address passed")
        expected = 200
        tx = get_transaction(
            "fea5cbf4efc220a5512d394279778f75937c253cac32c43047cadffc9ee4d85c").status_code
        self.assertEqual(expected, tx)

        # print("--------------------------------------------------------------")
        # print("Should decode transaction details and return the addresse of the sending address")
        # tx_to_decode = "01000000015cd8e49efcdfca4730c432ac3c257c93758f777942392d51a520c2eff4cba5fe010000008b4230333566623364616638353538383831616232366530393535653936656563373539333763353133643733306335656635383636623461326130626435323230363047304402203608e89b94feab1cc26f5350dfaaaa5a3d8feee8213e46305924e573e2cf19240220170415f4042ec1e9b3ee8edb51bb338277b5ded56595959289edb8d301bf782501ffffffff0280f0fa02000000001976a914ada5b5ba34eb8774388d0ac30c5bc3c8e8afae0388ac60cd4906000000001976a914029692862d60b5f84ba706b37939d074b6c5808588ac00000000"
        # response = BlockchainExplorer().decode_transaction(tx_to_decode).json()
        # expected = 'mfke2PVhGePAy1GfZNotr6LeXfQ5nwnZTa'
        # print(response)
        # self.assertEqual(expected, response['addresses'][1])

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

def request_UTXOs(address):
    request_UTXOs_url = "/addrs/{}".format(address)

    response = requests.get(blockchain_cypher_url + request_UTXOs_url)

    if response.status_code != 200:
        raise RuntimeError("The server returned an error: {}".format(response.json()))

    return (response, 'block_cypher')

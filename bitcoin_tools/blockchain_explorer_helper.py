import json
import requests

# 1st case -> move to its own Class?
# 5757068b376143b8aa5f7fc137dc2351
block_cypher_url = "https://api.blockcypher.com/v1/btc/test3"
block_cypher_token = "?token=c355cd4305b042a980c6b83c4e21bb4d"

# 2nd case -> move to its own Class?
block_trail_url = "https://api.blocktrail.com/v1/tBTC"
block_trail_token = "?api_key=8a2a363be9edf703cba639d7e3f8a1831978f483"

def ping():
    return requests.get(block_cypher_url)


def get_balance(address):
    balance_url = "/addrs/{}/balance".format(address)
    response = requests.get(block_cypher_url + balance_url)

    if response.status_code != 200:
        raise RuntimeError("The server returned an error: {}".format(response.json()))

    return response


def send_tx(raw_tx):
    send_tx_url = "/txs/push"

    json_tx = create_json_tx(raw_tx)

    response = requests.post(block_cypher_url + send_tx_url + block_cypher_token, data=json_tx)

    if response.status_code == 400:
        raise RuntimeError("Error sending the tx: {}".format(response.json()))

    return response


def get_transaction(transaction_hash):
    get_tx_url = "/txs/{}".format(transaction_hash)

    response = requests.get(block_cypher_url + get_tx_url)

    return response


def decode_transaction(raw_tx):
    decode_tx_url = "/txs/decode"

    json_tx = create_json_tx(raw_tx)

    response = requests.post(block_cypher_url + decode_tx_url + block_cypher_token, data=json_tx)

    return response


def create_json_tx(raw_tx):
    tx_object = {"tx": raw_tx}
    return json.dumps(tx_object)

def request_balance(address):
    # 1st case
    request_balance_url = "/addrs/{}/balance".format(address)

    try:
        response = requests.get(block_cypher_url + request_balance_url)

        if response.status_code != 200:
            raise RuntimeError("The server returned an error: {}".format(response.json()))

    except:
        raise RuntimeError("API Limit reached: {}".format(response.json()))

    # 2nd case
    # Block trail does not have a balance request
    try:
        request_UTXOs_url = "/address/{}/unspent-outputs".format(address)

        response = requests.get(block_trail_url + request_UTXOs_url + block_trail_token)

        if response.status_code != 200:
            raise RuntimeError("The server returned an error: {}".format(response.json()))

    except:
        raise RuntimeError("API Limit reached: {}".format(response.json()))
        
    print("Response from Block Trail: {}".format(response))

    return response

def request_UTXOs(address):

    response = None
    schema = None

    # 1st case
    try: 
        request_UTXOs_url = "/addrs/{}".format(address)

        response = requests.get(block_cypher_url + request_UTXOs_url)

        if response.status_code != 200:
            raise RuntimeError("The server returned an error: {}".format(response.json()))

        schema = 'block_cypher'
    except:
        raise RuntimeError("API Limit reached: {}".format(response.json()))


    # 2nd case
    try: 
        request_UTXOs_url = "/address/{}/unspent-outputs".format(address)
        response = requests.get(block_trail_url + request_UTXOs_url + block_trail_token)

        if response.status_code != 200:
            raise RuntimeError("The server returned an error: {}".format(response.json()))

        schema = 'block_trail'

    except:
        raise RuntimeError("API Limit reached: {}".format(response.json()))    

    return (response, schema)
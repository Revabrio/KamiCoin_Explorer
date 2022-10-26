import json
import config
import requests

def get_num_block_blockchain():
    req = requests.get(config.MINER_NODE_URL + '/block_num')
    return json.loads(req.text)

def get_block_from_blockchain(block_num):
    data = {"block": str(block_num)}
    req = requests.get(config.MINER_NODE_URL + '/block_get', json=data)
    return json.loads(req.text)
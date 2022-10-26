import json
import database
import funtions
from flask import Flask
import hashlib as hasher
from flask import request
from multiprocessing import Process, Pipe

node = Flask(__name__)

def check_new_blocks():
    while True:
        blockchain_num_blocks = int(funtions.get_num_block_blockchain()['blocks_num'])
        if blockchain_num_blocks > database.get_block_num():
            for i in range(database.get_block_num(), blockchain_num_blocks):
                block = funtions.get_block_from_blockchain(i)
                block['data'] = json.loads(block['data'])
                print(f'Обрабатываем блок #{i}, hash - {block["hash"]}')
                transactions = block['data']['transactions']
                for transaction in transactions:
                    if transaction['from'] != 'reward_center':
                        database.update_wallet_balance(transactions['from_address'],
                        float(database.get_wallet_balance(transactions['from_address']))-float(transactions['amount']))
                        wallet_receiver_data = database.get_wallet_balance(transaction['to_address'])
                        if wallet_receiver_data[0] == 0:
                            database.add_new_wallet(transaction['to_address'])
                        database.update_wallet_balance(transaction['to_address'],
                                                       float(database.get_wallet_balance(
                                                           transaction['to_address'])[1]) + float(
                                                           transaction['amount']))
                    else:
                        wallet_receiver_data = database.get_wallet_balance(transaction['to_address'])
                        if wallet_receiver_data[0] == 0:
                            database.add_new_wallet(transaction['to_address'])
                        database.update_wallet_balance(transaction['to_address'],
                                                       float(database.get_wallet_balance(
                                                           transaction['to_address'])[1]) + float(
                                                           transaction['amount']))
                    sha = hasher.sha256()
                    sha.update((str(transaction['datetime'])+str(transaction['from'])+str(transaction['from_address'])+str(transaction['to_address'])+str(transaction['amount'])+str(transaction['signature'])+str(transaction['sig_message'])+str(transaction['message'])).encode('utf-8'))
                    hash_transaction = sha.hexdigest()
                    print(f'Обработали новую транзакцию {hash_transaction}')
                    transaction['hash'] = hash_transaction
                    database.add_transaction(transaction)
                database.add_block(block)

if __name__ == '__main__':
    print('Starting explorer server')

    b, a = Pipe(duplex=True)

    p1 = Process(target=check_new_blocks)
    p1.start()

    #Start server to recieve transactions
    #p2 = Process(target=node.run(host=miner_config.MINER_NODE_IP, port=miner_config.MINER_NODE_PORT), args=(b,))
    #p2.start()
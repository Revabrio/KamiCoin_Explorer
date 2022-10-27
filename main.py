import json
import config
import database
import funtions
from flask import Flask
from flask import request
from multiprocessing import Process, Pipe

explorer = Flask(__name__)

@explorer.route('/wallet_balance', methods=['GET'])
def get_wallet_balance():
    data = request.get_json()
    if data['wallet']:
        balance = database.get_wallet_balance(data['wallet'])
        if balance[0] == 0:
            return json.dumps({data['wallet']: str(0.0)})
        else:
            return json.dumps({data['wallet']: str(balance[1])})

if __name__ == '__main__':
    print('Starting explorer server')

    #b, a = Pipe(duplex=True)

    p1 = Process(target=funtions.check_new_blocks)
    p1.start()

    #Start server to recieve transactions
    p2 = Process(target=explorer.run(host=config.EXPLORER_IP, port=config.EXPLORER_PORT))
    p2.start()
import json
import sqlite3
from config import database_file

def add_block(block_data):
    conn = sqlite3.connect(database_file)
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO blocks (id, timestamp, data, previous_hash, prover, hash) VALUES (?, ?, ?, ?, ?, ?)",
                    (block_data['index'], block_data['timestamp'], json.dumps(block_data['data']),
                     block_data['previous_hash'], block_data['prover'], block_data['hash']))
        conn.commit()
        conn.close()
        return 1
    except:
        conn.close()
        return -1

def add_transaction(transaction):
    conn = sqlite3.connect(database_file)
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO transactions (from_type, from_address, to_address, amount, signature, sig_message, message, hash, timestamp_transaction)"
                    " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (str(transaction['from']), str(transaction['from_address']), str(transaction['to_address']),
                     str(transaction['amount']), str(transaction['signature']), str(transaction['sig_message']),
                     str(transaction['message']), str(transaction['hash']), str(transaction['datetime']),))
        conn.commit()
        conn.close()
        return 1
    except:
        conn.close()
        return -1

def add_new_wallet(wallet_key):
    conn = sqlite3.connect(database_file)
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO wallets (public_key, balance) VALUES (?, ?)", (str(wallet_key), '0.0',))
        conn.commit()
        conn.close()
        return 1
    except:
        conn.close()
        return -1

def get_block_num():
    conn = sqlite3.connect(database_file)
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(id) from blocks")
        row = cur.fetchone()
        return row[0]
    except:
        conn.close()
        return -1

def get_wallet_balance(wallet_key):
    conn = sqlite3.connect(database_file)
    try:
        cur = conn.cursor()
        cur.execute("SELECT balance FROM wallets WHERE public_key = ?", (str(wallet_key),))
        row = cur.fetchone()
        try:
            if row:
                conn.close()
                return 1, row[0]
            else:
                conn.close()
                return 0, 0
        except:
            return 0
    except:
        conn.close()
        return -1

def get_config_data(block_num=-1):
    conn = sqlite3.connect(database_file)
    try:
        cur = conn.cursor()
        if block_num != -1:
            cur.execute("SELECT data FROM config WHERE name = ?", ('block_num',))
            row = cur.fetchone()
        try:
            if row:
                conn.close()
                return row[0]
            else:
                conn.close()
                return 0
        except:
            return 0
    except:
        conn.close()
        return -1

def update_wallet_balance(wallet_key, new_amount):
    conn = sqlite3.connect(database_file)
    try:
        cur = conn.cursor()
        cur.execute("UPDATE wallets SET balance = ? WHERE public_key = ?", (str(new_amount), str(wallet_key),))
        conn.commit()
        conn.close()
        return 1
    except:
        conn.close()
        return -1
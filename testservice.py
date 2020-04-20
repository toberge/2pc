import socket
import sys
from random import randint
import re
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)

ADDRESS = ('', int(sys.argv[1]))
transactions = {}

with socket.create_server(ADDRESS) as server:
    server.listen(1)
    while True:
        conn, remote = server.accept()
        with conn:
            cmd = conn.recv(1024).decode()
            tokens = cmd.split()
            transaction_id = int(tokens[1])
            if tokens[0] == 'prepare':
                logging.log(logging.INFO, f'Preparing {transaction_id}')
                if randint(0,100) == 8:
                    conn.sendall(bytes(f'nope {transaction_id}', 'UTF-8'))
                else:
                    conn.sendall(bytes(f'ready {transaction_id}', 'UTF-8'))
                    transactions[transaction_id] = ' '.join(tokens[2:])
            elif tokens[0] == 'commit':
                logging.log(logging.INFO, f'Committing {transaction_id}')
                print(transactions[transaction_id]) # the "commit"
                if randint(0,5) == 3:
                    conn.sendall(bytes(f'failed {transaction_id}', 'UTF-8'))
                else:
                    conn.sendall(bytes(f'committed {transaction_id}', 'UTF-8'))
            elif tokens[0] == 'rollback':
                logging.log(logging.INFO, f'rolled {transaction_id} the heck back')
                conn.sendall(bytes(f'rolled {transaction_id} the heck back', 'UTF-8'))
            else:
                logging.log(logging.INFO, f'Received strange query')
                conn.sendall(b'what did u ask rly')

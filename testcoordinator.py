import socket
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)

addresses = [('', 8080), ('', 8082)]

logging.log(logging.INFO, 'Starting transaction: Voting phase')
# voting phase
for address in addresses:
    logging.log(logging.INFO, f'Informing {address} to prepare transaction')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(address)
        sock.sendall(b'prepare 42 as a solid state drive')
        #if address[1] == 8080:
        #    sock.sendall(b'hello u shalt commit sudoku')
        #else:
        #    sock.sendall(b'commit plz')
        tokens = str(sock.recv(1024), 'UTF-8').split()
        if tokens[0] != 'ready':
            logging.log(logging.ERROR, f'Transaction 42 aborted!')
            exit(1)

logging.log(logging.INFO, 'Transaction 42: Commit phase')
# commit phase
rollback_flag = False
for address in addresses:
    logging.log(logging.INFO, f'Informing {address} to start commit')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(address)
        sock.sendall(b'commit 42 so I can get home!')
        tokens = str(sock.recv(1024), 'UTF-8').split()
        if tokens[0] != 'committed':
            logging.log(logging.ERROR, f'Transaction 42 failed! rolling back!')
            rollback_flag = True
            break
else:
    logging.log(logging.INFO, f'Transaction 42 succeeded!')

if rollback_flag:
    for address in addresses:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(address)
            sock.sendall(b'rollback 42 or get sick')
            tokens = str(sock.recv(1024), 'UTF-8').split()
            if tokens[0] != 'rolled':
                logging.log(logging.ERROR, f'Transaction 42 failed to roll back!')


import socket
import sys
import logging
import pickle
import message as msg
from model.event import *
import model.event
from model.warehouse import Warehouse, Item

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)

ADDRESS = ('', int(sys.argv[2]))
transactions = {}
warehouse = Warehouse(sys.argv[1])

def prepare(message) -> msg.Message:
    event = message.event
    print(event)
    # OKAY OH WELL
    event = TransferEvent('A', 'B', Item('stonk', 9000))
    if isinstance(event, TransferEvent):
        item: Item = event.item
        if event.source == warehouse.name:
            our_item = warehouse.get_item(item.name)
            if our_item:
                if our_item.amount >= item.amount:
                    return msg.StatusMessage('ok we can give dis', message.id, True)
                else:
                    return msg.StatusMessage('not enough left', message.id, False)
            else:
                return msg.StatusMessage('not in stock', message.id, False)
        elif event.destination == warehouse.name:
            return msg.StatusMessage('ok we\'ll see', message.id, True)
        else:
            return msg.StatusMessage('I am not involved', message.id, False)
    else: return msg.StatusMessage('wtf', message.id, False)

def commit(message) -> msg.Message:
    if not message.id in transactions:
        logging.error(f'Unknown transaction {message.id}')
        return msg.StatusMessage('yolo nope', message.id, False)
    else:
        return msg.StatusMessage('eeeh', message.id, True)

def handle_transaction_stage(conn: socket.socket, message: msg.TransactionMessage):
    response = msg.Message('uhhhh', 'idk')
    try:
        response = prepare(message)
    except KeyError as e:
        logging.error(f'stuff {message.id} and {e}')
        response = msg.StatusMessage('nope', message.id, False)
        #logging.error(f'Unknown transaction {message.id}')
        #response = msg.StatusMessage('yolo nope', message.id, False)
        
    conn.sendall(pickle.dumps(response))

with socket.create_server(ADDRESS) as server:
    server.listen(1)
    while True:
        conn, remote = server.accept()
        with conn:
            message = pickle.loads(conn.recv(1024))
            if isinstance(message, msg.TransactionMessage):
                handle_transaction_stage(conn, message)
            else:
                conn.sendall(pickle.dumps(msg.StatusMessage('what', -1, False)))

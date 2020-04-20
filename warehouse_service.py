import socket
import sys
import logging
import pickle
from event import *
from model.warehouse import Warehouse, Item

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s'
)

ADDRESS = ('', int(sys.argv[2]))
transactions = {}
warehouse = Warehouse(sys.argv[1])
warehouse.add_item(Item('stonk', 9000, 255))

def prepare(event) -> Response:
    # OKAY OH WELL
    if isinstance(event, TransferEvent):
        item: Item = event.item
        if event.source == warehouse.name:
            our_item = warehouse.get_item(item.name)
            if our_item:
                if our_item.amount >= item.amount:
                    logging.debug(f'We have {our_item} and shall subtract {item}')
                    return Response(OK, 'ok we can give dis')
                else:
                    return Response(ERROR, 'not enough left')
            else:
                return Response(INVALID, 'not in stock')
        elif event.destination == warehouse.name:
            logging.debug(f'yeah ok sure, we have {warehouse.get_item(item.name)}')
            return Response(OK, 'ok we\'ll see')
        else:
            return Response(INVALID, 'I am not involved')
    else: return Response(INVALID, 'wtf')

def commit(event: Event) -> Response:
    if isinstance(event, TransferEvent):
        item = event.item
        if event.source == warehouse.name:
            our_item = warehouse.get_item(item.name)
            if our_item:
                if our_item.amount >= item.amount:
                    our_item.amount -= item.amount
                    logging.debug(f'there is now {our_item}')
                    return Response(OK, 'ok it is given')
                else:
                    return Response(ERROR, 'not enough left')
            else:
                return Response(INVALID, 'not in stock')
        elif event.destination == warehouse.name:
            warehouse.add_item(item)
            logging.debug(f'there is now {warehouse.get_item(item.name)}')
            return Response(OK, 'i got it!')
        else:
            return Response(INVALID, 'I am not involved')

def rollback(event: Event) -> Response:
    if isinstance(event,TransferEvent):
        item = event.item
        our_item = warehouse.get_item(item.name)
        if not our_item:
            return Response(INVALID, 'not in stock')
        
        if event.source == warehouse.name:
            warehouse.add_item(item)
            logging.debug(f'rollback: there is now {our_item}')
            return Response(OK, 'got it back')
        elif event.destination == warehouse.name:
            if warehouse.subtract_item(item):
                logging.debug(f'rollback: there is now {our_item}')
                return Response(OK, 'removed it')
            else:
                return Response(INVALID, 'cannot subtract that')
        else:
            return Response(INVALID, 'I am not involved')

def abort(event: Event) -> Response:
    # only relevant once there's some action log...
    return Response(OK, 'i guess it won\'t happen then')

that_map = {
    PREPARE: prepare,
    COMMIT: commit,
    ROLLBACK: rollback,
    ABORT: abort
}

def handle_transaction_stage(conn: socket.socket, message: Event):
    response = Response(FAILURE, 'idk')
    try:
        response = that_map[message.state](message)
    except KeyError as e:
        logging.error(f'stuff {message.id} and {e}')
        response = Response(FAILURE, 'Invalid message')
        
    conn.sendall(pickle.dumps(response))

with socket.create_server(ADDRESS) as server:
    server.listen(1)
    while True:
        conn, remote = server.accept()
        with conn:
            message = pickle.loads(conn.recv(4096))
            if isinstance(message, Event):
                handle_transaction_stage(conn, message)
            else:
                conn.sendall(pickle.dumps(Response(INVALID, 'not an event...')))

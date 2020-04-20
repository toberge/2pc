from model.warehouse import Item, Warehouse
from model.event import *
import logging
import socket
import pickle
from message import StatusMessage, TransactionMessage
import message as msg

warehouse_addresses = {
    'A': ('', 8080),
    'B': ('', 8082)
}

ledger_address = ('', 8090)

class Coordinator:
    def __init__(self):
        pass

    def listen(self, address: (str, int)):
        """Start listening on a specified address (ip, port)"""
        pass
    
    def handle_transaction(self, event: Event):
        if (
            event.type == 'transfer' 
            and event.source in warehouse_addresses
            and event.destination in warehouse_addresses
        ):
            transaction = Transaction(event, [
                warehouse_addresses[event.source],
                warehouse_addresses[event.destination],
                ledger_address
            ])
        elif event.type == 'loss' or event.type == 'gain':
            transaction = Transaction(event, [ledger_address])
        else:
            logging.error('Got invalid transaction request')
            return

        logging.info(f'~ {transaction} stage 1: Telling parties to please prepare')
        if transaction.start_preparation():
            logging.info(f'~ {transaction} stage 2: All parties ready')
            if transaction.start_commit():
                logging.info(f'~ {transaction} complete')
            else:
                logging.error(f'~ {transaction} stage 2: Rolling back')
                transaction.start_rollback()
        else:
            logging.error(f'~ {transaction} stage 1: Failed initiating')
            transaction.notify_failure()        

class Transaction:
    _id = 1
    def __init__(self, event: Event, parties):
        self.parties = parties
        self.event = event
        self.id = Transaction._id
        Transaction._id += 1
        self.processed_parties = [] # must be notfied at rollback
    
    def _run_around(self, context: str) -> bool:
        if self.event.state in {PREPARE, COMMIT}:
            self.processed_parties = []
            parties = self.parties
            append = True
        else: # rollback or abort
            parties = self.processed_parties
            append = False
        
        for address in parties:
            logging.info(context.format(address))
            if append: self.processed_parties.append(address)
            if address[1] == 8090:
                print('no')
                continue # skip ledger for now
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(address)
                sock.sendall(pickle.dumps(self.event))
                response: Response = pickle.loads(sock.recv(4096))
                if not response.code == OK:
                    logging.error(f'Failure at {address} because "{response.reason}"')
                    return False
            
        return True

    def start_preparation(self) -> bool:
        """Notify involved services about the upcoming transaction
        and ask if they are ready"""
        return self._run_around('Informing {} to prepare transaction')
        
    def notify_failure(self):
        """Notify all parties about a failure"""
        self.event.state = ABORT
        return self._run_around('Notifying {} about the failure')

    def start_commit(self) -> bool:
        """Notify involved parties that the transaction can proceed"""
        self.event.state = COMMIT
        return self._run_around('Commanding {} to commit')
    
    def start_rollback(self) -> bool:
        """Notify parties that a rollback should happen"""
        self.event.state = ROLLBACK
        return self._run_around('Commanding {} to roll back')

    def __str__(self):
        return f'transaction {self.id}'

import logging

if __name__ == '__main__':
    logging.basicConfig(
        #filename='logs/the_log.log',
        level=logging.DEBUG,
        #handlers=[hello],
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    logging.debug('hello')
    coordinator = Coordinator()
    coordinator.listen(('', 3000))
    coordinator.handle_transaction(
        TransferEvent('B', 'A', Item('stonk', 9000, 50))
    )

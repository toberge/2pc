class Coordinator:
    def __init__(self):
        pass

    def listen(self, address):
        """Start listening on a specified address (ip, port)"""
        pass

class Transaction:

    def __init__(self, parties):
        self.parties = parties
        self.done_parties = [] # must be notfied at rollback
    
    def notify_parties(self):
        """Notify involved services about the upcoming transaction
        and ask if they are ready"""
        pass

    def start_commit(self):
        """Notify involved parties that the transaction can proceed"""
        pass
    
    def start_rollback(self):
        """Notify parties that a rollback should happen"""
        pass

import logging

if __name__ == '__main__':
    logging.basicConfig(
        #filename='logs/the_log.log',
        level=logging.DEBUG,
        #handlers=[hello],
        format='%(asctime)s %(levelname)s:%(message)s'
    )
    logging.info('hi there')
    logging.debug('hello')

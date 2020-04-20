import json

class Message:
    """Base class for messages transmitted between parties"""
    def __init__(self, message, _type):
        self.message = message
        self.type = _type

class Transfer(Message):
    """Transfer item from A to B"""
    def __init__(self, message, source, destination, itemname):
        super().__init__(message, 'transfer')
        self.source = source
        self.destination = destination
        self.item = itemname

class Status(Message):
    """Status of tansaction, sent from one party"""
    def __init__(self, message, transactionid, success: bool):
        super().__init__(message, 'status')
        self.transactionid = transactionid
        self.success = success

class TransactionMessage(Message):
    """Sent from coordinator to parties"""
    def __init__(self, message, transactionid, event, command):
        super().__init__(message, 'prepare')
        self.id = transactionid
        self.event = event
        self.command = command

class Command:
    """very stupid idea"""
    PREPARE = 1
    COMMIT = 2
    RELAX = -1
    ROLLBACK = -2

TYPE_MAP = {
    'transfer': lambda d: Transfer(d['message'], d['source'], d['destination'], d['item'])
}

def loads(string) -> Message:
    """Parse message from JSON"""
    d = json.loads(string)
    if d['type'] and d['type'] in TYPE_MAP:
        return TYPE_MAP[d['type']](d)
    else:
        return None

def dumps(message: Message) -> str:
    """Serialize message to JSON"""
    if message.type == 'transfer':
        return json.dumps(message.__dict__)


if __name__ == '__main__':
    msg = Transfer('hi', '234', '5678', 'socks')
    print(loads(dumps(msg)))
    help(Transfer)
  

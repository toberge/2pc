from model.warehouse import Item, Warehouse
import logging

OK = 0
INVALID = 1
ERROR = 4
FAILURE = 2
IS_DOWN = 3

class Response:
    """Responses from services during transaction"""
    def __init__(self, code: int, reason: str):
        self.code = code
        self.reason = reason

PREPARE = 1
COMMIT = 2
ABORT = -1
ROLLBACK = -2

class Event:
    """Base class for events; they always deal with an item"""
    def __init__(self, _type, item: Item):
        self.type = _type
        self.state = PREPARE
        self.item = item
        #self.id = -1
    
    def perform(self, warehouse: Warehouse) -> Response:
        raise NotImplementedError()
    
    def revert(self, warehouse: Warehouse) -> Response:
        raise NotImplementedError()
    
    def __str__(self):
        return f'base event {self.type}; this should not happen'

class LossEvent(Event):
    """The case of an item being lost in transit between two warehouses"""
    def __init__(self, subject: str, item: Item):
        super().__init__('loss', item)
        self.subject = subject

    def __str__(self):
        return f'Package of {self.item} lost in transit'

class GainEvent(Event):
    """The case of receiving an amount of an item"""
    def __init__(self, subject: str, item: Item):
        super().__init__('gain', item)
        self.subject = subject

    def __str__(self):
        return f'Package of {self.item} received'

class TransferEvent(Event):
    """Transfer of an item between two warehouses, identified by name"""
    def __init__(self, source: str, destination: str, item: Item):
        super().__init__('transfer', item)
        self.source = source
        self.destination = destination
    
    def __str__(self):
        return f'Transfer of {self.item} from {self.source} to {self.destination}'

from warehouse import Item

class Event:

    def __init__(self, _type):
        self.type = _type

class LossEvent(Event):
    """The case of an item being lost in transit between two warehouses"""
    def __init__(self, item: Item):
        super().__init__('loss')
        self.item = item

    def __str__(self):
        return f'Package of {self.item} lost in transit'

class GainEvent(Event):
    """The case of receiving an amount of an item"""
    def __init__(self, item: Item):
        super().__init__('loss')
        self.item = item

    def __str__(self):
        return f'Package of {self.item} received'

class TransferEvent(Event):
    """Transfer of an item between two warehouses, identified by ID"""
    def __init__(self, source: str, destination: str, item: Item):
        super().__init__('transfer')
        self.source = source
        self.destination = destination
        self.item = item


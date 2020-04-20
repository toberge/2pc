class Item:
    _id = 0
    """henlo"""
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.amount = 1
        self.id = Item._id
        Item._id += 1

class Warehouse:
    """henlo"""
    def __init__(self, name: str):
        self.name = name
        self.items = {}
    
    def add_item(self, item: Item):
        if not self.items.get(item.id):
            self.items[item.id] = item
        else:
            self.items[item.id].amount += 1

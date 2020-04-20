class Item:
    """simple class for item in warehouse"""
    _id = 0
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.amount = 1
        self.id = Item._id
        Item._id += 1
    
    @classmethod
    def copyof(cls, item, amount):
        copy = cls(item.name, item.value)
        copy.id = item.id
        copy.amount = amount
        return copy
    
    def _plurality(self):
        return 's' if self.amount > 1 else ''
    
    def __str__(self):
        return f'{self.amount} {self.name}{self._plurality()}'

class Warehouse:
    """a warehouse, goddamn it"""
    def __init__(self, name: str):
        self.name = name
        self.items = {}
    
    def add_item(self, item: Item):
        if not self.items.get(item.id):
            self.items[item.id] = item
        else:
            self.items[item.id].amount += 1
    
    def get_item(self, _id):
        item = self.items.get(_id)
        return item

if __name__ == "__main__":
    item = Item('shoe', 22)
    print(str(item))
    item.amount = 22
    print(str(item))
    print(str(Item.copyof(item, 3)))

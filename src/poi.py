from item import Item, ItemType


class POI():

    def __init__(self, name: str, description: str, location: tuple[int, int], items: list[Item], is_open: bool = True):
        self.name = name
        self.description = description
        self.location = location
        self.items = items
        self.is_open = is_open

    def to_string(self):
        return f"Name: {self.name}, Description: {self.description}, Location: {self.location[0]} miles North by {self.location[1]} miles East, \
        Items: {", ".join(map(Item.to_string, self.items))}, Open/Closed: {self.is_open}"
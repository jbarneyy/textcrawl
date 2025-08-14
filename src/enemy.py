from item import Item
from poi import POI

class Enemy():

    def __init__(self, name: str, health: int, defence: int, items: list[Item] | None, level: int, current_POI: POI):
        self.name = name
        self.health = health
        self.defence = defence
        self.items = items
        self.level = level
        self.current_POI = current_POI

    
    def to_string(self):
        return f"Enemy: {self.name}, Health: {self.health}, Defence: {self.defence}, Level: {self.level}, Current POI: {self.current_POI.name}"
    

    
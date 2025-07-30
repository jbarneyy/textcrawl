
class POI():

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def to_string(self):
        return f"Name: {self.name}, Description: {self.description}"
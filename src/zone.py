from poi import POI


class Zone():

    def __init__(self, name: str, points_of_interest: list[POI], description: str):
        self.name = name
        self.points_of_interest = points_of_interest
        self.description = description

    def to_string(self):
        return f"Zone: {self.name}, Description: {self.description}"
    
from poi import POI

class Zone():

    def __init__(self, name: str, points_of_interest: list[POI]):
        self.name = name
        self.points_of_interest = points_of_interest
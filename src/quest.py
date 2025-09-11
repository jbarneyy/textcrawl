

class Quest():

    def __init__(self, name: str, description: str, objectives: list[str], is_complete: bool = False, is_active: bool = False):
        self.name = name
        self.description = description
        self.objectives = objectives
        self.is_complete = is_complete
        self.is_active = is_active

    
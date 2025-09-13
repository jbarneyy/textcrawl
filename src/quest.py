
class Quest():

    def __init__(self, name: str, description: str, objective: str, is_complete: bool = False):
        self.name = name
        self.description = description
        self.objective = objective
        self.is_complete = is_complete

    def to_string(self):
        return f"Quest: {self.name} - Description: {self.description} - Objective: {self.objective}"
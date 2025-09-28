from typing import Callable

class Quest():

    def __init__(self, name: str, description: str, accept_message: str, check_complete: Callable, is_complete: bool, xp_reward: int, complete_message: str):
        self.name = name
        self.description = description
        self.accept_message = accept_message
        self.check_complete = check_complete
        self.is_complete = is_complete
        self.complete_message = complete_message

        self.xp_reward = xp_reward

    def to_string(self):
        return f"Quest: {self.name} - Description: {self.description} - Completed: {self.is_complete}"
    
    def update(self, player, gamestate):
        if self.check_complete(player, gamestate) is True:
            self.is_complete = True

            print(self.complete_message)
            print(f"Congratulations! You have completed a quest: {self.name}! You gain {self.xp_reward} experience!")
            return True
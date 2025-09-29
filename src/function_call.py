import sys
import time

from google.genai import types
from player import Player
from gamestate import GameState


def slow_print_text(text: str, delay: float = 0.03):
    for char in text:
        # Writes single character to stdout. #
        sys.stdout.write(char)

        # Flushes stdout's buffer to the CLI, without this it would build text and return at end. #
        sys.stdout.flush()

        # Delays next action by float (delay) seconds. #
        time.sleep(delay)
    
    sys.stdout.write("\n")


def call_function(function: types.FunctionCall, player: Player, game_state: GameState):
    function_args = function.args
    function_name = function.name

    #print("Inside CALL_FUNCTION")

    """
    Function call for Player() grab_item. If grab_item() is True will grab item and return.

    If grab_item() is False will not call grab_item().
    """
    if (function_name == "grab_item"):
        target_item_name = function_args["Name"]
        target_item = game_state.items[target_item_name]

        result = player.grab_item(target_item)

        if (result is True):
            game_state.update_gamestate()
            return f"{player.name} grabs {target_item_name}."
        else:
            return f"{player.name} cannot pickup {target_item_name}."
        

    """
    Function call for Player() list_items. Will always evaluate to True and will return list of Player's equipment, inventory, and quests.
    """
    if (function_name == "list_items"):
        game_state.update_gamestate()
        return player.list_items()
    
    
    """
    Function call for Player() move(). If Player() can move to listed POI will move Player().

    If Player() cannot move to requested POI will not move Player().
    """
    if (function_name == "move"):
        target_poi_name = function_args["Name"]

        result = player.move(target_location=game_state.pois[target_poi_name])

        if result is True:
            game_state.update_gamestate()
            return f"{player.name} moves to {player.current_POI.name}"
        else:
            return f"{player.name} is unable to go there at this time."
        
    
    """
    Function call for Player() equip_item. If Item() is in Player() inventory and can_equip, will equip item and swap with inventory slot.
    """
    if (function_name == "equip_item"):
        target_item_name = function_args["Name"]

        result = player.equip_item(item_name=target_item_name)

        if (result is True):
            game_state.update_gamestate()
            return f"{player.name} equips {target_item_name}."
        else:
            return f"{player.name} is unable to equip that."
        

    """
    Function call for GameState() attack_enemy(). If enemy is in same POI as Player() will start attack dialogue.

    Continue attack dialogue until Player() flees or completes battle.
    """
    if (function_name == "attack_enemy"):
        
        target_enemy_name = function_args["Name"]
        target_enemy = game_state.enemies[target_enemy_name]


        while True:
            print(f"{player.name} HP: {player.health} is battling {target_enemy.name} HP: {target_enemy.health}")
            print("1) Attack or 2) Run" + "\n")
            player_response = input("> ")

            if player_response not in ["1", "2"]:
                print(f"I'm sorry {player.name}, that is not an option.\n")
                continue

            if (player_response == "2"):
                return f"You flee from the {target_enemy.name} with shame."

            print(game_state.attack_enemy(player, target_enemy) + "\n")
            game_state.update_gamestate()

            if (player.health <= 0):
                return "You have been defeated."

            if (target_enemy.health <= 0):
                print(f"{player.name} has defeated {target_enemy.name}!\nYou have gained {target_enemy.xp_reward} experience!")

                did_player_levelup: bool = player.gain_xp(target_enemy.xp_reward)

                if (did_player_levelup):
                    print(f"Congratulations! You have gained a level! You are now level: {player.level}.")

                if (target_enemy.items is not None):
                    dropped_items = ""
                    for item in target_enemy.items:
                        player.items.append(item)
                        dropped_items += f"{item.name}, "
                
                    print(f"You take {dropped_items.rstrip(", ")} from {target_enemy.name}.")
                
                del game_state.enemies[target_enemy.name]
                game_state.update_gamestate()
                
                return f"Well fought."
            
            
    if (function_name == "trade"):
        character_name = function_args["Name"]
        character = game_state.characters[character_name]

        if (player.current_POI is not character.current_POI):
            return f"{character.name} is not anywhere nearby."
        
        else:
            print(f"Trading with {character.name}\n")

            player_inventory = ""
            for item in player.items:
                player_inventory += f"{item.name} - {item.description} -  {item.value} Gold\n"
            player_inventory = player_inventory.rstrip("\n")

            character_inventory = ""
            for item in character.items:
                character_inventory += f"{item.name} - {item.description} - {item.value} Gold\n"
            character_inventory = character_inventory.rstrip("\n")

            print(f"{player.name} Inventory:\n{player_inventory}\n")
            print(f"{character.name} Inventory:\n{character_inventory}\n")

            while True:
                is_buying = None

                print("Would you like to 1) Buy / 2) Sell / 3) Exit?\n")
                player_input = input("> ")

                if player_input not in ["1", "2", "3", "Buy", "Sell", "Exit", "buy", "sell", "exit"]:
                    print("Please select valid input.\n")
                    continue

                if player_input in ["3", "Exit", "exit"]:
                    return f"You finish trading with {character.name}."
                
                if player_input in ["1", "Buy", "buy"]:
                    is_buying = True
                    print("What item would you like to buy?\n")

                if player_input in ["2", "Sell", "sell"]:
                    is_buying = False
                    print("What item would you like to sell?\n")
                
                item_name = input("> ")

                if (item_name not in game_state.items):
                    print("Please enter valid item name with correct casing.\n")
                    continue

                return_string = game_state.trade(character, item_name, is_buying)
                game_state.update_gamestate()

                print(return_string + "\n")


    if (function_name == "accept_quest"):
        character_name = function_args["Name"]
        character = game_state.characters[character_name]
        quest = character.quests[0]

        if quest is None:
            return f"{character.name} does not have any quests for you at this moment."
        
        return_string = game_state.accept_quest(character)
        game_state.update_gamestate()

        return return_string
    

    if (function_name == "use_item"):
        item_name = function_args["Name"]
        item = game_state.items[item_name]

        return player.use_item(item)
    
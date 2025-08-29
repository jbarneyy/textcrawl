from google.genai import types

schema_grab_item = types.FunctionDeclaration(
    name="grab_item",
    description="Grab/pickup an item from the player/character's current POI and place it into character's inventory. Only call function if player explicitly commands 'grab' or 'pickup'.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "grab": types.Schema(
                type=types.Type.STRING,
                description="String representing the Item.name of the item player attempts to grab.",
            ),
        },
        required=["grab"]
    ),
)

schema_list_items = types.FunctionDeclaration(
    name="list_items",
    description="List/display/show character's inventory. Only call when 'inventory' keyword is passed. Function will return a formatted string displaying the character's inventory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={},
        required=[]
    ),
)

# schema_move = types.FunctionDeclaration(
#     name="move",
#     description=(
#         "Move character from current POI to another POI. "
#         "Only call if player explicitly commands 'move', 'go', or 'travel'. "
#         "Always set target_location to the EXACT string name of the POI. "
#     ),
#     parameters=types.Schema(
#         type=types.Type.OBJECT,
#         properties={
#             "target_location": types.Schema(
#                 type=types.Type.OBJECT,
#                 description="Name of POI / Point of Interest that character is attempting to move to.",
#                 properties={
#                     "Name": types.Schema(type=types.Type.STRING, description="Name of target POI / Point of Interest.")
#                 },
#                 required=["Name"]
#             )
#         },
#         required=["target_location"]
#     )
# )

schema_move = types.FunctionDeclaration(
    name="move",
    description=(
        "Move character from current POI to another POI. "
        "Only call if player explicitly commands 'move', 'go', or 'travel'. "
        "Always set target_location to the EXACT string name of the POI. "
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "Name": types.Schema(
                type=types.Type.STRING,
                description="Name of POI / Point of Interest that character is attempting to move to.",
            )
        },
        required=["Name"]
    )
)

schema_equip_item = types.FunctionDeclaration(
    name="equip_item",
    description="Equip an item from the player's inventory into either player's armor var or player's weapon var. Item must be in inventory and of ItemType.WEAPON or ItemType.ARMOR. Only call if player explicity commands 'equip'." \
    "If an item is already equipped, it will move the current equip into player's inventory. Returns True if item is successfully equipped to player.armor or player.weapon. False if equip is unsuccessful.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "item_name": types.Schema(
                type=types.Type.STRING,
                description="String representing the name of the item (Item.name) that player is attempting to equip.",
            ),
        },
        required=["item_name"]
    ),
)

schema_attack_enemy = types.FunctionDeclaration(
    name="attack_enemy",
    description="Attack an enemy if player and enemy are in the same POI. Rolls one attack round of player attacking enemy and enemy attacking player. Only call if player explicity commands 'attack' or 'fight' or 'battle'.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "player": types.Schema(
                type=types.Type.OBJECT,
                description="Player object representing our player from class Player()"
            ),
            "enemy": types.Schema(
                type=types.Type.OBJECT,
                description="Enemy object representing the Enemy() our player is attacking.",
                properties={
                    "Name": types.Schema(type=types.Type.STRING, description="Name of the enemy.")
                },
                required=["Name"]
            )
        },
        required=["player", "enemy"]
    )
)

schema_get_nearby_pois = types.FunctionDeclaration(
    name="get_nearby_pois",
    description="Only call function when Player requests information on nearby areas. Player could ask what villages/places/areas/towns/locations are nearby or when Player asks where they can travel or go to.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={},
        required=[]
    )
)

# Must wrap function declaration schemes as a types.Tool to pass in as list[Tool] to client config. #
available_functions = types.Tool(
    function_declarations=[
        schema_grab_item,
        schema_list_items,
        schema_move,
        schema_equip_item,
        schema_attack_enemy
    ]
)
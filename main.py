import os
import time
from weapons import *
from characters import *
from armour import *
from map import *

# keeps track of the game's run status
run = False

# keeps track of the player's weapons
weapon_inventory = [fists]

# keeps track of the player's armour
armour_inventory = [clothes]

# keeps track of the player's current location
current_area = all_areas["Short Grasslands"]

# displays a list of game commands
def commands():
    print(f"\nAvailable Commands:")
    print("-" * 90)
    print(f"{'go <direction>': <20} | {'Move in a direction (e.g. go north)': <90}")
    print(f"-" * 90)
    print(f"{'pick up <item>': <20} | {'Pick up an item in the current area (e.g. pick up bone)': <90}")
    print(f"-" * 90)
    print(f"{'show weapons': <20} | {'Displays weapons in you inventory': <90}")
    print(f"-" * 90)
    print(f"{'show armour': <20} | {'Displays armour in your inventory': <90}")
    print(f"-" * 90)
    print(f"{'equip weapon': <20} | {'Equip a weapon by its code (e.g.equip weapon 0)': <90}")
    print(f"-" * 90)
    print(f"{'equip armour': <20} | {'Equip armour by its code (e.g. equip armour 0)': <90}")
    print(f"-" * 90)
    print(f"{'status': <20} | {'Display your current status, including HP, weapon, and armour': <90}")
    print(f"-" * 90)
    print(f"{'commands': <20} | {'Show this list of commands': <90}")
    print(f"-" * 90)

# =======================================
# Displays current area and moves
# =======================================
def status():
    moves = current_area.exits.keys()   # list of all possible exits (actions)

    # Centred title with area name
    print(f"Current Location: {current_area.name}".center(len(current_area.description) + 10))
    print("-----" + "-" * len(current_area.description) + "-----")

    # Area description
    print(f"{current_area.description}".center(len(current_area.description) + 10))
    print("-----" + "-" * len(current_area.description) + "-----")

    # Available moves
    print("Available Moves:".center(len(current_area.description) + 10))
    for move in moves:
        print(f"{move.title()}".center(len(current_area.description) + 10))
    print("-----" + "-" * len(current_area.description) + "-----")

    # Items in area (if any)
    if current_area.item:
        print(f"Item here: {current_area.item.name}".center(len(current_area.description) + 10))
        print(f"Description: {current_area.item.description}".center(len(current_area.description) + 10))
    else:
        print("No items here".center(len(current_area.description) + 10))
    print("-----" + "-" * len(current_area.description) + "-----")
    print("Use 'commands' to see available commands".center(len(current_area.description) + 10))
    print("-----" + "-" * len(current_area.description) + "-----")



# ========================================
# Display weapon inventory
# ========================================
def display_weapons():
    print("\nWeapons:")
    print("-" * 120)
    print(f"{' Code': <5} | {'Name': <20} | {'Stats': <25} | Description")
    print("-" * 120)
    for item in weapon_inventory:
        stats = []       # collect stats in a list for each weapon

        # Check if the item has specific attributes and append them to the stats list
        if hasattr(item, "min_damage"):
            stats.append(f"Damage: {item.min_damage} - {item.max_damage}")

        if hasattr(item, "min_special"):
            stats.append(f"Special: {item.min_special} - {item.max_special}")
            
        if hasattr(item, "crit_ch"):
            stats.append(f"Crit Chance: {item.crit_ch}%")

        if hasattr(item, "inflict_min_sickness"):
            stats.append(f"Sickness: {item.inflict_min_sickness} - {item.inflict_max_sickness}")
        
        # Get the index of the item in the inventory to be used for equipping
        code = weapon_inventory.index(item)     

        # Print weapon info (first stat inline)
        print(f"{str(code).center(5): <5} | {item.name: <20} | {stats[0]: <25} | {item.description}")

        # Print remaining stats underneath with other columns empty
        for stat in stats[1:]:
            print(f"{'': <5} | {'': <20} | {stat: <25} |")
        print("-" * 120)


# ========================================
# Display armour inventory
# ========================================
def display_armour():
    print("\nArmour:")
    print("-" * 120)
    print(f"{'Code': <5} | {'Name': <20} | {'Stats': <25} | Description")
    print("-" * 120)
    for item in armour_inventory:
        stats = []      # collect stats in a list for armour

        # Check and append stats
        if hasattr(item, "hp"):
            stats.append(f"HP: {item.hp}")

        if hasattr(item, "agility"):
            stats.append(f"Agility: {item.agility}")
            
        if hasattr(item, "damage_reduction"):
            stats.append(f"Damage Reduction: {int(item.damage_reduction * 100)}%")
        
        code = armour_inventory.index(item)

        # Print armour info
        print(f"{str(code).center(5): <5} | {item.name: <20} | {stats[0]: <25} | {item.description}")
        for stat in stats[1:]:
            print(f"{'': <5} | {'': <20} | {stat: <25} |")
        print("-" * 120)


# ========================================
# Display enemy information
# ========================================
def display_enemy(enemy):
    print("-" * 50)
    print(f"Enemy: {enemy.name} (Group of {enemy.current_group_size})".center(50))
    print("-" * 50)
    print(f"HP: {enemy.hp}")
    print(f"Agility: {enemy.agility}")
    print(f"-" * 50)

    print(f"Attack: {enemy.min_damage} - {enemy.max_damage}")
    if enemy.crit_ch > 0:
        print(f"Crit Chance: {enemy.crit_ch}%")

    if enemy.inflict_min_sickness > 0:
        print(f"Poison: {enemy.inflict_min_sickness} - {enemy.inflict_max_sickness}")
    print("-" * 50)


# ========================================
# Display player information
# ========================================
def display_player():
    print("-" * 40)
    print(f"Player: {player.name}")
    print("-" * 40)
    print(f"HP: {player.hp}")
    print(f"Agility: {player.agility}")
    print(f"-" * 40)

    # Equipped weapon info
    print(f"Weapon: {player.weapon.name}")
    print(f"Damage: {player.weapon.min_damage} - {player.weapon.max_damage}")
    if hasattr(player.weapon, "crit_ch"):
        print(f"Crit Chance: {player.weapon.crit_ch}%")

    if hasattr(player.weapon, "inflict_min_sickness"):
        print(f"Poison: {player.weapon.inflict_min_sickness} - {player.weapon.inflict_max_sickness}")
    print("-" * 40)

    # Equipped armour info
    print(f"Armour: {player.armour.name}")
    print(f"HP Bonus: {player.armour.hp}")
    print(f"Agility Bonus: {player.armour.agility}")
    print(f"Damage Reduction: {int(player.armour.damage_reduction * 100)}%")
    print("-" * 40)


# ========================================
# Item pick up
# ========================================
def check_item():
    """
    Checks if there is an item in the current area
    If there is an item and no enemy, it allows the player to pick it up
    If there is an enemy, it informs the player that they cannot pick up items while in combat
    If the area is already complete, it informs the player that there are no items to pick up
    """
    if current_area.enemy == None and current_area.item != None:
        pick_up(current_area.item)      # pick up the item
        current_area.item = None
    elif current_area.enemy != None:
        print("You can't pick up items while in combat!")
    elif current_area.complete:
        print("You have already completed this area, no items to pick up.")
    else:
        print("There are no items to pick up in this area.")


def pick_up(item):
    """
    Adds an item to the relevant inventory (weapon or armour)
    But only if it is not already in the inventory
    """
    global weapon_inventory     
    global armour_inventory

    # Prevents duplicates
    if item not in weapon_inventory or armour_inventory:
        # Check if the item is a weapon or armour (not weapon) and add it to the respective inventory
        if isinstance(item, Weapon):
            weapon_inventory.append(item)
        else:
            armour_inventory.append(item)

    print(f"You have picked up {item.name}")


# ========================================
# Player's turn in battle
# ========================================
def turn(hero, enemy):
    hero.defend = False
    prompt = input("Do you want to defend or attack? ").lower().strip()   
    if len(prompt) == 0:      # empty input
        print("Please enter a command")
        turn(hero, enemy)      # recalls the function
    else:
        if prompt == "defend":
            hero.defend = True
        elif prompt == "attack":
            hero.attack(enemy)
        else:
            print("Invalid option! Choose to either attack or defend")
            turn(hero, enemy)       

# ========================================
# Check for enemy and handle battle
# ========================================
def check_enemy(enemy):
    if current_area.enemy:      # if enemy exists, start battle
            battle(player, current_area.enemy)
    else:
        pass    # no enemy, do nothing


def battle(hero, enemy):
    global run      # to update the run variable and exit the game if player is defeated
    while hero.hp > 0 and enemy.hp > 0:
        os.system("cls")        # clear the console for a clean battle display
        print(f"A wild {enemy.name} appears!")
        display_enemy(enemy)

        print("\nYour Turn:")
        turn(hero, enemy)

        # Check if enemy was defeated before its turn
        if current_area.enemy.hp <= 0:
            print(f"{current_area.enemy.name} has been defeated!")
            player.hp = player.armour.hp  # restore player's HP after defeating an enemy
            current_area.enemy = None
            input("Press enter to continue...")
            return
        
        print("\nEnemy Turn:")
        enemy.attack(hero)

        # Check if player is defeated
        if player.hp <= 0:
            print("You have been defeated! Game Over!")
            display_player()
            run = False     # ends the main game loop, exitting the game when the player is defeated
        input("Press enter to continue...")


# ========================================
# Equipping items
# ========================================
def equip_weapon(code):
    if code in range(len(weapon_inventory)):
        player.weapon = weapon_inventory[code]
        player.crit_ch = player.weapon.crit_ch      # update player's crit chance based on the equipped weapon
        print(f"You have equipped {player.weapon.name} as your weapon")
    else:
        print("Please provide a valid code for the weapon you want to equip")
    display_player()


def equip_armour(code):
    if code in range(len(armour_inventory)):
        player.armour = armour_inventory[code] 
        player.hp = player.armour.hp                # update player's HP based on the equipped armour
        player.agility = player.armour.agility      # update player's agility based on the equipped armour
        print(f"You have equipped {player.armour.name} as your armour")
    else:
        print("Please provide a valid code for the armour you want to equip")
    display_player()


# ========================================
# Player movement
# ========================================
def move_player(action):
    """
    Moves the player to a new area based on the action provided
    Uses the global all_areas dictionary from the 'map' file so that the player can move between regions
    """
    global current_area     # to update the current_area variable defined outside this function

    # check if the current area has an exit for the given action
    if action in current_area.exits:
        new_area_name = current_area.exits[action]      # get the name of the new area from the exits dictionary
        current_area = all_areas[new_area_name]
        print(f"You go to {current_area.name}")
        print(current_area.description)
    else:
        print("You can't go that way.")


# ========================================
# Action handling
# ========================================
def action():
    """
    Handles player input for actions in the game
    Prompts the player for an action then splits the input into a list of individual words
    This allows to check for the first word to determine the action and to check for additional parameters
    If the input is empty, it prompts the player to enter a command
    """
    os.system("cls")
    status()

    prompt = input("What do you want to do? ").strip().lower().split()

    if len(prompt) == 0:        # empty input
        print("Please enter a command")
        action()
    else:

        # Movement
        if prompt[0] ==  "go":
            # Checks the length of the prompt to ensure a direction is specified
            if len(prompt) < 2: 
                print("Please specify a direction to go")
                input("Press enter to continue... ")
                action()

            # Allows for multiple word commands
            else:
                if len(prompt) == 3:
                    direction = f"{prompt[1]} {prompt[2]}"
                    move_player(direction)
                else:
                    move_player(prompt[1])

        # Pick up
        elif prompt[0] == "pick":
            check_item()

        # Show inventories
        elif prompt[0] == "show":
            if prompt[1] == "weapons":
                display_weapons()
            elif prompt[1] == "armour":
                display_armour()
        
        # Equip items
        elif prompt[0] == "equip":
            if len(prompt) < 3:     # checks if the command is complete
                print("Invalid equip command. Use 'equip weapon <code>' or 'equip armour <code>'")
                input("Press enter to continue... ")
                action()
            else:
                if prompt[2].isdigit():     # checks if the code is a number

                    # Converts the code into an integer
                    code = int(prompt[2])   
                    if prompt[1] == "weapon":
                        equip_weapon(code)
                    elif prompt[1] == "armour":
                        equip_armour(code)
                else:
                    print("Invalid code. Check weapons ('show weapons') or armour (show armour') inventories for valid codes")
                    input("Press enter to continue... ")
                    action()

        # Status
        elif prompt[0] == "status":
            display_player()

        # Commands
        elif prompt[0] == "commands":
            commands()

        # Invalid command fallback
        else:
            print("Invalid action. Try 'commands' to see available actions")
            input("Press enter to continue... ")
            action()

# ========================================
# Establish Story
# ========================================
def start():
    global run
    os.system("cls")
    print("=" * 100)
    print("You stumble upon a mysterious artefact during an archaeological excavation.")
    print("As you touch it, the artefact activates, engulfing you in a bright light and you lose conciousness")
    print("You hear echoes of soft whispers")
    print("When you regain conciousness, you find yourself in the dense and untamed world of the Stone Age.")
    print("You can't seem to remember your name, until you see the nametag on your chest")
    print("=" * 100)

    prompt = input("What does the nametag say? ")
    check = input("Are you sure that's what the nametag says? ").lower().strip()
    if check == "yes":
        player.name = prompt
        print(f"Welcome, {player.name}!")
        input("Press enter to continue... ")
        run = True
    else: 
        print("Read it correctly then!")
        input("Press enter to continue... ")
        start()

start()

# Main game loop
while run:
    os.system("cls") 
    check_enemy(current_area.enemy)   

    # Checks if player died during battle
    if not run:
        break       # immediately break out of loop

    action()
    input("Press enter to continue... ")

    # Checks if the current are has an enemy or item
    # If not, area is complete
    if current_area.enemy == None and current_area.item == None:
        current_area.complete = True

    # Checks if the final area is complete and ends game
    if arena.complete:
        print("You have freed your souls from this cruel game! You win!")
        print("Final Status:")
        display_player()
        input("Press enter to continue...")
        run = False
        break
    

    
    
    



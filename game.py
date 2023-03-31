import random
import time
import os
import pickle
from colorama import init, Fore, Style
import crafting,woodcutting,mining

# Define player class
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack = 10
        self.defense = 5
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.woodcutting_level = woodcutting.WoodcuttingLevel()
        self.crafting_level = crafting.CraftingLevel()
        self.inventory = []
        self.headgear = None
        self.chestplate = None
        self.leggings = None
        self.boots = None
        self.weapon = None
        self.mining_level = mining.MiningLevel()


    def buy_item(self, item_cost):
        if self.gold >= item_cost:
            self.gold -= item_cost
            return True
        else:
            print(Fore.RED + "You don't have enough gold." + Style.RESET_ALL)
            return False
    
    def sell_item(self, item_cost):
        self.gold += item_cost

def chop_tree(player):
    print("Which tree do you want to chop?")
    print("1. Normal tree (level 1)")
    print("2. Oak tree (level 15)")
    print("3. Willow tree (level 30)")
    print("4. Maple tree (level 45)")
    print("5. Yew tree (level 60)")
    print("6. Magic tree (level 75)")
    print("7. Redwood tree (level 90)")
    print("8. Elder tree (level 99)")
    print("q. Quit")
    print("Your gold: {}".format(player.gold))
    print("Your woodcutting level: {}".format(player.woodcutting_level.level))

    choice = input("Enter your choice: ")
    num_trainings = int(input("How many times do you want to train? "))
    for i in range(num_trainings):
        time.sleep(0.1)
        if choice == "1":
            tree = woodcutting.tree1
        elif choice == "2":
            tree = woodcutting.tree2
        elif choice == "3":
            tree = woodcutting.tree3
        elif choice == "4":
            tree = woodcutting.tree4
        elif choice == "5":
            tree = woodcutting.tree5
        elif choice == "6":
            tree = woodcutting.tree6
        elif choice == "7":
            tree = woodcutting.tree7
        elif choice == "8":
            tree = woodcutting.tree8
        elif choice == "q":
            return
        else:
            print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
            return
        cost = tree.level * 5
        if player.gold < cost:
            print(Fore.RED + "You don't have enough gold to chop this tree." + Style.RESET_ALL)
            return
        logs_obtained = player.woodcutting_level.chop_tree(tree)
        if logs_obtained > 0:
            player.gold -= cost
            print(Fore.GREEN + "You obtained {} logs.".format(logs_obtained) + Style.RESET_ALL)

        else:
            print(Fore.RED + "Your woodcutting level is too low" + Style.RESET_ALL)
        save_game(player)

def mine_item(player):
    print("Which item do you want to mine?")
    print("1. Copper ore (level 1)")
    print("2. Tin ore (level 15)")
    print("3. Iron ore (level 30)")
    print("4. Coal ore (level 45)")
    print("5. Mithril ore (level 60)")
    print("6. Adamantite ore (level 75)")
    print("7. Runite ore (level 90)")
    print("8. Dragonite ore (level 99)")
    print("q. Quit")
    print("Your gold: {}".format(player.gold))
    print("Your mining level: {}".format(player.mining_level.level))

    choice = input("Enter your choice: ")
    num_trainings = int(input("How many times do you want to train? "))
    for i in range(num_trainings):
        time.sleep(0.1)
        if choice == "1":
            item = mining.rock1
        elif choice == "2":
            item = mining.rock2
        elif choice == "3":
            item = mining.rock3
        elif choice == "4":
            item = mining.rock4
        elif choice == "5":
            item = mining.rock5
        elif choice == "6":
            item = mining.rock6
        elif choice == "7":
            item = mining.rock7
        elif choice == "8":
            item = mining.rock8
        elif choice == "q":
            return
        else:
            print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
            return
        cost = item.level * 5
        if player.gold < cost:
            print(Fore.RED + "You don't have enough gold to mine this item." + Style.RESET_ALL)
            return
        item_obtained = player.mining_level.mine_item(item)
        if item_obtained > 0:
            player.gold -= cost
            print(Fore.GREEN + "You obtained {} {}.".format(item_obtained, item.name) + Style.RESET_ALL)

        else:
            print(Fore.RED + "Your mining level is too low" + Style.RESET_ALL)
        save_game(player)

def craft_item(player):
    print("Which item do you want to craft?")
    print("1. Pretty Gem (level 1)")
    print("2. Bold Gem (level 15)")
    print("3. Glowing Gem (level 30)")
    print("4. Shining Gem (level 45)")
    print("5. Radiant Gem (level 60)")
    print("6. Gleaming Gem (level 75)")
    print("q. Quit")
    print("Your gold: {}".format(player.gold))
    print("Your crafting level: {}".format(player.crafting_level.level))

    choice = input("Enter your choice: ")
    num_trainings = int(input("How many times do you want to train? "))
    for i in range(num_trainings):
        time.sleep(0.1)
        if choice == "1":
            item = crafting.item1
        elif choice == "2":
            item = crafting.item2
        elif choice == "3":
            item = crafting.item3
        elif choice == "4":
            item = crafting.item4
        elif choice == "5":
            item = crafting.item5
        elif choice == "6":
            item = crafting.item6
        elif choice == "q":
            return
        else:
            print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
            return
        cost = item.level * 5
        if player.gold < cost:
            print(Fore.RED + "You don't have enough gold to craft this item." + Style.RESET_ALL)
            return
        items_obtained = player.crafting_level.craft_item(item)
        if items_obtained > 0:
            player.gold -= cost
            print(Fore.GREEN + "You obtained {} items.".format(items_obtained) + Style.RESET_ALL)
            add_item_to_inventory(player, item)
        save_game(player)


#define a method to add an item to the player's inventory
def add_item_to_inventory(player, item):
    player.inventory.append(item)
    print(Fore.GREEN + "You obtained a {}.".format(item.name) + Style.RESET_ALL)

#define a method to display the inventory
def display_inventory(player):
    print("Your inventory:")
    for item in player.inventory:
        print(item.name + " ({} gold)".format(item.cost))
    print("Your gold: {}".format(player.gold))

def sell_item(player, item):
    if item in player.inventory:
        player.inventory.remove(item)
        player.gold += item.cost
        print(Fore.GREEN + "You sold a {}.".format(item.name) + Style.RESET_ALL)
    else:
        print(Fore.RED + "You don't have a {}.".format(item.name) + Style.RESET_ALL)

def sellAll(player):
    for item in player.inventory:
        sell_item(player, item)

# Define enemy class
class Enemy:
    def __init__(self, name, health, attack, defense, level):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.level = level

# Define function to calculate damage
def calculate_damage(attacker, defender):
    damage = attacker.attack - defender.defense
    if damage < 0:
        damage = 0
    return damage

def openInventory(player):
    print("1. Buy health potion (50 gold)")
    print("2. Buy attack potion (50 gold)")
    print("3. Buy defense potion (50 gold)")
    print("4. Sell Pretty gem (50 gold)")
    print("5. Sell Bold gem (250 gold)")
    print("6. Sell Glowing gem (500 gold)")
    print("7. Sell Shining gem (1000 gold)")
    print("8. Sell Radiant gem (2000 gold)")
    print("9. Sell Gleaming gem (5000 gold)")
    print("10. Sell all items")

    print("q. Quit")
    print("Your gold: {}".format(player.gold))
    choice = input("Enter your choice: ")
    if choice == "1":
        if player.buy_item(50):
            player.health += 10
            print(Fore.GREEN + "You obtained a health potion." + Style.RESET_ALL)
    elif choice == "2":
        if player.buy_item(50):
            player.attack += 5
            print(Fore.GREEN + "You obtained an attack potion." + Style.RESET_ALL)
    elif choice == "3":
        if player.buy_item(50):
            player.defense += 5
            print(Fore.GREEN + "You obtained a defense potion." + Style.RESET_ALL)
    elif choice == "4":
        sell_item(player, crafting.item1)
    elif choice == "5":
        sell_item(player, crafting.item2)
    elif choice == "6":
        sell_item(player, crafting.item3)
    elif choice == "7":
        sell_item(player, crafting.item4)
    elif choice == "8":
        sell_item(player, crafting.item5)
    elif choice == "9":
        sell_item(player, crafting.item6)
    elif choice == "10":
        sellAll(player)
    elif choice == "q":
        return
    else:
        print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
        return

# Define function to fight enemy
def fight_enemy(player, enemy):
    print("You encounter a {}!".format(enemy.name))
    while player.health > 0 and enemy.health > 0:
        print("Your health: {}".format(player.health))
        print("{}'s health: {}".format(enemy.name, enemy.health))
        player_damage = calculate_damage(player, enemy)
        enemy_damage = calculate_damage(enemy, player)
        print(Fore.GREEN + "You deal {} damage to the {}.".format(player_damage, enemy.name) + Style.RESET_ALL)
        enemy.health -= player_damage
        if enemy.health <= 0:
            break
        print(Fore.CYAN + "The {} deals {} damage to you.".format(enemy.name, enemy_damage) + Style.RESET_ALL)
        player.health -= enemy_damage
    if player.health <= 0:
        print(Fore.CYAN + "You died! Game over."  + Style.RESET_ALL)
        return False
    else:
        print(Fore.GREEN + "You defeated the {}!".format(enemy.name) + Style.RESET_ALL)
        player.gold += 10
        player.exp += enemy.level * 10
        if player.exp >= player.level * 100:
            player.level += 1
            player.health += 10
            player.attack += 5
            player.defense += 5
            player.exp -= player.level * 100
            print(Fore.YELLOW + "You leveled up to level {}!".format(player.level) + Style.RESET_ALL)
        return True

# Define function to save game
def save_game(player):
    with open("savefile.pickle", "wb") as f:
        pickle.dump(player, f)
    print("Game saved!")

# Define function to load game
def load_game():
    try:
        with open("savefile.pickle", "rb") as f:
            player = pickle.load(f)
        print("Game loaded!")
        return player
    except FileNotFoundError:
        print("Save file not found.")

# Define function to start game
def start_game(skip = False):
    print(Fore.CYAN + "Welcome to RuneScape Adventure!" + Style.RESET_ALL)
    if skip == False:
        choice = input("Do you want to start a new game or load a saved game? (new/load) ")
        if choice == "new":
            name = input("What is your name? ")
            player = Player(name)
        else:
            player = load_game()
    
    while True:
        print("You are in the town square.")
        print(Fore.GREEN + "11. Fight goblins" + " - " + "Level: 1 " + " - " + "Health: 50 " + " - " + "Attack: 5 " + " - " + "Defense: 5")
        print(Fore.GREEN + "12. Fight dragon" + " - " + "Level: 5 " + " - " + "Health: 100 " + " - " + "Attack: 10 " + " - " + "Defense: 10")
        print(Fore.GREEN + "13. Fight giant spider" + " - " + "Level: 3 " + " - " + "Health: 75 " + " - " + "Attack: 7 " + " - " + "Defense: 7")
        print(Fore.GREEN + "14. Fight skeleton" + " - " + "Level: 2 " + " - " + "Health: 60 " + " - " + "Attack: 6 " + " - " + "Defense: 6")
        print(Fore.GREEN + "15. Fight zombie" + " - " + "Level: 1 " + " - " + "Health: 50 " + " - " + "Attack: 5 " + " - " + "Defense: 5")
        print(Fore.GREEN + "16. Fight troll" + " - " + "Level: 4 " + " - " + "Health: 90 " + " - " + "Attack: 9 " + " - " + "Defense: 9")
        print(Fore.GREEN + "17. Fight orc" + " - " + "Level: 3 " + " - " + "Health: 75 " + " - " + "Attack: 7 " + " - " + "Defense: 7")
        print(Fore.GREEN + "18. Fight giant rat" + " - " + "Level: 1 " + " - " + "Health: 50 " + " - " + "Attack: 5 " + " - " + "Defense: 5")
        print(Fore.GREEN + "19. Fight giant bat" + " - " + "Level: 2 " + " - " + "Health: 60 " + " - " + "Attack: 6 " + " - " + "Defense: 6")

        print(Fore.RED + "1. View inventory")
        print(Fore.BLUE + "2. View status")
        print(Fore.MAGENTA + "3. Buy item")
        print(Fore.YELLOW + "4. Train")
        print(Fore.CYAN + "5. Chop a tree")
        print(Fore.CYAN + "6. Craft an item")
        print(Fore.CYAN + "7. Mine an item")
        print("8. Quit game")

        choice = input("What do you want to do? ")
        if choice == "1":
            # write the code to open the inventory
            openInventory(player)

        if choice == "11":
            enemy = Enemy("Goblin", 50, 5, 2, 1)
            if not fight_enemy(player, enemy):
                break
        if choice == "12":
            enemy = Enemy("Dragon", 350, 30, 30, 20)
            if not fight_enemy(player, enemy):
                break
        if choice == "13":
            enemy = Enemy("Giant spider", 100, 10, 5, 5)
            if not fight_enemy(player, enemy):
                break
        if choice == "14":
            enemy = Enemy("Skeleton", 150, 15, 10, 10)
            if not fight_enemy(player, enemy):
                break
        if choice == "15":
            enemy = Enemy("Zombie", 200, 20, 15, 15)
            if not fight_enemy(player, enemy):
                break
        if choice == "16":
            enemy = Enemy("Troll", 250, 25, 20, 20)
            if not fight_enemy(player, enemy):
                break
        elif choice == "17":
            enemy   = Enemy("Massive spider", 1000, 100, 50, 50)
            if not fight_enemy(player, enemy):
                break
        elif choice == "18":
            enemy = Enemy("Giant zombie", 1500, 500, 2570, 250)
            if not fight_enemy(player, enemy):
                break
        elif choice == "19":
            enemy = Enemy("Giant skeleton", 2500, 500, 25, 25)
        elif choice == "2":
            print("Name: {}".format(player.name))
            print("Health: {}".format(player.health))
            print("Attack: {}".format(player.attack))
            print("Defense: {}".format(player.defense))
            print("Level: {}".format(player.level))
            print("Experience: {}".format(player.exp))
            print("Gold: {}".format(player.gold))
            display_inventory(player)            
            print("Woodcutting level: {}".format(player.woodcutting_level.level))
            print("crafting level: {}".format(player.crafting_level.level))
        elif choice == "3":
            item_cost = 20 # set the item cost
            if player.buy_item(item_cost):
                print("You bought an item!")
            else:
                print("You couldn't buy the item.")
        elif choice == "4":
            if player.level >= 2:
                num_trainings = int(input("How many times do you want to train? "))
                for i in range(num_trainings):
                    time.sleep(0.1)
                    print("Training {} of {}".format(i+1, num_trainings))
                    exp = random.randint(1, 10) * player.level
                    gold = random.randint(1, 10) * player.level
                    player.exp += exp
                    player.gold += gold

                    if player.exp >= player.level * 100:
                        player.level += 1
                        player.health += 2 * player.level
                        player.attack += 1 * player.level
                        player.defense += 1 * player.level
                        player.gold += random.randint(1, 10) * player.level
                        player.exp -= player.level * 100
                        print("You leveled up to level {}!".format(player.level))
                    else:
                        print("You gained " + str(exp) + " experience points and " + str(gold) + " gold.")
                        save_game(player)
            else:
                print("You need to be at least level 2 to train.")
        elif choice == "5":
            chop_tree(player)
        elif choice == "6":
            craft_item(player)
        elif choice == "7":
            mine_item(player)
        elif choice == "8":
            break
        else:
            print("=========================================")
    if choice != "new":
        save_game(player)




try:
    start_game()
except KeyboardInterrupt:
    print("You pressed Ctrl+C. Going back to main menu...")
    start_game()

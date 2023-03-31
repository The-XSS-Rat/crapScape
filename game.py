import random
import time
import pickle
from colorama import init, Fore, Style


class WoodcuttingLevel:
    def __init__(self):
        self.level = 1
        self.exp = 0

    def chop_tree(self, tree):
        logs_obtained = 0
        if self.level >= tree.level:
            logs_obtained = tree.logs
            self.exp += tree.exp
            if self.exp >= self.level * 100:
                self.level += 1
                self.exp = 0
        return logs_obtained


class Tree:
    def __init__(self, name, level, logs, exp):
        self.name = name
        self.level = level
        self.logs = logs
        self.exp = exp

    def __str__(self):
        return self.name


tree1 = Tree("Normal tree", 1, 1, 10)
tree2 = Tree("Oak tree", 15, 10, 100)
tree3 = Tree("Willow tree", 30, 25, 250)
tree4 = Tree("Maple tree", 45, 50, 500)
tree5 = Tree("Yew tree", 60, 100, 1000)


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
        self.woodcutting_level = WoodcuttingLevel()


    def buy_item(self, item_cost):
        if self.gold >= item_cost:
            self.gold -= item_cost
            return True
        else:
            print(Fore.RED + "You don't have enough gold." + Style.RESET_ALL)
            return False

def chop_tree(player):
    print("Which tree do you want to chop?")
    print("1. Normal tree (level 1)")
    print("2. Oak tree (level 15)")
    print("3. Willow tree (level 30)")
    print("4. Maple tree (level 45)")
    print("5. Yew tree (level 60)")
    choice = input("Enter your choice: ")
    num_trainings = int(input("How many times do you want to train? "))
    for i in range(num_trainings):
        time.sleep(5) # sleep for 2 seconds
        if choice == "1":
            tree = tree1
        elif choice == "2":
            tree = tree2
        elif choice == "3":
            tree = tree3
        elif choice == "4":
            tree = tree4
        elif choice == "5":
            tree = tree5
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
        print(Fore.GREEN + "11. Fight goblins")
        print(Fore.GREEN + "12. Fight dragon")
        print(Fore.BLUE + "2. View status")
        print(Fore.MAGENTA + "3. Buy item")
        print(Fore.YELLOW + "4. Train")
        print(Fore.CYAN + "5. Chop a tree")
        print("6. Quit game")

        choice = input("What do you want to do? ")
        if choice == "11":
            enemy = Enemy("Goblin", 50, 5, 2, 1)
            if not fight_enemy(player, enemy):
                break
        if choice == "12":
            enemy = Enemy("Dragon", 350, 30, 30, 20)
            if not fight_enemy(player, enemy):
                break
        elif choice == "2":
            print("Name: {}".format(player.name))
            print("Health: {}".format(player.health))
            print("Attack: {}".format(player.attack))
            print("Defense: {}".format(player.defense))
            print("Level: {}".format(player.level))
            print("Experience: {}".format(player.exp))
            print("Gold: {}".format(player.gold))
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
                    time.sleep(5)
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
            break
        else:
            print("Invalid choice.")
    if choice != "new":
        save_game(player)




try:
    start_game()
except KeyboardInterrupt:
    print("You pressed Ctrl+C. Going back to main menu...")
    start_game()

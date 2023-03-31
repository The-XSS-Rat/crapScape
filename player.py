import crafting,woodcutting

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


    def buy_item(self, item_cost):
        if self.gold >= item_cost:
            self.gold -= item_cost
            return True
        else:
            print(Fore.RED + "You don't have enough gold." + Style.RESET_ALL)
            return False
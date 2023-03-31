
class CraftingLevel:
    def __init__(self):
        self.level = 1
        self.exp = 0
        self.cost = 0

    def craft_item(self, item):
        item_crafted = 0
        if self.level >= item.level:
            item_crafted = item.items
            self.exp += item.exp
            if self.exp >= self.level * 100:
                self.level += 1
                self.exp = 0
        return item_crafted
    
class Item:
    def __init__(self, name, level, items, exp, cost):
        self.name = name
        self.level = level
        self.items = items
        self.exp = exp
        self.cost = cost

    def __str__(self):
        return self.name
    
item1 = Item("Pretty Gem", 1, 1, 10, 15)
item2 = Item("Bold Gem", 15, 10, 100, 150)
item3 = Item("Glowing Gem", 30, 25, 250, 300)
item4 = Item("Shining Gem", 45, 50, 500, 600)
item5 = Item("Radiant Gem", 60, 100, 1000, 2000)
item6 = Item("Gleaming Gem", 75, 250, 2500,4500)
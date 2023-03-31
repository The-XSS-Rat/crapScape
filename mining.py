
class MiningLevel:
    def __init__(self):
        self.level = 1
        self.exp = 0
        self.cost = 0

    def mine_item(self, item):
        item_crafted = 0
        if self.level >= item.level:
            item_crafted = item.items
            self.exp += item.exp
            if self.exp >= self.level * 100:
                self.level += 1
                self.exp = 0
        return item_crafted
    
class Rock:
    def __init__(self, name, level, items, exp, cost):
        self.name = name
        self.level = level
        self.items = items
        self.exp = exp
        self.cost = cost

    def __str__(self):
        return self.name
    
rock1 = Rock("Tin", 1, 1, 10, 15)
rock2 = Rock("Copper", 15, 10, 100, 150)
rock3 = Rock("Iron", 30, 25, 250, 300)
rock4 = Rock("Coal", 45, 50, 500, 600)
rock5 = Rock("Mithril", 60, 100, 1000, 2000)
rock6 = Rock("Adamantite", 75, 250, 2500,4500)
rock7 = Rock("Runite", 90, 500, 5000, 10000)
rock8 = Rock("Dragonite", 99, 1000, 10000, 20000)
rock9 = Rock("Godstone", 99, 1000, 10000, 25000)
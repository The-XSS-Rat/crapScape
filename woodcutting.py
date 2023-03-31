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
tree6 = Tree("Magic tree", 75, 250, 2500)
tree7 = Tree("Redwood tree", 90, 500, 5000)
tree8 = Tree("Elder tree", 99, 1000, 10000)
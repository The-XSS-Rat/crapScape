import pygame
import sys
import random
import math
import sqlite3
import json
from button import Button
from smelting import *
from enemy import Enemy
import numpy as np


# Add the following imports
from health_bar import HealthBar

# Add the following constant
ENEMY_SPEED = 2
all_sprites = pygame.sprite.Group()

speed = 4


# Grid dimensions
rows, columns = 5, 2
cell_size = 100
spacing = 10
pygame.font.init()

# Fonts and colors
font = pygame.font.Font(None, 36)
text_color = (255, 255, 255)
background_color = (0, 0, 0)


# Initialize Pygame
pygame.init()

numbers = np.arange(0, 45)
probabilities = np.array([1 / (i + 1) for i in numbers])
probabilities /= probabilities.sum()

amountOfItemsToSpawn = np.random.choice(numbers, p=probabilities)


screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w -100
SCREEN_HEIGHT = screen_info.current_h -200
BACKGROUND_COLOR = (0, 0, 0)
FPS = 30
TEXT_COLOR = (255, 255, 255)
baseInv = {"Copper": 0, "Iron": 0, "Gold": 0, "Silver": 0, "Mithril": 0, "Adamant": 0, "Runite": 0, "Dragon": 0,"Tin": 0, "Coal": 0}


# Rock types
ROCK_TYPES = [
    {"name": "Copper", "color": (184, 115, 51), "min_level": 1},
    {"name": "Tin", "color": (184, 115, 51), "min_level": 1},
    {"name": "Iron", "color": (206, 153, 117), "min_level": 10},
    {"name": "Coal", "color": (0, 0, 0), "min_level": 30},
    {"name": "Gold", "color": (255, 215, 0), "min_level": 20},
    {"name": "Silver", "color": (192, 192, 192), "min_level": 36},
    {"name": "Mithril", "color": (119, 136, 153), "min_level": 55},
    {"name": "Adamantite", "color": (129, 125, 125), "min_level": 70},
    {"name": "Runite", "color": (0, 0, 0), "min_level": 85},
    {"name": "Platinum", "color": (229, 228, 226), "min_level": 100},
    {"name": "Obsidian", "color": (59, 56, 56), "min_level": 120},
    {"name": "Zircon", "color": (255, 209, 102), "min_level": 140},
    {"name": "Titanium", "color": (191, 194, 199), "min_level": 160},
    {"name": "Sapphire", "color": (15, 82, 186), "min_level": 180},
    {"name": "Ruby", "color": (224, 17, 95), "min_level": 200},
    {"name": "Emerald", "color": (0, 128, 0), "min_level": 220},
    {"name": "Topaz", "color": (255, 128, 0), "min_level": 240},
    {"name": "Diamond", "color": (185, 242, 255), "min_level": 260},
    {"name": "Moonstone", "color": (211, 211, 211), "min_level": 280},
    {"name": "Sunstone", "color": (255, 165, 0), "min_level": 300},
    {"name": "Amethyst", "color": (148, 0, 211), "min_level": 320},
    {"name": "Turquoise", "color": (64, 224, 208), "min_level": 340},
    {"name": "Jade", "color": (0, 168, 107), "min_level": 360},
    {"name": "Quartz", "color": (238, 130, 238), "min_level": 380},
    {"name": "Lapis Lazuli", "color": (0, 0, 255), "min_level": 400},
    {"name": "Onyx", "color": (53, 56, 57), "min_level": 420},
    {"name": "Garnet", "color": (255, 0, 0), "min_level": 440},
    {"name": "Aquamarine", "color": (127, 255, 212), "min_level": 460},
    {"name": "Opal", "color": (255, 224, 205), "min_level": 480},
    {"name": "Peridot", "color": (50, 205, 50), "min_level": 500},
    {"name": "Pearl", "color": (255, 255, 255), "min_level": 520},
    {"name": "Alexandrite", "color": (112, 219, 147), "min_level": 540},
    {"name": "Citrine", "color": (255, 247, 0), "min_level": 560},
    {"name": "Carnelian", "color": (255, 97, 3), "min_level": 580},
    {"name": "Apatite", "color": (0, 255, 255), "min_level": 600},
    {"name": "Kyanite", "color": (0, 123, 167), "min_level": 620},
    {"name": "Spinel", "color": (255, 111, 97), "min_level": 640},
    {"name": "Sodalite", "color": (0, 0, 139), "min_level": 660},
    {"name": "Morganite", "color": (255, 182, 193), "min_level": 680},
    {"name": "Tanzanite", "color": (148, 0, 211), "min_level": 700}
]

TREE_TYPES = [
    {"name": "Normal", "color": (50, 150, 0), "min_level": 1},
    {"name": "Oak", "color": (90, 100, 0), "min_level": 15},
    {"name": "Willow", "color": (0, 180, 180), "min_level": 30},
    {"name": "Maple", "color": (250, 100, 0), "min_level": 45},
    {"name": "Yew", "color": (100, 0, 0), "min_level": 60},
    {"name": "Magic", "color": (150, 0, 150), "min_level": 75},
    {"name": "Elder", "color": (200, 100, 50), "min_level": 90},
    {"name": "Divine", "color": (255, 255, 0), "min_level": 105},
    {"name": "Ancient", "color": (128, 0, 128), "min_level": 120},
    {"name": "Frost", "color": (0, 255, 255), "min_level": 135},
    {"name": "Fire", "color": (255, 0, 0), "min_level": 150},
    {"name": "Wind", "color": (0, 255, 0), "min_level": 165},
    {"name": "Water", "color": (0, 0, 255), "min_level": 180},
    {"name": "Earth", "color": (139, 69, 19), "min_level": 195},
    {"name": "Shadow", "color": (128, 128, 128), "min_level": 210},
    {"name": "Light", "color": (255, 255, 255), "min_level": 225},
    {"name": "Spirit", "color": (0, 128, 128), "min_level": 240},
    {"name": "Chaos", "color": (255, 0, 255), "min_level": 255},
    {"name": "Order", "color": (255, 215, 0), "min_level": 270},
    {"name": "Sky", "color": (135, 206, 250), "min_level": 285},
    {"name": "Celestial", "color": (255, 20, 147), "min_level": 300},
    {"name": "Cosmic", "color": (0, 191, 255), "min_level": 315},
    {"name": "Void", "color": (47, 79, 79), "min_level": 330},
    {"name": "Galactic", "color": (0, 0, 139), "min_level": 345},
    {"name": "Temporal", "color": (75, 0, 130), "min_level": 360},
    {"name": "Mystic", "color": (147, 112, 219), "min_level": 375},
    {"name": "Ethereal", "color": (72, 61, 139), "min_level": 390},
]


def draw_pickaxe(screen, font, pickaxe, x, y):
    pygame.draw.rect(screen, (255, 255, 255), (x, y, 100, 20), 2)
    pickaxe_text = font.render(pickaxe["name"], True, (255, 255, 255))
    screen.blit(pickaxe_text, (x + 10, y + 2))

# Load mining animation
mining_animation = [pygame.Surface((8, 8)) for _ in range(400)]
for i in range(400):
    mining_animation[i].fill((255, 255, 0))
    pygame.draw.circle(mining_animation[i], (255, 0, 0), (16, 16), 8 * (i + 1))

def display_shop(screen, font, player):
    shop_text = font.render("Shop", True, TEXT_COLOR)
    gold_text = font.render(f"Gold: {player.gold}", True, TEXT_COLOR)
    pickaxe_text = font.render(f"Pickaxe: {player.pickaxe['name']}", True, TEXT_COLOR)
    
    sell_text = "Sell: "
    for item, amount in player.inventory.items():
        if item != "Gold":
            sell_text += f"{item} ({amount}) - {item} x 10 gold | "
    
    buy_text = "Buy pickaxes:"
    pickaxes = [
        {"name": "Bronze", "cost": 50, "speed_modifier": 1},
        {"name": "Iron", "cost": 100, "speed_modifier": 2},
        {"name": "Steel", "cost": 500, "speed_modifier": 3},
        {"name": "Black", "cost": 1000, "speed_modifier": 3},
        {"name": "Mithril", "cost": 2500, "speed_modifier": 4},
        {"name": "Adamant", "cost": 5000, "speed_modifier": 5},
        {"name": "Rune", "cost": 10000, "speed_modifier": 6},
        {"name": "Dragon", "cost": 25000, "speed_modifier": 7},
        {"name": "Infernal", "cost": 50000, "speed_modifier": 8},
        {"name": "Crystal", "cost": 100000, "speed_modifier": 9},
        {"name": "3rd_age", "cost": 200000, "speed_modifier": 10},
    ]

    for pickaxe in pickaxes:
        buy_text += f"{pickaxe['name']} ({pickaxe['cost']} gold) | "
    
    screen.blit(shop_text, (10, 130))
    screen.blit(gold_text, (10, 160))
    screen.blit(pickaxe_text, (10, 190))

    screen.blit(font.render(sell_text, True, TEXT_COLOR), (10, 220))
    screen.blit(font.render(buy_text, True, TEXT_COLOR), (10, 250))

def sell_item(player, item_name):
    if player.inventory[item_name] > 0:
        player.inventory[item_name] -= 1
        player.gold += 10

def buy_pickaxe(player, pickaxe):
    if player.gold >= pickaxe["cost"]:
        player.gold -= pickaxe["cost"]
        player.pickaxe = pickaxe

# Create the player character class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.auto_mine = False
        self.mining_level = 1
        self.inventory = baseInv
        self.woodcutting_level = 1
        self.woodcutting_xp = 0
        self.mining_animation_counter = 0
        self.mining_xp = 0
        self.gold = 0
        self.pickaxe = {"name": "Basic", "speed_modifier": 1}
        self.attack_timer = 0
        self.health = 100
        self.attack_cooldown = 3
        self.attack = 10
        self.auto_wc = False
        self.resting = False
        self.restingPoints = 0

    def save_state(self):
        state = {
            "x": self.rect.x,
            "y": self.rect.y,
            "auto_mine": self.auto_mine,
            "mining_level": self.mining_level,
            "mining_xp": self.mining_xp,
            "inventory": self.inventory,
            "woodcutting_level": self.woodcutting_level,
            "woodcutting_xp": self.woodcutting_xp,
            "auto_wc": self.auto_wc,
            "gold": self.gold,
            "pickaxe": self.pickaxe,
            "resting": self.resting,
            "restingPoints": self.restingPoints
        }
        with open("game_state.json", "w") as f:
            json.dump(state, f)


    def load_state(self):
        try:
            with open("game_state.json", "r") as f:
                state = json.load(f)
                self.rect.x = state["x"]
                self.rect.y = state["y"]
                self.auto_mine = state["auto_mine"]
                self.mining_level = state["mining_level"]
                self.woodcutting_level = state["woodcutting_level"]
                self.woodcutting_xp = state["woodcutting_xp"]
                self.auto_wc = state["auto_wc"]
                self.mining_xp = state["mining_xp"]
                self.inventory = state["inventory"]
                self.gold = state["gold"]
                self.pickaxe = state["pickaxe"]
                self.resting = state["resting"]
                self.restingPoints = state["restingPoints"]
        except FileNotFoundError:
            pass



    def update(self, keys_pressed, rocks, enemies):
        if keys_pressed[pygame.K_UP]:
            self.rect.y -= 5
        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += 5
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += 5

        if self.auto_mine:
            self.move_to_nearest_rock(inLevelRocks)
        
        if self.auto_wc:
            self.move_to_nearest_tree(inLevelTrees)

        if self.resting:
            self.rest()

    def toggle_auto_mine(self):
        self.resting = 0
        self.auto_wc = 0
        self.auto_mine = not self.auto_mine

    def toggle_auto_wc(self):
        self.resting = 0
        self.auto_mine = 0
        self.auto_wc = not self.auto_wc

    def toggle_rest(self):
        self.auto_wc = 0
        self.auto_mine = 0
        self.resting = not self.resting

    def rest(self):
        self.auto_mine = 0
        self.auto_wc = 0
        if(self.restingPoints <= 10000):
            self.restingPoints += 1

    def move_to_nearest_rock(self, rocks):
        if player.restingPoints <= 0:
            self.resting = True
            return

        player.restingPoints -= 0.1 * speed

        if not rocks:
            clear_rocks()
            add_rocks(np.random.choice(numbers, p=probabilities))
            return
        nearest_rock = min(rocks, key=lambda rock: self.distance_to(rock))
        if self.distance_to(nearest_rock) < 5 * speed:
            self.mining_animation_counter += 1
            if self.mining_animation_counter >= (random.randint(4*nearest_rock.min_level,100*nearest_rock.min_level) + (nearest_rock.min_level/500)) // player.pickaxe["speed_modifier"] :  # Mine a rock every 20 frames                self.mining_animation_counter = 0
                if self.mining_level >= nearest_rock.min_level:
                    rocks.remove(nearest_rock)
                    all_sprites.remove(nearest_rock)
                    self.inventory[nearest_rock.name] = self.inventory.get(nearest_rock.name, 0) + 1
                    add_rocks(random.randint(0, 1))
                    player.save_state()
                    self.mining_xp += nearest_rock.xp
                    if self.mining_xp >= self.mining_level * 100:
                        self.mining_xp = 0
                        self.mining_level += 1
            self.image = mining_animation[self.mining_animation_counter // 400]
        else:
            self.image.fill((0, 255, 0))
            dx, dy = nearest_rock.rect.x - self.rect.x, nearest_rock.rect.y - self.rect.y
            distance = math.sqrt(dx * dx + dy * dy)
            self.rect.x += 5 * speed * dx / distance
            self.rect.y += 5 * speed * dy / distance

    def distance_to(self, rock):
        dx, dy = self.rect.x - rock.rect.x, self.rect.y - rock.rect.y
        return math.sqrt(dx * dx + dy * dy)
    
    def move_to_nearest_tree(self, trees):
        if player.restingPoints <= 0:
            self.resting = True
            return()
        
        player.restingPoints -= 0.1
        if not trees:
            clear_trees()
            add_trees(np.random.choice(numbers, p=probabilities))
            return
        nearest_tree = min(trees, key=lambda tree: self.distance_to(tree))
        if self.distance_to(nearest_tree) < 5 * speed:
            self.mining_animation_counter += 1
            if self.mining_animation_counter >= (random.randint(4*nearest_tree.min_level,100*nearest_tree.min_level) + (nearest_tree.min_level/5000)) // player.pickaxe["speed_modifier"] :  # Mine a rock every 20 frames                self.mining_animation_counter = 0
                if self.woodcutting_level >= nearest_tree.min_level:
                    trees.remove(nearest_tree)
                    all_sprites.remove(nearest_tree)
                    self.inventory[nearest_tree.name] = self.inventory.get(nearest_tree.name, 0) + 1
                    add_trees(random.randint(0, 1))
                    player.save_state()
                    self.woodcutting_xp += nearest_tree.xp
                    if self.woodcutting_xp >= self.woodcutting_level * 100:
                        self.woodcutting_xp -= self.woodcutting_level * 100
                        self.woodcutting_level += 1

            self.image = mining_animation[self.mining_animation_counter // 400]
        else:
            self.image.fill((0, 255, 0))
            dx, dy = nearest_tree.rect.x - self.rect.x, nearest_tree.rect.y - self.rect.y
            distance = math.sqrt(dx * dx + dy * dy)
            self.rect.x += 5 * speed * dx / distance
            self.rect.y += 5 * speed * dy / distance


def draw_random_circle(surface, color, center, min_radius, max_radius):
    num_points = random.randint(6, 12)  # Number of points to create the circle
    points = []
    for i in range(num_points):
        angle = i * (2 * math.pi / num_points)
        radius = random.uniform(min_radius, max_radius)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)
    
import random
import math

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, tree_type):
        super().__init__()
        circle_radius_min = 8
        circle_radius_max = 16
        circle_color = tree_type["color"]
        
        # Create a surface with a transparent background
        self.image = pygame.Surface((circle_radius_max * 2, circle_radius_max * 2), pygame.SRCALPHA)
        
        # Draw the random circle
        self.draw_random_circle(self.image, circle_color, (circle_radius_max, circle_radius_max), circle_radius_min, circle_radius_max)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.min_level = tree_type["min_level"]
        self.name = tree_type["name"]
        self.xp = self.min_level * 10
        self.font = pygame.font.Font(None, 14)

    def draw_random_circle(self, surface, base_color, center, min_radius, max_radius):
        num_points = random.randint(6, 12)  # Number of points to create the circle
        points = []
        for i in range(num_points):
            angle = i * (2 * math.pi / num_points)
            radius = random.uniform(min_radius, max_radius)
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))

            # Add random color variation to the base color
            color_variation = random.randint(-20, 20)
            color = (max(0, min(base_color[0] + color_variation, 255)),
                     max(0, min(base_color[1] + color_variation, 255)),
                     max(0, min(base_color[2] + color_variation, 255)))

            # Draw a line with the varied color
            if i > 0:
                pygame.draw.line(surface, color, points[-2], points[-1], 2)

        # Close the shape by drawing the last line
        color_variation = random.randint(-20, 20)
        color = (max(0, min(base_color[0] + color_variation, 255)),
                 max(0, min(base_color[1] + color_variation, 255)),
                 max(0, min(base_color[2] + color_variation, 255)))
        pygame.draw.line(surface, color, points[-1], points[0], 2)


    def draw_name(self, screen):
        text_surface = self.font.render(self.name + " tree", True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x - (text_surface.get_width() // 2 - self.image.get_width() // 2), self.rect.y - text_surface.get_height()))


# Create the rock class for mining
class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, rock_type):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(rock_type["color"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.min_level = rock_type["min_level"]
        self.name = rock_type["name"]
        self.xp = self.min_level * 10
        self.font = pygame.font.Font(None, 14)

    
    def draw_name(self, screen, rocks_group):
        if self in rocks_group:
            text_surface = self.font.render(self.name + " rock", True, (255, 255, 255))
            screen.blit(text_surface, (self.rect.x - (text_surface.get_width() // 2 - self.image.get_width() // 2), self.rect.y - text_surface.get_height()))

ROCK_TYPE_WEIGHTS = [1 / rock_type["min_level"] for rock_type in ROCK_TYPES]


# Add rocks to the game
def add_rocks(num_rocks):
    for _ in range(num_rocks):
        x = random.randint(0, SCREEN_WIDTH - 64)
        y = random.randint(0, SCREEN_HEIGHT - 64)
        rock_type = random.choices(ROCK_TYPES, ROCK_TYPE_WEIGHTS)[0]
        rock = Rock(x, y, rock_type)
        all_sprites.add(rock)
        rocks.add(rock)
        if rock_type["min_level"] <= player.mining_level:
            inLevelRocks.add(rock)

TREE_TYPE_WEIGHTS = [1 / tree_type["min_level"] for tree_type in TREE_TYPES]

def add_trees(num_trees):
    for _ in range(num_trees): 
        x = random.randint(0, SCREEN_WIDTH - 64)
        y = random.randint(0, SCREEN_HEIGHT - 64)
        tree_type = random.choices(TREE_TYPES, TREE_TYPE_WEIGHTS)[0]
        tree = Tree(x, y, tree_type)
        all_sprites.add(tree)
        trees.add(tree)
        if tree_type["min_level"] <= player.woodcutting_level:
            inLevelTrees.add(tree)


trees = pygame.sprite.Group()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

backgrounds = ["bg.png", "bg2.png", "bg3.png"]

# Load the images
loaded_backgrounds = [pygame.image.load(bg).convert() for bg in backgrounds]

# Choose a random background
selected_background = random.choice(loaded_backgrounds)

scaled_background = pygame.transform.scale(selected_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Set up the game window and main loop
pygame.display.set_caption("RuneScape Clone - Automated Mining with Levels")
clock = pygame.time.Clock()

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
rocks = pygame.sprite.Group()
inLevelRocks = pygame.sprite.Group()
inLevelTrees = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy1 = Enemy(100, 100)
enemy2 = Enemy(500, 400)
enemies.add(enemy1)
enemies.add(enemy2)
all_sprites.add(enemy1)
all_sprites.add(enemy2)

player_health_bar = HealthBar(10, 100)
enemy1_health_bar = HealthBar(100, 100)
enemy2_health_bar = HealthBar(500, 100)


all_sprites.add(player)
add_rocks(np.random.choice(numbers, p=probabilities))
add_trees(np.random.choice(numbers, p=probabilities))

player.load_state()


show_shop = False
show_smithing = False
rest_button = Button(SCREEN_WIDTH - 150, 10, 140, 40, "Rest", (255, 255, 255), (128, 128, 128))
auto_mine_button = Button(SCREEN_WIDTH - 150, 60, 140, 40, "Toggle Auto Mine", (255, 255, 255), (128, 128, 128))
auto_woodcut_button = Button(SCREEN_WIDTH - 150, 110, 140, 40, "Toggle woodCut", (255, 255, 255), (128, 128, 128))

shop_button = Button(SCREEN_WIDTH - 150, 110, 140, 40, "Open Shop", (255, 255, 255), (128, 128, 128))
smithing_menu = Button(SCREEN_WIDTH - 150, 160, 140, 40, "Open Smithing", (255, 255, 255), (128, 128, 128))
respawn_button = Button(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100, 140, 40, "Respawn rocks", (255, 255, 255), (128, 128, 128))
all_sprites.add(auto_mine_button)
all_sprites.add(auto_woodcut_button)
all_sprites.add(respawn_button)
all_sprites.add(rest_button)

def clear_rocks():
    rocks.empty()
    selected_background = random.choice(backgrounds)

    background_image = pygame.image.load(selected_background).convert()
    scaled_background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    for sprite in all_sprites:
        if isinstance(sprite, Rock):
            all_sprites.remove(sprite)

def clear_trees():
    trees.empty()
    selected_background = random.choice(backgrounds)

    background_image = pygame.image.load(selected_background).convert()
    scaled_background = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    for sprite in all_sprites:
        if isinstance(sprite, Tree):
            all_sprites.remove(sprite)

def smith_item(player, item_name):
    item = next((x for x in SMITHING_ITEMS if x["name"] == item_name), None)
    if item is not None and player.mining_level >= item["min_level"]:
        if all(player.inventory[res] >= amt for res, amt in item["resources"].items()):
            for res, amt in item["resources"].items():
                player.inventory[res] -= amt
            player.inventory[item_name] = player.inventory.get(item_name, 0) + 1
            # Add XP gain and level up logic if needed


# Buttons for the shop
sell_copper_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 140, 40, "Buy Copper", (255, 255, 255), (128, 128, 128))
sell_iron_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 140, 40, "Buy Iron", (255, 255, 255), (128, 128, 128))
sell_gold_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 140, 40, "Buy Gold", (255, 255, 255), (128, 128, 128))
sell_silver_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, 140, 40, "Buy Silver", (255, 255, 255), (128, 128, 128))
sell_shop_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 140, 40, "Close Shop", (255, 255, 255), (128, 128, 128))

font = pygame.font.Font(None, 24)

running = True
while running:
    clock.tick(FPS)
    
    screen.blit(scaled_background, (0, 0))

    #screen.fill((0, 0, 0))  # Fill the screen with black (R, G, B)

        # Draw the inventory grid
    for item, amount in player.inventory.items():
        row = i // columns
        column = i % columns

        x = spacing + column * (cell_size + spacing)
        y = spacing + row * (cell_size + spacing)

        # Draw the background rectangle
        pygame.draw.rect(screen, (150, 150, 150), (x, y, cell_size, cell_size))

        # Draw the item name and count
        item_text = font.render(f"{item}: {amount}", True, text_color)
        screen.blit(item_text, (x + 5, y + 5))

    draw_pickaxe(screen, font, player.pickaxe, 10, 130)

    # Draw the smelting menu
    draw_smelting_menu(screen, font, SMITHING_ITEMS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                player.toggle_auto_mine()
            if keys_pressed[pygame.K_SPACE] and player.attack_timer <= 0:
                player.attack_timer = player.attack_cooldown
                player.attack(enemies)
            elif event.key == pygame.K_b:
                show_shop = not show_shop
            elif event.key == pygame.K_s:
                show_smithing = not show_smithing
            elif show_smithing:
                if event.key == pygame.K_1:
                    smith_item(player, "Bronze Bar")
                elif event.key == pygame.K_2:
                    smith_item(player, "Iron Bar")
                # ... add more key bindings for other items

            elif show_shop:
                if event.key == pygame.K_c:
                    sell_item(player, "Copper")
                elif event.key == pygame.K_i:
                    sell_item(player, "Iron")
                elif event.key == pygame.K_g:
                    sell_item(player, "Gold")
                elif event.key == pygame.K_DOWN:
                    sell_item(player, "Silver")

                elif event.key == pygame.K_1:
                    buy_pickaxe(player, {"name": "Iron", "cost": 100, "speed_modifier": 2})
                elif event.key == pygame.K_2:
                    buy_pickaxe(player, {"name": "Steel", "cost": 500, "speed_modifier": 4})
                elif event.key == pygame.K_3:
                    buy_pickaxe(player, {"name": "Mithril", "cost": 1000, "speed_modifier": 6})
                elif event.key == pygame.K_4:
                    buy_pickaxe(player, {"name": "Adamant", "cost": 5000, "speed_modifier": 8})
                elif event.key == pygame.K_5:
                    buy_pickaxe(player, {"name": "Runite", "cost": 10000, "speed_modifier": 10})
                elif event.key == pygame.K_6:
                    buy_pickaxe(player, {"name": "Dragon", "cost": 50000, "speed_modifier": 12})
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
                
            if auto_mine_button.is_clicked(event):
                player.toggle_auto_mine()

            elif respawn_button.is_clicked(event):
                clear_rocks()
                add_rocks(5)

            elif auto_woodcut_button.is_clicked(event):
                player.toggle_auto_wc()

            elif rest_button.is_clicked(event):
                player.toggle_rest()


    keys_pressed = pygame.key.get_pressed()
    player.update(keys_pressed, rocks, enemies)


    for rock in rocks:
        rock.draw_name(screen, rocks)

    for tree in trees:
        tree.draw_name(screen)

    #screen.fill(BACKGROUND_COLOR)
    all_sprites.draw(screen)

    player_health_bar.update(player.health)
    enemy1_health_bar.update(enemy1.health)
    enemy2_health_bar.update(enemy2.health)

    player_health_bar.draw(screen)
    enemy1_health_bar.draw(screen)
    enemy2_health_bar.draw(screen)

    # Display mining status, inventory, and mining level
    mining_status = "ON" if player.auto_mine else "OFF"
    status_text = font.render(f"Auto Mine: {mining_status}", True, TEXT_COLOR)
    status_text_auto_wc = font.render(f"Auto Woodcut: {player.auto_wc}", True, TEXT_COLOR)
    #inventory_text = font.render(f"Inventory: {player.inventory}", True, TEXT_COLOR)
    mining_level_text = font.render(f"Mining Level: {player.mining_level}", True, TEXT_COLOR)
    mining_xp_text = font.render(f"EXP: {player.mining_xp}", True, TEXT_COLOR)
    woodcut_level_text = font.render(f"Woodcutting Level: {player.woodcutting_level}", True, TEXT_COLOR)
    woodcut_xp_text = font.render(f"EXP: {player.woodcutting_xp}", True, TEXT_COLOR)
    resting_text = font.render(f"Resting: {player.resting}", True, TEXT_COLOR)
    exp_level_text = font.render(f"EXP: {player.mining_xp}", True, TEXT_COLOR)

    # Define the black box parameters
    box_x, box_y = 5, 5
    box_width, box_height = 310, 280
    box_color = (0, 0, 0)
        # Draw the black box
    pygame.draw.rect(screen, box_color, (box_x, box_y, box_width, box_height))

    # Health bar settings
    health_bar_width = 200
    health_bar_height = 20
    health_bar_bg_color = (128, 128, 128)  # Grey background color
    health_bar_color = (0, 255, 0)  # Green health color

    # Calculate the width of the health bar based on the player's resting points
    current_health_width = int((player.restingPoints / 10000) * health_bar_width)

    # Draw the background rectangle of the health bar
    pygame.draw.rect(screen, health_bar_bg_color, (10, 220, health_bar_width, health_bar_height))

    # Draw the current health rectangle
    pygame.draw.rect(screen, health_bar_color, (10, 220, current_health_width, health_bar_height))

    # Draw the resting points text above the health bar
    resting_point_text = font.render(f"Resting Point: {player.restingPoints}", True, TEXT_COLOR)
    #screen.blit(resting_point_text, (10, 10 - resting_point_text.get_height()))



    # Draw the text
    screen.blit(status_text, (10, 10))
    screen.blit(status_text_auto_wc, (10, 40))
    screen.blit(resting_text, (10, 70))

    screen.blit(mining_level_text, (10, 100))
    screen.blit(exp_level_text, (10, 130))
    screen.blit(woodcut_level_text, (10, 160))
    screen.blit(woodcut_xp_text, (10, 190))
    #screen.blit(resting_point_text, (10, 250))


    if show_shop:
        display_shop(screen, font, player)

    if show_smithing:
        display_smithing(screen, font, player)




    # Save the game state
    player.save_state()
    pygame.display.flip()


pygame.quit()
sys.exit()

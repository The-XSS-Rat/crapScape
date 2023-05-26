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
import random
import math
import os
from PIL import Image, ImageChops, ImageOps

# Add the following imports
from health_bar import HealthBar

# Add the following constant
ENEMY_SPEED = 2
all_sprites = pygame.sprite.Group()

# Grid dimensions
rows, columns = 5, 2
cell_size = 100
spacing = 10
pygame.font.init()

last_background_change = pygame.time.get_ticks()


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
SCREEN_WIDTH = screen_info.current_w - 100
SCREEN_HEIGHT = screen_info.current_h - 100
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

FISH_TYPES = [
    {"name": "Minnow", "color": (102, 102, 255), "min_level": 1},
    {"name": "Trout", "color": (0, 153, 153), "min_level": 10},
    {"name": "Salmon", "color": (255, 51, 51), "min_level": 20},
    {"name": "Tuna", "color": (0, 0, 153), "min_level": 30},
    {"name": "Lobster", "color": (255, 80, 0), "min_level": 40},
    {"name": "Swordfish", "color": (0, 51, 102), "min_level": 50},
    {"name": "Shark", "color": (102, 102, 102), "min_level": 60},
    {"name": "Monkfish", "color": (153, 0, 153), "min_level": 70},
    {"name": "Giant Carp", "color": (0, 102, 102), "min_level": 80},
    {"name": "Manta Ray", "color": (0, 204, 204), "min_level": 90},
    {"name": "Anglerfish", "color": (255, 255, 102), "min_level": 100},
    {"name": "Electric Eel", "color": (255, 204, 0), "min_level": 110},
    {"name": "Sea Serpent", "color": (51, 204, 51), "min_level": 120},
    {"name": "Crystal Fish", "color": (153, 255, 255), "min_level": 130},
    {"name": "Firefish", "color": (255, 102, 0), "min_level": 140},
    {"name": "Abyssal Leech", "color": (102, 0, 204), "min_level": 150},
    {"name": "Golden Trout", "color": (255, 204, 0), "min_level": 160},
    {"name": "Phantom Fish", "color": (204, 204, 204), "min_level": 170},
    {"name": "Celestial Tuna", "color": (204, 102, 0), "min_level": 180},
    {"name": "Cosmic Cod", "color": (0, 153, 255), "min_level": 190},
    {"name": "Void Angelfish", "color": (0, 51, 51), "min_level": 200},
    {"name": "Galactic Guppy", "color": (0, 0, 102), "min_level": 210},
    {"name": "Temporal Tetra", "color": (102, 0, 102), "min_level": 220},
    {"name": "Mystic Mackerel", "color": (204, 204, 255), "min_level": 230},
    {"name": "Ethereal Eelpout", "color": (51, 51, 102), "min_level": 240},
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
        self.speed = 1
        self.attack_timer = 0
        self.health = 100
        self.attack_cooldown = 3
        self.attack = 10
        self.auto_wc = False
        self.resting = False
        self.restingPoints = 0
        self.fishing_level = 1
        self.fishing_xp = 0
        self.auto_fish = False
        self.maxRestPoints = 10000


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
            "restingPoints": self.restingPoints,
            "fishing_level": self.fishing_level,
            "fishing_xp": self.fishing_xp,
            "auto_fish": self.auto_fish,
            "speed" : self.speed,
            "maxRestPoints" : self.maxRestPoints
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
                self.fishing_level = state["fishing_level"]
                self.fishing_xp = state["fishing_xp"]
                self.auto_fish = state["auto_fish"]
                self.speed = state["speed"]
                self.maxRestPoints = state["maxRestPoints"]
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

        if self.auto_fish:
            self.move_to_nearest_fish(inLevelFishies)

    def toggle_auto_mine(self):
        self.resting = 0
        self.auto_wc = 0
        self.auto_fish = 0
        self.auto_mine = not self.auto_mine

    def toggle_auto_wc(self):
        self.resting = 0
        self.auto_mine = 0
        self.auto_fish = 0
        self.auto_wc = not self.auto_wc
    
    def toggle_auto_fish(self):
        self.resting = 0
        self.auto_mine = 0
        self.auto_wc = 0
        self.auto_fish = not self.auto_fish


    def toggle_rest(self):
        self.auto_wc = 0
        self.auto_mine = 0
        self.auto_fish = 0
        self.resting = not self.resting

    def rest(self):
        self.auto_mine = 0
        self.auto_wc = 0
        if(self.restingPoints <= self.maxRestPoints):
            self.restingPoints += 1

    def move_to_nearest_rock(self, rocks):
        if player.restingPoints <= 0:
            self.resting = True
            return

        player.restingPoints -= 0.1

        if not rocks:
            clear_rocks()
            add_rocks(np.random.choice(numbers, p=probabilities),selected_map_data)
            return
        nearest_rock = min(rocks, key=lambda rock: self.distance_to(rock))
        if self.distance_to(nearest_rock) < 5 * self.speed:
            self.mining_animation_counter += 1
            if self.mining_animation_counter >= (random.randint(4*nearest_rock.min_level,100*nearest_rock.min_level) + (nearest_rock.min_level/500)) // player.pickaxe["speed_modifier"] :  # Mine a rock every 20 frames                self.mining_animation_counter = 0
                if self.mining_level >= nearest_rock.min_level:
                    rocks.remove(nearest_rock)
                    all_sprites.remove(nearest_rock)
                    self.inventory[nearest_rock.name] = self.inventory.get(nearest_rock.name, 0) + 1
                    add_rocks(random.randint(0, 1),selected_map_data)
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
            self.rect.x += 5 * self.speed * dx / distance
            self.rect.y += 5 * self.speed * dy / distance

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
        if self.distance_to(nearest_tree) < 5 * self.speed:
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
            self.rect.x += 5 * self.speed * dx / distance
            self.rect.y += 5 * self.speed * dy / distance
    
    def move_to_nearest_fish(self,fish):
        if player.restingPoints <= 0:
            self.resting = True
            self.auto_fish = False
            return()
        
        player.restingPoints -= 0.1
        if not fish:
            clear_fish()
            add_fish(np.random.choice(numbers, p=probabilities))
            return
        nearest_fish = min(fish, key=lambda fish: self.distance_to(fish))
        if self.distance_to(nearest_fish) < 5 * self.speed:
            self.mining_animation_counter += 1
            if self.mining_animation_counter >= (random.randint(4*nearest_fish.min_level,100*nearest_fish.min_level) + (nearest_fish.min_level/5000)) // player.pickaxe["speed_modifier"] :
                if self.fishing_level >= nearest_fish.min_level:
                    fish.remove(nearest_fish)
                    all_sprites.remove(nearest_fish)
                    self.inventory[nearest_fish.name] = self.inventory.get(nearest_fish.name, 0) + 1
                    add_fish(random.randint(0, 1))
                    player.save_state()
                    self.fishing_xp += nearest_fish.xp
                    if self.fishing_xp >= self.fishing_level * 100:
                        self.fishing_xp -= self.fishing_level * 100
                        self.fishing_level += 1
            self.image = mining_animation[self.mining_animation_counter // 400]
        else:
            self.image.fill((0, 255, 0))
            dx, dy = nearest_fish.rect.x - self.rect.x, nearest_fish.rect.y - self.rect.y
            distance = math.sqrt(dx * dx + dy * dy)
            self.rect.x += 5 * self.speed * dx / distance
            self.rect.y += 5 * self.speed * dy / distance


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
    

# Fish class
class Fish(pygame.sprite.Sprite):
    def __init__(self, x, y, fish_type):
        super().__init__()

        circle_color = fish_type["color"]        
        
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.draw_random_fish((8, 8),circle_color)  # Call the new method to draw the tree        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
    
        self.rect.x = x
        self.rect.y = y
        self.min_level = fish_type["min_level"]
        self.name = fish_type["name"]
        self.xp = self.min_level * 10
        self.font = pygame.font.Font(None, 14)

      # Draw random rock routine
    def draw_random_fish(self, center, color):
        # Get a list of all images in the directory
        image_dir = "/Users/wesleythijs/crapScape/random_fish_images"
        image_files = [f for f in os.listdir(image_dir) if f.endswith('.png')]

        # Select a random image file
        selected_image_file = random.choice(image_files)

        # Load the image using PIL
        image_path = os.path.join(image_dir, selected_image_file)
        pil_image = Image.open(image_path)

        # Tint the image
        tinted_image = tint_image(pil_image, color)

        # Convert the PIL image to a Pygame Surface
        image = pygame.image.fromstring(tinted_image.tobytes(), tinted_image.size, tinted_image.mode)

        # Position the image's center at the given center
        rect = image.get_rect()
        rect.center = center

        # Draw the image
        self.image.blit(image, rect)



    def draw_name(self, surface):
        text = self.font.render(self.name + "Fish", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.midtop = (self.rect.x + self.rect.width / 2, self.rect.y)
        surface.blit(text, text_rect)

    
def tint_image(image, tint_color, alpha_value=255):
    # Check if the image is already in RGBA mode, if not, convert it
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    # Convert the tint color to RGBA by adding an alpha value
    tint_color = tint_color + (alpha_value,)

    # Create a solid color image with the same dimensions as the input image
    color_image = Image.new("RGBA", image.size, tint_color)

    # Blend the input image and the color image using the input image's alpha channel as a mask
    tinted_image = ImageChops.multiply(image, color_image)

    return tinted_image

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, tree_type):
        super().__init__()
        circle_radius_min = 8
        circle_radius_max = 16
        circle_color = tree_type["color"]
        
        
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.draw_random_tree((8, 8),circle_color)  # Call the new method to draw the tree        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.min_level = tree_type["min_level"]
        self.name = tree_type["name"]
        self.xp = self.min_level * 10
        self.font = pygame.font.Font(None, 14)

    def draw_random_tree(self, center, color):
        # Get a list of all images in the directory
        image_dir = "/Users/wesleythijs/crapScape/random_tree_images"
        image_files = [f for f in os.listdir(image_dir) if f.endswith('.png')]

        # Select a random image file
        selected_image_file = random.choice(image_files)

        # Load the image using PIL
        image_path = os.path.join(image_dir, selected_image_file)
        pil_image = Image.open(image_path)

        # Tint the image
        tinted_image = tint_image(pil_image, color)

        # Convert the PIL image to a Pygame Surface
        image = pygame.image.fromstring(tinted_image.tobytes(), tinted_image.size, tinted_image.mode)

        # Position the image's center at the given center
        rect = image.get_rect()
        rect.center = center

        # Draw the image
        self.image.blit(image, rect)

    def draw_name(self, screen):
        text_surface = self.font.render(self.name + " tree", True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x - (text_surface.get_width() // 2 - self.image.get_width() // 2), self.rect.y - text_surface.get_height()))


# Create the rock class for mining
class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, rock_type):
        super().__init__()
        circle_color = rock_type["color"]

        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.draw_random_rock((8, 8),circle_color)  # Call the new method to draw the tree        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.min_level = rock_type["min_level"]
        self.name = rock_type["name"]
        self.xp = self.min_level * 10
        self.font = pygame.font.Font(None, 14)


    # Draw random rock routine
    def draw_random_rock(self, center, color):
        # Get a list of all images in the directory
        image_dir = "/Users/wesleythijs/crapScape/random_rock_images"
        image_files = [f for f in os.listdir(image_dir) if f.endswith('.png')]

        # Select a random image file
        selected_image_file = random.choice(image_files)

        # Load the image using PIL
        image_path = os.path.join(image_dir, selected_image_file)
        pil_image = Image.open(image_path)

        # Tint the image
        tinted_image = tint_image(pil_image, color)

        # Convert the PIL image to a Pygame Surface
        image = pygame.image.fromstring(tinted_image.tobytes(), tinted_image.size, tinted_image.mode)

        # Position the image's center at the given center
        rect = image.get_rect()
        rect.center = center

        # Draw the image
        self.image.blit(image, rect)

    
    def draw_name(self, screen, rocks_group):
        if self in rocks_group:
            text_surface = self.font.render(self.name + " rock", True, (255, 255, 255))
            screen.blit(text_surface, (self.rect.x - (text_surface.get_width() // 2 - self.image.get_width() // 2), self.rect.y - text_surface.get_height()))

ROCK_TYPE_WEIGHTS = [1 / rock_type["min_level"] for rock_type in ROCK_TYPES]

# Add fish to the game
def add_fish(num_fish):
    for _ in range(num_fish):
        x = random.randint(0, SCREEN_WIDTH - 64)
        y = random.randint(0, SCREEN_HEIGHT - 64)
        fish_type = random.choices(FISH_TYPES, FISH_TYPE_WEIGHTS)[0]
        fish = Fish(x, y, fish_type)
        all_sprites.add(fish)
        fishies.add(fish)
        if fish_type["min_level"] <= player.fishing_level:
            inLevelFishies.add(fish)

# Add rocks to the game
def add_rocks(num_rocks, map_data):
    for _ in range(num_rocks):
        x = random.randint(0, SCREEN_WIDTH - 64)
        y = random.randint(0, SCREEN_HEIGHT - 64)
        rock_type = random.choices(ROCK_TYPES, ROCK_TYPE_WEIGHTS)[0]
        rock = Rock(x, y, rock_type)
        all_sprites.add(rock)
        rocks.add(rock)
        if rock_type["min_level"] <= player.mining_level:
            inLevelRocks.add(rock)


FISH_TYPE_WEIGHTS = [1 / fish_type["min_level"] for fish_type in FISH_TYPES]

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

# Set the path to the random_map_images folder
image_folder = "random_map_images"


# Get a list of all images in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]
map_files = [f for f in os.listdir(image_folder) if f.endswith('.json')]

maps_data = []
for map_file in map_files:
    with open(os.path.join(image_folder, map_file), "r") as file:
        maps_data.append(json.load(file))

# Load the JSON files into Python objects
maps_data = []
for map_file in map_files:
    with open(os.path.join(image_folder, map_file), "r") as file:
        maps_data.append(json.load(file))

# Get a list of all images in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]

# Load the images
backgrounds = [pygame.image.load(os.path.join(image_folder, bg)).convert() for bg in image_files]

# Choose a random index
random_index = random.randint(0, len(maps_data) - 1)

# Select the background and map data using the same index
selected_map_data = maps_data[random_index]
selected_background = backgrounds[random_index]

scaled_background = pygame.transform.scale(selected_background, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Set up the game window and main loop
pygame.display.set_caption("RuneScape Clone - Automated Mining with Levels")
clock = pygame.time.Clock()

player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
rocks = pygame.sprite.Group()
fishies = pygame.sprite.Group()
inLevelFishies = pygame.sprite.Group()
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
add_rocks(np.random.choice(numbers, p=probabilities),selected_map_data)
add_trees(np.random.choice(numbers, p=probabilities))
add_fish(np.random.choice(numbers, p=probabilities))

player.load_state()


show_shop = False
show_smithing = False
rest_button = Button(SCREEN_WIDTH - 150, 10, 140, 40, "Rest", (255, 255, 255), (128, 128, 128))
auto_mine_button = Button(SCREEN_WIDTH - 150, 60, 140, 40, "Toggle Auto Mine", (255, 255, 255), (128, 128, 128))
auto_woodcut_button = Button(SCREEN_WIDTH - 150, 110, 140, 40, "Toggle woodCut", (255, 255, 255), (128, 128, 128))
auto_fish_button = Button(SCREEN_WIDTH - 150, 160, 140, 40, "Toggle Auto Fish", (255, 255, 255), (128, 128, 128))

shop_button = Button(SCREEN_WIDTH - 150, 110, 140, 40, "Open Shop", (255, 255, 255), (128, 128, 128))
smithing_menu = Button(SCREEN_WIDTH - 150, 160, 140, 40, "Open Smithing", (255, 255, 255), (128, 128, 128))
respawn_button = Button(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100, 140, 40, "Respawn rocks", (255, 255, 255), (128, 128, 128))

upgrade_speed_button = Button(SCREEN_WIDTH - 150, 210, 140, 40, "Upgrade Speed", (255, 255, 255), (128, 128, 128))
all_sprites.add(auto_mine_button)
all_sprites.add(auto_woodcut_button)
all_sprites.add(respawn_button)
all_sprites.add(rest_button)
all_sprites.add(auto_fish_button)
all_sprites.add(shop_button)
all_sprites.add(upgrade_speed_button)

def clear_fish():
    fishies.empty()
    for sprite in all_sprites:
        if isinstance(sprite, Fish):
            all_sprites.remove(sprite)

def clear_rocks():
    rocks.empty()
    for sprite in all_sprites:
        if isinstance(sprite, Rock):
            all_sprites.remove(sprite)

def clear_trees():
    trees.empty()
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
                add_rocks(5,selected_map_data)

            elif auto_woodcut_button.is_clicked(event):
                player.toggle_auto_wc()

            elif rest_button.is_clicked(event):
                player.toggle_rest()

            elif auto_fish_button.is_clicked(event):
                player.toggle_auto_fish()

            elif upgrade_speed_button.is_clicked(event):
                if player.mining_level >= 10 * player.speed and player.woodcutting_level >= 10 * player.speed and player.fishing_level >= 10 * player.speed:
                    player.mining_level -= 10 * (player.speed - 1)
                    player.woodcutting_level -= 10 * (player.speed - 1)
                    player.fishing_level -= 10 * (player.speed - 1)
                    player.speed += 1
                    player.maxRestPoints += 100 * (player.maxRestPoints/10000)




    keys_pressed = pygame.key.get_pressed()
    player.update(keys_pressed, rocks, enemies)


    for rock in rocks:
        rock.draw_name(screen, rocks)

    for tree in trees:
        tree.draw_name(screen)

    for fish in fishies:
        fish.draw_name(screen)


    draw_pickaxe(screen, font, player.pickaxe, 10, 130)

     # Get the current time in milliseconds
    current_time = pygame.time.get_ticks()

    # Check if 5 minutes (300,000 milliseconds) have passed since the last background change
    if current_time - last_background_change >= 60000:
        # Choose a new random map background and data
        random_index = random.randint(0, len(maps_data) - 1)
        selected_map_data = maps_data[random_index]
        selected_background = backgrounds[random_index]

        # Scale the new background to fit the screen dimensions
        scaled_background = pygame.transform.scale(selected_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Update the time of the last background change
        last_background_change = current_time



    #screen.fill(BACKGROUND_COLOR)
    all_sprites.draw(screen)


    box_width = 100
    box_height = SCREEN_HEIGHT  # make the box extend to the bottom of the screen
    box_x = SCREEN_WIDTH - box_width
    box_y = 0

    
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
    fishing_level_text = font.render(f"Fishing Level: {player.fishing_level}", True, TEXT_COLOR)
    fishing_xp_text = font.render(f"EXP: {player.fishing_xp}", True, TEXT_COLOR)
    resting_text = font.render(f"Resting: {player.resting}", True, TEXT_COLOR)
    exp_level_text = font.render(f"EXP: {player.mining_xp}", True, TEXT_COLOR)
    speed_text = font.render(f"Speed: {player.speed}", True, TEXT_COLOR)

    # Define the black box parameters
    box_x, box_y = 5, 5
    box_width, box_height = 310, 400
    box_color = (0, 0, 0)
        # Draw the black box
    pygame.draw.rect(screen, box_color, (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))

    # Health bar settings
    health_bar_width = 200
    health_bar_height = 20
    health_bar_bg_color = (128, 128, 128)  # Grey background color
    health_bar_color = (0, 255, 0)  # Green health color

    # Calculate the width of the health bar based on the player's resting points
    
    current_health_width = int((player.restingPoints / player.maxRestPoints) * health_bar_width)

    # Draw the background rectangle of the health bar
    pygame.draw.rect(screen, health_bar_bg_color, (10, 310, health_bar_width, health_bar_height))

    # Draw the current health rectangle
    pygame.draw.rect(screen, health_bar_color, (10, 310, current_health_width, health_bar_height))

    # Draw the resting points text above the health bar
    resting_point_text = font.render(f"Resting Point: {round(player.restingPoints,2)}" + "/" + str(player.maxRestPoints), True, TEXT_COLOR)
    #screen.blit(resting_point_text, (10, 10 - resting_point_text.get_height()))





    # Draw the text
    screen.blit(status_text, (10, 10))
    screen.blit(status_text_auto_wc, (10, 40))
    screen.blit(resting_text, (10, 70))

    screen.blit(mining_level_text, (10, 100))
    screen.blit(exp_level_text, (10, 130))
    screen.blit(woodcut_level_text, (10, 160))
    screen.blit(woodcut_xp_text, (10, 190))
    screen.blit(fishing_level_text, (10, 220))
    screen.blit(fishing_xp_text, (10, 250))
    screen.blit(speed_text, (10, 280))
    screen.blit(resting_point_text, (10, 350))




    if show_shop:
        display_shop(screen, font, player)

    if show_smithing:
        display_smithing(screen, font, player)




    # Save the game state
    player.save_state()
    pygame.display.flip()


pygame.quit()
sys.exit()

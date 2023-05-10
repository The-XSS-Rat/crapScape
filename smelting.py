import pygame


TEXT_COLOR = (255, 255, 255)
SMITHING_ITEMS = [
    {"name": "Bronze Bar", "min_level": 1, "resources": {"Copper": 1}},
    {"name": "Iron Bar", "min_level": 15, "resources": {"Iron": 1}},
    {"name": "Steel Bar", "min_level": 30, "resources": {"Iron": 1, "Coal": 2}},
    # ... add more items
]

def display_smithing(screen, font, player):
    smithing_text = font.render("Smithing", True, TEXT_COLOR)
    screen.blit(smithing_text, (10, 280))

    for index, item in enumerate(SMITHING_ITEMS):
        if player.mining_level >= item["min_level"]:
            item_text = font.render(f"{item['name']} ({item['min_level']}): {', '.join([f'{res} x {amt}' for res, amt in item['resources'].items()])}", True, TEXT_COLOR)
            screen.blit(item_text, (10, 310 + index * 30))


def draw_smelting_menu(screen, font, smelting_options):
    menu_x = 100
    menu_y = 100
    menu_spacing = 40

    for index, option in enumerate(smelting_options):
        option_text = f"{option['name']} - {', '.join([f'{k}: {v}' for k, v in option['resources'].items()])}"
        option_surface = font.render(option_text, True, (255, 255, 255))
        screen.blit(option_surface, (menu_x, menu_y + menu_spacing * index))

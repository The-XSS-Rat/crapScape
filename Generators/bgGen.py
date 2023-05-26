import random
import noise
from PIL import Image, ImageDraw
import os
import json

threshold = 0


def draw_building(draw, x, y, width, height, color):
    x = x - width // 2
    y = y - height // 2
    draw.rectangle([x, y, x + width, y + height], fill=color)

    # Draw roof
    roof_color = (100, 50, 0)
    draw.polygon([(x, y), (x + width, y), (x + width // 2, y - height // 3)], fill=roof_color)

    # Draw windows
    window_color = (255, 255, 255)
    num_windows_x = width // 15
    num_windows_y = height // 15
    window_width = 5
    window_height = 10
    window_spacing_x = (width - window_width * num_windows_x) // (num_windows_x + 1)
    window_spacing_y = (height - window_height * num_windows_y) // (num_windows_y + 1)

    for wx in range(num_windows_x):
        for wy in range(num_windows_y):
            window_x = x + (wx + 1) * window_spacing_x + wx * window_width
            window_y = y + (wy + 1) * window_spacing_y + wy * window_height
            draw.rectangle([window_x, window_y, window_x + window_width, window_y + window_height], fill=window_color)



def generate_map_image(map_type='town', size=(1024, 740), scale=10, seed=None):
    if seed is None:
        seed = random.randint(0, 999999)

    img = Image.new("RGB", size, (0, 0, 0))
    draw = ImageDraw.Draw(img)

    threshold = 0


    water_color = (0, 0, 50)
    sand_color = (0, 0, 102)
    grass_color = (0, 0, 0)
    town_color = (128, 128, 128)
    building_color = (139, 69, 19)
    forest_color = (0, 128, 0)
    mountain_color = (105, 105, 105)
    island_color = (255, 255, 255)

    map_data = []

    for x in range(size[0]):
        row_data = []
        for y in range(size[1]):
            nx = x / size[0] * scale - 0.5
            ny = y / size[1] * scale - 0.5
            elevation = noise.pnoise2(nx + seed, ny + seed, octaves=6, persistence=0.5, lacunarity=2.0)

            if map_type == 'town':
                threshold = -0.1
            elif map_type == 'dungeon':
                threshold = 0.1

            if elevation < threshold:
                color = water_color
                section = 'water'
            elif threshold <= elevation < threshold + 0.02:
                color = sand_color
                section = 'land'
            else:
                color = grass_color if map_type == 'town' else town_color
                section = 'land'

            # Add forests
            if elevation >= 0.1 and random.random() < 0.1:
                color = forest_color

            # Add mountains
            if elevation >= 0.3 and random.random() < 0.2:
                color = mountain_color

            draw.point((x, y), fill=color)
            row_data.append(section)

            if (map_type == 'town' or map_type=='cave' or map_type=='island' or map_type=='mountain') and (color == grass_color or color == forest_color or color == mountain_color or color == island_color) and random.random() < 0.0001:
                building_width = random.randint(10, 30)
                building_height = random.randint(10, 30)
                draw_building(draw, x - building_width // 2, y - building_height // 2, building_width, building_height, building_color)

            # Add rivers
            if elevation >= 0.02 and elevation <= 0.05 and random.random() < 0.001:
                river_length = random.randint(10, 30)
                river_color = water_color
                river_width = 2
                for i in range(river_length):
                    dx = random.randint(-1, 1)
                    dy = random.randint(-1, 1)
                    x_river = x + dx * i
                    y_river = y + dy * i
                    if 0 <= x_river < size[0] and 0 <= y_river < size[1]:
                        draw.line((x_river, y_river, x_river + river_width, y_river + river_width), fill=river_color, width=river_width)

        map_data.append(row_data)

    return img, map_data




output_dir = "random_map_images"
os.makedirs(output_dir, exist_ok=True)

num_maps = 5

for i in range(num_maps):
    map_type = random.choice(['town', 'dungeon', 'forest', 'desert', 'mountain', 'cave', 'island'])  # Add the new map types to the list of choices

    img, map_data = generate_map_image(map_type=map_type)
    img.save(os.path.join(output_dir, f"{map_type}_map_{i+1}.png"))

    json_data = {'map_type': map_type, 'map_data': map_data}
    json_file_path = os.path.join(output_dir, f"{map_type}_map_{i+1}.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file)

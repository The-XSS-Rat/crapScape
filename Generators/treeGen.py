import os
import random
from PIL import Image, ImageDraw

# Function to generate random tree
def generate_tree_image(size=(16, 16)):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    tree_color = (random.randint(0, 255), random.randint(100, 255), random.randint(0, 255), 255)
    trunk_color = (139, 69, 19, 255)

    # Draw the trunk
    trunk_width = random.randint(2, 5)
    trunk_height = random.randint(3, 5)
    trunk_x = size[0] // 2 - trunk_width // 2
    trunk_y = size[1] - trunk_height
    draw.rectangle([trunk_x, trunk_y, trunk_x + trunk_width, trunk_y + trunk_height], fill=trunk_color)

    # Draw the foliage
    foliage_width = random.randint(10, 16)
    foliage_height = random.randint(8, 12)
    foliage_x = size[0] // 2 - foliage_width // 2
    foliage_y = trunk_y - foliage_height
    draw.ellipse([foliage_x, foliage_y, foliage_x + foliage_width, foliage_y + foliage_height], fill=tree_color)

    return img


# Generate and save random tree images
output_dir = "random_tree_images"
os.makedirs(output_dir, exist_ok=True)

num_images = 100  # Specify the number of images you want to generate

for i in range(num_images):
    img = generate_tree_image()
    img.save(os.path.join(output_dir, f"tree_{i+1}.png"))

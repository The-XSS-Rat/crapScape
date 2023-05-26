import os
import random
from PIL import Image, ImageDraw

def generate_rock_image(size=(16, 16)):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    rock_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255), 255)

    # Draw the rock
    rock_width = random.randint(10, 16)
    rock_height = random.randint(8, 12)
    rock_x = size[0] // 2 - rock_width // 2
    rock_y = size[1] // 2 - rock_height // 2
    draw.ellipse([rock_x, rock_y, rock_x + rock_width, rock_y + rock_height], fill=rock_color)

    return img

# Generate and save random rock images
output_dir = "random_rock_images"
os.makedirs(output_dir, exist_ok=True)

num_images = 100  # Specify the number of images you want to generate

for i in range(num_images):
    img = generate_rock_image()
    img.save(os.path.join(output_dir, f"rock_{i+1}.png"))

import os
import random
from PIL import Image, ImageDraw

def generate_fish_image(size=(16, 16)):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    fish_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)

    # Draw the fish body
    body_width = random.randint(6, 10)
    body_height = random.randint(2, 6)
    body_x = size[0] // 2 - body_width // 2
    body_y = size[1] // 2 - body_height // 2
    draw.ellipse([body_x, body_y, body_x + body_width, body_y + body_height], fill=fish_color)

    # Draw the fish tail
    tail_width = random.randint(2, 4)
    tail_height = random.randint(4, 8)
    tail_x = body_x + body_width
    tail_y = size[1] // 2 - tail_height // 2
    draw.polygon([tail_x, tail_y, tail_x + tail_width, size[1] // 2, tail_x, tail_y + tail_height], fill=fish_color)

    return img

# Generate and save random fish images
output_dir = "random_fish_images"
os.makedirs(output_dir, exist_ok=True)

num_images = 100  # Specify the number of images you want to generate

for i in range(num_images):
    img = generate_fish_image()
    img.save(os.path.join(output_dir, f"fish_{i+1}.png"))

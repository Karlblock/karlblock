#!/usr/bin/env python3
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random

# Message secret pour le CTF
secret_message = "CYBA{L4UNCH_CTF_2025_J01N_TH3_W4RF4R3}"

# Créer une image de base - format bannière
width, height = 1200, 400
# Fond noir profond style espace
image = Image.new('RGB', (width, height), color=(2, 2, 10))
draw = ImageDraw.Draw(image)

# Créer un fond étoilé
for _ in range(300):
    x = random.randint(0, width)
    y = random.randint(0, height)
    brightness = random.randint(100, 255)
    size = random.choice([1, 1, 1, 2])
    
    if size == 1:
        draw.point((x, y), fill=(brightness, brightness, brightness))
    else:
        draw.ellipse([x-1, y-1, x+1, y+1], fill=(brightness, brightness, brightness))

# Quelques étoiles brillantes
for _ in range(15):
    x = random.randint(0, width)
    y = random.randint(0, height)
    # Étoile avec effet de croix
    draw.ellipse([x-2, y-2, x+2, y+2], fill=(255, 255, 255))
    draw.line([x-4, y, x+4, y], fill=(128, 128, 128))
    draw.line([x, y-4, x, y+4], fill=(128, 128, 128))

# Fonts
try:
    font_huge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 140)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
except:
    font_huge = ImageFont.load_default()
    font = ImageFont.load_default()

# CYBA en gros au centre
cyba_text = "CYBA"
# Couleur CYBA Universe (cyan comme dans le repo)
cyba_color = (6, 182, 212)  # Cyan-500 (#06B6D4)

# Mesurer le texte
bbox = font_huge.getbbox(cyba_text)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (width - text_width) // 2
y = (height - text_height) // 2 - 20

# Effet de lueur simple
for offset in [4, 3, 2, 1]:
    draw.text((x-offset, y), cyba_text, font=font_huge, fill=(3, 91, 106))
    draw.text((x+offset, y), cyba_text, font=font_huge, fill=(3, 91, 106))
    draw.text((x, y-offset), cyba_text, font=font_huge, fill=(3, 91, 106))
    draw.text((x, y+offset), cyba_text, font=font_huge, fill=(3, 91, 106))

# Texte principal CYBA
draw.text((x, y), cyba_text, font=font_huge, fill=cyba_color)

# Sous-titre
subtitle = "CYBER WARFARE DEFENSE"
bbox2 = font.getbbox(subtitle)
subtitle_width = bbox2[2] - bbox2[0]
subtitle_x = (width - subtitle_width) // 2
draw.text((subtitle_x, y + text_height + 10), subtitle, font=font, fill=(96, 165, 250))

# Cacher le message dans les LSB
pixels = np.array(image)
binary_secret = ''.join(format(ord(char), '08b') for char in secret_message)
data_index = 0

for i in range(50, 150):
    for j in range(50, 150):
        if data_index < len(binary_secret):
            r, g, b = pixels[i, j]
            r = (r & 0xFE) | int(binary_secret[data_index])
            pixels[i, j] = (r, g, b)
            data_index += 1

# Sauvegarder
stego_image = Image.fromarray(pixels.astype('uint8'))
stego_image.save('/home/user1/karlblock/assets/cyba-launch-signal.png')

print(f"Bannière créée avec la couleur cyan CYBA Universe!")
print(f"Message caché: {secret_message}")
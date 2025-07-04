#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import random

# Créer la bannière
width, height = 1200, 400
image = Image.new('RGB', (width, height), color=(2, 2, 10))
draw = ImageDraw.Draw(image)

# Étoiles simples
for _ in range(200):
    x = random.randint(0, width)
    y = random.randint(0, height)
    brightness = random.randint(100, 255)
    draw.point((x, y), fill=(brightness, brightness, brightness))

# Font par défaut
font = ImageFont.load_default()

# CYBA centré - couleur cyan du repo
cyba_color = (6, 182, 212)
text = "CYBA"
# Position approximative au centre
x = width // 2 - 50
y = height // 2 - 20

# Texte simple
draw.text((x, y), text, font=font, fill=cyba_color)

# Sauvegarder
image.save('/home/user1/karlblock/assets/cyba-banner-test.png')
print("Bannière créée!")
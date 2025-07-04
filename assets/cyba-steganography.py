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

# Créer un fond étoilé - constellation
stars = []
for _ in range(200):  # Petites étoiles
    x = random.randint(0, width)
    y = random.randint(0, height)
    brightness = random.randint(150, 255)
    size = 1
    stars.append((x, y, brightness, size))

for _ in range(50):  # Étoiles moyennes
    x = random.randint(0, width)
    y = random.randint(0, height)
    brightness = random.randint(200, 255)
    size = 2
    stars.append((x, y, brightness, size))

for _ in range(10):  # Grandes étoiles brillantes
    x = random.randint(0, width)
    y = random.randint(0, height)
    brightness = 255
    size = 3
    stars.append((x, y, brightness, size))

# Dessiner les étoiles
for star in stars:
    x, y, brightness, size = star
    if size == 1:
        draw.point((x, y), fill=(brightness, brightness, brightness))
    elif size == 2:
        draw.ellipse([x-1, y-1, x+1, y+1], fill=(brightness, brightness, brightness))
    else:
        # Étoile avec effet de croix pour les plus brillantes
        draw.ellipse([x-2, y-2, x+2, y+2], fill=(brightness, brightness, brightness))
        draw.line([x-3, y, x+3, y], fill=(brightness//2, brightness//2, brightness//2))
        draw.line([x, y-3, x, y+3], fill=(brightness//2, brightness//2, brightness//2))

# Texte principal
try:
    font_huge = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf", 120)
    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 30)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 16)
except:
    try:
        font_huge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 120)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 30)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
    except:
        font_huge = ImageFont.load_default()
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()

# CYBA en gros au centre
cyba_text = "CYBA"
# Calculer la taille du texte pour le centrer
bbox = draw.textbbox((0, 0), cyba_text, font=font_huge)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (width - text_width) // 2
y = (height - text_height) // 2

# Couleur CYBA Universe (cyan comme dans le repo)
cyba_color = (6, 182, 212)  # Cyan-500 (#06B6D4)
glow_color = (34, 211, 238)  # Cyan-400 (#22d3ee) pour la lueur

# Effet de lueur simple
for offset in range(10, 0, -1):
    alpha = int(80 - (offset * 8))
    if alpha > 0:
        # Lueur horizontale
        draw.text((x-offset, y), cyba_text, font=font_huge, fill=(glow_color[0]//2, glow_color[1]//2, glow_color[2]//2))
        draw.text((x+offset, y), cyba_text, font=font_huge, fill=(glow_color[0]//2, glow_color[1]//2, glow_color[2]//2))
        # Lueur verticale
        draw.text((x, y-offset), cyba_text, font=font_huge, fill=(glow_color[0]//2, glow_color[1]//2, glow_color[2]//2))
        draw.text((x, y+offset), cyba_text, font=font_huge, fill=(glow_color[0]//2, glow_color[1]//2, glow_color[2]//2))

# Texte principal CYBA
draw.text((x, y), cyba_text, font=font_huge, fill=cyba_color)

# Sous-titre centré avec gradient de couleur
subtitle = "CYBER WARFARE DEFENSE"
bbox_subtitle = draw.textbbox((0, 0), subtitle, font=font)
subtitle_width = bbox_subtitle[2] - bbox_subtitle[0]
subtitle_x = (width - subtitle_width) // 2
# Couleur plus cyan/bleu pour rester dans le thème
draw.text((subtitle_x, y + text_height + 20), subtitle, font=font, fill=(96, 165, 250))  # Blue-400

# Convertir le message secret en binaire
binary_secret = ''.join(format(ord(char), '08b') for char in secret_message)

# Cacher le message dans les LSB (Least Significant Bits)
pixels = np.array(image)
data_index = 0

for i in range(50, 150):  # Zone spécifique où cacher le message
    for j in range(50, 150):
        if data_index < len(binary_secret):
            # Modifier le LSB du canal rouge
            r, g, b = pixels[i, j]
            r = (r & 0xFE) | int(binary_secret[data_index])
            pixels[i, j] = (r, g, b)
            data_index += 1

# Sauvegarder l'image avec le message caché
stego_image = Image.fromarray(pixels.astype('uint8'))
stego_image.save('/home/user1/karlblock/assets/cyba-launch-signal.png')

# Créer aussi un script pour extraire le message
extractor_script = '''#!/usr/bin/env python3
# CYBA CTF - Signal Analyzer
# Can you decode the transmission?

from PIL import Image
import sys

def extract_lsb(image_path):
    """Extract hidden message from LSB"""
    try:
        img = Image.open(image_path)
        pixels = img.load()
        
        binary_data = ""
        # Scan the specific area
        for i in range(50, 150):
            for j in range(50, 150):
                pixel = pixels[j, i]
                binary_data += str(pixel[0] & 1)
        
        # Convert binary to text
        message = ""
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            if len(byte) == 8:
                char = chr(int(byte, 2))
                if char.isprintable():
                    message += char
                else:
                    break
        
        return message
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 signal_analyzer.py <image_path>")
        sys.exit(1)
    
    result = extract_lsb(sys.argv[1])
    print(f"Decoded transmission: {result}")
'''

with open('/home/user1/karlblock/assets/signal_analyzer.py', 'w') as f:
    f.write(extractor_script)

print("Stéganographie créée avec succès!")
print(f"Message caché: {secret_message}")
print("Image sauvegardée: /home/user1/karlblock/assets/cyba-launch-signal.png")
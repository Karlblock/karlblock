#!/usr/bin/env python3
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

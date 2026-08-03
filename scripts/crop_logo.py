from PIL import Image
import os

site_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../site'))
favicon_path = os.path.join(site_dir, 'favicon.png')
logo_path = os.path.join(site_dir, 'owgt-rewards-logo.png')

img = Image.open(favicon_path)
if img.mode != 'RGBA':
    img = img.convert('RGBA')

# Get tight bounding box of non-transparent content
bbox = img.getbbox()
print(f"Original size: {img.size}, bbox: {bbox}")

if bbox:
    # Crop to exact bounding box
    cropped = img.crop(bbox)
    print(f"Cropped size: {cropped.size}")
    
    # Save cropped image to owgt-rewards-logo.png
    cropped.save(logo_path, format='PNG')
    print(f"Successfully saved cropped logo to {logo_path}")
else:
    print("Could not determine bounding box.")

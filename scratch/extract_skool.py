import os
import glob
import re

source_dir = 'organized-data/skool-communites/guides'
dest_dir = 'organized-data/Guides'
os.makedirs(dest_dir, exist_ok=True)

files = glob.glob(f"{source_dir}/*.md")

for filepath in files:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        
    # Generate Name from filename
    name = filename.replace('.md', '').replace('-', ' ').title()
    
    # Generate Description from first paragraph
    first_p = ""
    lines = content.split('\n')
    for line in lines:
        clean_line = line.strip()
        if clean_line and not clean_line.startswith('#') and not clean_line.startswith('-') and not clean_line.startswith('*'):
            first_p = clean_line
            break
            
    if len(first_p) > 150:
        first_p = first_p[:147] + "..."
    if not first_p:
        first_p = f"A guide on {name.lower()}."
        
    # Build new content
    new_content = f"### Name\n{name}\n\n### Description\n{first_p}\n\n### Content\n\n{content}\n\n### Category\nGuides\n\n### Tags\n- Skool\n- Community\n- Guide\n"
    
    # Write to new location
    dest_path = os.path.join(dest_dir, filename)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

print(f"Processed {len(files)} skool guides.")

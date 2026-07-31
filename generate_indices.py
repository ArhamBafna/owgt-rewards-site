import os
import json
import re

def generate_indices():
    base_dir = 'c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/organized-data'
    
    data = {}
    
    for root, dirs, files in os.walk(base_dir):
        category_dir = os.path.basename(root)
        if root == base_dir:
            continue
            
        cat_key = category_dir.lower()
        if cat_key not in data:
            data[cat_key] = []
            
        for file in files:
            if file.endswith('.md') and file not in ['README.md']:
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, base_dir).replace('\\', '/')
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                name_match = re.search(r'### (?:Name|Title)\n(.*?)(?=\n### |$)', content, re.IGNORECASE | re.DOTALL)
                name = name_match.group(1).strip() if name_match else os.path.splitext(file)[0]
                
                data[cat_key].append({
                    "name": name,
                    "path": rel_path
                })
                
    # Sort everything
    for k in data:
        data[k] = sorted(data[k], key=lambda x: x['name'].lower())
        
    # Write master.json
    with open(os.path.join(base_dir, 'master.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    # Write master.md
    with open(os.path.join(base_dir, 'master.md'), 'w', encoding='utf-8') as f:
        f.write("# Master Index\n\n")
        f.write("This index is automatically generated.\n\n")
        
        for cat in sorted(data.keys()):
            f.write(f"## {cat.title()}\n\n")
            for item in data[cat]:
                f.write(f"- [{item['name']}]({item['path']})\n")
            f.write("\n")

if __name__ == '__main__':
    generate_indices()

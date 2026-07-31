import os
import json

base_dir = 'organized-data'
exclude_dirs = ['pdfs-to-text', 'skool-communites', 'youtube']

data = {}

for root, dirs, files in os.walk(base_dir):
    # filter out excluded dirs
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    
    for file in files:
        if file.endswith('.md') and file not in ['README.md', 'master.md', 'decisions.md']:
            rel_dir = os.path.relpath(root, base_dir)
            if rel_dir == '.':
                continue
                
            cat = rel_dir
            if cat not in data:
                data[cat] = []
                
            filepath = os.path.join(root, file)
            name = file.replace('.md', '').replace('-', ' ').title()
            
            # extract real name from file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip() == '### Name' and i + 1 < len(lines):
                        name = lines[i+1].strip()
                        break
                        
            data[cat].append({
                "name": name,
                "path": f"{cat}/{file}".replace('\\', '/')
            })

# Sort items inside categories
for cat in data:
    data[cat] = sorted(data[cat], key=lambda x: x['name'].lower())

# Sort categories
sorted_cats = sorted(data.keys())

# write json
with open(os.path.join(base_dir, 'master.json'), 'w', encoding='utf-8') as f:
    # use lowercase keys for json
    json_data = {k.lower(): v for k, v in data.items()}
    json.dump(json_data, f, indent=2)

# write md
with open(os.path.join(base_dir, 'master.md'), 'w', encoding='utf-8') as f:
    f.write("# Master Index\n\n")
    for cat in sorted_cats:
        f.write(f"## {cat}\n")
        for item in data[cat]:
            f.write(f"- [{item['name']}]({item['path']})\n")
        f.write("\n")

print("Master indexes generated.")

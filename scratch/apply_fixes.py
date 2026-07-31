import os
import glob
import re

print("Starting fixes...")

# 1. Fix Legacy Formatting
legacy_file = "organized-data/Guides/prompt-engineering.md"
if os.path.exists(legacy_file):
    with open(legacy_file, 'r', encoding='utf-8') as f:
        content = f.read()
    if "# Prompt Engineering Guide\n" in content:
        content = content.replace("# Prompt Engineering Guide\n", "### Name\nPrompt Engineering Guide\n")
        with open(legacy_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Fixed prompt-engineering.md")

# 2. Delete Garbage Prompts from Prompts/
prompts = glob.glob("organized-data/Prompts/*.md")
garbage_count = 0
for filepath in prompts:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for empty descriptions from prompts.txt
    if "### Description\nA prompt for  tasks." in content or "### Description\nA prompt for tasks." in content:
        os.remove(filepath)
        garbage_count += 1
        continue
        
    # Check for website architecture notes
    if "navbar" in filepath.lower() or "floating-island" in filepath.lower() or "hero-section" in filepath.lower() \
       or "protocol-sticky" in filepath.lower() or "footer-deep" in filepath.lower() \
       or "preset-" in filepath.lower() or "card-" in filepath.lower():
        os.remove(filepath)
        garbage_count += 1
        continue

print(f"Deleted {garbage_count} garbage prompts.")

# 3. Fix Descriptions (AI Tools, AI Skills, Claude Prompts)
all_files = glob.glob("organized-data/**/*.md", recursive=True)
fixed_desc = 0

for filepath in all_files:
    if os.path.basename(filepath) in ['README.md', 'master.md', 'decisions.md']:
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "Extracted from" not in content:
        continue
        
    # Find Name
    name_match = re.search(r'### Name\n(.*?)\n', content)
    name = name_match.group(1).strip() if name_match else os.path.basename(filepath)
    
    new_desc = ""
    
    if "Prompts" in filepath:
        new_desc = f"A powerful prompt to {name.lower()}."
        
    elif "Tools" in filepath:
        # Try to find "What it does:"
        what_match = re.search(r'\*\*What it does:\*\* (.*?)(Workflow it replaces:|Business outcome:|Best for:|$)', content, re.DOTALL)
        if what_match:
            new_desc = what_match.group(1).replace('\n', ' ').strip()
        else:
            new_desc = f"An AI tool for {name.lower()}."
            
    elif "Learning" in filepath or "Skills" in filepath:
        # Try to find "What it is:"
        what_match = re.search(r'What it is: (.*?)(Who is hiring:|Advanced:|Tool to start:|$)', content, re.DOTALL | re.IGNORECASE)
        if what_match:
            new_desc = what_match.group(1).replace('\n', ' ').strip()
        else:
            new_desc = f"An essential AI skill regarding {name.lower()}."
            
    if new_desc:
        # replace the old description
        content = re.sub(r'### Description\n(.*?)(###|$)', f'### Description\n{new_desc}\n\n\\2', content, flags=re.DOTALL)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_desc += 1

print(f"Fixed descriptions for {fixed_desc} files.")

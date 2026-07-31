import os
import glob
import re

prompts_dir = os.path.join("organized-data", "Prompts")
for filepath in glob.glob(os.path.join(prompts_dir, "*.md")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace "Use this prompt for [title]." with "A strategic template for [title]."
    new_content = re.sub(r'Use this prompt for ([^.]+)\.', r'A strategic template to \1.', content)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

print("Fixed lazy descriptions.")

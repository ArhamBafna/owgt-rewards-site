import os
import glob

tools = glob.glob("organized-data/Tools/*.md")
count = 0
for t in tools:
    with open(t, 'r', encoding='utf-8') as f:
        content = f.read()
    if "**What it does:**" in content or "Workflow being replaced" in content:
        os.remove(t)
        count += 1
print(f"Deleted {count} corrupted AI tools.")

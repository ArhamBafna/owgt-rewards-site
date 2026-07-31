import os
import re

with open('organized-data/prompts.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split by the weird header icons or capital text like "dY\"? CONTENT CREATION PROMPTS"
# Actually, let's just parse line by line.

categories = {
    "CONTENT CREATION": "Marketing",
    "EMAIL & COMMUNICATION": "Communication",
    "MARKETING & SALES": "Marketing",
    "SALES & MARKETING": "Marketing",
    "PRODUCTIVITY & WORKFLOW": "Productivity",
    "BUSINESS STRATEGY": "Business",
    "BUSINESS": "Business",
    "CODING": "Coding",
    "RESEARCH": "Research"
}

os.makedirs('organized-data/Prompts', exist_ok=True)
with open('organized-data/Prompts/README.md', 'w') as f:
    f.write("# Prompts\n\nThis folder contains standalone, high-value prompts categorized by use case. Each prompt should be directly usable without needing additional context.\n")

lines = text.split('\n')
current_category = "Miscellaneous"

prompts_extracted = 0
prompts_skipped = 0

for line in lines:
    line = line.strip()
    if not line:
        continue
        
    # Detect category headers
    if "PROMPTS" in line.upper():
        for key, val in categories.items():
            if key in line.upper():
                current_category = val
                break
        continue
        
    # Match pattern: Name: 'Prompt text' or Name: "Prompt text"
    match = re.match(r"^([^:]+):\s*['\"](.*)['\"]$", line)
    if not match:
        match = re.match(r"^([^:]+):\s*(.*)$", line) # fallback without quotes
        
    if match:
        title = match.group(1).strip()
        prompt_text = match.group(2).strip()
        
        # QUALITY FILTER
        word_count = len(prompt_text.split())
        # Reject generic one-liners
        if word_count < 12 and "['" not in prompt_text and "[" not in prompt_text:
            prompts_skipped += 1
            continue
            
        if len(title) > 40: # Probably not a title
            continue
            
        desc = f"A prompt for {title.lower()} tasks."
        
        # Tags
        tags = [current_category, "Prompt", title.split()[0]]
        
        content = f"### Title\n{title}\n\n### Description\n{desc}\n\n### Prompt\n```text\n{prompt_text}\n```\n\n### Category\n{current_category}\n\n### Tags\n"
        for t in tags:
            if len(t) > 2:
                content += f"- {t.title()}\n"
                
        safe_title = title.lower()
        safe_title = re.sub(r'[^a-z0-9\-]', '-', safe_title)
        safe_title = re.sub(r'-+', '-', safe_title).strip('-')
        if not safe_title:
            safe_title = f"prompt-{prompts_extracted}"
        filepath = f"organized-data/Prompts/{safe_title}.md"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        prompts_extracted += 1

print(f"Extracted {prompts_extracted} prompts, skipped {prompts_skipped} low-quality/short prompts.")

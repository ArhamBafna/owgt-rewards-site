import os
import re

with open('data/prompts.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# We know categories are separated by lines containing "PROMPTS"
blocks = content.split('\n\n')

prompts = []
current_category = "General"

for block in blocks:
    block = block.strip()
    if not block:
        continue
        
    if "PROMPTS" in block and len(block.split('\n')) == 1:
        current_category = block.replace('dY"?', '').replace('dY"', '').strip()
        continue
        
    # Check for Master Prompt v3
    if "MASTER PROMPT v3" in block:
        prompts.append({
            "title": "Cinematic Real Estate Listing Video",
            "prompt": block,
            "category": "Video"
        })
        continue
        
    if "Higgsfield UGC Prompt" in block:
        prompts.append({
            "title": "Higgsfield UGC Prompt",
            "prompt": block,
            "category": "Video"
        })
        continue
        
    # Standard single line or colon format
    # Example: "Week of Captions: 'Write 5 social media captions...'"
    match = re.match(r"^([^:]+):\s*['\"]?(.*)$", block, re.DOTALL)
    if match:
        title = match.group(1).strip()
        text = match.group(2).strip().strip("'").strip('"')
        
        # Quality check as per instructions
        if len(text.split()) > 15 or '[' in text:
            prompts.append({
                "title": title,
                "prompt": text,
                "category": current_category
            })
            
for i, p in enumerate(prompts):
    print(f"--- Prompt {i+1} ---")
    print(f"Title: {p['title']}")
    print(f"Category: {p['category']}")
    print(f"Length: {len(p['prompt'].split())} words")
    print(f"Preview: {p['prompt'][:100]}...\n")

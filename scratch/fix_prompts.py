import os
import glob
import re

# 1. Clean up old bad extractions from prompts.txt
old_prompts = glob.glob("organized-data/Prompts/*.md")
deleted_count = 0
for f in old_prompts:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    # If the file was extracted from prompts.txt (identified by the old categories)
    if re.search(r'### Category\n(CONTENT CREATION|EMAIL & COMMUNICATION|MARKETING & SALES|PRODUCTIVITY & WORKFLOW|BUSINESS STRATEGY|BUSINESS|CODING|RESEARCH)', content, re.IGNORECASE):
        os.remove(f)
        deleted_count += 1
    # Also delete files that have extremely short prompts (the bad ones that slipped through)
    elif "### Prompt\n```text\n" in content:
        prompt_match = re.search(r'### Prompt\n```text\n(.*?)```', content, re.DOTALL)
        if prompt_match:
            prompt_len = len(prompt_match.group(1).split())
            if prompt_len < 10:
                os.remove(f)
                deleted_count += 1
                
print(f"Deleted {deleted_count} bad/old prompts.")

# 2. Extract perfectly from prompts.txt
with open('data/prompts.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Custom manual categories mapping based on visual inspection
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

blocks = text.split('\n\n')

prompts_extracted = 0
current_category = "General"

def safe_filename(name):
    safe_name = name.lower()
    safe_name = re.sub(r'[^a-z0-9\-]', '-', safe_name)
    safe_name = re.sub(r'-+', '-', safe_name).strip('-')
    return safe_name[:60]

# Add logic to handle the complex multi-line ones that don't use ":"
multi_line_prompts = []

for block in blocks:
    block = block.strip()
    if not block:
        continue
        
    # Check for category header
    if "PROMPTS" in block.upper() and len(block.split('\n')) == 1:
        clean_cat = re.sub(r'[^a-zA-Z\s&]', '', block).replace('PROMPTS', '').strip()
        if clean_cat in categories:
            current_category = categories[clean_cat]
        else:
            current_category = clean_cat.title() if clean_cat else "General"
        continue
        
    # Check for Master Prompt v3
    if "MASTER PROMPT v3" in block or "Cinematic Real Estate Listing Video" in block:
        multi_line_prompts.append({
            "title": "Cinematic Real Estate Listing Video",
            "prompt": block,
            "category": "Video"
        })
        continue
        
    if "Higgsfield UGC Prompt" in block:
        multi_line_prompts.append({
            "title": "Higgsfield UGC Prompt",
            "prompt": block,
            "category": "Video"
        })
        continue
        
    # Match standard single line "Title: 'Prompt'"
    match = re.match(r"^([^:]+):\s*['\"]?(.*)$", block, re.DOTALL)
    if match:
        title = match.group(1).strip()
        prompt_text = match.group(2).strip().strip("'").strip('"')
        
        # QUALITY FILTER from organizer-spec.md
        # Must be usable without context. Trash short/waste prompts.
        word_count = len(prompt_text.split())
        if word_count < 12 and "[" not in prompt_text:
            continue
            
        desc = f"A prompt for {title.lower()} tasks."
        tags = [current_category, "Prompt", title.split()[0].title()]
        
        content_md = f"### Name\n{title}\n\n### Description\n{desc}\n\n### Prompt\n```text\n{prompt_text}\n```\n\n### Category\n{current_category}\n\n### Tags\n"
        for t in tags:
            if len(t) > 2:
                content_md += f"- {t}\n"
                
        fname = safe_filename(title)
        if not fname:
            fname = f"prompt-{prompts_extracted}"
            
        filepath = f"organized-data/Prompts/{fname}.md"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content_md)
            
        prompts_extracted += 1

# Process multi-line ones
# In the file, the Master Prompt v3 is spread across multiple blocks due to \n\n.
# We should actually use the whole file content to extract the master prompts by finding their boundaries.
master_prompt_match = re.search(r'MASTER PROMPT v3.*?================================================================(.*?)(---|$)', text, re.DOTALL)
if master_prompt_match:
    full_prompt = master_prompt_match.group(1).strip()
    content_md = f"### Name\nCinematic Real Estate Listing Video\n\n### Description\nA master prompt for generating cinematic real estate listing videos using Higgsfield and Claude.\n\n### Prompt\n```text\n{full_prompt}\n```\n\n### Category\nVideo\n\n### Tags\n- Video\n- Prompt\n- Real Estate\n"
    with open('organized-data/Prompts/cinematic-real-estate-listing.md', 'w', encoding='utf-8') as f:
        f.write(content_md)
    prompts_extracted += 1

ugc_prompt_match = re.search(r'Higgsfield UGC Prompt\n\n(.*)', text, re.DOTALL)
if ugc_prompt_match:
    full_prompt = ugc_prompt_match.group(1).strip()
    content_md = f"### Name\nHiggsfield UGC Prompt\n\n### Description\nA detailed prompt for creating an authentic UGC selfie video using Higgsfield.\n\n### Prompt\n```text\n{full_prompt}\n```\n\n### Category\nVideo\n\n### Tags\n- Video\n- Prompt\n- UGC\n"
    with open('organized-data/Prompts/higgsfield-ugc-prompt.md', 'w', encoding='utf-8') as f:
        f.write(content_md)
    prompts_extracted += 1

print(f"Extracted {prompts_extracted} valid, accurate prompts from prompts.txt.")

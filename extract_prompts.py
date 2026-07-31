import os
import re

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s-]+', '-', s)
    return s

files = [
    "data/pdfs-to-text/V1 - 50 Claude Prompts Every Founder Should Bookmark-text.txt",
    "data/pdfs-to-text/V1 -  The AI Decision Playbook 25 Claude Prompts for Better Business Decisions-text.txt",
    "data/pdfs-to-text/THE AI REPORT - 75 CLAUDE PROMPTS-text.txt",
    "data/pdfs-to-text/(V1) 37 CLAUDE PROMPTS THAT SAVE MANAGERS 10+ HOURS PER WEEK Organised by the 8 Situations Every Manager Faces-text.txt"
]

prompt_pattern = re.compile(r'^\d{1,2}\.\s+([A-Za-z0-9\s\'-]+)\n([^\n].*?(?=\n\d{1,2}\.|\Z|\n\s*\n))', re.DOTALL | re.MULTILINE)

created_count = 0

for fpath in files:
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # We clean up some common OCR artifacts like "3 years covering AI for business leaders daily |"
    content = re.sub(r'3 years covering AI for business leaders daily.*?\n', '', content)
    content = re.sub(r'The AI Decision Playbook \| The AI Report.*?\n', '', content)
    
    matches = prompt_pattern.findall(content)
    for title, prompt_text in matches:
        title = title.strip()
        if len(title) > 100 or len(title) < 5:
            continue
            
        filename = slugify(title) + ".md"
        out_path = os.path.join("organized-data", "Prompts", filename)
        
        prompt_text = prompt_text.strip().strip('"').replace('\n', ' ')
        
        # Filter low-value generic prompts
        if len(prompt_text) < 50 or "hello" in prompt_text.lower():
            continue
            
        md_content = f"### Name\n{title}\n\n### Description\nUse this prompt for {title.lower()}.\n\n### Content\n```\n{prompt_text}\n```\n\n### Category\nPrompts\n\n### Tags\n- Claude\n- Prompt\n"
        
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        # overwrite it to be safe
        with open(out_path, "w", encoding="utf-8") as out_f:
            out_f.write(md_content)
        created_count += 1

print(f"Created {created_count} prompt files.")

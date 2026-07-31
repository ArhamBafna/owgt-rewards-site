import os
import re

filepath = 'organized-data/pdfs-to-text/19 AI SKILLS COMPANIES ARE HIRING  FOR RIGHT NOW (V2)-text.txt'

def clean_filename(name):
    safe_name = name.lower()
    safe_name = re.sub(r'[^a-z0-9\-]', '-', safe_name)
    safe_name = re.sub(r'-+', '-', safe_name).strip('-')
    return safe_name[:60]

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()
    
parts = re.split(r'(SKILL \d+: )', text)
if len(parts) >= 3:
    for i in range(1, len(parts)-1, 2):
        marker = parts[i]
        content_block = parts[i+1]
        
        lines = content_block.strip().split('\n')
        skill_name = lines[0].strip()
        
        content_text = "\n".join(lines[1:]).strip()
        content_text_clean = re.sub(r'(THEKiREPORT|Q1 2026 I theaireport.ai.*|--- Page \d+ ---)', '', content_text, flags=re.IGNORECASE)
        content_text_clean = content_text_clean.strip()
        
        safe_name = clean_filename(skill_name)
        if safe_name:
            md_content = f"### Name\n{skill_name}\n\n### Description\nExtracted from 19 AI SKILLS COMPANIES ARE HIRING FOR RIGHT NOW\n\n### Content\n\n{content_text_clean}\n\n### Category\nLearning\n\n### Tags\n- Skill\n- Career\n"
            out_path = f"organized-data/Learning/{safe_name}.md"
            with open(out_path, 'w', encoding='utf-8') as out_f:
                out_f.write(md_content)

print("AI Skills extraction complete.")

import os
import glob
import re

files_to_process = [
    'data/pdfs-to-text/(V1) 37 CLAUDE PROMPTS THAT SAVE MANAGERS 10+ HOURS PER WEEK Organised by the 8 Situations Every Manager Faces-text.txt',
    'data/pdfs-to-text/THE AI REPORT - 75 CLAUDE PROMPTS-text.txt',
    'data/pdfs-to-text/V1 -  The AI Decision Playbook 25 Claude Prompts for Better Business Decisions-text.txt',
    'data/pdfs-to-text/V1 - 50 Claude Prompts Every Founder Should Bookmark-text.txt'
]

for filepath in files_to_process:
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    current_item = None
    current_content = []
    
    header_regex = re.compile(r'^(?:Prompt #\d+:|\d+\.)\s*([A-Z].+)$')
    
    count = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        match = header_regex.match(line)
        if match:
            if current_item and current_content:
                content_text = "\n".join(current_content).strip()
                prompt_match = re.search(r'"([^"]+)"', content_text, re.DOTALL)
                if prompt_match:
                    prompt_text = prompt_match.group(1)
                    if len(prompt_text) > 15:
                        count += 1
                            
            current_item = match.group(1).strip()
            current_content = []
        else:
            if current_item:
                current_content.append(line)
                
    if current_item and current_content:
        content_text = "\n".join(current_content).strip()
        prompt_match = re.search(r'"([^"]+)"', content_text, re.DOTALL)
        if prompt_match:
            prompt_text = prompt_match.group(1)
            if len(prompt_text) > 15:
                count += 1
                
    print(f"{os.path.basename(filepath)}: {count}")

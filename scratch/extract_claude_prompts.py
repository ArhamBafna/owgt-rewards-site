import os
import glob
import re

# Clean existing Prompts
for f in glob.glob("organized-data/Prompts/*.md"):
    os.remove(f)

files_to_process = [
    'organized-data/pdfs-to-text/(V1) 37 CLAUDE PROMPTS THAT SAVE MANAGERS 10+ HOURS PER WEEK Organised by the 8 Situations Every Manager Faces-text.txt',
    'organized-data/pdfs-to-text/THE AI REPORT - 75 CLAUDE PROMPTS-text.txt',
    'organized-data/pdfs-to-text/V1 -  The AI Decision Playbook 25 Claude Prompts for Better Business Decisions-text.txt',
    'organized-data/pdfs-to-text/V1 - 50 Claude Prompts Every Founder Should Bookmark-text.txt'
]

def clean_filename(name):
    safe_name = name.lower()
    safe_name = re.sub(r'[^a-z0-9\-]', '-', safe_name)
    safe_name = re.sub(r'-+', '-', safe_name).strip('-')
    return safe_name[:60]

for filepath in files_to_process:
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    current_item = None
    current_content = []
    
    # regex for "Prompt #12: Title" or "12. Title" but MUST start with capital letter
    header_regex = re.compile(r'^(?:Prompt #\d+:|\d+\.)\s*([A-Z].+)$')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        match = header_regex.match(line)
        if match:
            if current_item and current_content:
                safe_name = clean_filename(current_item)
                if safe_name:
                    content_text = "\n".join(current_content).strip()
                    
                    # Extract the quote if present
                    prompt_match = re.search(r'"([^"]+)"', content_text, re.DOTALL)
                    if prompt_match:
                        prompt_text = prompt_match.group(1)
                        
                        prompt_text = re.sub(r'(Pro tip:.*|3 years covering AI.*|Also in this situation:.*)', '', prompt_text, flags=re.IGNORECASE|re.DOTALL).strip()
                        
                        if len(prompt_text) > 15:
                            md_content = f"### Name\n{current_item}\n\n### Description\nExtracted from {os.path.basename(filepath)}\n\n### Prompt\n```text\n{prompt_text}\n```\n\n### Category\nPrompts\n\n### Tags\n- Prompt\n- Workflow\n"
                            out_path = f"organized-data/Prompts/{safe_name}.md"
                            with open(out_path, 'w', encoding='utf-8') as out_f:
                                out_f.write(md_content)
                            
            current_item = match.group(1).strip()
            current_item = re.sub(r'Pro tip:.*', '', current_item, flags=re.IGNORECASE).strip()
            current_content = []
        else:
            if current_item:
                current_content.append(line)
                
    # Save the last one
    if current_item and current_content:
        safe_name = clean_filename(current_item)
        if safe_name:
            content_text = "\n".join(current_content).strip()
            prompt_match = re.search(r'"([^"]+)"', content_text, re.DOTALL)
            if prompt_match:
                prompt_text = prompt_match.group(1)
                prompt_text = re.sub(r'(Pro tip:.*|3 years covering AI.*|Also in this situation:.*)', '', prompt_text, flags=re.IGNORECASE|re.DOTALL).strip()
                
                if len(prompt_text) > 15:
                    md_content = f"### Name\n{current_item}\n\n### Description\nExtracted from {os.path.basename(filepath)}\n\n### Prompt\n```text\n{prompt_text}\n```\n\n### Category\nPrompts\n\n### Tags\n- Prompt\n- Workflow\n"
                    out_path = f"organized-data/Prompts/{safe_name}.md"
                    with open(out_path, 'w', encoding='utf-8') as out_f:
                        out_f.write(md_content)

print("Claude Prompts strict extraction complete.")

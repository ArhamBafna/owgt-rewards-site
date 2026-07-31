import os
import glob
import re

prompts = glob.glob("organized-data/Prompts/*.md")
fixed = 0
deleted = 0

for filepath in prompts:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "### Description\nA prompt for" not in content and "### Description\nA master prompt for" not in content and "### Description\nA detailed prompt for" not in content:
        continue
        
    # Extract prompt block
    prompt_match = re.search(r'### Prompt\n```text\n(.*?)```', content, re.DOTALL)
    if not prompt_match:
        continue
        
    prompt_text = prompt_match.group(1).strip()
    words = prompt_text.split()
    
    # Identify garbage
    if len(words) < 10 or "bg-[" in prompt_text or "class=" in prompt_text or "margin:" in prompt_text:
        os.remove(filepath)
        deleted += 1
        continue
        
    # Generate description
    # Get first sentence
    sentences = re.split(r'(?<=[.!?])\s+', prompt_text)
    first_sentence = sentences[0].strip()
    
    # Make it lower case except for the first letter?
    if len(first_sentence) > 100:
        first_sentence = first_sentence[:100] + "..."
        
    if "A master prompt for" in content or "A detailed prompt for" in content:
        # these are the higgsfield / cinematic ones, leave them
        continue
        
    new_desc = f"A ready-to-use prompt that instructs the AI to: {first_sentence}"
    
    # replace
    content = re.sub(r'### Description\nA prompt for.*?tasks\.', f'### Description\n{new_desc}', content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    fixed += 1

print(f"Fixed {fixed} descriptions and deleted {deleted} garbage prompts.")

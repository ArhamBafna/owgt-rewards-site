import os
import re

def fix_lazy_description(desc):
    prefixes_to_remove = [
        r"^a ready-to-use prompt that instructs the ai to:\s*",
        r"^a ready-to-use prompt that instructs the ai to\s*",
        r"^a prompt for\s+",
        r"^a prompt that\s+",
        r"^a prompt\s+",
        r"^this prompt\s+",
        r"^extracted from\s+",
        r"^guide on\s+",
        r"^a guide on\s+",
        r"^this guide\s+",
    ]
    
    original_desc = desc
    changed = True
    while changed:
        changed = False
        for prefix in prefixes_to_remove:
            new_desc = re.sub(prefix, "", desc, flags=re.IGNORECASE)
            if new_desc != desc:
                desc = new_desc
                changed = True
                
    if desc != original_desc and len(desc) > 0:
        desc = desc[0].upper() + desc[1:]
        
    return desc

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    if filename in ['README.md', 'master.md', 'decisions.md']:
        return

    # Fix internal headers
    # The structure should be:
    # ### Name
    # ...
    # ### Description
    # ...
    # ### Content / URL / Prompt
    # (internal content which might have ###)
    # ### Category
    # ...
    # ### Tags
    
    # We will find the text between ### Content/URL/Prompt and ### Category
    # and replace all ^### with #### inside it.
    
    pattern = r'(### (?:Content|URL|Prompt)\n.*?\n)(### Category\n)'
    
    def replacer(match):
        inner_content = match.group(1)
        # replace any ### that is NOT ### Content/URL/Prompt
        # Actually it's easier: just replace all ^### in inner_content
        # but the first line is ### Content (or URL or Prompt).
        lines = inner_content.split('\n')
        for i in range(1, len(lines)):
            if lines[i].startswith('### '):
                lines[i] = '#' + lines[i] # make it ####
        return '\n'.join(lines) + match.group(2)
        
    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)

    # Fix lazy description
    desc_match = re.search(r'(### Description\n)(.*?)(?=\n### )', new_content, re.DOTALL)
    if desc_match:
        original_desc = desc_match.group(2).strip()
        fixed_desc = fix_lazy_description(original_desc)
        if fixed_desc != original_desc:
            # Replace just the description part
            new_content = new_content[:desc_match.start(2)] + fixed_desc + "\n" + new_content[desc_match.end(2):]

    # Check if anything changed
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {filepath}")

def main():
    directory = 'c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/organized-data'
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fix_file(filepath)

if __name__ == '__main__':
    main()

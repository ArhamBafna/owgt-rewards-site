import os
import glob
import re

files_to_process = [
    'organized-data/pdfs-to-text/(V1)21 AI TOOLS MOST FORTUNE 500 TEAMS ARE TESTING IN 2026  ## What Large Organisations Are Deploying, Why, and Which Function Each One Serves-text.txt',
    'organized-data/pdfs-to-text/The 2026 AI Tool Stack The Best AI Tools for Every Business Function (1) (1)-text.txt',
    'organized-data/pdfs-to-text/V1_41 AI TOOLS REPLACING ENTIRE WORKFLOWS IN 2026 The Business Leader\'s Guide to Which AI Tools Cut the Most Time From Your Team\'s Workflows, and What the Work Looks Like After-text.txt'
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
        text = f.read()
        
    # We look for Capitalized names followed by "What it does:"
    # Because of pdf artifacts, there might be newlines or extra text.
    # We will search for "What it does:" and grab the 100 characters before it to find the name.
    
    parts = re.split(r'(What it does:)', text)
    if len(parts) < 3:
        continue
        
    for i in range(1, len(parts)-1, 2):
        preceding_text = parts[i-1]
        what_it_does_marker = parts[i]
        content_text = parts[i+1]
        
        # Extract tool name from the very end of preceding_text
        # Look for the last line that has capitalized words
        lines_before = preceding_text.strip().split('\n')
        tool_name = "Unknown Tool"
        for line in reversed(lines_before):
            line = line.strip()
            if line and not re.match(r'^(?:3 years|Workflow being replaced|Perplexity AI|xAI|Q1 2026|CATEGORY)', line, re.IGNORECASE):
                # We found a potential name
                tool_name = line
                break
                
        safe_name = clean_filename(tool_name)
        if not safe_name or safe_name == 'unknown-tool':
            continue
            
        # Now parse the content_text to extract the fields
        # It goes until the next split, so content_text has the rest of this tool's info.
        # It may have garbage at the end (like page numbers) before the next tool.
        # We'll just clean out standard footer garbage.
        content_text_clean = re.sub(r'(3 years covering AI.*?|Q1 2026.*?|CATEGORY \d+)', '', content_text, flags=re.IGNORECASE)
        content_text_clean = content_text_clean.strip()
        
        # Build Markdown
        md_content = f"### Name\n{tool_name}\n\n### Description\nExtracted from {os.path.basename(filepath)}\n\n### Content\n\n**What it does:** {content_text_clean}\n\n### Category\nTools\n\n### Tags\n- Tool\n- Workflow\n"
        
        out_path = f"organized-data/Tools/{safe_name}.md"
        with open(out_path, 'w', encoding='utf-8') as out_f:
            out_f.write(md_content)

print("AI Tools extraction complete.")

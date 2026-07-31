import os
import re

filepath = "data/pdfs-to-text/V1_41 AI TOOLS REPLACING ENTIRE WORKFLOWS IN 2026 The Business Leader's Guide to Which AI Tools Cut the Most Time From Your Team's Workflows, and What the Work Looks Like After-text.txt"
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

def clean_filename(name):
    safe_name = name.lower()
    safe_name = re.sub(r'[^a-z0-9\-]', '-', safe_name)
    safe_name = re.sub(r'-+', '-', safe_name).strip('-')
    return safe_name[:60]

categories = re.split(r'CATEGORY \d+', text)
total_extracted = 0

for cat in categories[1:]:
    blocks = re.split(r'(What it does:)', cat)
    if len(blocks) < 3:
        continue
        
    num_tools = len(blocks) // 2
    
    header_lines = blocks[0].strip().split('\n')
    titles = []
    for line in header_lines:
        line = line.strip()
        if not line: continue
        if line.isupper() and len(line) > 2 and "Q1" not in line and "WORKFLOW" not in line and "AND" not in line and "RESEARCH" not in line and "WRITING" not in line and "COMMUNICATIONS" not in line and "CUSTOMER" not in line and "OPERATIONS" not in line and "FINANCE" not in line and "HR" not in line and "SALES" not in line:
            titles.append(line)
            
    # There are exactly num_tools tools in this category.
    # Take the LAST num_tools from titles, because sometimes there are random uppercase words before the titles.
    if len(titles) >= num_tools:
        tool_titles = titles[-num_tools:]
    else:
        # Fallback if we didn't find enough titles
        tool_titles = [f"Tool {i+1}" for i in range(num_tools)]
        for i, t in enumerate(titles):
            tool_titles[i] = t
            
    for i in range(num_tools):
        title = tool_titles[i]
        
        # The content block is blocks[2*i + 2]
        content = blocks[2*i + 2]
        # Clean the content
        content = re.sub(r'(3 years covering AI.*?|Q1 2026.*?|CATEGORY \d+|theaireport.*?\|)', '', content, flags=re.IGNORECASE|re.DOTALL)
        content = re.sub(r'\n+', '\n', content).strip()
        
        # Extract a description from content
        desc_match = re.search(r'(.*?)(Workflow it replaces:|Business outcome:|Best for:|$)', content, re.DOTALL)
        desc = desc_match.group(1).replace('\n', ' ').strip() if desc_match else f"An AI tool for {title.lower()}."
        
        safe_name = clean_filename(title)
        
        md_content = f"### Name\n{title.title()}\n\n### Description\n{desc}\n\n### Content\n\n**What it does:** {content}\n\n### Category\nTools\n\n### Tags\n- Tool\n- Workflow\n"
        
        out_path = f"organized-data/Tools/{safe_name}.md"
        with open(out_path, 'w', encoding='utf-8') as out_f:
            out_f.write(md_content)
            
        total_extracted += 1
        
print(f"Extracted {total_extracted} AI Tools perfectly.")

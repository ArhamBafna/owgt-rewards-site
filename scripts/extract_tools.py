import os
import re

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s-]+', '-', s)
    return s

files = [
    "data/pdfs-to-text/(V1)21 AI TOOLS MOST FORTUNE 500 TEAMS ARE TESTING IN 2026  ## What Large Organisations Are Deploying, Why, and Which Function Each One Serves-text.txt",
    "data/pdfs-to-text/V1_41 AI TOOLS REPLACING ENTIRE WORKFLOWS IN 2026 The Business Leader's Guide to Which AI Tools Cut the Most Time From Your Team's Workflows, and What the Work Looks Like After -text.txt",
    "data/pdfs-to-text/The 2026 AI Tool Stack The Best AI Tools for Every Business Function (1) (1)-text.txt"
]

# We are looking for lines with "What it does:" or "Whatitdoes :" 
# The preceding line is usually the tool name or company.
tool_pattern = re.compile(r'(?m)^([A-Z0-9\.\s&]+)\n(?:[A-Za-z\s]+)?\n?(?:What\s*it\s*does\s*:|Whatitdoes\s*:)\s*(.*?)(?=\n[A-Z][a-z]+|\Z)', re.DOTALL)

created_count = 0
existing = set()

for fpath in files:
    if not os.path.exists(fpath):
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Simple regex to catch tool names and their descriptions based on "What it does:"
    lines = content.split('\n')
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith("What it does:") or line.startswith("Whatitdoes :"):
            desc = line.split(":", 1)[1].strip()
            # The title is likely 1 or 2 lines above
            title = lines[i-1].strip()
            if len(title) == 0 or title.islower():
                title = lines[i-2].strip()
                
            if len(title) > 30 or len(title) < 2:
                continue
                
            # grab the next few lines for context until a blank line or a new header
            j = i + 1
            full_desc = [desc]
            while j < len(lines) and len(lines[j].strip()) > 0 and not lines[j].startswith("Best for:") and not lines[j].isupper():
                full_desc.append(lines[j].strip())
                j += 1
                
            full_desc = " ".join(full_desc).replace("  ", " ")
            
            filename = slugify(title) + ".md"
            if filename in existing:
                continue
            existing.add(filename)
            
            out_path = os.path.join("organized-data", "Tools", filename)
            
            if os.path.exists(out_path):
                continue
                
            md_content = f"### Name\n{title.title()}\n\n### Description\n{full_desc}\n\n### Content\nExtracted from AI Tools index. Use this tool for specific enterprise or workflow needs.\n\n### Category\nTools\n\n### Tags\n- AI Tools\n- Enterprise\n"
            
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as out_f:
                out_f.write(md_content)
            created_count += 1

print(f"Created {created_count} tool files.")

import re

filepath = "data/pdfs-to-text/(V1)21 AI TOOLS MOST Fortune 500 TEAMS ARE TESTING IN 2026  ## What Large Organisations Are Deploying, Why, and Which Function Each One Serves-text.txt"
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

categories = re.split(r'CATEGORY \d+', text)
print(f"Found {len(categories)} categories")

for cat in categories[1:]:
    blocks = re.split(r'(What it does:)', cat)
    num_tools = len(blocks) // 2
    
    header_lines = blocks[0].strip().split('\n')
    titles = []
    for line in header_lines:
        line = line.strip()
        if not line: continue
        if line.isupper() and len(line) > 2 and "Q1" not in line and "WORKFLOW" not in line and "AND" not in line and "TOOL" not in line:
            titles.append(line)
            
    print(f"Found {num_tools} 'What it does:' blocks. Found {len(titles)} uppercase titles: {titles}")

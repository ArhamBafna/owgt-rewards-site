import os
import glob
import re

base_dir = r"c:\Users\bafna\Desktop\Projects\OWGT-Newsletter-Automation\rewards\organized-data"

# 1. Split set-team-priorities.md
priorities_path = os.path.join(base_dir, "Prompts", "set-team-priorities.md")
if os.path.exists(priorities_path):
    with open(priorities_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Split the prompts manually based on what I read earlier.
    # The second prompt starts with "I need to communicate [difficult news]"
    if '"I need to communicate' in content:
        p1 = content.split('"I need to communicate')[0].strip() + '"\n```'
        p2 = '```\n"I need to communicate' + content.split('"I need to communicate')[1]
        
        # Rewrite first file
        p1_full = content.replace(content.split('```')[1].strip(), p1.replace('```','').replace('"','').strip() )
        with open(priorities_path, "w", encoding="utf-8") as f:
            f.write(p1_full)
            
        # Create second file
        new_path = os.path.join(base_dir, "Prompts", "deliver-difficult-news.md")
        p2_full = f"""### Name
Deliver Difficult News

### Description
A template to structure the communication of difficult news to an audience.

### Content
```
I need to communicate [difficult news] to [audience]. The news is: [describe]. Help me structure the communication so it: leads with the most important fact, explains the reasoning honestly, acknowledges the impact on the audience, and ends with what happens next. Give me the one thing I'm most tempted to soften that I should instead say directly.
```

### Category
Leadership & Management

### Tags
- Claude
- Prompt
- Leadership
- Communication
"""
        with open(new_path, "w", encoding="utf-8") as f:
            f.write(p2_full)


# 2. Tag Normalization
tag_map = {
    "Workflows": "Workflow",
    "Tools": "Tool",
    "Prompts": "Prompt",
    "Templates": "Template",
    "AI Agents": "Agent",
    "Agents": "Agent",
    "Cold Email": "Cold",
    "Prompt Engineering": "Prompting"
}

def normalize_tags(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    if "### Tags" in text:
        parts = text.split("### Tags")
        tags_section = parts[1]
        new_tags = []
        for line in tags_section.split("\n"):
            if line.startswith("- "):
                tag = line[2:].strip()
                if tag in tag_map:
                    tag = tag_map[tag]
                if tag not in new_tags and tag:
                    new_tags.append(tag)
        
        new_tags_text = "\n".join([f"- {t}" for t in new_tags])
        new_text = parts[0] + "### Tags\n" + new_tags_text + "\n"
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_text)


for file_path in glob.glob(os.path.join(base_dir, "**/*.md"), recursive=True):
    normalize_tags(file_path)

# 3. Clean PDF artifacts from specific files.
def clean_pdf_artifacts(file_path, bad_strings):
    if not os.path.exists(file_path): return
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if not any(bad in line for bad in bad_strings):
            new_lines.append(line)
            
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

bad_learning = ["THEAiREPORT", "THEiREPORT", "XIEXECUTIVESPASS", "GETTHEAIEXECUTIVES", "AICONTENT AND COMMUNICATIONS", "PASS$199/YR", "THE NATURAL NEXT STEP", "The Al Executives Pass is the next level", "Get $14,000+ in Al perks and credits for just $199/year."]
for file_path in glob.glob(os.path.join(base_dir, "Learning", "*.md")):
    clean_pdf_artifacts(file_path, bad_learning)

bad_tools = ["LAVENDER", "MARKETO ENGAGE", "CAMPAIGN SCALE", "PIPELINE", "RELATIONSHIPS", "AI Leaders Launch Guide $27", "The AI Leaders Launch Guide builds the implementation system", "GET THE AI LEADER", "LAUNCH GUIDE $27"]
for file_path in glob.glob(os.path.join(base_dir, "Tools", "*.md")):
    clean_pdf_artifacts(file_path, bad_tools)

print("Data cleanup Phase 0 done.")

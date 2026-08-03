import os
import glob

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../organized-data'))

# Mapping dictionary for general merges
TAG_MAPPINGS = {
    "Idea": "Ideas",
    "Student": "Students",
    "Toolkit": "Toolkits",
    "Tailwind": "Tailwind CSS",
    "Week": "Weekly",
    "Prompting": "Prompt",
    "System Prompts": "Prompt",
    "Tool": "AI Tools",
    "AI Capabilities": "AI",
    "AI Literacy": "AI",
    "AI Skills": "AI",
    "Models": "AI Models",
    "Images": "Image Generation",
    "Video Generation": "Video",
    "Hiring": "Recruiting",
    "Candidate Coordination": "Recruiting",
    "Talent Intelligence": "Recruiting",
    "Dictation": "Speech to Text",
    "Voice": "Speech to Text",
    "Code": "Coding",
    "Software Engineering": "Coding",
    "Content": "Content Generation",
    "Tutorial": "Guide",
    "Business AI": "Business",
    "Business Ops": "Business",
    "Thinking & Strategy": "Strategy",
    "Free Tier": "Free"
}

def process_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    in_tags_section = False
    modified = False
    new_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('### '):
            if stripped == '### Tags':
                in_tags_section = True
            else:
                in_tags_section = False
            new_lines.append(line)
            continue
        
        if in_tags_section and stripped.startswith('- '):
            tag_val = stripped[2:].strip()
            
            # Special handling for "Skill"
            if tag_val == "Skill":
                if filename in ["impeccable.md", "hallmark.md"]:
                    new_tag = "Skills"
                else:
                    new_tag = "learn skill"
                indent = line[:line.find('-')]
                new_lines.append(f"{indent}- {new_tag}\n")
                modified = True
                continue
            
            # General tag mapping
            if tag_val in TAG_MAPPINGS:
                new_tag = TAG_MAPPINGS[tag_val]
                indent = line[:line.find('-')]
                new_lines.append(f"{indent}- {new_tag}\n")
                modified = True
                continue
        
        new_lines.append(line)

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Updated: {filepath}")

def main():
    md_files = glob.glob(os.path.join(DATA_DIR, '**/*.md'), recursive=True)
    for filepath in md_files:
        process_file(filepath)

if __name__ == '__main__':
    main()

import os
import glob
import json

# Rule 1: Plurals, Hyphens, Casing, Synonyms
RENAME_MAP = {
    "Prompts": "Prompt",
    "Agents": "Agent",
    "Resources": "Resource",
    "Apps": "App",
    "Tools": "Tool",
    "AI Tools": "AI Tools",
    "Open-Source": "Open Source",
    "No-Code": "Workflow Automation",
    "No Code": "Workflow Automation",
    "ai": "AI",
    "api": "API",
    "ml": "Machine Learning",
    "gpt": "GPT",
    "rag": "RAG",
    "llm": "LLM",
    "UI Design": "UI",
    "UI/UX": "UI",
    "Generative AI": "AI Tools",
    "Generation": "AI Tools",
    "Generative": "AI Tools",
    "Machine Learning": "Machine Learning",
    "MLOps": "Machine Learning",
    "AI Agents": "Agent",
    "AI Copywriter": "Writing & Communication",
    "Copywriting": "Writing & Communication",
    "AI Presentations": "Design",
    "API & Backend": "API",
    "App Growth": "Marketing",
    "Backend": "Developer Tools",
    "Blockchain & Web3": "Web Development",
    "Browser Extension": "Developer Tools",
    "Chatbot": "LLM",
    "Code Snippets": "Developer Tools",
    "Data Science": "Machine Learning",
    "HR & Hiring": "Career",
    "Infrastructure": "Web Development",
    "Media Generation": "Content Creation",
    "Performance": "Developer Tools",
    "Prompt Engineering": "Prompt",
    "Security & Auth": "Developer Tools",
    "Slides": "Design",
    "Social Media": "Marketing",
    "Text Generation": "Writing & Communication",
    "Video Generation": "Content Creation",
    "Web Audio": "Audio & Speech"
}

# Rule 2: Single-Item Tag Mapping (125 isolated tags to group tags)
SINGLE_TAG_MAP = {
    "Mobile": "Marketing",
    "Attention": "Marketing",
    "Entrepreneurship": "Business",
    "GoHighLevel": "Workflow Automation",
    "Agency": "Business",
    "Make": "Workflow Automation",
    "App Development": "Software Engineering",
    "Software": "Software Engineering",
    "Job Search": "Career",
    "Product Ideas": "Business",
    "Obsidian": "Knowledge Base",
    "Notion": "Knowledge Base",
    "Second Brain": "Knowledge Base",
    "Solopreneur": "Business",
    "MVP": "Business",
    "SDK": "Developer Tools",
    "Developer Docs": "Developer Tools",
    "Market Research": "Analysis & Research",
    "Tool Evaluation": "AI Tools",
    "Procurement": "Business",
    "Certification": "Learning",
    "Kaggle": "Machine Learning",
    "Microsoft": "AI & Technical",
    "Beginners": "Learning",
    "Email Marketing": "Marketing",
    "Q&A": "RAG",
    "Production": "Machine Learning",
    "Architecture": "AI & Technical",
    "GPT": "LLM",
    "Training": "Machine Learning",
    "Real Estate": "Content Creation",
    "Client": "Writing & Communication",
    "Competitor": "Analysis & Research",
    "Leadership": "Business Operations",
    "Audit": "Analysis & Research",
    "System": "Analysis & Research",
    "Hashtag": "Marketing",
    "UGC": "Content Creation",
    "Hook": "Writing & Communication",
    "Job": "Business Operations",
    "Objection": "Sales & Outreach",
    "Offer": "Sales & Outreach",
    "Polite": "Writing & Communication",
    "Proposal": "Sales & Outreach",
    "Repurposing": "Content Creation",
    "Sop": "Business Operations",
    "Hackathons": "Community",
    "Events": "Community",
    "AI Research": "Research",
    "Quests": "Learning",
    "Projects": "Software Engineering",
    "Roleplay": "Prompt",
    "List": "Resource",
    "Cursor": "AI Coding",
    "Figma": "UI",
    "Backgrounds": "UI",
    "Google Drive": "Cloud Services",
    "Cloudflare": "Web Development",
    "UI Sounds": "Audio & Speech",
    "Interactions": "UI",
    "Brand Guidelines": "Design",
    "Design Engineering": "UI",
    "Google Cloud": "Cloud Services",
    "Activities": "Learning",
    "Framer Motion": "Animation",
    "Web": "Web Development",
    "DEV Community": "Community",
    "Studio": "Design",
    "Official": "Developer Tools",
    "GitHub Gist": "Developer Tools",
    "Shaders": "Web Development",
    "Effects": "Web Development",
    "Reddit": "Marketing",
    "Promotion": "Marketing",
    "Y Combinator": "Startups",
    "Success Stories": "Startups",
    "Revenue": "Startups",
    "Database": "Developer Tools",
    "Multi-Channel": "Customer Service",
    "Voice": "Audio & Speech",
    "Library": "Developer Tools",
    "Terminal": "Developer Tools",
    "Chat Interface": "LLM",
    "Fast": "Developer Tools",
    "Integration": "Workflow Automation",
    "Scientific Literature": "Research",
    "Git": "Developer Tools",
    "Conversational Marketing": "Marketing",
    "Sales Qualification": "Sales & Outreach",
    "Proxy": "API",
    "Focus": "Productivity",
    "App Blocker": "Productivity",
    "Audio": "Audio & Speech",
    "Presentations": "Design",
    "Google Labs": "AI Tools",
    "shadcn": "UI",
    "Video Interview": "Career",
    "Web3": "Web Development",
    "Complex Logic": "Workflow Automation",
    "Internal Knowledge": "Knowledge Base",
    "Experiment": "AI Tools",
    "OpenAI": "LLM",
    "OAuth": "Developer Tools",
    "Multi-Agent": "Agent",
    "Framework": "Developer Tools",
    "LaTeX": "Document Generator",
    "Interactive": "Animation",
    "Graphics": "Design",
    "RSS": "Automation",
    "Relay.app": "Automation",
    "Chrome Extension": "Developer Tools",
    "Live Chat": "Customer Service",
    "ByteDance": "AI Coding",
    "Uncensored": "LLM",
    "Codeium": "AI Coding",
    "Creative": "Content Creation",
    "Photorealistic": "Image Generation"
}

# Rule 3: File-specific domain tag enrichments for generative/misclassified tools
FILE_ENRICHMENT = {
    "z-image-ai.md": ["Image Generation", "AI Tools"],
    "ideogram-4-0.md": ["Image Generation", "Design"],
    "gamma.md": ["Design", "Document Generator"],
    "copy-ai.md": ["Writing & Communication", "Marketing"],
    "fathom-ai.md": ["Meeting Assistant", "Transcription", "AI Tools"],
    "tactiq.md": ["Meeting Assistant", "Transcription", "Developer Tools"],
    "fritz-ai.md": ["Meeting Assistant", "Transcription", "Audio & Speech"]
}

# Build case-insensitive lookup dictionaries
RENAME_MAP_LOWER = {k.lower(): v for k, v in RENAME_MAP.items()}
SINGLE_TAG_MAP_LOWER = {k.lower(): v for k, v in SINGLE_TAG_MAP.items()}

def clean_tag(t):
    t_strip = t.strip()
    if not t_strip:
        return t_strip
    
    t_lower = t_strip.lower()
    if t_lower in RENAME_MAP_LOWER:
        t_strip = RENAME_MAP_LOWER[t_lower]
        t_lower = t_strip.lower()
        
    if t_lower in SINGLE_TAG_MAP_LOWER:
        t_strip = SINGLE_TAG_MAP_LOWER[t_lower]
        t_lower = t_strip.lower()

    if t_lower in RENAME_MAP_LOWER:
        t_strip = RENAME_MAP_LOWER[t_lower]

    return t_strip

def clean_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    filename = os.path.basename(file_path).lower()
    new_lines = []
    current_tags = []

    i = 0
    while i < len(lines):
        line = lines[i]
        line_strip = line.strip()

        if line_strip.startswith('### Tags'):
            new_lines.append(line)
            i += 1
            # Collect existing tags under ### Tags
            while i < len(lines):
                next_line = lines[i]
                next_strip = next_line.strip()
                if next_strip.startswith('###') or (next_strip and not next_strip.startswith('-')):
                    break
                if next_strip.startswith('-'):
                    tag_val = next_strip[1:].strip()
                    if tag_val:
                        current_tags.append(tag_val)
                i += 1

            # Process collected tags
            processed_tags = [clean_tag(t) for t in current_tags]

            # Check File Enrichment
            if filename in FILE_ENRICHMENT:
                for extra_tag in FILE_ENRICHMENT[filename]:
                    processed_tags.append(clean_tag(extra_tag))

            # Deduplicate tags keeping order
            final_tags = []
            seen = set()
            for t in processed_tags:
                t_clean = t.strip()
                if t_clean and t_clean.lower() not in seen:
                    seen.add(t_clean.lower())
                    final_tags.append(t_clean)

            # Write formatted tags back
            for t in final_tags:
                new_lines.append(f"- {t}\n")
            
            continue

        new_lines.append(line)
        i += 1

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def run():
    files = glob.glob('organized-data/**/*.md', recursive=True)
    print(f"Cleaning tags across {len(files)} files with case-insensitive matching...")
    for f in files:
        clean_markdown_file(f)
    print("All markdown files updated successfully!")

if __name__ == '__main__':
    run()

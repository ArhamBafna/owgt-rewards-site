import os
import glob
import json
import re

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../organized-data'))
SITE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_JSON_PATH = os.path.join(SITE_DIR, 'data.json')
SEARCH_INDEX_PATH = os.path.join(SITE_DIR, 'search-index.json')

# Subcategory mapping keywords
SUBCAT_RULES = {
    "Sales & Outreach": ["sales", "cold email", "outreach", "proposal", "cold dm", "investor", "pitch"],
    "Writing & Communication": ["writing", "communication", "email", "newsletter", "summary", "draft", "message", "explanation"],
    "Leadership & Management": ["leadership", "team", "management", "hiring", "culture", "onboarding", "performance", "employee"],
    "Analysis & Research": ["analysis", "research", "competitor", "data", "feedback", "audit", "diagnose"],
    "Business Operations": ["operations", "sop", "kpi", "business", "finance", "workflow", "process", "kickoff", "pricing"],
    "Creative & Content": ["creative", "content", "video", "social media", "hook", "caption", "real estate", "repurposing"],
    "AI & Technical": ["prompt", "prompt engineering", "ai", "agent", "stack", "midjourney", "code", "technical"],
    "Strategy & Thinking": ["strategy", "thinking", "decision", "planning", "scenario", "first principles", "assumption", "blind spot"]
}

def determine_subcategory(title, desc, tags):
    search_text = f"{title} {desc} {' '.join(tags)}".lower()
    for subcat, keywords in SUBCAT_RULES.items():
        for kw in keywords:
            if kw in search_text:
                return subcat
    return "Strategy & Thinking" # Fallback

def parse_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = {}
    current_section = None
    current_content = []

    for line in content.split('\n'):
        if line.startswith('### '):
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = line[4:].strip()
            current_content = []
        else:
            if current_section:
                current_content.append(line)

    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()

    tags = []
    if 'Tags' in sections:
        tags = [t.replace('- ', '').strip() for t in sections['Tags'].split('\n') if t.strip().startswith('-')]

    return sections, tags

def main():
    items = []
    search_index = []
    
    # Process files
    md_files = glob.glob(os.path.join(DATA_DIR, '**', '*.md'), recursive=True)
    
    for file in md_files:
        # skip any markdown files at root of organized-data that are not in categories
        if os.path.dirname(file) == DATA_DIR:
            continue
            
        sections, tags = parse_markdown(file)
        
        name = sections.get('Name', '')
        if not name:
            continue
            
        desc = sections.get('Description', '')
        category = sections.get('Category', '')
        url = sections.get('URL', '')
        
        # Look for content in 'Content' or 'Prompt'
        body = sections.get('Content', '')
        if not body:
            body = sections.get('Prompt', '')
            
        slug = os.path.splitext(os.path.basename(file))[0]
        
        # Determine deep vs shallow
        # Shallow if it has URL but very little/no content
        is_shallow = False
        if url and len(body) < 100:
            is_shallow = True
        
        # Force deep for Prompts and Guides
        if category in ["Prompts", "Guides"]:
            is_shallow = False
            
        # Determine Subcategory for Prompts
        subcategory = ""
        if category == "Prompts":
            subcategory = determine_subcategory(name, desc, tags)
            
        item = {
            "id": slug,
            "name": name,
            "description": desc,
            "category": category,
            "subcategory": subcategory,
            "tags": tags,
            "url": url,
            "content": body,
            "is_shallow": is_shallow,
            "path": f"{category.lower().replace(' ', '-')}/{slug}"
        }
        items.append(item)
        
        # Add to search index (lightweight)
        search_index.append({
            "id": slug,
            "name": name,
            "description": desc,
            "category": category,
            "subcategory": subcategory,
            "tags": tags,
            "path": item["path"],
            "is_shallow": is_shallow
        })
        
    # Use Case Bundles logic
    use_cases = {
        "cold-outreach-stack": {"name": "Cold Outreach Stack", "items": []},
        "content-creation": {"name": "Content Creation", "items": []},
        "ai-research": {"name": "AI Research", "items": []},
        "build-ai-apps": {"name": "Build AI Apps", "items": []},
        "prompt-engineering": {"name": "Prompt Engineering", "items": []},
        "video-and-motion": {"name": "Video & Motion", "items": []},
        "career-and-hiring": {"name": "Career & Hiring", "items": []},
        "marketing-stack": {"name": "Marketing Stack", "items": []},
        "developer-toolkit": {"name": "Developer Toolkit", "items": []},
        "no-code-automation": {"name": "No-Code Automation", "items": []}
    }
    
    for item in items:
        lower_tags = [t.lower() for t in item["tags"]]
        
        if any(t in lower_tags for t in ["cold", "cold email", "sales", "outreach"]):
            use_cases["cold-outreach-stack"]["items"].append(item["id"])
            
        if any(t in lower_tags for t in ["content", "writing", "copywriting", "newsletter"]):
            use_cases["content-creation"]["items"].append(item["id"])
            
        if any(t in lower_tags for t in ["research", "ai research", "perplexity", "rag"]):
            use_cases["ai-research"]["items"].append(item["id"])
            
        if any(t in lower_tags for t in ["coding", "app development", "agents", "api"]):
            use_cases["build-ai-apps"]["items"].append(item["id"])
            
        if any(t in lower_tags for t in ["prompt engineering", "prompting", "prompt"]):
            use_cases["prompt-engineering"]["items"].append(item["id"])
            
        if any(t in lower_tags for t in ["video", "animation", "motion", "graphics"]):
            use_cases["video-and-motion"]["items"].append(item["id"])
            
        if any(t in lower_tags for t in ["career", "job", "hiring", "recruiting", "job search"]):
            use_cases["career-and-hiring"]["items"].append(item["id"])
            
        if any(t in lower_tags for t in ["marketing", "email marketing", "seo", "growth"]):
            use_cases["marketing-stack"]["items"].append(item["id"])
            
        if any(t in lower_tags for t in ["cli", "api", "github", "developer tools", "frontend"]):
            use_cases["developer-toolkit"]["items"].append(item["id"])
            
        if any(t in lower_tags for t in ["no-code", "automation", "workflow", "zapier", "make"]):
            use_cases["no-code-automation"]["items"].append(item["id"])

    # Tag Counts
    tag_counts = {}
    for item in items:
        for t in item["tags"]:
            tag_counts[t] = tag_counts.get(t, 0) + 1
            
    # Filter for tags with 3+ uses
    popular_tags = {k: v for k, v in tag_counts.items() if v >= 3}
    
    # Save outputs
    with open(DATA_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump({"items": items, "use_cases": use_cases, "tags": tag_counts}, f, indent=2)
        
    with open(SEARCH_INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, separators=(',', ':'))

    print(f"Processed {len(items)} items.")
    print(f"Generated {DATA_JSON_PATH}")
    print(f"Generated {SEARCH_INDEX_PATH}")

if __name__ == "__main__":
    main()

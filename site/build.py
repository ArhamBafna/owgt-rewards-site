import os
import glob
import json
import re

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../organized-data'))
SITE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_JSON_PATH = os.path.join(SITE_DIR, 'data.json')
SEARCH_INDEX_PATH = os.path.join(SITE_DIR, 'search-index.json')

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
    return "Strategy & Thinking"

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

def cat_to_filename(category):
    c = category.lower().replace(' ', '')
    if c == 'cheatsheets': return 'cheatsheets.html'
    return f"{category.lower().replace(' ', '-')}.html"

def generate_category_page(category, cat_items):
    cat_file = cat_to_filename(category)
    filepath = os.path.join(SITE_DIR, cat_file)
    
    cards_html = []
    for item in cat_items:
        tags_str = ' '.join([f"#{t}" for t in item['tags'][:3]])
        
        if item['is_shallow']:
            card = f"""
            <div class="card card--expandable" style="--cat-color: var(--color-accent-2);">
              <div class="card__accent-strip"></div>
              <div class="card__header" style="display: flex; justify-content: space-between; align-items: start;">
                <span class="tag" style="font-size: 9px; padding: 2px 6px;">{item['category']}</span>
                <button class="btn--ghost" data-bookmark-id="{item['id']}" data-title="{item['name']}" data-path="{item['path']}" data-category="{item['category']}" style="border: 1px solid var(--color-ink); padding: 2px 6px; font-family: var(--font-outlier); font-size: 10px;">♡ Save</button>
              </div>
              <div class="card__body">
                <h3 class="card__title">{item['name']}</h3>
                <p class="card__desc">{item['description']}</p>
              </div>
              <button class="card__expand-btn" aria-expanded="false" onclick="this.setAttribute('aria-expanded', this.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'); this.nextElementSibling.classList.toggle('is-open');">
                <span>Quick View</span>
                <span class="card__expand-arrow">↓</span>
              </button>
              <div class="card__expand-content">
                <p style="font-size: var(--text-sm);">{item['description']}</p>
                {f'<a href="{item["url"]}" target="_blank" class="btn btn--primary" style="margin-top: var(--space-sm); width: 100%;">Visit Resource ↗</a>' if item['url'] else ''}
              </div>
            </div>
            """
        else:
            card = f"""
            <a href="{item['id']}" class="card" style="--cat-color: var(--color-cat-prompts);">
              <div class="card__accent-strip"></div>
              <div class="card__header" style="display: flex; justify-content: space-between; align-items: start;">
                <span class="tag" style="font-size: 9px; padding: 2px 6px;">{item['subcategory'] or item['category']}</span>
                <button class="btn--ghost" data-bookmark-id="{item['id']}" data-title="{item['name']}" data-path="{item['path']}" data-category="{item['category']}" style="border: 1px solid var(--color-ink); padding: 2px 6px; font-family: var(--font-outlier); font-size: 10px;">♡ Save</button>
              </div>
              <div class="card__body">
                <h3 class="card__title">{item['name']}</h3>
                <p class="card__desc">{item['description']}</p>
              </div>
              <div class="card__footer">
                <span class="meta">{tags_str}</span>
                <span class="card__expand-arrow">→</span>
              </div>
            </a>
            """
        cards_html.append(card)

    with open(os.path.join(SITE_DIR, 'templates', 'category.html'), 'r', encoding='utf-8') as tf:
        template = tf.read()

    html = template.replace('{category}', category) \
                   .replace('{category_upper}', category.upper()) \
                   .replace('{item_count}', str(len(cat_items))) \
                   .replace('{cards_html}', ''.join(cards_html))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_deep_item_pages(items):
    for idx, item in enumerate(items):
        if item['is_shallow']:
            continue
            
        filepath = os.path.join(SITE_DIR, f"{item['id']}.html")
        
        prev_item = items[idx - 1] if idx > 0 else None
        next_item = items[idx + 1] if idx < len(items) - 1 else None
        
        prev_html = f'<a href="{prev_item["id"]}" class="item-nav-btn"><span class="meta">← Previous</span><span style="font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase;">{prev_item["name"]}</span></a>' if prev_item else '<a class="item-nav-btn disabled"><span class="meta">← Previous</span><span style="font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase;">Start of Library</span></a>'
        next_html = f'<a href="{next_item["id"]}" class="item-nav-btn next"><span class="meta">Next →</span><span style="font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase;">{next_item["name"]}</span></a>' if next_item else '<a class="item-nav-btn next disabled"><span class="meta">Next →</span><span style="font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase;">End of Library</span></a>'
        
        tags_html = ''.join([f'<span class="tag" style="background: var(--color-paper); border: 1px solid var(--color-ink); padding: 4px 12px; font-size: 10px;">#{t}</span>' for t in item['tags']])
        
        with open(os.path.join(SITE_DIR, 'templates', 'deep-item.html'), 'r', encoding='utf-8') as tf:
            template = tf.read()

        html = template.replace('{item_name}', str(item['name'])) \
                       .replace('{category_upper}', str(item['category']).upper()) \
                       .replace('{item_desc}', str(item['description'])) \
                       .replace('{tags_html}', tags_html) \
                       .replace('{item_content}', str(item['content'] or item['description'])) \
                       .replace('{prev_html}', prev_html) \
                       .replace('{next_html}', next_html)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

def main():
    items = []
    search_index = []
    
    md_files = glob.glob(os.path.join(DATA_DIR, '**', '*.md'), recursive=True)
    
    for file in md_files:
        if os.path.dirname(file) == DATA_DIR:
            continue
            
        sections, tags = parse_markdown(file)
        
        name = sections.get('Name', '')
        if not name:
            continue
            
        desc = sections.get('Description', '')
        category = sections.get('Category', '')
        url = sections.get('URL', '')
        
        body = sections.get('Content', '')
        if not body:
            body = sections.get('Prompt', '')
            
        slug = os.path.splitext(os.path.basename(file))[0]
        
        is_shallow = False
        if url and len(body) < 100:
            is_shallow = True
        
        if category in ["Prompts", "Guides"]:
            is_shallow = False
            
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
            "path": f"{slug}"
        }
        items.append(item)
        
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

    tag_counts = {}
    categories_dict = {}

    for item in items:
        cat = item['category']
        if cat not in categories_dict:
            categories_dict[cat] = []
        categories_dict[cat].append(item)

        for t in item["tags"]:
            tag_counts[t] = tag_counts.get(t, 0) + 1

    # Generate Category HTML files
    for cat, cat_items in categories_dict.items():
        if cat:
            generate_category_page(cat, cat_items)

    # Generate Deep Item HTML files
    generate_deep_item_pages(items)

    with open(DATA_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump({"items": items, "use_cases": use_cases, "tags": tag_counts}, f, indent=2)
        
    with open(SEARCH_INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, separators=(',', ':'))

    print(f"Successfully built {len(items)} items and category pages!")

if __name__ == "__main__":
    main()

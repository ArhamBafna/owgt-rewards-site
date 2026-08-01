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
            <a href="{item['id']}.html" class="card" style="--cat-color: var(--color-cat-prompts);">
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

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{category} - OWGT Rewards Library</title>
  <link rel="stylesheet" href="css/tokens.css">
  <link rel="stylesheet" href="css/base.css">
  <style>
    .nav-mast {{ display: grid; gap: var(--space-2xs); padding: var(--space-md) var(--page-gutter) 0; text-align: center; }}
    .mast-name {{ font-family: var(--font-display); font-size: clamp(2.25rem, 5vw, 3.75rem); letter-spacing: -0.01em; line-height: 0.95; margin: 0; color: var(--color-ink); }}
    .mast-line {{ font-variant: small-caps; letter-spacing: 0.08em; font-size: var(--text-xs); color: var(--color-muted); font-family: var(--font-outlier); }}
    .mast-nav ul {{ display: inline-flex; flex-wrap: wrap; justify-content: center; gap: var(--space-md); list-style: none; padding: 0; margin: var(--space-2xs) 0 0; }}
    .mast-nav a {{ font-family: var(--font-outlier); text-transform: uppercase; font-size: var(--text-sm); letter-spacing: var(--ls-label); }}
    .mast-nav a:hover, .mast-nav a.active {{ color: var(--color-accent); }}
    .mast-rule.double {{ border: 0; border-top: 1px solid var(--color-ink); border-bottom: 1px solid var(--color-ink); height: 4px; margin: var(--space-sm) 0 0; }}
    .category-header {{ padding: var(--space-3xl) var(--page-gutter) var(--space-xl); text-align: center; background: var(--color-paper-2); border-bottom: 2px solid var(--color-ink); }}
    .foot-mast {{ padding: var(--space-3xl) var(--page-gutter); text-align: center; border-top: 2px solid var(--color-ink); }}
    .foot-mast .wordmark {{ font-family: var(--font-display); font-size: var(--text-2xl); text-transform: uppercase; }}
  </style>
</head>
<body>
  <header class="nav-mast">
    <p class="mast-line">No 01 · Curated AI Library · OWGT Rewards</p>
    <a href="index.html" style="text-decoration: none;"><h1 class="mast-name">OWGT REWARDS</h1></a>
    <nav class="mast-nav" aria-label="Primary">
      <ul>
        <li><a href="prompts.html">Prompts</a></li>
        <li><a href="tools.html">Tools</a></li>
        <li><a href="guides.html">Guides</a></li>
        <li><a href="resources.html">Resources</a></li>
        <li><a href="tags.html">Tags</a></li>
        <li><a href="bookmarks.html">Bookmarks</a></li>
      </ul>
    </nav>
    <hr class="mast-rule double" aria-hidden="true">
  </header>

  <main class="page-wrap">
    <header class="category-header">
      <div class="container container--narrow">
        <h1 class="display-hero" style="font-size: clamp(3rem, 8vw, 8rem);">{category.upper()}</h1>
        <p style="margin: var(--space-md) auto 0; font-size: var(--text-lg);">{len(cat_items)} curated entries.</p>
      </div>
    </header>

    <section class="section">
      <div class="container container--wide">
        <div class="card-grid card-grid--4">
          {''.join(cards_html)}
        </div>
      </div>
    </section>
  </main>

  <footer class="foot-mast">
    <div class="container">
      <p class="wordmark">OWGT Rewards</p>
      <p class="tagline muted">The world's best digital knowledge library for AI.</p>
    </div>
  </footer>
  <script src="js/app.js"></script>
</body>
</html>"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_deep_item_pages(items):
    for idx, item in enumerate(items):
        if item['is_shallow']:
            continue
            
        filepath = os.path.join(SITE_DIR, f"{item['id']}.html")
        
        prev_item = items[idx - 1] if idx > 0 else None
        next_item = items[idx + 1] if idx < len(items) - 1 else None
        
        prev_html = f'<a href="{prev_item["id"]}.html" class="item-nav-btn"><span class="meta">← Previous</span><span style="font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase;">{prev_item["name"]}</span></a>' if prev_item else '<a class="item-nav-btn disabled"><span class="meta">← Previous</span><span style="font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase;">Start of Library</span></a>'
        next_html = f'<a href="{next_item["id"]}.html" class="item-nav-btn next"><span class="meta">Next →</span><span style="font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase;">{next_item["name"]}</span></a>' if next_item else '<a class="item-nav-btn next disabled"><span class="meta">Next →</span><span style="font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase;">End of Library</span></a>'
        
        tags_html = ''.join([f'<span class="tag" style="background: var(--color-paper); border: 1px solid var(--color-ink); padding: 4px 12px; font-size: 10px;">#{t}</span>' for t in item['tags']])
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{item['name']} - OWGT Rewards</title>
  <link rel="stylesheet" href="css/tokens.css">
  <link rel="stylesheet" href="css/base.css">
  <style>
    .nav-mast {{ display: grid; gap: var(--space-2xs); padding: var(--space-md) var(--page-gutter) 0; text-align: center; }}
    .mast-name {{ font-family: var(--font-display); font-size: clamp(2.25rem, 5vw, 3.75rem); letter-spacing: -0.01em; line-height: 0.95; margin: 0; color: var(--color-ink); }}
    .mast-line {{ font-variant: small-caps; letter-spacing: 0.08em; font-size: var(--text-xs); color: var(--color-muted); font-family: var(--font-outlier); }}
    .mast-nav ul {{ display: inline-flex; flex-wrap: wrap; justify-content: center; gap: var(--space-md); list-style: none; padding: 0; margin: var(--space-2xs) 0 0; }}
    .mast-nav a {{ font-family: var(--font-outlier); text-transform: uppercase; font-size: var(--text-sm); letter-spacing: var(--ls-label); }}
    .deep-header {{ padding: var(--space-3xl) var(--page-gutter) var(--space-xl); text-align: center; background: var(--color-paper-2); border-bottom: 2px solid var(--color-ink); }}
    .prompt-box {{ background: var(--color-paper); border: 2px solid var(--color-ink); box-shadow: var(--card-shadow); padding: var(--space-xl); margin: var(--space-2xl) auto; max-width: 800px; }}
    .prompt-text {{ font-family: var(--font-outlier); font-size: var(--text-base); line-height: var(--lh-body); white-space: pre-wrap; }}
    .copy-bar {{ display: flex; justify-content: space-between; align-items: center; margin-top: var(--space-xl); padding-top: var(--space-md); border-top: 1px solid var(--color-paper-3); }}
    .item-nav {{ display: flex; justify-content: space-between; max-width: 800px; margin: var(--space-2xl) auto; gap: var(--space-md); }}
    .item-nav-btn {{ flex: 1; padding: var(--space-md); border: 2px solid var(--color-ink); background: var(--color-paper-2); text-decoration: none; color: var(--color-ink); display: flex; flex-direction: column; }}
    .item-nav-btn.next {{ text-align: right; }}
    .item-nav-btn.disabled {{ opacity: 0.5; border-style: dashed; }}
    .foot-mast {{ padding: var(--space-3xl) var(--page-gutter); text-align: center; border-top: 2px solid var(--color-ink); }}
  </style>
</head>
<body>
  <header class="nav-mast">
    <p class="mast-line">No 01 · Curated AI Library · OWGT Rewards</p>
    <a href="index.html" style="text-decoration: none;"><h1 class="mast-name">OWGT REWARDS</h1></a>
    <nav class="mast-nav" aria-label="Primary">
      <ul>
        <li><a href="prompts.html">Prompts</a></li>
        <li><a href="tools.html">Tools</a></li>
        <li><a href="guides.html">Guides</a></li>
        <li><a href="resources.html">Resources</a></li>
      </ul>
    </nav>
    <hr class="mast-rule double" aria-hidden="true">
  </header>

  <main class="page-wrap">
    <header class="deep-header">
      <div class="container container--narrow">
        <p class="eyebrow" style="color: var(--color-accent); margin-bottom: var(--space-sm);">◆ {item['category'].upper()}</p>
        <h1 style="font-size: clamp(2.5rem, 6vw, 5rem);">{item['name']}</h1>
        <p style="margin-top: var(--space-md); font-size: var(--text-lg);">{item['description']}</p>
        <div class="cluster" style="justify-content: center; margin-top: var(--space-md);">
          {tags_html}
        </div>
      </div>
    </header>

    <section class="section">
      <div class="container">
        <div class="prompt-box">
          <div class="prompt-text">{item['content'] or item['description']}</div>
          <div class="copy-bar">
            <span class="meta">Press 'C' to copy</span>
            <button class="btn btn--primary copy-main-btn" onclick="copyToClipboard(this.previousElementSibling.parentElement.previousElementSibling.innerText, this)">Copy Content</button>
          </div>
        </div>

        <nav class="item-nav">
          {prev_html}
          {next_html}
        </nav>
      </div>
    </section>
  </main>

  <footer class="foot-mast">
    <div class="container">
      <p class="wordmark">OWGT Rewards</p>
    </div>
  </footer>
  <script src="js/app.js"></script>
</body>
</html>"""
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

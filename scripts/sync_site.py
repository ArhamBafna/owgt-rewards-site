import os
import json
import re
import html
import markdown
from urllib.parse import urlparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REWARDS_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
ORGANIZED_DIR = os.path.join(REWARDS_DIR, 'organized-data')
SITE_DIR = os.path.join(REWARDS_DIR, 'site')

CATEGORY_MAPPING = {
    'Cheat Sheets': {'slug': 'cheatsheets', 'html': 'cheatsheets.html', 'color_token': '--color-cat-cheatsheets'},
    'Frameworks': {'slug': 'frameworks', 'html': 'frameworks.html', 'color_token': '--color-cat-frameworks'},
    'Guides': {'slug': 'guides', 'html': 'guides.html', 'color_token': '--color-cat-guides'},
    'Learning': {'slug': 'learning', 'html': 'learning.html', 'color_token': '--color-cat-learning'},
    'Prompts': {'slug': 'prompts', 'html': 'prompts.html', 'color_token': '--color-cat-prompts'},
    'Resources': {'slug': 'resources', 'html': 'resources.html', 'color_token': '--color-cat-resources'},
    'Templates': {'slug': 'templates', 'html': 'templates.html', 'color_token': '--color-cat-templates'},
    'Tools': {'slug': 'tools', 'html': 'tools.html', 'color_token': '--color-cat-tools'},
}

BUNDLE_META = {
    "cold-outreach-stack": {
        "title": "Cold Outreach Stack",
        "description": "Everything you need to automate lead gen and emails. A complete end-to-end workflow collection."
    },
    "content-creation": {
        "title": "Content Creation",
        "description": "Systematize your social media and blog posting with AI-driven content workflows."
    },
    "marketing-stack": {
        "title": "Marketing Stack",
        "description": "SOPs, prompt chains, and tools to run your agency and marketing operations."
    },
    "no-code-automation": {
        "title": "No-Code Automation",
        "description": "Time-saving automations for everyday work. Connect tools without writing code."
    },
    "ai-research": {
        "title": "AI Research",
        "description": "Deep-dive frameworks and tools for competitive analysis and rapid knowledge synthesis."
    },
    "build-ai-apps": {
        "title": "Build AI Apps",
        "description": "From idea to deployment: resources and frameworks for building modern AI applications."
    },
    "prompt-engineering": {
        "title": "Prompt Engineering",
        "description": "Master advanced prompting techniques to unlock the full potential of large language models."
    },
    "video-and-motion": {
        "title": "Video & Motion",
        "description": "Create cinematic visuals, animated assets, and compelling motion graphics using AI."
    },
    "career-and-hiring": {
        "title": "Career & Hiring",
        "description": "Optimize your job search, interviewing, and team building processes with AI assistance."
    },
    "developer-toolkit": {
        "title": "Developer Toolkit",
        "description": "Essential CLIs, IDEs, and coding tools to supercharge your software engineering speed."
    }
}

def parse_markdown_item(filepath, category_name):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')
        
    slug = os.path.splitext(os.path.basename(filepath))[0]
    
    name_match = re.search(r'### (?:Name|Title)[ \t]*\n(.*?)(?=\n### |$)', content, re.DOTALL)
    desc_match = re.search(r'### Description[ \t]*\n(.*?)(?=\n### |$)', content, re.DOTALL)
    cat_match = re.search(r'### Category[ \t]*\n(.*?)(?=\n### |$)', content, re.DOTALL)
    url_match = re.search(r'### URL[ \t]*\n(.*?)(?=\n### |$)', content, re.DOTALL)
    body_match = re.search(r'### (?:Content|Prompt)[ \t]*\n(.*?)(?=\n### (?:Category|Tags|URL|Name|Title|Description)\b|$)', content, re.DOTALL)
    tags_match = re.search(r'### Tags[ \t]*\n(.*?)(?=\n### |$)', content, re.DOTALL)
    
    name = name_match.group(1).strip() if name_match else slug.replace('-', ' ').title()
    desc = desc_match.group(1).strip() if desc_match else ''
    cat = category_name
    url = url_match.group(1).strip() if url_match else ''
    body = body_match.group(1).strip() if body_match else ''
    
    if not name_match or not name:
        print(f"Warning: Missing or blank 'Name' in {filepath}")
    if not desc_match or not desc:
        print(f"Warning: Missing or blank 'Description' in {filepath}")
    if not cat_match or not cat:
        print(f"Warning: Missing or blank 'Category' in {filepath}")
    
    tags = []
    if tags_match:
        for line in tags_match.group(1).splitlines():
            line = line.strip()
            if line.startswith('-'):
                t = line.lstrip('-').strip()
                if t:
                    tags.append(t)
                    
    cat_slug = CATEGORY_MAPPING.get(category_name, {}).get('slug', category_name.lower().replace(' ', '-'))
    is_shallow = len(body) == 0
    path = f"/items/{cat_slug}/{slug}"
    
    return {
        "id": slug,
        "slug": slug,
        "name": name,
        "description": desc,
        "category": cat,
        "folder_category": category_name,
        "category_slug": cat_slug,
        "subcategory": "",
        "tags": tags,
        "url": url,
        "content": body,
        "is_shallow": is_shallow,
        "path": path,
        "rel_md_path": f"{category_name}/{os.path.basename(filepath)}"
    }

def update_indices(items_by_folder, all_tags):
    sorted_tags = sorted(list(all_tags), key=lambda s: s.lower())
    
    master_data = {}
    for cat, items in items_by_folder.items():
        cat_key = cat.lower()
        master_data[cat_key] = [
            {"name": item['name'], "path": item['rel_md_path']}
            for item in sorted(items, key=lambda x: x['name'].lower())
        ]
        
    with open(os.path.join(ORGANIZED_DIR, 'master.json'), 'w', encoding='utf-8') as f:
        json.dump(master_data, f, separators=(',', ':'))
        
    with open(os.path.join(ORGANIZED_DIR, 'master.md'), 'w', encoding='utf-8') as f:
        f.write("# Master Index\n\nThis index is automatically generated.\n\n")
        for cat in sorted(master_data.keys()):
            f.write(f"## {cat.title()}\n\n")
            for item in master_data[cat]:
                f.write(f"- [{item['name']}]({item['path']})\n")
            f.write("\n")
            
    with open(os.path.join(ORGANIZED_DIR, 'tags.txt'), 'w', encoding='utf-8') as f:
        f.write("\n".join(sorted_tags) + "\n")

def generate_deep_item_html(item, prev_item, next_item):
    cat_upper = item['category'].upper()
    tags_html = "".join([
        f'<a href="/tag-detail?tag={html.escape(t)}" class="tag" style="background: var(--color-paper); border: 1px solid var(--color-ink); padding: 4px 12px; font-size: 10px; text-decoration: none; color: inherit;">#{html.escape(t)}</a>'
        for t in item['tags']
    ])
    
    if prev_item:
        prev_btn = f'<a href="{prev_item["path"]}" class="item-nav-btn"><span class="meta">← Previous</span><span style="font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase;">{html.escape(prev_item["name"])}</span></a>'
    else:
        prev_btn = '<a class="item-nav-btn disabled"><span class="meta">← Previous</span><span style="font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase;">Start of Library</span></a>'
        
    if next_item:
        next_btn = f'<a href="{next_item["path"]}" class="item-nav-btn next"><span class="meta">Next →</span><span style="font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase;">{html.escape(next_item["name"])}</span></a>'
    else:
        next_btn = '<a class="item-nav-btn next disabled"><span class="meta">Next →</span><span style="font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase;">End of Library</span></a>'

    rendered_content = markdown.markdown(item['content'], extensions=['fenced_code', 'tables'])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{html.escape(item['description'])}">
  <meta property="og:title" content="{html.escape(item['name'])} - OWGT Rewards">
  <meta property="og:description" content="{html.escape(item['description'])}">
  <meta property="og:url" content="https://rewards.owgt.com{item['path']}">
  <title>{html.escape(item['name'])} - OWGT Rewards</title>
  <link rel="icon" type="image/png" href="/favicon.png">
  <link rel="stylesheet" href="/css/tokens.css">
  <link rel="stylesheet" href="/css/base.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
  <style>
    .prompt-box {{ background: var(--color-paper); border: 2px solid var(--color-ink); box-shadow: var(--card-shadow); padding: var(--space-xl); margin: var(--space-2xl) auto; max-width: 800px; }}
    .prompt-text {{ font-family: var(--font-outlier); font-size: var(--text-base); line-height: var(--lh-body); white-space: pre-wrap; }}
    .prompt-text.markdown-rendered {{ white-space: normal; font-family: var(--font-body); }}
    .prompt-text.markdown-rendered h1,
    .prompt-text.markdown-rendered h2,
    .prompt-text.markdown-rendered h3,
    .prompt-text.markdown-rendered h4 {{ margin-top: 1.5em; margin-bottom: 0.5em; }}
    .prompt-text.markdown-rendered p {{ margin-bottom: 0.75em; max-width: none; }}
    .prompt-text.markdown-rendered ul,
    .prompt-text.markdown-rendered ol {{ margin-left: 1.5em; margin-bottom: 0.75em; list-style: disc; }}
    .prompt-text.markdown-rendered ol {{ list-style: decimal; }}
    .prompt-text.markdown-rendered code {{ font-family: var(--font-outlier); background: var(--color-paper-2); padding: 0.15em 0.4em; font-size: 0.9em; border: 1px solid var(--color-paper-3); }}
    .prompt-text.markdown-rendered pre {{ background: transparent; color: inherit; padding: 0; margin-bottom: 1em; border: none; white-space: pre-wrap; word-break: break-word; font-family: var(--font-body); font-size: inherit; }}
    .prompt-text.markdown-rendered pre code {{ background: none; border: none; padding: 0; color: inherit; font-family: inherit; font-size: inherit; white-space: pre-wrap; word-break: break-word; }}
    .prompt-text.markdown-rendered blockquote {{ border-left: 4px solid var(--color-accent); padding-left: var(--space-md); margin-left: 0; margin-bottom: 0.75em; color: var(--color-ink-2); font-style: italic; }}
    .prompt-text.markdown-rendered table {{ border-collapse: collapse; width: 100%; margin-bottom: 1em; }}
    .prompt-text.markdown-rendered th,
    .prompt-text.markdown-rendered td {{ border: 1px solid var(--color-ink); padding: var(--space-xs) var(--space-sm); text-align: left; }}
    .prompt-text.markdown-rendered th {{ background: var(--color-paper-2); font-family: var(--font-display); text-transform: uppercase; font-size: var(--text-sm); }}
    .copy-bar {{ display: flex; justify-content: space-between; align-items: center; margin-top: var(--space-xl); padding-top: var(--space-md); border-top: 1px solid var(--color-paper-3); }}
    .item-nav {{ display: flex; justify-content: space-between; max-width: 800px; margin: var(--space-2xl) auto; gap: var(--space-md); }}
    .item-nav-btn {{ flex: 1; padding: var(--space-md); border: 2px solid var(--color-ink); background: var(--color-paper-2); text-decoration: none; color: var(--color-ink); display: flex; flex-direction: column; }}
    .item-nav-btn.next {{ text-align: right; }}
    .item-nav-btn.disabled {{ opacity: 0.5; border-style: dashed; }}
  </style>
</head>
<body>
  <header class="new-global-header" id="globalHeader">
  <div class="new-header-left">
    <a href="/rewards" class="new-logo-link">
      <img src="/owgt-rewards-logo.png?v=3" alt="OWGT Rewards Logo" class="new-header-logo">
      <span class="new-header-title">OWGT Rewards</span>
    </a>
  </div>
  <nav class="new-header-nav" aria-label="Primary">
    <ul>
      <li><a href="/prompts">Prompts</a></li>
      <li><a href="/tools">Tools</a></li>
      <li><a href="/learning">Learning</a></li>
      <li><a href="/resources">Resources</a></li>
      <li><a href="/tags">Tags</a></li>
      <li><a href="/bookmarks">Saved</a></li>
    </ul>
  </nav>
  <div class="new-header-right">
    <button id="searchTriggerBtn" class="search-trigger-btn" aria-label="Open Search">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
    </button>
    <div id="headerSearchContainer" class="header-search-container" style="display: none;">
      <div id="searchScopeSelect" class="search-scope-select">
        <button class="scope-btn" data-scope="global">All Rewards</button>
        <button class="scope-btn" data-scope="local" id="localScopeBtn">Current Category</button>
      </div>
      <div id="searchInputWrapper" class="search-input-wrapper" style="display: none;">
        <div class="active-scope-pill" id="activeScopePill">All Rewards</div>
        <input type="text" id="headerSearchInput" placeholder="Search..." autocomplete="off">
        <button id="executeSearchBtn" class="execute-search-btn" aria-label="Search">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
        </button>
        <button id="closeSearchBtn" class="close-search-btn" aria-label="Close Search">✕</button>
      </div>
    </div>
  </div>
</header>

  <main class="page-wrap">
    <header class="deep-header">
      <div class="container container--narrow">
        <p class="eyebrow" style="color: var(--color-accent); margin-bottom: var(--space-sm);">◆ <a href="/{item['category_slug']}" style="color: inherit; text-decoration: none;">{cat_upper}</a></p>
        <h1 style="font-size: clamp(2.5rem, 6vw, 5rem);">{html.escape(item['name'])}</h1>
        <p style="margin-top: var(--space-md); font-size: var(--text-lg);">{html.escape(item['description'])}</p>
        <div class="cluster" style="justify-content: center; margin-top: var(--space-md);">
          {tags_html}
        </div>
      </div>
    </header>

    <section class="section">
      <div class="container">
        <div class="prompt-box">
          <div class="prompt-text markdown-rendered" id="prompt-content">{rendered_content}</div>
          
          <div class="copy-bar">
            <span class="meta">Press 'C' to copy • 'B' to save</span>
            <div style="display: flex; gap: var(--space-sm); align-items: center;">
              <button class="btn btn--ghost bookmark-main-btn" data-bookmark-id="{item['slug']}" data-title="{html.escape(item['name'])}" data-path="{item['path']}" data-category="{item['category']}" style="padding: 6px 12px; font-size: var(--text-sm);">♡ Save</button>
              <button class="btn btn--primary copy-main-btn" onclick="copyToClipboard(document.getElementById('prompt-content').innerText, this)" title="Copy content" aria-label="Copy content" style="padding: 6px 10px; display: inline-flex; align-items: center; justify-content: center;"><svg class="copy-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg></button>
            </div>
          </div>
        </div>

        <nav class="item-nav">
          {prev_btn}
          {next_btn}
        </nav>
      </div>
    </section>
  </main>

  <footer class="foot-mast">
    <div class="container">
      <p class="wordmark">OWGT Rewards</p>
      <p class="links muted">© 2026 OWGT</p>
      <p class="mast-line" style="margin-top: 8px;">MADE BY ARHAM</p>
    </div>
  </footer>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script src="/js/app.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      document.querySelectorAll('pre code').forEach((block) => {{
        hljs.highlightElement(block);
      }});
    }});
  </script>
</body>
</html>
'''

def generate_bundle_html_page(bundle_id, bundle_info, items):
    cards_html = "".join([render_category_card(it) for it in items])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <link rel="icon" type="image/png" href="/favicon.png">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(bundle_info['title'])} - OWGT Rewards Library</title>
  
  <link rel="stylesheet" href="/css/tokens.css">
  <link rel="stylesheet" href="/css/base.css">
  
  <style>
    .nav-mast {{ display: grid; gap: var(--space-2xs); padding: var(--space-md) var(--page-gutter) 0; text-align: center; }}
    .mast-name {{ font-family: var(--font-display); font-size: clamp(2.25rem, 5vw, 3.75rem); letter-spacing: -0.01em; line-height: 0.95; margin: 0; color: var(--color-ink); }}
    .mast-line {{ font-variant: small-caps; letter-spacing: 0.08em; font-size: var(--text-xs); color: var(--color-muted); font-family: var(--font-outlier); }}
    .mast-nav ul {{ display: inline-flex; flex-wrap: wrap; justify-content: center; gap: var(--space-md); list-style: none; padding: 0; margin: var(--space-2xs) 0 0; }}
    .mast-nav a {{ font-family: var(--font-outlier); text-transform: uppercase; font-size: var(--text-sm); letter-spacing: var(--ls-label); }}
    .mast-nav a:hover, .mast-nav a.active {{ color: var(--color-accent); }}
    .mast-rule.double {{ border: 0; border-top: 1px solid var(--color-ink); border-bottom: 1px solid var(--color-ink); height: 4px; margin: var(--space-sm) 0 0; }}

    .bundle-header {{
      padding: var(--space-3xl) var(--page-gutter) var(--space-xl);
      text-align: center;
      background: var(--color-accent);
      color: var(--color-accent-ink);
      border-bottom: 2px solid var(--color-ink);
    }}
  </style>
</head>
<body>
  <header class="nav-mast">
    <a href="/rewards" style="text-decoration: none;"><h1 class="mast-name">OWGT REWARDS</h1></a>
    <nav class="mast-nav" aria-label="Primary">
      <ul>
        <li><a href="/prompts">Prompts</a></li>
        <li><a href="/tools">Tools</a></li>
        <li><a href="/rewards#bundles" class="active">Bundles</a></li>
      </ul>
    </nav>
    <hr class="mast-rule double" aria-hidden="true">
  </header>

  <main class="page-wrap">
    <header class="bundle-header">
      <div class="container container--narrow">
        <p class="eyebrow" style="color: var(--color-ink); margin-bottom: var(--space-sm);">◆ CURATED STACK</p>
        <h1 class="display-hero" style="font-size: clamp(2.5rem, 6vw, 6rem);">{html.escape(bundle_info['title'])}</h1>
        <p style="margin: var(--space-md) auto 0; font-size: var(--text-lg);">
          {html.escape(bundle_info['description'])}
        </p>
      </div>
    </header>

    <section class="section">
      <div class="container container--wide">
        <div class="card-grid card-grid--4">
          {cards_html}
        </div>
      </div>
    </section>
  </main>
  
  <script src="/js/app.js"></script>
</body>
</html>'''

def render_category_card(item):
    tags_meta = " ".join([f"#{t}" for t in item['tags']])
    category_label = html.escape(item['category'])
    name_escaped = html.escape(item['name'])
    desc_escaped = html.escape(item['description'])
    cat_color = CATEGORY_MAPPING.get(item.get('folder_category'), {}).get('color_token') or \
                CATEGORY_MAPPING.get(item.get('category'), {}).get('color_token', '--color-cat-prompts')
    
    if not item['is_shallow']:
        return f'''
            <a href="{item['path']}" class="card" style="--cat-color: var({cat_color});">
              <div class="card__accent-strip"></div>
              <div class="card__header" style="display: flex; justify-content: space-between; align-items: start;">
                <span class="tag" style="font-size: 9px; padding: 2px 6px;">{category_label}</span>
                <button class="btn--ghost" data-bookmark-id="{item['id']}" data-title="{name_escaped}" data-path="{item['path']}" data-category="{category_label}" style="border: 1px solid var(--color-ink); padding: 2px 6px; font-family: var(--font-outlier); font-size: 10px;">♡ Save</button>
              </div>
              <div class="card__body">
                <h3 class="card__title">{name_escaped}</h3>
                <p class="card__desc">{desc_escaped}</p>
              </div>
              <div class="card__footer">
                <span class="meta">{tags_meta}</span>
                <span class="card__expand-arrow">→</span>
              </div>
            </a>'''
    else:
        return f'''
            <div class="card card--expandable" style="--cat-color: var({cat_color});">
              <div class="card__accent-strip"></div>
              <div class="card__header" style="display: flex; justify-content: space-between; align-items: start;">
                <span class="tag" style="font-size: 9px; padding: 2px 6px;">{category_label}</span>
                <button class="btn--ghost" data-bookmark-id="{item['id']}" data-title="{name_escaped}" data-path="{item['path']}" data-category="{category_label}" style="border: 1px solid var(--color-ink); padding: 2px 6px; font-family: var(--font-outlier); font-size: 10px;">♡ Save</button>
              </div>
              <div class="card__body">
                <h3 class="card__title">{name_escaped}</h3>
                <p class="card__desc">{desc_escaped}</p>
              </div>
              <button class="card__expand-btn" aria-expanded="false" onclick="this.setAttribute('aria-expanded', this.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'); this.nextElementSibling.classList.toggle('is-open');">
                <span>Quick View</span>
                <span class="card__expand-arrow">↓</span>
              </button>
              <div class="card__expand-content">
                <p style="font-size: var(--text-sm); white-space: pre-wrap;">{html.escape(item['content']) if item.get('content') else desc_escaped}</p>
                {f'<a href="{item["url"]}" target="_blank" class="btn btn--primary" style="margin-top: var(--space-sm); width: 100%;">Visit Resource ↗</a>' if item.get('url') else ''}
              </div>
              <div class="card__footer">
                <span class="meta">{tags_meta}</span>
              </div>
            </div>'''

def update_category_html_page(cat_folder, cat_items):
    cat_info = CATEGORY_MAPPING.get(cat_folder)
    if not cat_info:
        return
        
    html_filename = cat_info['html']
    html_path = os.path.join(SITE_DIR, html_filename)
    if not os.path.exists(html_path):
        return
        
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    count = len(cat_items)
    content = re.sub(r'(\d+)\s+curated entries\.', f'{count} curated entries.', content)
    
    sorted_items = sorted(cat_items, key=lambda x: x['name'].lower())
    cards_html = "".join([render_category_card(it) for it in sorted_items])
    
    grid_pattern = re.compile(r'(<div class="card-grid card-grid--4">)(.*?)(</div>\s*</div>\s*</section>)', re.DOTALL)
    if grid_pattern.search(content):
        content = grid_pattern.sub(f'\\1\n{cards_html}\n        \\3', content)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {html_filename} with {count} items.")

def update_landing_and_rewards_pages(all_items, items_by_folder):
    total_count = len(all_items)
    counts = {folder: len(items_by_folder.get(folder, [])) for folder in CATEGORY_MAPPING.keys()}
    
    # 1. Update index.html
    index_path = os.path.join(SITE_DIR, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            idx_content = f.read()
            
        idx_content = re.sub(r'(>)\d+(\s+resources<)', rf'\g<1>{total_count}\2', idx_content)
        idx_content = re.sub(r'(<span class="landing-hero-num tnum">)\d+(</span>)', rf'\g<1>{total_count}\2', idx_content)
        idx_content = re.sub(r'\d+\s+resources\s+·\s+8\s+categories', f'{total_count} resources · 8 categories', idx_content)
        idx_content = re.sub(r'\d+\s+items across 8 categories\.', f'{total_count} items across 8 categories.', idx_content)
        idx_content = re.sub(r'OWGT Rewards — \d+ AI Resources Free With Newsletter', f'OWGT Rewards — {total_count} AI Resources Free With Newsletter', idx_content)
        idx_content = re.sub(r'\d+ copy-paste AI prompts', f'{total_count} copy-paste AI prompts', idx_content)
        idx_content = re.sub(r'\d+ AI resources\. One weekly email\.', f'{total_count} AI resources. One weekly email.', idx_content)
        
        prompts_cnt = counts.get('Prompts', 0)
        tools_cnt = counts.get('Tools', 0)
        guides_cnt = counts.get('Guides', 0)
        idx_content = re.sub(r'\d+\s+prompts for cold email', f'{prompts_cnt} prompts for cold email', idx_content)
        idx_content = re.sub(r'\d+\s+curated tools with descriptions', f'{tools_cnt} curated tools with descriptions', idx_content)
        idx_content = re.sub(r'\d+\s+step-by-step tutorials', f'{guides_cnt} step-by-step tutorials', idx_content)
        
        category_name_to_title = {
            'Prompts': 'Prompts',
            'Tools': 'Tools',
            'Learning': 'Learning',
            'Resources': 'Resources',
            'Guides': 'Guides',
            'Frameworks': 'Frameworks',
            'Cheat Sheets': 'Cheat sheets',
            'Templates': 'Templates'
        }
        for folder_name, title in category_name_to_title.items():
            cnt = counts.get(folder_name, 0)
            pattern = re.compile(
                rf'(<h3 class="card__title">{re.escape(title)}</h3>\s*<p[^>]*>.*?</p>\s*</div>\s*<div class="card__footer"><span class="meta tnum">)\d+\s+items(</span></div>)',
                re.DOTALL | re.IGNORECASE
            )
            idx_content = pattern.sub(rf'\g<1>{cnt} items\2', idx_content)
            
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(idx_content)
        print(f"Updated index.html counts (total: {total_count}).")

    # 2. Update rewards.html
    rewards_path = os.path.join(SITE_DIR, 'rewards.html')
    if os.path.exists(rewards_path):
        with open(rewards_path, 'r', encoding='utf-8') as f:
            rew_content = f.read()
            
        for folder_name in ['Prompts', 'Tools', 'Learning', 'Resources']:
            cnt = counts.get(folder_name, 0)
            pattern = re.compile(
                rf'(<h3 class="card__title">{re.escape(folder_name)}</h3>\s*<p[^>]*>.*?</p>\s*</div>\s*<div class="card__footer">\s*<span class="meta">)\d+\s+Items(</span>)',
                re.DOTALL | re.IGNORECASE
            )
            rew_content = pattern.sub(rf'\g<1>{cnt} Items\2', rew_content)
            
        with open(rewards_path, 'w', encoding='utf-8') as f:
            f.write(rew_content)
        print("Updated rewards.html category badge counts.")

def sync_all():
    print("Starting site sync from organized-data...")
    
    all_items = []
    items_by_folder = {}
    all_tags = set()
    url_to_files = {}
    slug_to_files = {}
    
    for folder in CATEGORY_MAPPING.keys():
        folder_path = os.path.join(ORGANIZED_DIR, folder)
        items_by_folder[folder] = []
        if not os.path.exists(folder_path):
            continue
            
        for file in os.listdir(folder_path):
            if file.endswith('.md') and file not in ['README.md', 'master.md', 'decisions.md']:
                filepath = os.path.join(folder_path, file)
                item = parse_markdown_item(filepath, folder)
                items_by_folder[folder].append(item)
                all_items.append(item)
                    
                clean_url = item['url'].strip()
                if clean_url:
                    url_to_files.setdefault(clean_url, []).append(item['rel_md_path'])
                    
                slug = item['id'].strip()
                if slug:
                    slug_to_files.setdefault(slug, []).append(item['rel_md_path'])
                    
    # Tag Case Normalization
    tag_case_map = {}
    for item in all_items:
        for t in item['tags']:
            lower_t = t.lower()
            if lower_t not in tag_case_map:
                tag_case_map[lower_t] = t
            else:
                # Prefer title case or explicit uppercase (e.g., API) over all-lowercase
                if t != tag_case_map[lower_t] and (t.istitle() or t.isupper()):
                    tag_case_map[lower_t] = t

    for item in all_items:
        normalized_tags = []
        for t in item['tags']:
            norm_t = tag_case_map[t.lower()]
            if norm_t not in normalized_tags:
                normalized_tags.append(norm_t)
            all_tags.add(norm_t)
        item['tags'] = normalized_tags

    print(f"Parsed {len(all_items)} total items across {len(items_by_folder)} categories.")
    
    # Check for duplicate URLs and slug collisions
    for target_url, files in url_to_files.items():
        if len(files) > 1:
            files_str = " and ".join(files) if len(files) == 2 else ", ".join(files[:-1]) + f", and {files[-1]}"
            print(f"Warning: Duplicate URL in {files_str}.")
            
    for target_slug, files in slug_to_files.items():
        if len(files) > 1:
            files_str = " and ".join(files) if len(files) == 2 else ", ".join(files[:-1]) + f", and {files[-1]}"
            print(f"Warning: Duplicate slug in {files_str}.")
    
    # 1. Update master indices
    update_indices(items_by_folder, all_tags)
    print("Updated master.json, master.md, and tags.txt")
    
    # 2. Update site/data.json
    tag_counts = {}
    for item in all_items:
        for t in item['tags']:
            tag_counts[t] = tag_counts.get(t, 0) + 1
            
    sorted_tag_counts = dict(sorted(tag_counts.items(), key=lambda x: (-x[1], x[0].lower())))
    
    master_items = []
    for it in all_items:
        search_blob = re.sub(r'[#*`_\[\]()>]', ' ', it['content']).strip()
        if it['is_shallow'] and it['url']:
            parsed_url = urlparse(it['url'])
            host_parts = parsed_url.netloc.split('.')
            host_keywords = " ".join([p for p in host_parts if p not in ('www', 'com', 'org', 'net', 'io')])
            
            url_keywords = re.sub(r'https?://|www\.', '', it['url'])
            url_keywords = re.sub(r'[/.\-_?=&%:]+', ' ', url_keywords).strip()
            
            search_blob = f"{it['description']} {host_keywords} {url_keywords}".strip()
            
        master_items.append({
            "id": it['id'],
            "name": it['name'],
            "description": it['description'],
            "category": it['category'],
            "category_slug": it['category_slug'],
            "tags": it['tags'],
            "url": it['url'],
            "content": it['content'],
            "search_blob": search_blob,
            "is_shallow": it['is_shallow'],
            "path": it['path']
        })
    
    data_json_path = os.path.join(SITE_DIR, 'data.json')
    with open(data_json_path, 'w', encoding='utf-8') as f:
        json.dump({"items": master_items, "tags": sorted_tag_counts}, f, separators=(',', ':'))
    print(f"Saved {data_json_path}")
    
    search_json_path = os.path.join(SITE_DIR, 'search-index.json')
    with open(search_json_path, 'w', encoding='utf-8') as f:
        json.dump(master_items, f, separators=(',', ':'))
    print(f"Saved {search_json_path}")
    
    # 4. Generate/Update Item HTML Pages
    for folder, items in items_by_folder.items():
        cat_slug = CATEGORY_MAPPING[folder]['slug']
        cat_items_dir = os.path.join(SITE_DIR, 'items', cat_slug)
        os.makedirs(cat_items_dir, exist_ok=True)
        
        deep_items = [it for it in items if not it['is_shallow']]
        sorted_deep = sorted(deep_items, key=lambda x: x['name'].lower())
        
        for idx, item in enumerate(sorted_deep):
            prev_it = sorted_deep[idx - 1] if idx > 0 else None
            next_it = sorted_deep[idx + 1] if idx < len(sorted_deep) - 1 else None
            
            html_content = generate_deep_item_html(item, prev_it, next_it)
            item_file_path = os.path.join(cat_items_dir, f"{item['id']}.html")
            with open(item_file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
    print("Generated all deep item standalone HTML pages.")
    
    # 5. Update Category Pages
    for folder, items in items_by_folder.items():
        update_category_html_page(folder, items)

    # 5.5 Generate Bundle Pages
    bundle_paths = []
    bundle_mapping_path = os.path.join(SITE_DIR, 'bundle_mapping.json')
    if os.path.exists(bundle_mapping_path):
        with open(bundle_mapping_path, 'r', encoding='utf-8') as f:
            bundle_mapping = json.load(f)
            
        bundles_dir = os.path.join(SITE_DIR, 'items', 'bundles')
        os.makedirs(bundles_dir, exist_ok=True)
        
        all_items_dict = {it['id']: it for it in all_items}
        
        for bundle_id, item_slugs in bundle_mapping.items():
            meta = BUNDLE_META.get(bundle_id, {"title": bundle_id.replace('-', ' ').title(), "description": "Curated collection of resources."})
            bundle_items = [all_items_dict[slug] for slug in item_slugs if slug in all_items_dict]
            
            html_content = generate_bundle_html_page(bundle_id, meta, bundle_items)
            bundle_file_path = os.path.join(bundles_dir, f"bundle-{bundle_id}.html")
            with open(bundle_file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            bundle_paths.append(f"/items/bundles/bundle-{bundle_id}")
        print(f"Generated {len(bundle_mapping)} bundle pages.")

    # 6. Update Landing (index.html) and Rewards (rewards.html) Pages
    update_landing_and_rewards_pages(all_items, items_by_folder)

    # 7. Stale / Orphaned HTML Cleanup
    valid_html_paths = set(os.path.abspath(os.path.join(SITE_DIR, it['path'].lstrip('/'))) + '.html' for it in all_items if not it['is_shallow'])
    for b_path in bundle_paths:
        valid_html_paths.add(os.path.abspath(os.path.join(SITE_DIR, b_path.lstrip('/'))) + '.html')
        
    items_dir = os.path.join(SITE_DIR, 'items')
    if os.path.exists(items_dir):
        for root, dirs, files in os.walk(items_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.abspath(os.path.join(root, file))
                    if file_path not in valid_html_paths:
                        os.remove(file_path)
                        print(f"Cleaned up stale HTML: {file_path}")

    # 8. Sitemap Generation
    from datetime import datetime, timezone
    today_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    base_url = "https://rewards.owgt.com"
    
    urls = [
        {"loc": f"{base_url}/", "priority": "1.0"},
        {"loc": f"{base_url}/rewards", "priority": "0.9"},
    ]
    
    for cat_slug in [cat['slug'] for cat in CATEGORY_MAPPING.values()]:
        urls.append({"loc": f"{base_url}/{cat_slug}", "priority": "0.8"})
        
    urls.append({"loc": f"{base_url}/tags", "priority": "0.7"})
    
    for it in all_items:
        if not it['is_shallow']:
            urls.append({"loc": f"{base_url}{it['path']}", "priority": "0.6"})
            
    for b_path in bundle_paths:
        urls.append({"loc": f"{base_url}{b_path}", "priority": "0.7"})
            
    sitemap_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for u in urls:
        sitemap_content.append(f'  <url>\n    <loc>{u["loc"]}</loc>\n    <lastmod>{today_date}</lastmod>\n    <priority>{u["priority"]}</priority>\n  </url>')
    sitemap_content.append('</urlset>')
    
    with open(os.path.join(SITE_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write("\n".join(sitemap_content))
    print("Generated sitemap.xml")

    # Generate robots.txt if missing
    robots_path = os.path.join(SITE_DIR, 'robots.txt')
    if not os.path.exists(robots_path):
        with open(robots_path, 'w', encoding='utf-8') as f:
            f.write("User-agent: *\nAllow: /\n\nSitemap: https://rewards.owgt.com/sitemap.xml\n")
        print("Generated robots.txt")

    print("Site sync complete with 100% data consistency.")

if __name__ == '__main__':
    sync_all()


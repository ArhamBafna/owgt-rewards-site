import json
import os
import re

def build_all_50():
    raw_path = r'C:\Users\bafna_sb19qr0\.gemini\antigravity-ide\brain\5239dcb5-4d60-45b4-8ec4-ee6838cb2d79\.system_generated\steps\12\content.md'
    with open(raw_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    idx = raw.find('window.HACKS = [')
    end_idx = raw.find('window.CATEGORIES = [')
    js_text = raw[idx:end_idx]

    # Parse using regex accurately per object
    # Find all object boundaries
    # Each object has: id, title, agents, category, summary, body, code, source
    # Let's extract with regex
    pattern = re.compile(
        r'\{\s*id:\s*"([^"]+)",\s*title:\s*"([^"]+)",\s*agents:\s*\[(.*?)\],\s*category:\s*"([^"]+)",\s*summary:\s*"([^"]+)",\s*body:\s*"([^"]+)",\s*code:\s*`?(.*?)`?,\s*source:\s*"([^"]+)",?\s*\}',
        re.DOTALL
    )

    matches = pattern.findall(js_text)
    print(f"Found {len(matches)} hacks with regex")
    
    hacks = []
    for m in matches:
        hid, title, agents_raw, category, summary, body, code, source = m
        agents = [a.strip().strip('"').strip("'") for a in agents_raw.split(',') if a.strip()]
        hacks.append({
            "id": hid,
            "title": title,
            "agents": agents,
            "category": category,
            "summary": summary,
            "body": body,
            "code": code.strip(),
            "source": source
        })

    # If some failed to match due to formatting, let's verify count
    if len(hacks) != 50:
        # Fallback to node exported json if needed
        if os.path.exists('temp_hacks.json'):
            with open('temp_hacks.json', 'r', encoding='utf-8') as f:
                hacks = json.load(f)
            print(f"Using node exported json with {len(hacks)} items")

    agent_names = {
        "claude-code": "Claude Code",
        "codex": "Codex",
        "cursor": "Cursor"
    }

    # Group by category in logical order
    cat_order = ["context", "workflow", "prompting", "automation", "tools"]
    cat_titles = {
        "context": "Context & Configuration",
        "workflow": "Workflow & Task Management",
        "prompting": "Prompting & Specification",
        "automation": "Automation & Hooks",
        "tools": "Tools & Plugins"
    }

    md_lines = []
    md_lines.append("### Name")
    md_lines.append("The Code — 50+ Coding Agent Hacks\n")
    md_lines.append("### Description")
    md_lines.append("A curated directory of 50 practical hacks, configuration patterns, hooks, and workflows for developers building with AI coding agents including Claude Code, Codex, and Cursor.\n")
    md_lines.append("### Category")
    md_lines.append("Cheat Sheets\n")
    md_lines.append("### URL")
    md_lines.append("https://hackbook-chi.vercel.app/\n")
    md_lines.append("### Content\n")
    md_lines.append("#### Overview")
    md_lines.append("A complete, curated directory of 50 practical hacks, prompts, workflows, and configuration recipes for developers building with Claude Code, OpenAI Codex, and Cursor.\n")

    counter = 1
    for cat in cat_order:
        cat_hacks = [h for h in hacks if h.get("category") == cat]
        if not cat_hacks:
            continue
        md_lines.append("---\n")
        md_lines.append(f"### {cat_titles[cat]}\n")
        for h in cat_hacks:
            agents_formatted = ", ".join([agent_names.get(a, a) for a in h.get("agents", [])])
            md_lines.append(f"#### {counter}. {h['title']}")
            md_lines.append(f"- **Agent(s)**: {agents_formatted}")
            md_lines.append(f"- **Summary**: {h['summary']}")
            md_lines.append(f"- **Details**: {h['body']}")
            if h.get('code'):
                code_snippet = h['code']
                # Determine language fence
                fence = "bash"
                if code_snippet.startswith("{") or code_snippet.startswith("//"):
                    fence = "json"
                elif code_snippet.startswith("# spec.md") or code_snippet.startswith("# CLAUDE.md") or code_snippet.startswith("---"):
                    fence = "markdown"
                elif "Agent({" in code_snippet:
                    fence = "javascript"
                md_lines.append(f"```{fence}\n{code_snippet}\n```")
            if h.get('source'):
                md_lines.append(f"- **Source**: {h['source']}")
            md_lines.append("")
            counter += 1

    md_lines.append("### Tags")
    tags = [
        "AI Coding",
        "Claude",
        "CLI",
        "Coding",
        "Developer Tools",
        "Prompt",
        "Workflow",
        "Best Practices",
        "Automation",
        "IDE"
    ]
    for t in tags:
        md_lines.append(f"- {t}")

    full_md = "\n".join(md_lines) + "\n"

    # Write organized-data md
    target_md = os.path.abspath(r'c:\Users\bafna_sb19qr0\Desktop\Projects\OWGT-Newsletter-Automation\rewards\organized-data\Cheat Sheets\the-code-coding-agent-hacks.md')
    with open(target_md, 'w', encoding='utf-8') as f:
        f.write(full_md)
    print(f"Saved {target_md} ({len(hacks)} hacks, {len(full_md)} bytes)")

    # Extract Content section for data.json
    content_idx = full_md.find("### Content\n")
    tags_idx = full_md.find("\n### Tags\n")
    content_body = full_md[content_idx + len("### Content\n"):tags_idx].strip()

    # Update data.json & search-index.json
    data_json_path = os.path.abspath(r'c:\Users\bafna_sb19qr0\Desktop\Projects\OWGT-Newsletter-Automation\rewards\site\data.json')
    search_json_path = os.path.abspath(r'c:\Users\bafna_sb19qr0\Desktop\Projects\OWGT-Newsletter-Automation\rewards\site\search-index.json')

    with open(data_json_path, 'r', encoding='utf-8') as f:
        site_data = json.load(f)

    item_entry = {
        "id": "the-code-coding-agent-hacks",
        "name": "The Code — 50+ Coding Agent Hacks",
        "description": "A curated directory of 50 practical hacks, configuration patterns, hooks, and workflows for developers building with Claude Code, Codex, and Cursor.",
        "category": "Cheat Sheets",
        "subcategory": "",
        "tags": tags,
        "url": "https://hackbook-chi.vercel.app/",
        "content": content_body,
        "is_shallow": False,
        "path": "/items/cheatsheets/the-code-coding-agent-hacks"
    }

    items = site_data.get("items", [])
    existing_idx = next((i for i, item in enumerate(items) if item.get("id") == item_entry["id"]), -1)
    if existing_idx >= 0:
        items[existing_idx] = item_entry
    else:
        items.append(item_entry)
    site_data["items"] = items

    tag_counts = {}
    for itm in items:
        for t in itm.get("tags", []):
            tag_counts[t] = tag_counts.get(t, 0) + 1
    site_data["tags"] = tag_counts

    with open(data_json_path, 'w', encoding='utf-8') as f:
        json.dump(site_data, f, indent=2)

    with open(search_json_path, 'r', encoding='utf-8') as f:
        search_data = json.load(f)

    search_entry = {
        "id": item_entry["id"],
        "name": item_entry["name"],
        "description": item_entry["description"],
        "category": item_entry["category"],
        "subcategory": item_entry["subcategory"],
        "tags": item_entry["tags"],
        "path": item_entry["path"],
        "url": item_entry["url"],
        "is_shallow": item_entry["is_shallow"],
        "content": item_entry["content"]
    }

    s_idx = next((i for i, s in enumerate(search_data) if s.get("id") == search_entry["id"]), -1)
    if s_idx >= 0:
        search_data[s_idx] = search_entry
    else:
        search_data.append(search_entry)

    with open(search_json_path, 'w', encoding='utf-8') as f:
        json.dump(search_data, f, indent=2)

    # Rebuild the HTML item page
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Code — 50+ Coding Agent Hacks - OWGT Rewards</title>
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
    .prompt-text.markdown-rendered pre {{ background: var(--color-ink); color: #f8f8f2; padding: var(--space-md); margin-bottom: 1em; border: 1px solid var(--color-ink); border-radius: 4px; overflow-x: auto; font-family: var(--font-outlier); font-size: var(--text-sm); }}
    .prompt-text.markdown-rendered pre code {{ background: none; border: none; padding: 0; color: inherit; font-family: inherit; font-size: inherit; white-space: pre; }}
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
    <a href="/home" class="new-logo-link">
      <img src="/owgt-rewards-logo.png?v=3" alt="OWGT Rewards Logo" class="new-header-logo">
      <span class="new-header-title">OWGT Rewards</span>
    </a>
  </div>
  <nav class="new-header-nav" aria-label="Primary">
    <ul>
      <li><a href="/prompts">Prompts</a></li>
      <li><a href="/tools">Tools</a></li>
      <li><a href="/guides">Guides</a></li>
      <li><a href="/resources">Resources</a></li>
      <li><a href="/tags">Tags</a></li>
      <li><a href="/bookmarks">Bookmarks</a></li>
    </ul>
  </nav>
  <div class="new-header-right">
    <!-- Search Trigger Icon -->
    <button id="searchTriggerBtn" class="search-trigger-btn" aria-label="Open Search">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
    </button>
    
    <!-- Expanded Search Container -->
    <div id="headerSearchContainer" class="header-search-container" style="display: none;">
      <!-- Step 1: Scope Selection -->
      <div id="searchScopeSelect" class="search-scope-select">
        <button class="scope-btn" data-scope="global">All Rewards</button>
        <button class="scope-btn" data-scope="local" id="localScopeBtn">Current Category</button>
      </div>
      
      <!-- Step 2: Search Input -->
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
        <p class="eyebrow" style="color: var(--color-accent); margin-bottom: var(--space-sm);">◆ CHEAT SHEETS</p>
        <h1 style="font-size: clamp(2.5rem, 6vw, 5rem);">The Code — 50+ Coding Agent Hacks</h1>
        <p style="margin-top: var(--space-md); font-size: var(--text-lg);">A curated directory of 50 practical hacks, configuration patterns, hooks, and workflows for developers building with Claude Code, Codex, and Cursor.</p>
        <div class="cluster" style="justify-content: center; margin-top: var(--space-md);">
          <span class="tag" style="background: var(--color-paper); border: 1px solid var(--color-ink); padding: 4px 12px; font-size: 10px;">#AI Coding</span><span class="tag" style="background: var(--color-paper); border: 1px solid var(--color-ink); padding: 4px 12px; font-size: 10px;">#Claude</span><span class="tag" style="background: var(--color-paper); border: 1px solid var(--color-ink); padding: 4px 12px; font-size: 10px;">#CLI</span><span class="tag" style="background: var(--color-paper); border: 1px solid var(--color-ink); padding: 4px 12px; font-size: 10px;">#Coding</span><span class="tag" style="background: var(--color-paper); border: 1px solid var(--color-ink); padding: 4px 12px; font-size: 10px;">#Developer Tools</span><span class="tag" style="background: var(--color-paper); border: 1px solid var(--color-ink); padding: 4px 12px; font-size: 10px;">#Workflow</span>
        </div>
        <div style="margin-top: var(--space-md);">
          <a href="https://hackbook-chi.vercel.app/" target="_blank" class="btn btn--primary" style="font-size: var(--text-sm);">Visit Official Website ↗</a>
        </div>
      </div>
    </header>

    <section class="section">
      <div class="container">
        <div class="prompt-box">
          <div class="prompt-text" id="prompt-content">{content_body}</div>
          
          <div class="copy-bar">
            <span class="meta">Press 'C' to copy</span>
            <button class="btn btn--primary copy-main-btn" onclick="copyToClipboard(document.getElementById('prompt-content').innerText, this)" title="Copy content" aria-label="Copy content" style="padding: 6px 10px; display: inline-flex; align-items: center; justify-content: center;"><svg class="copy-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg></button>
          </div>
        </div>

        <nav class="item-nav">
          <a href="/items/cheatsheets/chatgpt-and-ai-cheatsheet" class="item-nav-btn"><span class="meta">← Previous</span><span style="font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase;">ChatGPT & AI Cheatsheet</span></a>
          <a href="/items/cheatsheets/mobile-app-growth-cheat-sheet" class="item-nav-btn next"><span class="meta">Next →</span><span style="font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase;">Mobile App Growth Cheat Sheet</span></a>
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
  <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script src="/js/app.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      const el = document.getElementById('prompt-content');
      if (el) {{
        const raw = el.textContent;
        if (/^#{{1,6}}\s|^\*\s|^-\s|^>\s|```|^\d+\.\s|\*\*|__/m.test(raw)) {{
          marked.setOptions({{
            breaks: true,
            gfm: true,
            highlight: function(code, lang) {{
              if (lang && hljs.getLanguage(lang)) {{
                return hljs.highlight(code, {{ language: lang }}).value;
              }}
              return hljs.highlightAuto(code).value;
            }}
          }});
          el.innerHTML = marked.parse(raw);
          el.classList.add('markdown-rendered');
        }}
      }}
    }});
  </script>
</body>
</html>"""

    target_html = os.path.abspath(r'c:\Users\bafna_sb19qr0\Desktop\Projects\OWGT-Newsletter-Automation\rewards\site\items\cheatsheets\the-code-coding-agent-hacks.html')
    with open(target_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Saved {target_html}")

if __name__ == '__main__':
    build_all_50()

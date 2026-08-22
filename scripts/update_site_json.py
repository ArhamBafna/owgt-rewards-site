import os
import json
import re

def update_site_json():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    rewards_dir = os.path.abspath(os.path.join(base_dir, '..'))
    
    data_json_path = os.path.join(rewards_dir, 'site', 'data.json')
    search_json_path = os.path.join(rewards_dir, 'site', 'search-index.json')
    md_file_path = os.path.join(rewards_dir, 'organized-data', 'Cheat Sheets', 'the-code-coding-agent-hacks.md')
    
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
        
    name_m = re.search(r'### (?:Name|Title)\n(.*?)(?=\n### |$)', md_text, re.IGNORECASE | re.DOTALL)
    desc_m = re.search(r'### Description\n(.*?)(?=\n### |$)', md_text, re.IGNORECASE | re.DOTALL)
    cat_m = re.search(r'### Category\n(.*?)(?=\n### |$)', md_text, re.IGNORECASE | re.DOTALL)
    url_m = re.search(r'### URL\n(.*?)(?=\n### |$)', md_text, re.IGNORECASE | re.DOTALL)
    content_m = re.search(r'### Content\n(.*?)(?=\n### |$)', md_text, re.IGNORECASE | re.DOTALL)
    tags_m = re.search(r'### Tags\n(.*?)(?=\n### |$)', md_text, re.IGNORECASE | re.DOTALL)
    
    name = name_m.group(1).strip() if name_m else "The Code — Coding Hacks for AI Agents"
    desc = desc_m.group(1).strip() if desc_m else ""
    cat = cat_m.group(1).strip() if cat_m else "Cheat Sheets"
    url = url_m.group(1).strip() if url_m else ""
    content = content_m.group(1).strip() if content_m else ""
    
    tags = []
    if tags_m:
        for line in tags_m.group(1).splitlines():
            line = line.strip()
            if line.startswith('-'):
                t = line.lstrip('-').strip()
                if t:
                    tags.append(t)
                    
    item_entry = {
        "id": "the-code-coding-agent-hacks",
        "name": name,
        "description": desc,
        "category": cat,
        "subcategory": "",
        "tags": tags,
        "url": url,
        "content": content,
        "is_shallow": False,
        "path": "/items/cheatsheets/the-code-coding-agent-hacks"
    }
    
    # Update data.json
    with open(data_json_path, 'r', encoding='utf-8') as f:
        site_data = json.load(f)
        
    items = site_data.get("items", [])
    # Replace if exists, else append
    existing_idx = next((i for i, item in enumerate(items) if item.get("id") == item_entry["id"]), -1)
    if existing_idx >= 0:
        items[existing_idx] = item_entry
    else:
        items.append(item_entry)
        
    site_data["items"] = items
    
    # Recalculate tag counts
    tag_counts = {}
    for itm in items:
        for t in itm.get("tags", []):
            tag_counts[t] = tag_counts.get(t, 0) + 1
    site_data["tags"] = tag_counts

    with open(data_json_path, 'w', encoding='utf-8') as f:
        json.dump(site_data, f, indent=2)
    print(f"Updated {data_json_path}, total items: {len(items)}")
    
    # Update search-index.json
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
    print(f"Updated {search_json_path}, total search items: {len(search_data)}")

if __name__ == '__main__':
    update_site_json()

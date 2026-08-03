import json
import os
from collections import defaultdict, Counter

def analyze():
    data_path = os.path.join('site', 'data.json')
    if not os.path.exists(data_path):
        print("site/data.json not found!")
        return

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data.get('items', [])
    print(f"Total items analyzed: {len(items)}")

    # Build tag mapping: tag -> list of items
    tag_to_items = defaultdict(list)
    item_to_tags = {}

    for item in items:
        item_id = item.get('name') or item.get('id')
        tags = item.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        
        item_to_tags[item_id] = tags
        for t in tags:
            t_clean = t.strip()
            if t_clean:
                tag_to_items[t_clean].append(item)

    total_tags = len(tag_to_items)
    print(f"Total unique tags: {total_tags}")

    # Count breakdown
    counts = Counter({t: len(ilist) for t, ilist in tag_to_items.items()})
    
    print("\n--- TAG FREQUENCY BREAKDOWN ---")
    freq_counts = Counter(counts.values())
    for f in sorted(freq_counts.keys()):
        print(f"  Count = {f} item(s): {freq_counts[f]} tags")

    # 1. SINGLE-ITEM TAGS ANALYSIS
    single_item_tags = {t: ilist for t, ilist in tag_to_items.items() if len(ilist) == 1}
    print(f"\n--- SINGLE ITEM TAGS ({len(single_item_tags)} total) ---")
    
    single_details = []
    for tag, ilist in sorted(single_item_tags.items()):
        it = ilist[0]
        single_details.append({
            'tag': tag,
            'title': it.get('name'),
            'category': it.get('category'),
            'subcategory': it.get('subcategory'),
            'path': it.get('path'),
            'desc': it.get('description', '')[:100]
        })

    # 2. DUPLICATES / NEAR-DUPLICATES / CASING / PLURAL / HYPHENATION
    tag_normalized = defaultdict(list)
    for tag in tag_to_items.keys():
        # norm key: lowercase, strip hyphens/spaces, basic singular
        norm = tag.lower().replace('-', ' ').replace('_', ' ')
        norm = ' '.join(norm.split())
        tag_normalized[norm].append(tag)

    near_duplicates = {k: v for k, v in tag_normalized.items() if len(v) > 1}

    # 3. GENERIC / REDUNDANT TAGS
    generic_tag_names = ['App', 'Apps', 'Tool', 'Tools', 'Resource', 'Resources', 'General', 'Other', 'Software', 'Web', 'Website', 'Online', 'Free', 'AI', 'Ai']
    generic_found = {t: len(tag_to_items[t]) for t in generic_tag_names if t in tag_to_items}

    # 4. WRONGLY TAGGED / MISCLASSIFIED ITEMS (e.g. Generative tools tagged as App, or category redundant tags)
    misclassifications = []
    for item in items:
        title = item.get('name')
        cat = item.get('category')
        subcat = item.get('subcategory')
        tags = item.get('tags', [])
        desc = (item.get('description') or '').lower()
        content = (item.get('content') or '').lower()

        # Check if category matches tag (e.g. Category "Tools" -> Tag "Tool")
        for t in tags:
            if cat and t.lower() == cat.lower()[:-1] or (cat and t.lower() == cat.lower()):
                misclassifications.append({
                    'type': 'Category-Tag Redundancy',
                    'title': title,
                    'category': cat,
                    'tag': t,
                    'reason': f"Tag '{t}' duplicates Category '{cat}'"
                })
            
            # Generative tools tagged as plain App/Software without generative tag
            if any(kw in desc for kw in ['generat', 'create image', 'video gen', 'ai image', 'text-to-']) and t in ['App', 'Software', 'Web App', 'Tool']:
                if not any('gen' in tag.lower() or 'image' in tag.lower() or 'video' in tag.lower() or 'creative' in tag.lower() for tag in tags):
                    misclassifications.append({
                        'type': 'Generic Tag on Generative/Specific Tool',
                        'title': title,
                        'category': cat,
                        'tag': t,
                        'all_tags': tags,
                        'reason': f"Generative/Creative tool has generic tag '{t}' but lacks specific generative/domain tag"
                    })

    report = {
        'total_items': len(items),
        'total_tags': total_tags,
        'single_item_tags': single_details,
        'near_duplicates': near_duplicates,
        'generic_tags': generic_found,
        'misclassifications': misclassifications
    }

    with open('scripts/tag_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    print("\nReport written to scripts/tag_analysis_report.json")

if __name__ == '__main__':
    analyze()

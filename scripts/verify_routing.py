import sys
import json
import os
import re

def get_test_paths():
    paths = [
        "/",
        "/rewards",
        "/prompts",
        "/tools",
        "/learning",
        "/resources",
        "/guides",
        "/frameworks",
        "/cheatsheets",
        "/templates",
        "/tags",
        "/tag-detail?tag=Marketing",
        "/bookmarks",
        "/saved",
        "/css/tokens.css",
        "/css/base.css",
        "/css/landing.css",
        "/js/app.js",
        "/js/landing.js",
        "/sending-email.jpg",
        "/favicon.png",
        "/data.json",
        "/search-index.json",
        "/robots.txt",
        "/sitemap.xml"
    ]
    
    data_path = os.path.join(os.path.dirname(__file__), '..', 'site', 'data.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data.get("items", []):
                if not item.get("is_shallow") and item.get("path"):
                    paths.append(item["path"])
    except:
        pass
        
    bundle_path = os.path.join(os.path.dirname(__file__), '..', 'site', 'bundle_mapping.json')
    try:
        with open(bundle_path, 'r', encoding='utf-8') as f:
            bundles = json.load(f)
            for bundle_id in bundles.keys():
                paths.append(f"/items/bundles/bundle-{bundle_id}")
    except:
        pass
        
    return paths

def simulate_vercel_routing(path):
    path = path.split('?')[0]
    if path == '/':
        path = '/index'
        
    site_dir = os.path.join(os.path.dirname(__file__), '..', 'site')
    
    # 1. Try exact match
    exact_path = os.path.join(site_dir, path.lstrip('/'))
    if os.path.isfile(exact_path):
        return True
        
    # 2. Try cleanUrls (.html)
    html_path = os.path.join(site_dir, path.lstrip('/') + '.html')
    if os.path.isfile(html_path):
        return True
        
    return False

def main():
    test_paths = get_test_paths()
    failures = []
            
    for p in test_paths:
        if not simulate_vercel_routing(p):
            failures.append((p, "HTTP 404 (File not found by Vercel routing rules)"))
            
    if failures:
        print(f"FAIL: {len(failures)} out of {len(test_paths)} paths failed.")
        for path, error in failures:
            print(f"- {path} failed: {error}")
        sys.exit(1)
    else:
        print(f"PASS: All {len(test_paths)} paths resolved successfully based on vercel.json rules.")

if __name__ == "__main__":
    main()

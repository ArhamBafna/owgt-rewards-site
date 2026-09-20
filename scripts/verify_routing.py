import urllib.request
import urllib.error
import sys
import json
import os

BASE_URL = "http://localhost:3000"

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
        "/owgt-rewards-logo.png",
        "/sending-email.jpg",
        "/favicon.png",
        "/data.json",
        "/search-index.json",
        "/robots.txt",
        "/sitemap.xml"
    ]
    
    # Load deep item pages
    data_path = os.path.join(os.path.dirname(__file__), '..', 'site', 'data.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data.get("items", []):
                if not item.get("is_shallow") and item.get("path"):
                    paths.append(item["path"])
    except Exception as e:
        pass
        
    # Load bundles
    bundle_path = os.path.join(os.path.dirname(__file__), '..', 'site', 'bundle_mapping.json')
    try:
        with open(bundle_path, 'r', encoding='utf-8') as f:
            bundles = json.load(f)
            for bundle_id in bundles.keys():
                paths.append(f"/items/bundles/bundle-{bundle_id}")
    except Exception as e:
        pass
        
    return paths

def main():
    test_paths = get_test_paths()
    failures = []
    
    import http.client
    # Quick check if server is up
    try:
        urllib.request.urlopen(BASE_URL + "/")
    except (urllib.error.URLError, http.client.RemoteDisconnected, ConnectionRefusedError) as e:
        print("The local server isn't running. Please start it using 'python scripts/serve.py'")
        sys.exit(1)
            
    for p in test_paths:
        url = BASE_URL + p
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req)
            status = res.getcode()
            if status != 200:
                failures.append((p, f"HTTP {status}"))
        except urllib.error.HTTPError as e:
            failures.append((p, f"HTTP {e.code}"))
        except Exception as e:
            failures.append((p, str(e)))
            
    if failures:
        print(f"FAIL: {len(failures)} out of {len(test_paths)} paths failed.")
        for path, error in failures:
            print(f"- {path} failed: {error}")
        sys.exit(1)
    else:
        print(f"PASS: All {len(test_paths)} paths loaded successfully.")

if __name__ == "__main__":
    main()

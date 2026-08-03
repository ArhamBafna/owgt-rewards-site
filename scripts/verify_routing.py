import urllib.request
import sys

BASE_URL = "http://localhost:8000"

test_paths = [
    "/",
    "/home",
    "/index",
    "/prompts",
    "/tools",
    "/guides",
    "/tags",
    "/bookmarks",
    "/items/prompts/act-as-a-skeptical-senior",
    "/act-as-a-skeptical-senior",
    "/items/bundles/bundle-cold-outreach-stack",
    "/bundle-cold-outreach-stack",
    "/search-index.json",
    "/data.json",
    "/css/base.css",
    "/js/app.js"
]

all_passed = True

print("--- ROUTING VERIFICATION TEST ---")
for p in test_paths:
    url = BASE_URL + p
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req)
        status = res.getcode()
        if status == 200:
            print(f"[OK] {p} -> HTTP {status}")
        else:
            print(f"[FAIL] {p} -> HTTP {status}")
            all_passed = False
    except Exception as e:
        print(f"[ERROR] {p} -> {e}")
        all_passed = False

if all_passed:
    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!")
else:
    print("\nSOME TESTS FAILED - INSPECT LOGS ABOVE!")

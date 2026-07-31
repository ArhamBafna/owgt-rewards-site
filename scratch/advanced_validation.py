import os
import glob
import re

all_md = glob.glob("organized-data/**/*.md", recursive=True)
failures = []

for f in all_md:
    basename = os.path.basename(f)
    if basename in ['README.md', 'master.md', 'decisions.md']:
        continue
        
    parent_dir = os.path.basename(os.path.dirname(f))
        
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Check headers
    headers = re.findall(r'^### (.*)', content, re.MULTILINE)
    expected_headers = {'Name', 'Description', 'Category', 'Tags'}
    
    if not expected_headers.issubset(set(headers)):
        failures.append(f"{f}: Missing essential headers. Found {headers}")
        
    # Check Name
    name_match = re.search(r'### Name\n(.*?)\n', content)
    if not name_match or len(name_match.group(1).strip()) < 2:
        failures.append(f"{f}: Name is missing or too short")
        
    # Check Description
    desc_match = re.search(r'### Description\n(.*?)(###|$)', content, re.DOTALL)
    if not desc_match:
        failures.append(f"{f}: Description block missing")
    else:
        desc = desc_match.group(1).strip()
        if len(desc) < 15:
            failures.append(f"{f}: Description too short ({len(desc)} chars): '{desc}'")
        if desc.startswith("Extracted from"):
            failures.append(f"{f}: Description still has 'Extracted from'")
            
    # Check Category exists and is not empty
    cat_match = re.search(r'### Category\n(.*?)\n', content)
    if not cat_match:
        failures.append(f"{f}: Category block missing")
    else:
        cat = cat_match.group(1).strip()
        if len(cat) < 2:
            failures.append(f"{f}: Category '{cat}' is too short or empty")
            
    # Check Tags
    tags_match = re.search(r'### Tags\n(.*)', content, re.DOTALL)
    if not tags_match or "- " not in tags_match.group(1):
        failures.append(f"{f}: Tags are missing or malformed")
        
if failures:
    print(f"FAILED: Found {len(failures)} errors!")
    for err in failures:
        print(err)
else:
    print("SUCCESS: 0 Errors!")

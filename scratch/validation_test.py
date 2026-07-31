import os
import glob
import re

def test_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    errors = []
    
    if "### Name\n" not in content and "### Title\n" not in content:
        errors.append("Missing ### Name or ### Title")
        
    desc_match = re.search(r'### Description\n(.*?)(###|$)', content, re.DOTALL)
    if not desc_match:
        errors.append("Missing ### Description")
    else:
        desc = desc_match.group(1).strip()
        if len(desc) < 15:
            errors.append(f"Description too short: '{desc}'")
        if desc.startswith("Extracted from"):
            errors.append("Description violates spec (starts with 'Extracted from')")
            
    if "### Category\n" not in content:
        errors.append("Missing ### Category")
        
    if "### Tags\n" not in content:
        errors.append("Missing ### Tags")
        
    if "Prompts\\" in filepath or "Prompts/" in filepath:
        if "### Prompt\n" not in content:
            errors.append("Prompt file missing ### Prompt header")
            
    return errors

all_md_files = glob.glob("organized-data/**/*.md", recursive=True)
total_files = 0
failed_files = {}

for f in all_md_files:
    if os.path.basename(f) in ['README.md', 'master.md', 'decisions.md']:
        continue
        
    total_files += 1
    errs = test_file(f)
    if errs:
        failed_files[f] = errs

print(f"Total files checked: {total_files}")
print(f"Total files failed: {len(failed_files)}")

# Print summary of failures by directory
failures_by_dir = {}
for f, errs in failed_files.items():
    directory = os.path.dirname(f)
    if directory not in failures_by_dir:
        failures_by_dir[directory] = []
    failures_by_dir[directory].append((os.path.basename(f), errs))

for d, files in failures_by_dir.items():
    print(f"\n{d}: {len(files)} failures")
    # print up to 3 examples
    for fname, errs in files[:3]:
        print(f"  - {fname}: {errs}")

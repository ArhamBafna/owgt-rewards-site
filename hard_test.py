import os
import re

def check_kebab_case(filename):
    name = os.path.splitext(filename)[0]
    if name in ['README', 'master']:
        return True
    return bool(re.match(r'^[a-z0-9\-]+$', name))

def check_file(filepath):
    errors = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    if filename in ['README.md', 'master.md', 'decisions.md']:
        return errors

    if not check_kebab_case(filename):
        errors.append(f"Filename '{filename}' is not perfectly kebab-cased.")

    # Find all h3 headers
    headers = re.findall(r'^###\s+(.*)$', content, re.MULTILINE)
    
    valid_header_3 = ['Content', 'URL', 'Prompt']
    
    if len(headers) != 5:
        errors.append(f"Expected exactly 5 headers, found {len(headers)}: {headers}")
    else:
        if headers[0] not in ['Name', 'Title']:
            errors.append(f"First header should be Name or Title, got '{headers[0]}'")
        if headers[1] != 'Description':
            errors.append(f"Second header should be Description, got '{headers[1]}'")
        if headers[2] not in valid_header_3:
            errors.append(f"Third header should be one of {valid_header_3}, got '{headers[2]}'")
        if headers[3] != 'Category':
            errors.append(f"Fourth header should be Category, got '{headers[3]}'")
        if headers[4] != 'Tags':
            errors.append(f"Fifth header should be Tags, got '{headers[4]}'")

    # Check for lazy description
    desc_match = re.search(r'### Description\n(.*?)(?=\n### )', content, re.DOTALL)
    if desc_match:
        desc = desc_match.group(1).strip().lower()
        lazy_phrases = [
            "a prompt for",
            "a prompt that",
            "a ready-to-use prompt",
            "extracted from",
            "guide on",
            "a guide on",
            "this prompt",
            "this guide"
        ]
        for phrase in lazy_phrases:
            if phrase in desc:
                errors.append(f"Lazy description found containing '{phrase}': {desc}")
                break

    return errors

def main():
    directory = 'c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/organized-data'
    total_errors = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                errors = check_file(filepath)
                if errors:
                    print(f"Errors in {filepath}:")
                    for err in errors:
                        print(f"  - {err}")
                    total_errors += len(errors)
    
    if total_errors == 0:
        print("Success: 0 errors found.")
    else:
        print(f"Total errors: {total_errors}")

if __name__ == '__main__':
    main()

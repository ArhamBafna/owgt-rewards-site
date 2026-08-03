import os
import re

SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../site'))
HEADER_TEMPLATE_PATH = os.path.join(SITE_DIR, '_templates', 'header.html')

with open(HEADER_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    HEADER_HTML = f.read()

header_regex = re.compile(r'<header class="new-global-header"[^>]*>[\s\S]*?</header>')

updated_count = 0
for root, dirs, files in os.walk(SITE_DIR):
    if '_templates' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if header_regex.search(content):
                new_content = header_regex.sub(HEADER_HTML, content)
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    updated_count += 1

print(f"Updated header in {updated_count} HTML files.")

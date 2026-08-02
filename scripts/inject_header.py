import os
import re

SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../site'))
HEADER_TEMPLATE_PATH = os.path.join(SITE_DIR, '_templates', 'header.html')

with open(HEADER_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
    HEADER_HTML = f.read()

# 1. Update build.py to read header.html and inject it.
build_py_path = os.path.join(SITE_DIR, 'build.py')
with open(build_py_path, 'r', encoding='utf-8') as f:
    build_py_content = f.read()

if 'HEADER_HTML =' not in build_py_content:
    # Read header at the top of build.py
    insertion = """
HEADER_TEMPLATE_PATH = os.path.join(SITE_DIR, '_templates', 'header.html')
try:
    with open(HEADER_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        HEADER_HTML = f.read()
except:
    HEADER_HTML = ''
"""
    build_py_content = build_py_content.replace('DATA_JSON_PATH =', insertion + '\nDATA_JSON_PATH =')
    
    # Replace in templates
    build_py_content = build_py_content.replace(".replace('{cards_html}', ''.join(cards_html))", ".replace('{cards_html}', ''.join(cards_html)).replace('{header}', HEADER_HTML)")
    build_py_content = build_py_content.replace(".replace('{tags_html}', ''.join(tags_html))", ".replace('{tags_html}', ''.join(tags_html)).replace('{header}', HEADER_HTML)")
    
    # Write back
    with open(build_py_path, 'w', encoding='utf-8') as f:
        f.write(build_py_content)
    print("Updated build.py to inject {header}")

# 2. Update standalone pages
standalone_pages = ['index.html', 'tags.html', 'bookmarks.html', 'templates.html', 'tag-detail.html']
old_header_regex = re.compile(r'<header class="new-global-header"[^>]*>[\s\S]*?</header>')

for page in standalone_pages:
    page_path = os.path.join(SITE_DIR, page)
    if os.path.exists(page_path):
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '{header}' in content:
            content = content.replace('{header}', HEADER_HTML)
        else:
            content = old_header_regex.sub(HEADER_HTML, content)
            
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Injected header into {page}")

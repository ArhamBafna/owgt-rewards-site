import os
import glob

SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../site'))

old_button = '<button class="btn btn--primary copy-main-btn" onclick="copyToClipboard(document.getElementById(\'prompt-content\').innerText, this)">Copy Content</button>'
new_button = '<button class="btn btn--primary copy-main-btn" onclick="copyToClipboard(document.getElementById(\'prompt-content\').innerText, this)" title="Copy content" aria-label="Copy content" style="padding: 6px 10px; display: inline-flex; align-items: center; justify-content: center;"><svg class="copy-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg></button>'

updated_count = 0
for filepath in glob.glob(os.path.join(SITE_DIR, '**/*.html'), recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_button in content:
        content = content.replace(old_button, new_button)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_count += 1

print(f"Successfully updated copy icon in {updated_count} HTML files.")

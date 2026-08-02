import os
import re

SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../site'))

NEW_HEADER = '''  <header class="new-global-header" id="globalHeader">
    <div class="new-header-left">
      <a href="/home" class="new-logo-link">
        <img src="owgt-rewards-logo.png" alt="OWGT Rewards Logo" class="new-header-logo">
        <span class="new-header-title">OWGT Rewards</span>
      </a>
    </div>
    <nav class="mast-nav new-header-nav" aria-label="Primary">
      <ul>
        <li><a href="prompts">Prompts</a></li>
        <li><a href="tools">Tools</a></li>
        <li><a href="guides">Guides</a></li>
        <li><a href="resources">Resources</a></li>
        <li><a href="tags">Tags</a></li>
        <li><a href="bookmarks">Bookmarks</a></li>
      </ul>
    </nav>
  </header>'''

CSS_TO_APPEND = '''
/* New Global Header */
.new-global-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background-color: var(--color-ink);
  color: var(--color-paper-2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-sm) var(--page-gutter);
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.new-global-header.hidden-on-home {
  opacity: 0;
  pointer-events: none;
  transform: translateY(-100%);
}
.new-global-header.visible-on-home {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0);
}
.new-header-left {
  display: flex;
  align-items: center;
}
.new-logo-link {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  text-decoration: none;
  color: var(--color-paper-2);
}
.new-header-logo {
  height: 28px;
  width: auto;
}
.new-header-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: -0.01em;
}
.new-header-nav ul {
  display: flex;
  gap: var(--space-md);
  margin: 0;
  padding: 0;
  list-style: none;
}
.new-header-nav a {
  color: var(--color-paper-2);
  font-family: var(--font-outlier);
  text-transform: uppercase;
  font-size: var(--text-xs);
  letter-spacing: var(--ls-label);
  text-decoration: none;
}
.new-header-nav a:hover {
  color: var(--color-accent);
}
.new-header-nav li:not(:last-child) {
  border-right: none;
  margin-right: 0;
  padding-right: 0;
}
body {
  padding-top: 60px; /* Space for the fixed header */
}
body.is-home {
  padding-top: 0; /* No space needed initially on home */
}
'''

JS_TO_APPEND = '''
// Global Header Scroll Logic
document.addEventListener('DOMContentLoaded', () => {
  const header = document.getElementById('globalHeader');
  if (!header) return;
  
  if (window.location.pathname === '/' || window.location.pathname.endsWith('/index.html') || window.location.pathname === '/home') {
    document.body.classList.add('is-home');
    header.classList.add('hidden-on-home');
    
    const target = document.querySelector('.hero-marquee'); // Using hero section
    if (target) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) {
            header.classList.remove('hidden-on-home');
            header.classList.add('visible-on-home');
          } else {
            header.classList.add('hidden-on-home');
            header.classList.remove('visible-on-home');
          }
        });
      }, { threshold: 0.1 });
      observer.observe(target);
    }
  }
});
'''

# 1. Update CSS
base_css_path = os.path.join(SITE_DIR, 'css', 'base.css')
with open(base_css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()
if '.new-global-header' not in css_content:
    with open(base_css_path, 'a', encoding='utf-8') as f:
        f.write(CSS_TO_APPEND)
    print("Updated base.css")

# 2. Update JS
app_js_path = os.path.join(SITE_DIR, 'js', 'app.js')
with open(app_js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()
if 'Global Header Scroll Logic' not in js_content:
    with open(app_js_path, 'a', encoding='utf-8') as f:
        f.write(JS_TO_APPEND)
    print("Updated app.js")

# 3. Update HTML Files
files_to_update = [
    'index.html',
    'tags.html',
    'bookmarks.html',
    'templates.html',
    'tag-detail.html',
    '_templates/category.html',
    '_templates/deep-item.html'
]

old_header_regex = re.compile(r'<header class="nav-mast">[\s\S]*?</header>')

for rel_path in files_to_update:
    file_path = os.path.join(SITE_DIR, rel_path)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '<header class="nav-mast">' in content:
            new_content = old_header_regex.sub(NEW_HEADER, content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {rel_path}")
        else:
            print(f"No old header found in {rel_path}")
    else:
        print(f"File not found: {rel_path}")

print("Done updating files.")

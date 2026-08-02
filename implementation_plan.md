# Refactor Site Folder: Organize Object & Bundle Pages into Subdirectories

This plan details how to refactor and organize ~250 individual item `.html` files and `bundle-*.html` files out of the `site/` root directory into neat category-based subfolders inside `site/items/`.

---

## Architecture Overview

Currently, `build.py` generates all individual deep item HTML pages (e.g. `1m-attention.html`, `claude.html`) and bundle pages directly in the `site/` root directory alongside core pages like `index.html`. This creates ~290 loose files in `site/`.

### Proposed Folder Structure (`rewards/site/`)

```
rewards/site/
├── index.html                    (Homepage)
├── prompts.html                  (Category Hub)
├── tools.html                    (Category Hub)
├── guides.html                   (Category Hub)
├── resources.html                (Category Hub)
├── learning.html                 (Category Hub)
├── cheatsheets.html              (Category Hub)
├── templates.html                (Category Hub)
├── frameworks.html               (Category Hub)
├── tags.html                     (Global Tags Page)
├── tag-detail.html               (Tag Detail Page)
├── bookmarks.html                (Bookmarks Vault Page)
├── _templates/                   (HTML Header/Category/Item Templates)
├── css/                          (Stylesheet assets)
├── js/                           (JavaScript app logic)
├── data.json                     (Vault JSON data)
├── search-index.json             (Search Index)
├── bundle_mapping.json           (Bundle mappings)
├── build.py                      (Build Script)
├── serve.py                      (Local HTTP Server)
└── items/                        (NEW: Organized Object Subdirectories)
    ├── prompts/                  (*.html files for Prompts)
    ├── tools/                    (*.html files for Tools)
    ├── guides/                   (*.html files for Guides)
    ├── resources/                (*.html files for Resources)
    ├── learning/                 (*.html files for Learning)
    ├── cheatsheets/              (*.html files for Cheatsheets)
    ├── templates/                (*.html files for Templates)
    ├── frameworks/               (*.html files for Frameworks)
    └── bundles/                  (bundle-*.html files)
```

---

## User Review Required

> [!IMPORTANT]
> **Essential Files Preserved at Root:** `index.html`, category hub pages (`prompts.html`, `tools.html`, `guides.html`, etc.), global pages (`tags.html`, `bookmarks.html`), assets, templates, and scripts will stay at `site/` root. Only individual item pages and bundle detail pages move into `site/items/<Category>/`.

> [!NOTE]
> **URL Compatibility:** `serve.py` will automatically resolve both short clean URLs (e.g., `/1m-attention`) and full nested paths (e.g., `/items/guides/1m-attention`), ensuring backwards compatibility for links and bookmarks.

---

## Proposed Changes

### Build System (`build.py`)

#### [MODIFY] [build.py](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/build.py)
- Create `SITE_DIR/items/` subdirectories automatically during build: `prompts/`, `tools/`, `guides/`, `resources/`, `learning/`, `cheatsheets/`, `templates/`, `frameworks/`, `bundles/`.
- Update `generate_deep_item_pages()`:
  - Save items to `site/items/<category_slug>/<item_id>.html`.
  - Update relative anchor links (`prev_html`, `next_html`) to use `/items/<category_slug>/<item_id>` paths.
- Update `generate_bundle_page()`:
  - Save bundle pages to `site/items/bundles/bundle-<bundle_id>.html`.
- Update item metadata `path` field in `data.json` and `search-index.json` to store `items/<category_slug>/<item_id>`.
- Update card link `href` targets in `generate_category_page()` and `generate_bundle_page()` to point to `/items/<category_slug>/<item_id>`.

---

### Local Server (`serve.py`)

#### [MODIFY] [serve.py](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/serve.py)
- Update `CleanURLHandler` GET routing:
  - If requested path matches a file directly in `site/`, serve it.
  - If path doesn't exist at root (e.g. `/1m-attention`), search subdirectories inside `site/items/` to find and serve `site/items/*/<slug>.html`.
  - If path specifies nested `/items/...`, translate and serve directly.

---

### Frontend Application Logic (`app.js`)

#### [MODIFY] [app.js](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/js/app.js)
- Ensure search overlay results and randomizer navigate using full `item.path` (`items/<category_slug>/<item_id>`).

---

### Root File Cleanup

#### [DELETE] Loose object HTML files in root `site/`
- Remove all loose deep item `.html` files (e.g., `1m-attention.html`, `claude.html`, etc.) and `bundle-*.html` from `rewards/site/` root after building them into `rewards/site/items/`.

---

## Verification Plan

### Automated Build Verification
1. Run `python build.py` from `rewards/site/`.
2. Confirm `site/items/` subdirectories are populated with organized `.html` files.
3. Confirm `site/` root contains only essential hub pages, scripts, and directories.
4. Verify `data.json` and `search-index.json` contain updated item paths.

### Server & Link Verification
1. Run `python site/serve.py`.
2. Test navigating to category pages, bundle pages, and individual deep item pages.
3. Verify clean URL resolution works for both short URLs and nested item URLs.

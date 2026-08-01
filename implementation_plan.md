# Complete OWGT Rewards Problems & Fix Implementation Plan (Concrete & Refined)

This document organizes all reported issues across the OWGT Rewards website and defines the finalized, highly concrete technical solutions based on codebase inspection and user feedback.

---

## User Decisions & Clarifications (Resolved)

1. **Spotlight Alignment:** Top navigation (`Browse | Spotlight | Use Cases`) will have "Spotlight" centered with balanced link spacing and visual separators retained.
2. **Spotlight Shallow Items:** Shallow objects will display all content directly on the Spotlight card view; no external links or details subpages will open.
3. **Tag System Overhaul:** Tag system will be completely refactored to render dynamically from `data.json` via JavaScript instead of static hardcoded HTML.
4. **Category Items Mismatch:** Investigate root cause (fetching logic vs. DOM rendering vs. JSON data) to ensure item count badges match displayed items.
5. **Shallow Item Expansion:** Retain current Quick View expansion UI/behavior, but expand whole `.card` click area so clicking anywhere on the card container triggers expansion.
6. **Curated Bundles:** Create dedicated bundle pages/views for each of the bundle items listed on the homepage and link each button directly to its corresponding bundle.
7. **Missing Object Links:** Audit both Python ingestion scripts and Markdown data files in `organized-data/` to locate missing URLs/content and populate them.
8. **Markdown Rendering:** Integrate full Markdown parser library (`marked.js` + `highlight.js`) to render all Markdown features (headers, code blocks with syntax highlighting, lists, tables).
9. **Header Logo URL:** Change logo link target to `/home` across all pages.

---

## Concrete Technical Changes

### 1. Homepage Navigation Alignment
- **Files:** [base.css](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/css/base.css), [index.html](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/index.html)
- **Concrete Fix:** Update `.mast-nav ul` CSS to set equal margin and padding (`gap: var(--space-xl)`) on both sides of middle items in `.mast-nav li:not(:last-child)`, retaining vertical rule borders while keeping "Spotlight" visually centered.

### 2. Copy Button Behavior & Feedback
- **File:** [app.js](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/js/app.js#L215-L232)
- **Concrete Fix:** In `copyToClipboard()` and `initSpotlight()`, remove the call to `showToast()`. Update button styling on click: set `backgroundColor = "var(--color-success)"` (green `#22c55e`), change text to `"✔ COPIED!"`, and revert after 2 seconds.

### 3. Spotlight Shallow Resource View
- **File:** [app.js](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/js/app.js#L263-L323)
- **Concrete Fix:** In `updateSpotlight()`, check `item.is_shallow`. If `item.is_shallow` is `true`, hide `#spotlight-link-btn` (View details) and display the full item content directly in `#spotlight-desc`.

### 4. Tag System Dynamic Overhaul
- **Files:** [build.py](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/build.py), [tags.html](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/tags.html), [tag-detail.html](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/tag-detail.html)
- **Concrete Fix:**
  - Update `build.py` to write exact `tag_counts` into `data.json`.
  - Refactor `tags.html` JavaScript to fetch `data.json`, dynamically render all tag pills with exact counts, and handle tag filter clicks.

### 5. Category Item Count & Card Rendering Sync
- **File:** [build.py](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/build.py#L62-L122)
- **Concrete Fix:** Re-run `python build.py` after verifying template string substitution so `{item_count}` equals `len(cat_items)` and all `cat_items` from `organized-data/` are rendered in `cards_html` across all category pages (`prompts.html`, `tools.html`, `guides.html`, `templates.html`, `frameworks.html`).

### 6. Subcategory Footer Centering
- **File:** [base.css](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/css/base.css)
- **Concrete Fix:** Apply `text-align: center; justify-content: center;` to `.foot-mast` and `.foot-mast .container` elements across all layout templates.

### 7. Global Footer Standardization
- **Files:** [category.html](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/_templates/category.html), [deep-item.html](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/_templates/deep-item.html), [index.html](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/index.html)
- **Concrete Fix:** Standardize footer HTML in `_templates/category.html` and `_templates/deep-item.html` to match `index.html` structure and append `<p class="mast-line" style="margin-top: 8px;">MADE BY ARHAM</p>`. Run `python build.py`.

### 8. Shallow Item Card Click Area & Placeholder Removal
- **Files:** [build.py](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/build.py#L70-L90), [app.js](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/js/app.js)
- **Concrete Fix:**
  - Remove generic placeholder text ("The world's best digital knowledge library for AI") from card templates in `build.py`.
  - In `app.js`, add event delegation on `.card--expandable` so clicking anywhere on the card container toggles expansion (while avoiding double-triggers on action buttons like Save or links).

### 9. Subcategory Header UI & Color Palette
- **Files:** [base.css](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/css/base.css), [build.py](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/build.py)
- **Concrete Fix:** Reduce category header font size from `clamp(3rem, 8vw, 8rem)` to `clamp(2rem, 5vw, 4rem)`. Inject genre-specific Hallmark color tokens (`var(--color-cat-prompts)`, `var(--color-cat-tools)`, etc.) into category header backgrounds.

### 10. Navigation Bar Link Consistency & Active Highlight
- **Files:** [category.html](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/_templates/category.html), [deep-item.html](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/_templates/deep-item.html), [app.js](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/js/app.js)
- **Concrete Fix:** Standardize `<nav class="mast-nav">` across all template files to include all 6 links: `Prompts`, `Tools`, `Guides`, `Resources`, `Tags`, `Bookmarks`. In `app.js`, add `highlightActiveNav()` to match `window.location.pathname` and apply `.active` CSS class.

### 11. Header Logo URL Update
- **Files:** [category.html](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/_templates/category.html), [deep-item.html](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/_templates/deep-item.html), [index.html](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/index.html)
- **Concrete Fix:** Update logo anchor `href` from `index.html` to `/home` across all template files.

### 12. Homepage Header Text Update
- **File:** [index.html](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/index.html#L124)
- **Concrete Fix:** Replace `<h2>Browse By Category</h2>` with `<h2>Categories</h2>`.

### 13. Curated Bundles Implementation
- **Files:** [build.py](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/build.py#L213-L224), [index.html](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/index.html)
- **Concrete Fix:** Update `build.py` to generate dynamic bundle detail pages (`bundle-cold-outreach-stack.html`, `bundle-content-creation.html`, `bundle-ai-research.html`, `bundle-build-ai-apps.html`) for all items in `use_cases`, and update homepage scroll-cards to link directly to these pages.

### 14. Full Markdown Parser & Syntax Highlighting
- **Files:** [deep-item.html](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/_templates/deep-item.html), [app.js](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/js/app.js)
- **Concrete Fix:** Add `marked.js` and `highlight.js` libraries to deep item pages. Parse markdown text dynamically on load and render code blocks with syntax highlighting and styled blockquotes.

### 15. Data & Ingestion Script Audit
- **Files:** [build.py](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/build.py), Markdown files in `organized-data/`
- **Concrete Fix:** Inspect Markdown files in `organized-data/` (such as `how-to-spot-100m-product-ideas.md`) to verify and populate missing `URL` or `Content` fields. Re-run `python build.py`.

### 16. Save Button Visual Color State
- **Files:** [app.js](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/js/app.js#L151-L165), [base.css](file:///c:/Users/bafna/Desktop/Projects/OWGT-Newsletter-Automation/rewards/site/css/base.css)
- **Concrete Fix:** Update `updateBookmarkUI()` in `app.js`: when `isBookmarked` is true, apply `background: var(--color-danger)` (red `#ef4444`), text color white, and button text `"♥ Saved"`. Remove dark pop-out shadow on hover.

---

## Verification Plan

### Automated Build Verification
- Execute `python build.py` from `rewards/site/` directory and confirm output reports clean generation of all item pages, category pages, `data.json`, and `search-index.json`.

### Manual Verification
- Test logo link points to `/home`.
- Click copy button and verify background turns green without toast.
- Verify Spotlight shallow resources display content inline without 404 links.
- Open `templates.html` and verify item count badge matches displayed cards.
- Click whole card container on shallow items to verify expansion.
- Check bundle buttons on homepage to verify navigation to bundle pages.
- Check deep item page to verify markdown headers, code block syntax highlighting, and blockquote styling.
- Click save button to verify red background and heart icon toggle.

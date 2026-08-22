---
name: add-reward-item
description: Ingest URL, prompt, guide, tool, or resource into rewards database across data/, organized-data/, and site/.
---

# Add Reward Item

Ingest item into `data/`, `organized-data/`, and `site/`. If input ambiguous, grill user with `/grill-me`.

## Rules

- **Exhaustive content**: If extracting content, extract 100% of items without loss or truncation. If 100% extraction cannot be guaranteed, store source URL redirect instead.
- **Pre-fetch first**: Fetch full text before deciding redirect vs inline content.
- **Raw-first**: Always save raw link/text into `data/` before organizing.
- **Tag reuse**: Match existing tags in `rewards/organized-data/tags.txt`. Only coin new tag if unique and necessary.
- **Relative paths**: Scripts must use `os.path.dirname(__file__)` — zero hardcoded absolute paths.
- **Zero temp residue**: Delete one-off helper scripts immediately after execution.

## Workflow

### 1. Ingest & Classify
- **Fetch**: Read full page text (`read_url_content`, Firecrawl, or Exa).
- **Process**: If step-by-step tutorial, run `rewards/.agents/skool-guide-to-md/SKILL.md` to de-brand and structure.
- **Description**: State exact utility and mechanism. Never write vague summaries ("App repo by X").

### 2. Save Raw (`data/`)
- Choose target in `rewards/data/` (`bookmarks.txt`, `prompts.txt`, `github.txt`, `notion.txt`, `skills.txt`, `skool-communites/`, `youtube/`). If uncertain, ask user.
- Append raw title and URL/text.

### 3. Save Organized Markdown (`organized-data/`)
- Assign category: `Cheat Sheets`, `Frameworks`, `Guides`, `Learning`, `Prompts`, `Resources`, `Templates`, `Tools`.
- Select tags from `rewards/organized-data/tags.txt`.
- Write `rewards/organized-data/<Category>/<slug>.md`:
  ```markdown
  ### Name
  <Title>

  ### Description
  <Exact utility and function>

  ### Category
  <Category>

  ### URL
  <URL or empty>

  ### Content
  <Full text / prompt / guide content>

  ### Tags
  - <Tag1>
  - <Tag2>
  ```
- Rebuild indices:
  ```powershell
  python scripts/generate_indices.py
  ```

### 4. Sync Site (`site/`)
- **JSON indices**: Update `site/data.json` and `site/search-index.json`. Recalculate `site/data.json["tags"]`.
- **Item page**: Create `site/items/<category-slug>/<slug>.html`. Wire `Previous` and `Next` links to sibling items.
- **Category page**: Add card to `site/<category-slug>.html` and increment header count badge (`X curated entries.`).
- **Cleanup**: Delete any scratch/sync script used.

### 5. Finalize & Publish
- Update code graph:
  ```powershell
  graphify update .
  ```
- Commit and push:
  ```powershell
  git add .
  git commit -m "add: <item-slug> reward entry"
  git push
  ```

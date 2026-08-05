---
name: add-reward-item
description: Add new item, URL, prompt, guide, tool, or resource into rewards database across data/, organized-data/, and site. Trigger when user pastes link, info, guide, or asks to add reward entry.
---

# Add Reward Item

Add new entry to `data/`, `organized-data/`, and `site/`. Read `/grill-me` skill. Use it anytime input ambiguous.

## Anti-Patterns
- NEVER store plain URL redirect without getting page content first.
- NEVER skip raw data entry in `data/`.
- NEVER leave `organized-data/` unindexed; always run build scripts.
- NEVER write generic or vague descriptions (e.g., "App repo by X").
- NEVER invent brand new tags if existing tags fit; check `rewards/organized-data/tags.txt` first.

## Workflow

### 1. Fetch & Parse Input
- **URL/Link**: If link, read full page text via `read_url_content` or Firecrawl/Exa. If content extractable, prefer directly stating content on site over giving link user to redirect to. Extract specific value proposition and details for description and content.
- **Guide/Tutorial**: If text extracted, if step-by-step guide, run `rewards/.agents/skool-guide-to-md/SKILL.md` to de-brand AI terms and structure markdown first.
- **Description Quality**: Do NOT write generic summaries. State exact function and utility (can use extracted info). If not 100% sure, use `/grill-me` to ask user for description.

### 2. Save Raw Data (`rewards/data/`)
- Ask user target raw file/folder in `rewards/data/` (`bookmarks.txt`, `prompts.txt`, `github.txt`, `notion.txt`, `skills.txt`, `skool-communites/`, `youtube/`).
- Write raw link/text into selected target.

### 3. Save Organized Item (`rewards/organized-data/`)
- Categorize: `Cheat Sheets`, `Frameworks`, `Guides`, `Learning`, `Prompts`, `Resources`, `Templates`, `Tools`.
- **Tags Selection**:
  - Read `rewards/organized-data/tags.txt` for existing tags.
  - MUST prefer existing tags from `tags.txt`.
  - Only add a NEW tag if item is unique, highly specific, or start of a new series/category.
- Create `rewards/organized-data/<Category>/<slug>.md`:
  ```markdown
  ### Name
  <Title>

  ### Description
  <Specific, high-value description>

  ### Category
  <Category>

  ### URL
  <URL or empty>

  ### Content
  <Full scraped text / prompt / guide content>

  ### Tags
  - <tag1>
  - <tag2>
  ```
- Run index script (updates `master.json`, `master.md`, `tags.txt`):
  ```powershell
  python scripts/generate_indices.py
  ```

### 4. Commands 
- Build Website (`rewards/site/`)
  ```powershell
  python site/build.py
  ```
- Update graphify:
  ```powershell
  graphify update .
  ```

### 5. Commit and Push Changes
- Stage, commit, and push changes to remote:
  ```powershell
  git add .
  git commit -m "add: <item-name> reward entry"
  git push
  ```


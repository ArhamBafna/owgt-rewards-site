---
name: add-reward-item
description: Add single or batch items, URLs, prompts, guides, tools, or resources into rewards database across data/, organized-data/, and site. Trigger on links, guides, snippets, or batch additions.
---

# Add Reward Item(s)

Add single or batch entries into `data/`, `organized-data/`, and `site/`.

## Core Guardrails
- **Full extraction or redirect**: If extracting page content, extract 100% of items without truncation or omission. If 100% extraction cannot be guaranteed, store redirect URL instead of partial text.
- **Always preserve raw data**: Every item must be recorded in `data/`.
- **Existing tags first**: Check `rewards/organized-data/tags.txt` and match existing tags before introducing new ones.
- **Specific utility descriptions**: State exact function and practical utility. Never write vague summaries (e.g. "App repo by X").
- **Inspect generated sync changes**: Never commit automated site edits without inspecting changed files via `view_file`.

## Phased Batch Workflow

### Phase 1: Parse & Segment
1. Inspect input and identify all discrete items (URLs, bullet lists, markdown guides, prompts, or text blocks).
2. Segment input into an ordered item queue: `[Item 1, Item 2, ... Item N]`.

### Phase 2: Fetch & Extract
For each item in the queue:
- **Web Pages / URLs**: Read full text via `read_url_content` or Firecrawl/Exa.
  - If content is completely extracted: retain parsed body for organized item.
  - If content is dynamic/paywalled/truncated: keep external URL redirect.
  - If URL is unreachable or 404: record item as failed and proceed with remaining queue.
- **Step-by-Step Guides**: Run `rewards/.agents/skool-guide-to-md/SKILL.md` to format markdown and remove AI branding.
- **Descriptions**: Derive specific utility description.

### Phase 3: Single-Round Ambiguity Resolution
If any item in the batch has unclear categorization, missing tags, doubtful description, or unknown raw target:
1. Aggregate all open questions across the entire batch.
2. Trigger a single `/grilling` round to resolve all ambiguities with the user before writing files.

### Phase 4: Batch Storage (Raw & Organized)
1. **Raw Storage (`rewards/data/`)**:
   Auto-route and append each raw item by source type:
   - Bookmarks / articles -> `rewards/data/bookmarks.txt`
   - Prompts -> `rewards/data/prompts.txt`
   - GitHub repositories -> `rewards/data/github.txt`
   - YouTube links -> `rewards/data/youtube/`
   - Notion pages -> `rewards/data/notion.txt`
   - Agent skills -> `rewards/data/skills.txt`

2. **Organized Markdown (`rewards/organized-data/`)**:
   Map category to one of: `Cheat Sheets`, `Frameworks`, `Guides`, `Learning`, `Prompts`, `Resources`, `Templates`, `Tools`.
   Write `rewards/organized-data/<Category>/<slug>.md` for each item:
   ```markdown
   ### Name
   <Title>

   ### Description
   <Specific utility description>

   ### Category
   <Category>

   ### URL
   <URL or empty>

   ### Content
   <Full extracted content / prompt / guide>

   ### Tags
   - <tag1>
   - <tag2>
   ```

### Phase 5: Single Index & Site Sync
1. **Regenerate indices**:
   ```powershell
   python scripts/generate_indices.py
   ```
2. **Sync site database and HTML pages**:
   - Update `rewards/site/data.json` and `rewards/site/search-index.json`.
   - Update tag counts and category counts.
   - Generate standalone item page: `rewards/site/items/<category-slug>/<slug>.html`.
   - Update category overview: `rewards/site/<category-slug>.html`.
   - Delete any temporary helper script used during sync.
3. **Verification Gate**:
   - Use `view_file` to inspect `data.json` and updated HTML files.
   - Ensure accurate card links, tag counts, and navigation pointers.

### Phase 6: Batch Git Commit & Summary
1. Update graphify:
   ```powershell
   graphify update .
   ```
2. Stage and commit all batch changes in a single commit:
   ```powershell
   git add .
   git commit -m "add reward: <Item 1>, <Item 2> (<N> items)"
   git push
   ```
3. Report completion summary to user:
   - List all successfully added items with assigned categories and tags.
   - List any failed items with failure reason.

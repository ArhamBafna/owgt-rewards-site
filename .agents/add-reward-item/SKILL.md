---
name: add-reward-item
description: Add single or batch items into rewards database (data/, organized-data/, site/). Trigger on links, guides, snippets, or batch additions.
---

# Add Reward Item(s)

### 1. Parse & Segment
Split input into item queue: `[Item 1, ... Item N]`.

### 2. Fetch & Extract
For each item:
- **URL**: Fetch full page. Extract full text if you can guarantee 100% complete; else store redirect URL. If 404/broken, mark failed and continue.
  - **Paywall/Login Rule**: If link is LinkedIn Learning, NVIDIA DLI, Coursera, Udemy, or YouTube, skip full-text web scrape and create shallow redirect course entry immediately.
- **If Appropriate**: Run `.agents/skool-guide-to-md/SKILL.md` to format markdown.
- **Description**: Write specific function/utility summary (no generic fluff).

### 3. Disambiguation (Sweet Spot)
- Prefer running routine steps autonomously.
- If anomaly/unknown conflict occurs, be very happy to aggregate into single round and ask user with recommended answer.
- I would rather have accurate (according to me) addition of reward items rather than you assuming and guessing things that are wrong .

### 4. Save Raw & Organized Data
1. **Raw (`rewards/data/`)**: Append to matching source based on auto-routing matrix:
   - `github.com` -> `rewards/data/github.txt`
   - `youtube.com` / `youtu.be` -> `rewards/data/youtube/` or `bookmarks.txt` (agent decides; ask if unsure)
   - `notion.so` / `notion.site` -> `rewards/data/notion.txt`
   - Pure prompt text (no URL) -> `rewards/data/prompts.txt`
   - Skill guide text -> `rewards/data/skills.txt`
   - Other web links -> `rewards/data/bookmarks.txt`
   - Unclassifiable -> Agent decides or asks human
2. **Organized (`rewards/organized-data/<Category>/<slug>.md`)**:
   - Categories: `Cheat Sheets`, `Frameworks`, `Guides`, `Learning`, `Prompts`, `Resources`, `Templates`, `Tools`.
   - **Slug Rule**: Lowercase, alphanumeric, hyphens only, no trailing punctuation (e.g. `openai-prompt-engineering` not `openai-prompt-engineering!`).
   - Tags: Match existing in `rewards/organized-data/tags.txt` first.
   - Format:
     ```markdown
     ### Name
     <Title>

     ### Description
     <Specific description>

     ### Category
     <Category>

     ### URL
     <URL or empty>

     ### Content
     <Full extracted text or empty>

     ### Tags
     - <tag1>
     - <tag2>
     ```

### 5. Site Sync & Verification
1. Run synchronizer:
   ```powershell
   python scripts/sync_site.py
   ```
2. Verify output files via `view_file`.

### 6. Git & Summary
1. Update graphify:
   ```powershell
   graphify update .
   ```
2. Commit & push. Follow batch naming convention:
   - 1 item: `add reward: <Item Name>`
   - 2+ items: `add rewards: <Item 1>, <Item 2> + N more (<Total> items)`
   ```powershell
   git add .
   git commit -m "<apply naming convention>"
   git push
   ```
3. Report added items and any failed URLs.

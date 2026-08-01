# OWGT Rewards — Information Architecture & UX Design Plan

> **Brand**: OWGT Rewards
> **Theme**: Hallmark Carnival (full energy — bold, unapologetically fun, premium)
> **Genre**: Playful (post-Linear soft school, mapped to Carnival's display-heavy warmth)
> **Access**: Open for now (auth layer planned for later)
> **Tech**: Multi-page static site (HTML/CSS/JS, no framework)
> **Library Size**: 353 items across 8 categories

---

## 1. DATA QUALITY ISSUES (Clean Before Build)

> **CAUTION**: The following issues MUST be resolved in `organized-data/` before site generation.

### 1.1 Duplicate Files
These pairs contain identical or near-identical content with different slugs:

| File A | File B |
|--------|--------|
| `diagnose-why-something-isn-t-working.md` | `diagnose-why-something-isnt-working.md` |
| `make-the-decision-you-ve-been-avoiding.md` | `make-the-decision-youve-been-avoiding.md` |
| `generate-alternatives-when-you-re-stuck.md` | `generate-alternatives-when-youre-stuck.md` |
| `get-devil-s-advocate-feedback.md` | `get-devils-advocate-feedback.md` |
| `apply-devil-s-advocate.md` | `apply-devils-advocate.md` |
| `claude-analyze-second-order-consequences.md` | `analyze-second-order-consequences.md` (different source, same intent) |
| `analyze-customer-feedback.md` | `analyze-customer-feedback-for-growth-signals.md` (potential overlap) |
| `Fireflies.Ai` (Tools): `fireflies-ai.md` | `firefliesai.md` |
| `Cursor`: `cursor.md` | `cursor-ide.md` |
| `React Bits`: appears in both Resources/ and Tools/ |
| `AnimeJS`: appears in both Resources/ and Tools/ |
| `Hover.dev`: appears in both Resources/ and Tools/ |
| `39 Claude Skills Examples`: appears in both Guides/ and Resources/ |

### 1.2 PDF Extraction Artifacts
Files with garbage text bleeding in from PDF column parsing:

- `Learning/ai-ethics-and-governance-awareness.md` — Contains `THEAiREPORT`, `XIEXECUTIVESPASS`, `GETTHEAIEXECUTIVES` junk at the bottom
- `Learning/ai-presentation-and-document-production.md` — Contains `AI-ASSISTEDRESEARCH`, `THEiREPORT` run-on text
- `Learning/ai-agent-coordination.md` — Contains `AICONTENT AND COMMUNICATIONS` junk from adjacent column
- `Tools/hubspot-ai.md` — Contains `LAVENDER` and `MARKETO ENGAGE` from adjacent entries plus ` | 18` page number
- `Tools/marketo-engage.md` — Contains `CAMPAIGN SCALE`, `PIPELINE`, `RELATIONSHIPS` chart labels plus ad text about "AI Leaders Launch Guide $27"
- Most Learning/ "skill" files have similar column-bleed issues

### 1.3 Misclassified Items
- `Prompts/execution-directive.md` — Name starts with `**Execution Directive` (formatting leak), content is an execution instruction, not a prompt
- `Prompts/stack.md` — Name starts with `- **Stack`, content is a tech stack specification, not a prompt
- `Prompts/time-of-day-light.md` — Name starts with `- Time of day / light`, content is a Midjourney parameter fragment
- `Prompts/set-team-priorities.md` — Contains TWO different prompts concatenated (Set Team Priorities + Deliver Difficult News)

### 1.4 Tag Inconsistencies
Near-duplicate tags that should be consolidated:

| Keep | Merge Into It |
|------|---------------|
| `Workflow` | `Workflows` |
| `Tool` | `Tools` |
| `Prompt` | `Prompts` |
| `Template` | `Templates` |
| `AI Agents` | `Agents`, `Agent` |
| `Cold Email` | `Cold` |
| `Prompt Engineering` | `Prompting` |

### 1.5 Missing/Broken Content
- `Cheat Sheets/mobile-app-growth-cheat-sheet.md` — Only 254 bytes, likely stub
- Many Resources/ entries are link-only (no description beyond a sentence + URL)
- Several Learning/ files (`lesson-*`) are link-only (URL + tags, no content body)

---

## 2. LIBRARY ORGANIZATION SUMMARY

### 2.1 Current Structure (Source of Truth)

| Category | Count | Schema Fields | Content Depth |
|----------|-------|---------------|---------------|
| **Prompts** | 158 | Name, Description, Prompt/Content, Category, Tags | Short to long (1 line to multi-page master prompts) |
| **Tools** | 84 | Name, Description, Content (optional), URL (optional), Category, Tags | Short descriptions, some with detailed "What it does / Workflow it replaces / Best for" blocks |
| **Resources** | 54 | Name, Description, URL, Category, Tags | Link-heavy, minimal descriptions |
| **Guides** | 25 | Name, Description, Content, Category, Tags | Long-form (1KB to 22KB), step-by-step tutorials |
| **Learning** | 25 | Name, Description, Content/URL, Category, Tags | Two sub-types: "Skills" (PDF-extracted skill descriptions) and "Lessons" (link-only course references) |
| **Frameworks** | 3 | Name, Description, URL, Category, Tags | Link-only references to external repos |
| **Cheat Sheets** | 2 | Name, Description, Content, Category, Tags | Dense quick-reference material |
| **Templates** | 2 | Name, Description, URL, Category, Tags | Link-only references to Google Sheets |

### 2.2 Prompt Subcategories (Existing, Within Files)

| Subcategory | Count | Examples |
|-------------|-------|----------|
| Generic "Prompts" | 128 | Most Claude prompts, many with no subcategory |
| Thinking & Strategy | 8 | SWOT, first-principles, scenario planning |
| Marketing | 7 | Hashtag strategy, content ideas, repurposing |
| Communication | 5 | Email reply, polite decline, meeting summary |
| Business Ops | 4 | SOP creation, onboarding, KPI design |
| Sales | 4 | Cold email, cold DM, objection response |
| Video | 2 | Cinematic real estate, video script |

### 2.3 Content Schemas (Per Type)

All files share a common structure:
```
### Name        -> Title of the item
### Description -> One-line summary
### Content     -> (or ### Prompt) — The actual body content
### URL         -> External link (when applicable)
### Category    -> Classification label
### Tags        -> Dash-prefixed list of tags
```

**Variation by type:**
- **Prompts** use `### Prompt` with a code block (most), or `### Content` with inline text
- **Tools** may or may not have `### Content` (some are metadata-only with URL)
- **Guides** always have `### Content` with long-form structured text
- **Resources** are almost always metadata + URL only
- **Learning** splits into "skill descriptions" (with Content) and "lesson links" (URL only)

---

## 3. INFORMATION ARCHITECTURE

### 3.1 Site Map

```
OWGT Rewards
|
+-- / (Homepage)
|   +-- Hero (rotating spotlight)
|   +-- Browse by Category (8 category cards)
|   +-- Auto-generated Collections
|   +-- Prompt Spotlight (random featured prompt)
|   +-- Quick Stats (353 items, 8 categories)
|   +-- Explore by Use Case (entry points)
|
+-- /prompts/ (Category Page)
|   +-- Search + Filters
|   +-- Subcategory Tabs
|   +-- Prompt Cards Grid
|       +-- /prompts/[slug]/ (Individual Prompt Page)
|
+-- /tools/ (Category Page)
|   +-- Search + Filters
|   +-- Tool Cards Grid
|       +-- /tools/[slug]/ (Individual Tool Page)
|
+-- /resources/ (Category Page)
|   +-- Search + Filters
|   +-- Resource Cards Grid
|       +-- /resources/[slug]/ (Individual Resource Page)
|
+-- /guides/ (Category Page)
|   +-- Search + Filters
|   +-- Guide Cards Grid
|       +-- /guides/[slug]/ (Individual Guide Page)
|
+-- /learning/ (Category Page)
|   +-- Search + Filters
|   +-- Learning Cards Grid
|       +-- /learning/[slug]/ (Individual Learning Page)
|
+-- /frameworks/ (Category Page)
|   +-- /frameworks/[slug]/
|
+-- /cheat-sheets/ (Category Page)
|   +-- /cheat-sheets/[slug]/
|
+-- /templates/ (Category Page)
|   +-- /templates/[slug]/
|
+-- /tags/ (Tag Index)
|   +-- /tags/[tag]/ (Tag Page — all items with this tag)
|
+-- /use-cases/ (Use Case Bundles)
|   +-- /use-cases/[slug]/ (e.g., "cold-outreach", "content-creation")
|
+-- /search/ (Dedicated Search Page)
|
+-- /bookmarks/ (User's Saved Items — local storage)
```

### 3.2 Navigation Architecture

#### Primary Navigation (Always Visible)
```
+-------------------------------------------------------------+
|  OWGT REWARDS    Prompts  Tools  Guides  More v   [S] [<3]  |
+-------------------------------------------------------------+
```

- **Logo/Brand**: "OWGT REWARDS" — links to homepage
- **Primary Links**: Prompts (158), Tools (84), Guides (25) — the three largest categories get top-level links
- **"More" Dropdown**: Resources, Learning, Frameworks, Cheat Sheets, Templates, Use Cases, Tags
- **Search Icon**: Opens search overlay (or links to /search/)
- **Bookmarks Icon**: Opens bookmarks sidebar or links to /bookmarks/

> **IMPORTANT**: Why not all 8 categories in the top nav? 8 links is too many. The top nav should surface the 3 categories people visit most (Prompts dominate at 45%, Tools at 24%, Guides at 7%). The remaining 5 categories are accessible from "More" and from the homepage category grid. This keeps the nav clean without hiding anything.

#### Mobile Navigation
- Hamburger menu -> full-screen overlay with all 8 categories + search + bookmarks
- Bottom sticky bar: Search | Prompts | Tools | Bookmarks

#### Breadcrumbs (Every Non-Homepage Page)
```
OWGT Rewards > Prompts > Cold Email
OWGT Rewards > Tags > Claude
OWGT Rewards > Use Cases > Cold Outreach
```

### 3.3 Page Hierarchy & Priority

| Priority | Pages | Rationale |
|----------|-------|-----------|
| P0 | Homepage, Prompts category, individual prompt pages | 45% of content, highest traffic |
| P1 | Tools category, individual tool pages | 24% of content, highest perceived value |
| P2 | Guides category, individual guide pages | Deep content, highest engagement time |
| P3 | Resources, Learning, Search, Tags, Use Cases | Supporting navigation |
| P4 | Frameworks, Cheat Sheets, Templates, Bookmarks | Small categories, utility pages |

---

## 4. PROMPT SUBCATEGORY REDESIGN

> **IMPORTANT**: This is the biggest IA challenge. 158 prompts in one bucket is overwhelming. The existing subcategories are inconsistent (128 are just "Prompts"). Here's the redesigned taxonomy based on actual content analysis.

### 4.1 New Prompt Subcategories (Derived from Content)

| Subcategory | Description | Approx. Count |
|-------------|-------------|----------------|
| **Strategy & Thinking** | First principles, devil's advocate, scenario planning, decision frameworks, risk assessment, SWOT, blind spots | ~25 |
| **Writing & Communication** | Email drafts, meeting summaries, announcements, diplomatic responses, executive summaries, talking points | ~30 |
| **Sales & Outreach** | Cold email, cold DM, objection handling, follow-ups, proposals, sales calls | ~15 |
| **Leadership & Management** | Team priorities, difficult conversations, performance reviews, culture assessment, onboarding, hiring | ~25 |
| **Analysis & Research** | Data analysis, competitor analysis, market research, root cause analysis, customer feedback | ~20 |
| **Business Operations** | SOPs, KPI frameworks, project kickoffs, workflow audits, pricing decisions, investment analysis | ~20 |
| **Creative & Content** | Content ideas, hooks, video scripts, captions, repurposing, newsletter drafts | ~15 |
| **AI & Technical** | Prompt engineering directives, stack specifications, AI workflow instructions | ~8 |

### 4.2 How Subcategories Work in the UI

On `/prompts/`:
```
+------------------------------------------------------+
|  ALL  Strategy  Writing  Sales  Leadership           |
|       Analysis  Business Ops  Creative  AI/Tech      |
+------------------------------------------------------+
|  [Search prompts...]           [Filter by tag v]     |
+------------------------------------------------------+
|  +----------+  +----------+  +----------+            |
|  | Cold     |  | SWOT     |  | Meeting  |            |
|  | Email    |  | Analysis |  | Summary  |            |
|  | -------- |  | -------- |  | -------- |            |
|  | Sales    |  | Strategy |  | Writing  |            |
|  +----------+  +----------+  +----------+            |
+------------------------------------------------------+
```

- **Horizontal tabs** for subcategories (scrollable on mobile)
- **"ALL" tab** shows everything (default)
- Each tab shows a count badge
- Tags are an orthogonal filter — you can be on "Sales" tab AND filter by "Claude" tag

---

## 5. USE CASE BUNDLES (Auto-Generated Collections)

> **Decision**: Auto-generate from tags/categories rather than manual curation.

### 5.1 Use Case Bundle Logic

Each "use case" is defined by a rule that pulls items matching certain tag/category combinations:

| Use Case | Rule | Expected Items |
|----------|------|----------------|
| **Cold Outreach Stack** | Tags include any of: Cold, Cold Email, Sales, Outreach | Prompts + Tools + Guides |
| **Content Creation** | Tags include: Content, Writing, Copywriting, Newsletter | Mixed |
| **AI Research** | Tags include: Research, AI Research, Perplexity, RAG | Mixed |
| **Build AI Apps** | Tags include: Coding, App Development, Agents, API | Guides + Tools + Frameworks |
| **Prompt Engineering** | Tags include: Prompt Engineering, Prompting, Prompt | Prompts + Guides + Cheat Sheets |
| **Video & Motion** | Tags include: Video, Animation, Motion, Graphics | Prompts + Tools + Guides |
| **Career & Hiring** | Tags include: Career, Job, Hiring, Recruiting, Job Search | Mixed |
| **Marketing Stack** | Tags include: Marketing, Email Marketing, SEO, Growth | Mixed |
| **Developer Toolkit** | Tags include: CLI, API, GitHub, Developer Tools, Frontend | Tools + Resources |
| **No-Code Automation** | Tags include: No-Code, Automation, Workflow, Zapier, Make | Tools + Guides |

### 5.2 Use Case Page Layout

Each use case page at `/use-cases/[slug]/` shows:
1. **Title + description** (auto-generated from the rule)
2. **Items grouped by content type** (Prompts section, Tools section, Guides section)
3. **Cross-links to full category pages** ("See all 158 prompts ->")

---

## 6. TAG SYSTEM

### 6.1 Tag Architecture

After deduplication, approximately **120 meaningful tags** remain. Tags are:
- **Clickable pills** on every card and every content page
- **Filter controls** on category pages (multi-select)
- **Browsable pages** at `/tags/[tag]/`

### 6.2 Tag Pages

`/tags/claude` shows:
```
+------------------------------------------------------+
|  TAG: Claude                           42 items      |
+------------------------------------------------------+
|  PROMPTS (18)                                        |
|  [card] [card] [card] [card] [card] ...              |
|                                                      |
|  TOOLS (12)                                          |
|  [card] [card] [card] ...                            |
|                                                      |
|  GUIDES (8)                                          |
|  [card] [card] ...                                   |
|                                                      |
|  RESOURCES (4)                                       |
|  [card] ...                                          |
+------------------------------------------------------+
```

### 6.3 Tag Index Page

`/tags/` shows all tags as a cloud or alphabetical list with counts:
```
Claude (42) - ChatGPT (38) - Workflow (28) - Sales (22) - Marketing (19) ...
```

### 6.4 Tag Visibility Threshold
Only surface tags used by **3+ items** in the browsing UI. Rare tags still exist in metadata for search but don't clutter the tag cloud or filter dropdowns.

---

## 7. SEARCH DESIGN

### 7.1 Search Behavior

- **Scope**: Metadata-first (title, description, tags), with full-content as secondary fallback
- **Location**: Search icon in nav -> opens search overlay OR dedicated `/search/` page
- **Instant results**: As-you-type filtering (client-side, no server needed)
- **Result format**: Shows item name, type badge (Prompt / Tool / Guide / etc.), description snippet, tags

### 7.2 Search Result Card

```
+------------------------------------------------------+
| Cold Email                              [PROMPT]     |
| Write a cold email to [name], [role] at [company].   |
| Sales - Cold Email - Claude                          |
+------------------------------------------------------+
| Apollo.io                               [TOOL]       |
| AI-powered sales intelligence and engagement...      |
| Sales - Outreach - Data                              |
+------------------------------------------------------+
```

### 7.3 Search Keyboard Shortcuts
- Press `/` anywhere to focus search
- `Esc` to close search overlay
- Arrow keys to navigate results
- `Enter` to open selected result

---

## 8. FILTERING SYSTEM

### 8.1 Available Filters Per Category Page

| Filter | Available On | UI Element |
|--------|-------------|------------|
| **Subcategory** | Prompts | Horizontal tabs |
| **Tags** | All category pages | Multi-select dropdown or pill cloud |
| **Content depth** | All | Toggle: "Quick Reference" / "In-Depth" (based on content length) |
| **Has URL** | Tools, Resources, Templates | Toggle: "Has link" |
| **Sort** | All | Dropdown: A-Z, Z-A, Recently Added |

### 8.2 Filter Interaction Model

- Filters are additive (AND logic within a filter type, OR logic between items in a multi-select)
- Active filters show as dismissible pills above the content grid
- URL updates with query params so filtered views are shareable
- "Clear all filters" button appears when any filter is active
- Item count updates live: "Showing 23 of 158 prompts"

---

## 9. PAGE-LEVEL DESIGNS

### 9.1 Homepage (`/`)

The homepage is the **magazine cover** — it sells the library, not lists it.

#### Section Flow:

1. **Hero Section** — Rotating spotlight
   - Large featured item (could be a prompt, guide, or collection)
   - Changes on each visit (random on page load)
   - "Explore" CTA button

2. **Quick Stats Bar**
   - `158 Prompts - 84 Tools - 25 Guides - 353 Total Resources`
   - Animated counter on first load

3. **Browse by Category** — 8 category cards in a responsive grid
   - Each card: Category icon + name + item count + 1-line description
   - Cards link to their category page
   - Visual weight proportional to item count (Prompts card is bigger)

4. **Prompt Spotlight** — Featured prompt of the day
   - Full prompt text visible
   - Copy-to-clipboard button
   - "Shuffle" button for another random prompt
   - Tags shown

5. **Use Case Bundles** — Horizontal scrolling row of collection cards
   - "Cold Outreach Stack (12 items)" -> links to use case page
   - "Build AI Apps (18 items)" -> links to use case page
   - Auto-generated, dynamically counted

6. **Popular Tags** — Cloud of top 20 tags by item count
   - Each tag is clickable -> links to `/tags/[tag]/`

7. **Footer**
   - Back to newsletter link
   - OWGT branding
   - Quick links to all categories

### 9.2 Category Pages (`/prompts/`, `/tools/`, etc.)

#### Common Layout (All Categories):

```
+------------------------------------------------------+
|  Breadcrumbs: OWGT Rewards > Prompts                 |
|                                                      |
|  ## PROMPTS                          158 items       |
|  Copy-paste AI prompts for every situation.          |
|                                                      |
|  [Search prompts...]        [Filter by tag v] [Sort] |
|                                                      |
|  ALL | Strategy | Writing | Sales | Leadership | ... |
|                                                      |
|  Active filters: Claude x  Sales x    [Clear all]    |
|  Showing 12 of 158 prompts                           |
|                                                      |
|  [Card] [Card] [Card] [Card]                         |
|  [Card] [Card] [Card] [Card]                         |
|  [Card] [Card] [Card] [Card]                         |
|                                                      |
|  [Load More]                                         |
+------------------------------------------------------+
```

- Default load: 24 items
- "Load More" adds another 24
- Subcategory tabs only appear on Prompts (other categories don't have subcategories)

#### Card Designs (By Content Type):

**Prompt Card:**
- Title, truncated description, subcategory badge, tags, copy button
- Click anywhere (except copy) -> goes to full prompt page

**Tool Card:**
- Title, truncated description, external link icon if URL present, tags
- "Details" link to individual page

**Guide Card:**
- Reading time estimate (based on word count ~200 wpm)
- Content type icon
- Tags

### 9.3 Individual Content Pages

#### Prompt Page (`/prompts/cold-email/`)

**Information Hierarchy:**
1. Breadcrumb (orientation)
2. Title + description (identity)
3. The prompt text in a distinct container with copy button (**the content — the thing they came for**)
4. Metadata: subcategory + tags (classification)
5. Related items (exploration)
6. Navigation: prev/next + back + bookmark + random (flow)

#### Tool Page (`/tools/apollo-io/`)

**Tool-specific elements:**
- External URL button ("Visit ->") is prominent at top
- "What it does / Workflow it replaces / Best for" structure preserved when available
- Missing content gracefully degraded (many tools are metadata-only)

#### Guide Page (`/guides/the-ai-research-system/`)

**Guide-specific elements:**
- Reading time estimate
- Auto-generated table of contents (from ## headings in content)
- Full content rendered as formatted HTML
- Code blocks within guides have their own copy buttons

#### Learning Page (`/learning/[slug]/`)

Two sub-types need distinct handling:

**Skill-type** (has Content):
- "What it is / Who is hiring / Beginner / Advanced / Tool to start" structure
- Skill level indicators

**Lesson-type** (URL-only):
- Minimal page — title, description, prominent "Start Course ->" button
- Consider: show these inline on category page without individual pages

#### Framework / Cheat Sheet / Template / Resource Page

These follow a simplified version of the Tool page layout:
- Title + description
- URL link (prominent)
- Content body (if exists)
- Tags + Related items + Bookmark

---

## 10. CROSS-LINKING STRATEGY

### 10.1 Related Content Algorithm

Related items are determined by tag overlap:

1. Score each other item by number of shared tags
2. Prioritize items from DIFFERENT categories (cross-type discovery is more valuable)
3. Show top 6 related items, max 2 per category
4. If no tag overlap, fall back to same-category items

### 10.2 Cross-Link Placements

| Location | What's Linked |
|----------|---------------|
| Individual page "Related" section | Top 6 related items by tag overlap |
| Prompt page | Related prompts + related tools + related guides |
| Tool page | Prompts that use this tool + guides mentioning it |
| Guide page | Tools mentioned + related prompts + related guides |
| Tag page | All items with that tag, grouped by type |
| Use case page | All items matching the use case rule |

### 10.3 "You Might Also Like" (Future Enhancement)

Based on bookmarked items' tags — shown only if user has bookmarks. A personalized recommendation layer.

---

## 11. POWER-USER FEATURES

### 11.1 Copy to Clipboard
- Available on: Prompt pages (copy entire prompt text)
- Available on: Any code block in guides/cheat sheets
- Visual feedback: Button text changes to "Copied!" with checkmark for 2s
- Keyboard: `C` when on a prompt page

### 11.2 Bookmarks (Local Storage)
- Heart icon on every card and every content page
- `/bookmarks/` page shows all bookmarked items
- Bookmarks persist in `localStorage` — no account needed
- Export bookmarks as JSON (power-user feature)
- Count badge on nav bookmark icon

### 11.3 Random / Surprise Me
- Shuffle button on homepage (random from entire library)
- Shuffle button on each content page (random from same category)
- Keyboard shortcut: `R` for random

### 11.4 Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `/` | Focus search |
| `Esc` | Close search / modal |
| `R` | Random item |
| `<-` / `->` | Previous / next item (on content pages) |
| `B` | Toggle bookmark |
| `C` | Copy prompt (on prompt pages) |

---

## 12. VISUAL DESIGN DIRECTION (Carnival Theme)

### 12.1 Theme Parameters
- **Paper band**: Light (> 85% L in OKLCH)
- **Display style**: Display-heavy (bold, chunky headings)
- **Accent hue**: Warm (red / orange / amber range)
- **Genre**: Playful — full Carnival energy

### 12.2 Personality Notes
- Headings should feel chunky and confident, NOT precious
- Color palette should be warm and inviting — think county fair poster, not clown costume
- Micro-animations should be playful (slight bounces, card tilts on hover, confetti on copy)
- The "premium" feeling comes from polish and spacing, not from restraint
- Every interaction should have feedback — nothing should feel dead
- Cards should feel tactile — slight shadows, rounded corners, maybe a paper texture

### 12.3 Content Type Visual Identity
Each category gets a distinct color accent and icon:

| Category | Accent Color | Icon |
|----------|-------------|------|
| Prompts | Amber/Gold | Terminal cursor |
| Tools | Blue/Teal | Wrench |
| Guides | Green | Book |
| Resources | Purple | Box |
| Learning | Orange | Graduation cap |
| Frameworks | Red | Scaffold |
| Cheat Sheets | Pink | Lightning |
| Templates | Cyan | Clipboard |

---

## 13. RESPONSIVE DESIGN NOTES

### 13.1 Breakpoints
- **Mobile**: 320-414px (single column, stacked cards)
- **Tablet**: 415-768px (2-column card grid)
- **Desktop**: 769px+ (3-4 column card grid)

### 13.2 Mobile-Specific Behavior
- Nav collapses to hamburger + bottom bar
- Subcategory tabs become horizontally scrollable
- Filter dropdowns become full-screen overlays
- Copy button on prompts becomes full-width sticky footer button
- Card grid becomes single column
- Search is always accessible from bottom bar

---

## 14. PERFORMANCE TARGETS

- **First paint**: < 1s (static HTML, no JS blocking)
- **Search**: Instant (client-side, pre-loaded JSON index)
- **Page transitions**: None (multi-page, traditional navigation)
- **Images**: None initially (text-heavy library — no images to optimize)
- **JS bundle**: < 50KB (search index + filtering + bookmarks + clipboard)

---

## 15. CHALLENGES & MITIGATIONS

> **WARNING**: Things that could go wrong or need careful handling.

1. **158 prompts is a LOT for one page.** Even with subcategories, the initial load of all prompt cards could feel overwhelming. **Mitigation**: Show 24 per page with "Load More" button.

2. **Many items are shallow.** A significant number of Resources, Tools, and Learning items are just a name + 1-line description + URL. Their individual pages will feel empty. **Mitigation**: For URL-only items, consider showing these inline on category pages with expandable cards instead of separate pages, or adding a "quick view" modal.

3. **Tag pollution.** ~200 tags across 353 items means many tags are used only once. The tag cloud will have a long tail of lonely tags. **Mitigation**: Only surface tags used by 3+ items in the browsing UI.

4. **Use case bundles depend on tag quality.** Auto-generating collections only works if tags are clean and consistent. **Mitigation**: Clean tags FIRST before building.

5. **No images anywhere.** A premium visual experience with zero images is hard. **Mitigation**: Carnival theme's boldness carries it. Consider adding category illustrations or abstract patterns to break up text-heavy pages.

---

## 16. BUILD ORDER (Recommended)

1. **Data cleanup** (dedupe, fix artifacts, normalize tags)
2. **Design tokens + base CSS** (Carnival theme tokens, typography, spacing)
3. **Homepage**
4. **Prompts category page + individual prompt page** (largest category, highest priority)
5. **Tools category page + individual tool page**
6. **Guides category page + individual guide page**
7. **Remaining category pages** (Resources, Learning, Frameworks, Cheat Sheets, Templates)
8. **Search**
9. **Tag pages + tag index**
10. **Use case bundle pages**
11. **Bookmarks**
12. **Power-user features** (keyboard shortcuts, random, etc.)
13. **Polish** (animations, micro-interactions, responsive fixes)

---

## 17. OPEN QUESTIONS

> **NOTE**: These are things I have opinions on but want your input before locking in.

1. **Should shallow items (URL-only resources, link-only lessons) get their own full pages?** My recommendation: No. Show them as expandable cards on their category page, and redirect the "visit" action to the external URL. This avoids thin pages.

2. **Prev/Next navigation on individual pages — should it loop (last item -> first item), or stop at the ends?** My recommendation: Loop. It encourages exploration.

3. **Should the homepage Prompt Spotlight change on page load, or on a daily basis?** My recommendation: On every page load (random). More playful, fits Carnival theme. A "shuffle" button is there for explicit randomization.

4. **Do you want a "What's New" or "Recently Added" section?** If you plan to keep adding items, this makes the library feel alive. But it requires a date field on items (not currently in the schema).

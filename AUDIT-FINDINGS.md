# OWGT Rewards — End-to-End Audit, Fix Log & Skill Review Notes

**Date:** 2026-09-20
**Scope:** entire `rewards/` project — `organized-data/`, `scripts/`, `site/`, deployment config
**Constraint honoured:** the five skill passes in Part 2 are *notes only* — no code was changed by them.
Only the bug fixes in Part 1 changed files.

---

## 0. What was actually verified (method & evidence)

Nothing was taken on trust. Every claim below is backed by one of these checks:

| Check | How it was run | Result |
|---|---|---|
| Data parses | `python scripts/sync_site.py` | 391/391 items parsed, **0 warnings** |
| Code fences balanced | per-file fence-count scan over all 391 markdown files | **0 unbalanced** |
| Category correctness | folder name vs `### Category` heading cross-check + `is_shallow` audit | consistent; 150 shallow, 241 deep |
| URL well-formedness | scan for non-`http(s)` `### URL` values | **0 malformed**, 0 missing descriptions |
| Every route returns 200 | raw-socket sweep of 281 paths through `scripts/serve.py` | **281/281 → HTTP 200, 0 failures** |
| Internal links resolve | every `href=` on every `.html` file resolved to a real file | all resolve (only `${…}` template literals flagged, and those are inside JS strings) |
| CSS variables exist | every `var(--x)` used in HTML checked against `tokens.css` | **all defined** |
| JS parses | `node --check site/js/app.js`, `landing.js` | clean |
| UI interactions | real browser session via the preview harness (see §1.5) | exercised & confirmed |

A full route sweep **before** and **after** the fixes returned 200 for all 281 paths, so the
fixes introduced no regressions.

---

## 1. Bug audit results by area

### 1.1 Area 1 — Markdown & data parser

**Verdict: healthy.** `scripts/sync_site.py` is the single source of truth and it is internally
consistent.

* All 8 category folders parse; each excludes its `README.md` correctly (that is why a folder with
  6 files yields 5 cards — intended, not a bug).
* Field extraction is line-anchored (`^### Name`, `^### Description`, …), so `###` headings *inside*
  body content (e.g. `Cheat Sheets/the-code-coding-agent-hacks.md` has `### Context & Configuration`,
  `### Automation & Hooks`) do **not** corrupt parsing. Confirmed by inspection and by the zero-warning run.
* The body regex deliberately stops at the next known top-level heading, which is why the prompt
  bodies render intact.
* Tag case normalisation works (e.g. `prompts` → `Prompts` when a Title-Case tag dominates).
* Duplicate-URL and duplicate-slug detectors are present and printed nothing.

**Data-shape observations (not parser bugs) — noted, not changed:**

| # | Observation | Why it is not a parser bug |
|---|---|---|
| D-1 | **14 entries in `Prompts/` have no prompt body** (e.g. `shift-ai-prompts-database`, `cro-prompts`, `superhuman-claude-prompt-library`) | These files are *link entries*: they carry `### URL` pointing at an external Notion/GitHub library and have no `### Prompt` block. The parser correctly marks them `is_shallow`. They render as "Quick View" link cards, so nothing is broken — but they sit in a category that is otherwise copy-paste prompts, which is a **content/product decision**, not a code fault. See Question Q-1. |
| D-2 | `organized-data/decisions.md` and `skills.txt` are dataset-level files, not items | Correctly excluded from parsing. |
| D-3 | Every item with a body gets a standalone page; the 150 body-less items do not | By design (`is_shallow`). Their `path` values still *look* routable, which caused bug **B-02**. |

### 1.2 Area 2 — Routing & clean URLs

**Verdict: all routes resolve locally. Deployment config has real gaps.**

* 281 paths tested: `/`, `/rewards`, every category page, all 8 short-slug variants, `/tags`,
  `/bookmarks`, `/saved`, `/tag-detail`, all 241 deep item pages, all 10 bundle pages, every unique
  `/items/...` href found in any HTML file, and every asset (`/css/*`, `/js/*`, favicon, logo,
  `data.json`, `search-index.json`, `robots.txt`, `sitemap.xml`).
* `scripts/serve.py` handles clean URLs by appending `.html` when the bare path does not exist —
  verified working for both category and deep pages.
* `saved.html` is a real file that meta-refreshes to `/bookmarks`, so `/saved` works even if the
  Vercel rewrite never fires.

**Config findings:**

| # | Finding | Explanation |
|---|---|---|
| R-1 | **Two different `vercel.json` files** — repo-root (`rewards/vercel.json`) has `cleanUrls` + rewrites for `/`, `/home`, `/saved`; `site/vercel.json` has **only** `cleanUrls`. | Which one applies depends on the Vercel project's Root Directory setting. If the root is `site/`, the rewrites in the repo-root file are **dead config**, `/home` would 404, and `/saved` only works because of the HTML meta-refresh. If the root is `rewards/`, the site would be served under `/site/...`. These cannot both be right. See Question Q-2. |
| R-2 | The `{"source": "/", "destination": "/rewards"}` rewrite appears to be a **no-op** | Vercel checks the filesystem *before* rewrites, and `index.html` exists, so `/` always serves the landing page. Harmless but misleading. |
| R-3 | 6 of the 10 bundle pages are **orphaned** — only `bundle-cold-outreach-stack`, `-content-creation`, `-marketing-stack`, `-no-code-automation` are linked from `rewards.html#bundles`. | `bundle-ai-research`, `bundle-build-ai-apps`, `bundle-prompt-engineering`, `bundle-video-and-motion`, `bundle-career-and-hiring`, `bundle-developer-toolkit` exist, return 200, and are in the sitemap, but nothing in the UI links to them. See Question Q-3. |
| R-4 | `site/items/` contains 7 **empty leftover directories** (`business-ops`, `communication`, `leadership-&-management`, `marketing`, `sales`, `thinking-&-strategy`, `video`) | Remnants of an older category scheme. The sync script's cleanup only deletes stale `.html` *files*, never empty dirs. Harmless (empty dirs are not deployed) but untidy. |

### 1.3 Area 3 — Links & assets

**Verdict: no broken links, no 404 assets.** Minor inconsistencies noted.

* Nav (all 6 items), footer, logo link (`/rewards`), every card link, every tag link
  (`/tag-detail?tag=…`), category eyebrows, prev/next item nav, and bundle links all resolve.
* `favicon.png` and `owgt-rewards-logo.png` both load — and are **byte-identical duplicates**
  (same MD5 `adff3005…`). The "logo" is the favicon file. Functional, but the header logo is not a
  distinct asset. See Question Q-4.
* `site/css/utilities.css` is a **one-line comment** containing no rules, yet `rewards.html` loads it.
  Dead file/request.
* `site/deep-prompt.html`, `site/deep-guide.html`, `site/use-case.html` are **orphan templates** —
  nothing links to them. They also use a *relative* logo link (`href="index.html"`) where every other
  page uses `/rewards`, so their logo goes to the landing page instead of the library.
* `index.html` and `rewards.html` load CSS with **relative** paths (`css/tokens.css`); every other
  page uses absolute (`/css/tokens.css`). Works at the root, but breaks if those pages are ever
  served from a deeper path.
* `site/AGENTS.md` points at `site\repomix-output.xml`, which **does not exist**.
* `patch_app.py` and `patch_search.py` sit in the project root — one-time patch scripts that
  `AGENTS.md` says should be deleted after use.
* Tag-cloud labels on `rewards.html` are lowercase (`#marketing`) while the hrefs and underlying
  tags are Title Case (`?tag=Marketing`). `tag-detail.html` matches case-insensitively, so this is
  cosmetic only.

### 1.4 Area 4 — UI & JavaScript interactions

All of the following were driven in a real browser against `scripts/serve.py` and confirmed:

| Interaction | Result |
|---|---|
| Quick View expand | `is-open` false → true, `aria-expanded="true"`, content shows the **real description** |
| Quick View collapse | second click returns `is-open` to false |
| Full-card click expands | card-level handler delegates to the expand button (buttons/links excluded) |
| Bookmark save | button `♡ Save` → `♥ Saved`, red background, id written to `localStorage.owgt_bookmarks` |
| Bookmark remove | toggle-off clears localStorage entry and restores `♡ Save` |
| Toast | `Saved to Vault` / `Copied to clipboard!` appear; toast is `pointer-events: none` |
| `/` shortcut | opens the search bar (previously threw `ReferenceError`) |
| `B` shortcut | bookmarks the open deep page (`localStorage` contains `cold-email`) |
| `C` shortcut | fires the copy path; without clipboard permission it now shows *"Copy failed — use Ctrl/Cmd+C"* instead of failing silently |
| `R` shortcut | 241 navigable candidates, **0** shallow items can be chosen |
| Search query | `cold email` → 7 results, heading correct, shallow results are non-link cards |
| Search result colours | deep result cards now show correct per-category accents (Prompts / Cheat Sheets / Guides) |
| Scope toggle | global vs local scope buttons switch correctly |
| Local scope on `/cheatsheets` | label "Cheat Sheets"; search returns 2 Cheat Sheets results (previously **0**) |
| Tag filtering | 165 cards → 2 when filtering tag `Cold`; badge `1`; reset → 165 |
| Category filtering | 173 tag-detail cards → 2 when filtering category `Cheat Sheets` (previously **no-op**) |
| Close search | main content restored byte-for-byte; filter drawer count stays **1** (previously accumulated duplicates) |

**One limitation, stated plainly:** the automated browser used for testing blocks clipboard
access by design, so what was actually confirmed for the copy buttons is that the *code path runs*
and the new failure message appears instead of silence. The clipboard *contents* were therefore not
verified end-to-end from the test harness — that requires a real person clicking the button in a
normal browser. Everything else in the table above was directly observed.

### 1.5 Bug register

Severity: **S1** = broken feature/data loss, **S2** = clearly wrong behaviour, **S3** = polish/inconsistency.

| ID | Sev | Bug (plain English) | Root cause | Status |
|---|---|---|---|---|
| **B-01** | S1 | Pressing `/` (or Escape while typing in the search box) threw `ReferenceError: toggleSearch is not defined`. The keyboard search shortcut, advertised in the copy ("Press 'C' to copy • 'B' to save"), simply did not work. | `initShortcuts()` called `toggleSearch()` at two sites, but the function was never defined anywhere in the codebase. | **FIXED** — defined `window.toggleSearch` which opens via the trigger button and closes via the close button, no-op on pages without search UI. `app.js:421` |
| **B-02** | S1 | The `R` (random resource) shortcut could navigate to a 404. 150 of 391 items have no page of their own; picking one sent the browser to a non-existent URL. ~38% chance per press. | `loadRandomResource()` picked uniformly from `search-index.json`, which includes `is_shallow` items whose `path` is not routable. | **FIXED** — filters to `!is_shallow && path` before choosing. `app.js:466-473` |
| **B-03** | S2 | Choosing the local ("Cheat Sheets") search scope on `/cheatsheets` returned **zero results for every query**. | `app.js` mapped `cheatsheets → 'Cheatsheets'` while the real data category is `'Cheat Sheets'`, so the strict equality filter rejected every item. The *filter* system had the correct spelling, which is why only search broke. | **FIXED** — map value corrected to `'Cheat Sheets'`. `app.js:54` |
| **B-04** | S2 | The "Saved" local scope on `/bookmarks` could never match anything; the saved-items code path was dead. | `isBookmarkScope` tested `currentScope === 'bookmarks'`, but the UI label sets `currentScope = 'Saved'`. | **FIXED** — accepts both `'bookmarks'` and `'saved'`. `app.js:169` |
| **B-05** | S2 | The "Tags" local scope on `/tags` returned nothing, because no item's category is literally `Tags`. | The category filter ran before the tag-scope logic could apply; the tag scope was treated as a category. | **FIXED** — category filter is skipped when `isTagScope`. `app.js:181` |
| **B-06** | S2 | Every deep item in **search results** rendered with Prompts-yellow accents regardless of its real category. | `renderResults()` read `item.category_slug`, a field that does not exist in `search-index.json`; the fallback produced `'prompts'` for everything. | **FIXED** — explicit category→token map with a Prompts fallback. `app.js:322-332` |
| **B-07** | S2 | Quick View on a **search result** and the Spotlight "Copy Prompt" button showed/copied *machine-mangled* text: for link-type items, a search blob like `"Directory of upcoming AI hackathons lablab ai-hackathons https lablab ai"`; for real prompts, text with `[brackets]`, `*asterisks*` and backticks stripped out. | `search-index.json`'s `content` field was built for *searching* (symbols stripped, shallow items replaced by a synthetic description+host+URL string), but three UI surfaces treated it as *display/copy* text. `data.json` (used by category, tag and bookmark pages) kept the raw text — hence the inconsistency. | **FIXED** — `sync_site.py` now emits `content` (raw, unchanged) **and** `search_blob` (search-optimised); `app.js` searches `search_blob` and displays/copies `content`. `sync_site.py:610-636`, `app.js:232-233` |
| **B-08** | S2 | The filter drawer's **Category** select did nothing to the visible cards — you could pick "Cheat Sheets", press Apply, see the badge change to `1`, and have every card stay on screen. | `filterPageCards()` only applied `subcategory` and `tags`; it never read `activeFilters.category`. | **FIXED** — category is now applied against the card's category label. `app.js:894` |
| **B-09** | S2 | Opening and closing the search repeatedly appended a **new hidden filter drawer** to `<body>` each time, creating duplicate `id="filterDrawer"` / `id="filterBackdrop"` elements and duplicate click listeners on the filter button. | `closeSearch()` re-ran `initFilterSystem()` after restoring `<main>` — but the drawer lives *outside* `<main>`, so re-initialising was both unnecessary and additive. | **FIXED** — removed the redundant re-init and added a one-shot guard. `app.js:133-137`, `app.js:661-662` |
| **B-10** | S2 | The landing page's `<title>`, meta description and signup copy said **"354"** while the page's own hero said **391** — a visible, contradictory count. | `update_landing_and_rewards_pages()` had regexes for the hero spans and the marquee, but none for the title, meta description, or the signup line, so those three strings stayed frozen. | **FIXED** — three new regexes in the sync script; regenerated (`354` → `391` in all three places). `sync_site.py:459-461` |
| **B-11** | S3 | The Spotlight copy button always read **"Copy Prompt"**, even when it was copying a tool/resource description. | Static label in `rewards.html`, never updated per item. | **FIXED** — label switches between "Copy Prompt" and "Copy Description". `app.js:546-548` |
| **B-12** | S3 | After the first toast, an invisible ~200×40 px element stayed fixed at bottom-centre and could swallow clicks in that spot for the rest of the session. | `showToast()` fades with `opacity: 0` but never removes the node and did not set `pointer-events: none`. | **FIXED** — `pointerEvents: 'none'`. `app.js:521-522` |
| **B-13** | S3 | Copy buttons failed **completely silently** on any non-secure origin (plain HTTP host), and on any clipboard rejection: no toast, no fallback, just an unhandled promise rejection. | `copyToClipboard` had no capability check and no `.catch`. | **FIXED** — capability guard + `.catch` with a user-visible hint. `app.js:484-504` |

#### Discrepancies found and deliberately **not** changed

These are real, but fixing them means either churning generated templates or making a product call.
They are recorded so they are not lost.

| ID | Sev | Discrepancy | Why left alone |
|---|---|---|---|
| **B-14** | S2 | **A `<button>` is nested inside an `<a>`** on every deep card (321 occurrences across category, tag, bookmarks, search and bundle pages) — invalid HTML; interactive content inside a link. | It works today because the handler calls `preventDefault()`/`stopPropagation()`. Fixing it properly means restructuring every card template *and* adding keyboard handling for the replacement element. That is a deliberate refactor, not a bug fix — it should be its own change. |
| **B-15** | S3 | The **"Type" (subcategory) filter is unreachable dead UI**: `subcategory` is `''` for all 391 items, so the select is always hidden. | The field is part of the data schema but never populated. Removing the UI or populating the schema is a product decision. |
| **B-16** | S3 | `filterPageCards()` reads the card's header `.tag` element as if it were a subcategory — but that element actually holds the **category**. Latent mis-wiring. | Harmless today only because subcategory is always empty (B-15). Fixing it is entangled with B-15. |
| **B-17** | S3 | `tag-detail.html` hard-codes `--color-cat-prompts` for **every** card, and shallow search-result cards hard-code `--color-accent-2`. | Cosmetic colour inconsistency; needs a shared colour map in 3–4 templates. |
| **B-18** | S3 | Bookmark button styling is split between a CSS class (`.is-saved`) and **inline styles written by JS** (`style.background = '#ef4444'`), so the class is effectively cosmetic and the two can drift. | Works; consolidating is cleanup, not a fix. |
| **B-19** | S3 | There is **no saved-count badge** in the header, even though `.nav__badge` CSS exists and was clearly intended for one. The only count is the text on `/bookmarks`. | New feature, not a defect. See Question Q-5. |
| **B-20** | S3 | Bookmarks removed from the dataset are **never pruned** from `localStorage`; `renderSavedPage()` silently drops unknown ids (so the visible count and the stored count can differ). | Self-healing on read; pruning is a small enhancement. |
| **B-21** | S3 | `search-index.json` (~308 KB) is fetched independently by **four** features (search, spotlight, filter drawer, random). | Works; a shared cached fetch would be a refactor. |
| **B-22** | S3 | `app.js` still contains dead guards for a legacy URL shape (`lastSeg === 'site'`, `'home.html'`) in three places. | Pre-existing cruft; see the simplification notes in Part 2. |

---

## 2. Skill passes (notes only — **no code changed**)

### 2.1 `/codebase-design`

Vocabulary applied deliberately: **module**, **interface**, **implementation**, **depth**, **seam**,
**adapter**, **leverage**, **locality**.

**Module inventory and depth assessment**

| Module | Interface (what a caller must know) | Depth verdict |
|---|---|---|
| `scripts/sync_site.py` — "dataset → site" | One entry point, `sync_all()`, no arguments; reads `organized-data/`, writes all of `site/`. Callers must know: run it from anywhere, it emits 8 categories plus bundles/sitemap, it deletes stale item pages, it is destructive to generated files. | **Deep.** A large amount of behaviour (parse, normalise tags, generate 241 item pages, 8 category pages, 10 bundle pages, sitemap, robots, cleanup) sits behind a zero-argument interface. This is the best-shaped module in the project. |
| `site/js/app.js` — page behaviour | One global side effect: a `DOMContentLoaded` listener that calls seven `init*` functions. Callers (HTML pages) must know which DOM ids/classes to provide. | **Shallow-to-medium.** Its interface is *implicit DOM contract* — the ids `searchTriggerBtn`, `headerSearchContainer`, `filterDrawer`, `spotlight-copy-btn`, the classes `.card--expandable`, `.bookmark-main-btn`, `.copy-main-btn`, plus four `window.*` globals it publishes (`toggleSearch`, `copyToClipboard`, `resetFilters`, `applyCurrentFilters`) and one it consumes (`initFilterSystem`). Every page must satisfy that contract by hand-copying a header block. |
| `site/js/landing.js` | IIFE, no exports, runs on the landing page only | **Deep and correctly isolated** — self-contained, dependency-free, no globals leaked. |
| `scripts/serve.py` | CLI: `python scripts/serve.py [port]` | **Deep** — one behaviour (clean-URL static serving) behind a tiny interface. A genuine **adapter** at the "how is a URL resolved to a file" **seam**; a second adapter (Vercel) already exists, which per the skill's rule means this is a *real* seam, not a hypothetical one. |
| `site/data.json` / `search-index.json` | Two JSON blobs with overlapping but **non-identical** schemas | **Leaky seam.** B-07 was caused precisely by one blob being used for two different purposes. See the deepening opportunity below. |

**Deepening opportunities (design-level, not yet actioned)**

1. **The generated header block is the project's biggest locality problem.** The same ~50 lines of
   header + search markup are duplicated into 15+ hand-written templates *and* into the Python string
   templates in `sync_site.py`. The `init*` functions' real interface is "this DOM must exist" —
   undocumented and unenforced. Deepening direction: give the sync script a single
   `render_header(active_category)` helper and have every page (including the hand-written ones)
   receive its header from the generator. **Leverage:** one change to nav/header/search markup
   updates all 260+ pages. **Locality:** the id/class contract lives next to the code that consumes it.
2. **Collapse the two data files behind one interface.** `data.json` (display-fidelity) and
   `search-index.json` (search-fidelity) exist only because search wants transformed text. B-07 shows
   the cost. Deepening direction: one emitted dataset with explicit fields (`content`, `search_blob`,
   `category_slug`) — which is *exactly* the shape the B-07 fix moved toward — and have every feature
   read the one file. **Deletion test:** delete `search-index.json` and complexity does *not* vanish
   (four features read it), which is the signal that it is earning its keep — but its *interface*
   should be one schema, not two. 
3. **`is_shallow` is a state with consequences spread across four call sites** (page generation,
   card rendering, random navigation, spotlight). That is a candidate state machine rather than a
   boolean — see the DSA pass (§2.4).

### 2.2 `/code-simplification`

Applied the Five Principles: preserve behaviour, follow project conventions, prefer clarity,
maintain balance, scope to what changed. Chesterton's Fence applied per item.

**Performed during this audit (behaviour-preserving):**

* Removed a *duplicate* `search-index.json` write I had briefly introduced mid-audit — it changed
  nothing (page rendering does not mutate item content) and was pure redundancy. Net effect: the
  sync script diff is now 3 regex lines, not a restructured pipeline.
* Replaced the ad-hoc `item.category_slug || item.category.toLowerCase()` expression with an
  explicit lookup table, which is clearer than a string-munging fallback and also fixes B-06.
* Replaced the stringly-typed `currentScope === 'bookmarks'` comparison with an explicit
  `['bookmarks','saved'].includes(...)`, which documents that the label and the internal name differ.

**Catalogued but NOT actioned (scoped out deliberately — these are cleanup, not fixes):**

| # | Opportunity | Signal |
|---|---|---|
| C-1 | **Duplicated `escapeHTML`** — the same 5-line escaper is re-declared in `app.js` *and* inline in `bookmarks.html`, `tag-detail.html`, and again inside `renderResults()`. | Duplicated code: extract one shared helper on `window`. |
| C-2 | **Duplicated `catColorMap`/`catMap`** — the category→token map now exists in three places (`app.js` search results, `app.js` filter, `bookmarks.html`) and the slug map in two. They have already drifted once (B-03 — `'Cheatsheets'` vs `'Cheat Sheets'`). | Divergent change waiting to happen; single source of truth needed. |
| C-3 | **Duplicated card templates** — a deep card and a shallow card are re-implemented in four places (Python generator, `app.js` search results, `bookmarks.html`, `tag-detail.html`). | Divergent change; every card tweak is a 4-file edit. |
| C-4 | **Duplicated "is this the home page?" logic** — the same `isHome`/`isHomePage` expression appears in three places in `app.js`, each with a slightly different token list. | Repeated conditionals: extract one `isHomePage()` predicate. |
| C-5 | **Dead legacy tokens** — `'site'`, `'home.html'`, `'rewards.html'`, `'index.html'` in those same guards are unreachable for the current routing. | Dead code (B-22). |
| C-6 | `switch` cases in `initShortcuts()` declare `const` without braces (`case 'b': const bBtn = …`). Legal but fragile. | Style/robustness. |
| C-7 | `scripts/verify_routing.py` asserts a **stale** contract: it expects `/home`, `/index`, `/act-as-a-skeptical-senior` and `/bundle-cold-outreach-stack` to return 200. The first two work by accident (rewrite/meta-refresh), the last two **404** by design (there is no flat `/bundle-*` route). | A test that encodes behaviour the site does not have is worse than no test — see Q-6. |
| C-8 | `site/css/utilities.css` is empty of rules but is still requested. | Dead file/inline the removal. |

Simplifications deliberately **rejected**: collapsing the two JSON files into one (larger blast
radius than the bug warranted) and converting the nested-save-button cards (a restructure, not a
simplification — see B-14).

### 2.3 `/code-review`

The skill defines a two-axis review (Standards vs Spec) of a diff against a fixed point, and
explicitly requires a **fixed point** plus a **spec**. Neither was supplied, and the repo has no
`docs/agents/issue-tracker.md`, no `CODING_STANDARDS.md`, and no `CONTRIBUTING.md`. Rather than
invent them, the review was adapted and the adaptation is recorded here.

* **Fixed point used:** `HEAD` (commit `d345b01`) — the audit reviewed the working tree against the
  last commit, i.e. exactly the changes listed in §1.5.
* **Standards source used:** this repo's only documented standard is `AGENTS.md`. Its binding rules:
  plain HTML/CSS/JS; prefer manual work over scripts; if a script is used it must live in `scripts/`,
  be written *after* reading the files it touches, never be trusted blindly, and **one-time scripts
  must be deleted after use**; always inspect script output.
  Plus the skill's **smell baseline** (Fowler ch.3), applied as judgement calls only.
* **Spec source used:** none exists, so the **Spec axis is reported as "no spec available"** — as the
  skill instructs. Substituting the audit checklist would have been fabrication.
* **Tooling-enforced items skipped:** JS/HTML syntax and file encoding (verified by `node --check`
  and the render sweep rather than reported as findings).

**Standards axis**

| Verdict | Finding |
|---|---|
| ✅ Compliant | All four changed files obey `AGENTS.md`: plain JS, no dependencies, no build step; the sync script lives in `scripts/`; no *new* one-time script was left behind (the two scratch files created during the audit — a link-checker and a path list — were both deleted). |
| ⚠️ Pre-existing violation, not mine | `patch_app.py` and `patch_search.py` at the project root violate "ANYTIME YOU CREATE ONE-TIME SCRIPT, DELETE AFTER USE". Flagged, not deleted (they are not my files and may be the user's working notes). |
| ⚠️ Judgement call — **Duplicated Code** | C-1/C-2/C-3 in §2.2. The `escapeHTML` and category-map duplication is the strongest instance: it has *already* caused a real bug (B-03). |
| ⚠️ Judgement call — **Divergent Change** | `app.js` is edited for search, bookmarks, filtering, spotlight, toasts, keyboard and navigation — seven unrelated reasons in one 900-line file. |
| ⚠️ Judgement call — **Speculative Generality** | The unreachable subcategory/"Type" filter (B-15/B-16): schema field, UI group, change listener and a comparison all exist for data that never populates it. |
| ⚠️ Judgement call — **Primitive Obsession** | `is_shallow` as a bare boolean on every record drives four different behaviours; `currentScope` as a free-form string that sometimes holds a category, sometimes one of `'global'`/`'Tags'`/`'Saved'` (and once mismatched a category name — B-03/B-04). |
| ➖ Not applicable | Feature Envy, Message Chains, Middle Man, Refused Bequest, Shotgun Surgery — no class hierarchies or object graphs in this codebase, and the four-file card-template spread is better described as Divergent Change. |

**Spec axis:** **no spec available** (no issue reference, no spec file under `docs/`, `specs/`, or
`.scratch/`, and no PR-linked commit messages). Per the skill, the Spec sub-agent step was skipped
rather than fabricated. If a feature spec exists for the Rewards library, re-run this axis against it.

**Summary line:** Standards — 1 compliance note, 1 pre-existing process violation, 5 judgement-call
smells (worst: duplicated category maps, which already caused B-03). Spec — not assessable: no spec
was supplied or found.

### 2.4 `/dsa-codebase-audit`

Read-only, coverage-contract based. This is an 8-source-file project, so the "small codebase
shortcut" applies: the whole repository was treated as one subsystem set and reviewed directly.

**Subsystem inventory (coverage contract)**

| ID | Subsystem | Boundary | Key files | Status |
|---|---|---|---|---|
| S1 | Dataset ingestion & normalisation | `organized-data/` → in-memory items | `scripts/sync_site.py` (`parse_markdown_item`, `sync_all`) | recommend |
| S2 | Site generation (pages, indices, sitemap) | items → `site/**/*.html`, `site/*.json`, `sitemap.xml` | `scripts/sync_site.py` (renderers), `site/bundle_mapping.json` | recommend |
| S3 | Client behaviour | `site/js/app.js` | one module, seven `init*` functions | recommend |
| S4 | Landing page behaviour | `site/js/landing.js` | isolated IIFE | skip |
| S5 | Local serving adapter | `scripts/serve.py` | clean-URL translation | skip |
| S6 | Deployment config | `vercel.json` ×2, `robots.txt`, `sitemap.xml` | — | recommend |
| S7 | Static presentation | `site/css/*`, hand-written HTML templates | — | skip |
| S8 | One-off maintenance utilities | `scripts/verify_routing.py`, `patch_*.py`, `crop_logo.py`, `clean_*.py`, `extract_*.py` | — | skip |

**Ranked recommendations** (evidence, model, scope, risk, validation, confidence)

| Priority | Subsystem | Recommendation | Evidence | Complexity / risk | Confidence |
|---|---|---|---|---|---|
| **P1** | S3 | **Replace the scattered `is_shallow` boolean + duplicated category maps with one record-shape helper.** Each item would carry an explicit `kind` (`'page'` vs `'link'`) and one `categorySlug`, and every consumer would ask the helper instead of re-deriving. | `app.js:181` (category compare), `app.js:322` (colour map), `app.js:466` (random filter), `bookmarks.html` (own map), `tag-detail.html` (hard-coded colour) — five independent re-derivations of the same two facts. B-03 and B-06 both came from this. | High leverage, low functional risk; touches 5 files. | **High** |
| **P2** | S3 | **Model the search scope as a discriminated value instead of a free-form string.** Today `currentScope` holds `'global'`, or a category name, or `'Tags'`, or `'Saved'`, and consumers re-test it with string comparisons that have already mismatched twice. A shape like `{mode:'global'|'category'|'tag'|'bookmarks', category?}` removes the class of bug entirely. | `app.js:38` (`currentScope='global'`), `:52-56` (label map), `:167-169` (scope tests), `:181-182` (filter branches) | Medium effort, contained to `initSearchSystem`. | **High** |
| **P3** | S2 | **Make the "is this item routable?" decision a single generator-side computed field.** `is_shallow` currently means "no body", but routing needs "has a generated page". Emitting an explicit `has_page` (and, ideally, only emitting routable `path` values) would make B-02's class of bug structurally impossible rather than fixed by a filter. | `sync_site.py` `parse_markdown_item` sets `path` for every item; `generate_deep_item_html` only writes deep ones; `loadRandomResource` had to compensate | Low effort, high safety value. | **High** |
| **P4** | S6 | **Resolve the two-config deployment ambiguity into one source of truth**, then delete the dead rewrite. | `rewards/vercel.json` vs `site/vercel.json`; `/` rewrite is unreachable because `index.html` wins filesystem precedence | Config-only, but must be confirmed against the live project settings (Q-2). | **Medium** |
| **P5** | S8 | **Delete or repair `scripts/verify_routing.py`.** It asserts four routes that do not exist and would report a healthy site as broken — the inverse of a useful test. | `scripts/verify_routing.py:9-24` (`/home`, `/index`, `/act-as-a-skeptical-senior`, `/bundle-cold-outreach-stack`) | Trivial effort. | **High** |
| **P6** | S1 | **Consider a separate `Links`/`Libraries` bucket for the 14 body-less `Prompts/` entries** (D-1) so a copy-paste prompt library does not present link cards as prompts. | `organized-data/Prompts/shift-ai-prompts-database.md` etc. | Product decision, not code. | **Low** (needs owner input) |

**Skips (with rationale)**

* **S4 `landing.js`** — self-contained, no globals, no shared state; nothing to simplify.
* **S5 `serve.py`** — 30 lines, one behaviour; already the correct deployment **adapter**. Adding
  abstraction here would be speculative.
* **S7 CSS/HTML** — presentation-only; the only structural issue (duplicated templates) is already
  captured as C-3 under S2/S3 rather than duplicated here.
* **S8 other utilities** (`clean_data.py`, `extract_*.py`, `crop_logo.py`, `convert_pdf.py`) —
  historical PDF→markdown pipeline, not on the live request path.

**Audit completeness check:** every subsystem has either a recommendation or an explicit skip; no
recommendation is duplicated across subsystems; no recommendation is style-only or a
line-count exercise; the repository was left unchanged by this pass (read-only).

### 2.5 `/improve-codebase-architecture`

The skill produces a visual HTML report in the OS temp directory (deliberately *not* in the repo) and
then asks which candidate to explore. Its candidates, surfaced from the friction found above:

| Candidate | Files | Problem | Solution | Strength |
|---|---|---|---|---|
| **A. One header, generated once** | `sync_site.py`, all 15+ hand-written templates, `app.js` | The header/search block is copy-pasted into every page; `app.js` therefore depends on an undocumented DOM contract (ids/classes) that nothing enforces. Understanding one concept (search) requires bouncing between 15 templates and 900 lines of JS. | Generator emits the header for every page (including hand-written ones) from one `render_header(active)` function. **Locality:** one place defines the markup and the ids it promises. **Leverage:** one edit updates every page. Tests become possible: render the header, assert the ids `app.js` needs are present. | **Strong** |
| **B. One dataset behind one interface** | `sync_site.py`, `data.json`, `search-index.json`, `app.js`, `bookmarks.html`, `tag-detail.html` | Two JSON files with *different fidelity per field*, and features pick whichever they happened to reach for. B-07 is the direct consequence: the same field name meant "display text" in one file and "search blob" in the other. | Emit one dataset whose fields declare their purpose (`content`, `search_blob`, `category_slug`), consumed by every feature. The B-07 fix is a partial move in exactly this direction. **Deletion test:** deleting the second file does *not* remove complexity (four readers exist) — but merging the *schemas* does, because the "which file has good text?" question disappears. | **Strong** |
| **C. Card rendering as one module** | `sync_site.py` (`render_category_card`), `app.js` (`renderResults`), `bookmarks.html`, `tag-detail.html` | Four independent implementations of the same two card shapes. Every card change is a four-file edit, and they have already drifted (B-17). | A single card-rendering seam (generator-side for static pages, one JS helper for dynamic ones) with an item in, markup out. **Locality:** the card shape lives in one place. **Testability:** feed it a deep item and a shallow item, assert the right shape; no DOM required. | **Worth exploring** |
| **D. Search scope as a value, not a string** | `app.js` `initSearchSystem` | `currentScope` is a free-form string meaning four different things, re-tested at four sites with string equality — the source of B-03, B-04 and B-05. | A discriminated value (`{mode, category?}`) produced once and consumed by one filter function. | **Worth exploring** |
| **E. Delete the dead subcategory dimension** | `sync_site.py` schema, `app.js` filter drawer, `filterPageCards` | A schema field, a UI group, a change listener, a comparison and a badge increment all exist for a value that is always empty. | Remove the dimension (YAGNI) or populate it deliberately. **Deletion test:** deleting it makes complexity vanish — the classic pass-through signal. | **Speculative** (product call) |

**Visual report written to the OS temp directory (deliberately outside the repo):**
`C:\Users\BAFNA_~2\AppData\Local\Temp\architecture-review-20260920-002531.html`
(self-contained; Tailwind + Mermaid via CDN; before/after diagrams for all five candidates).
The generator script used to emit it was a one-time scratch file and was deleted immediately, per
`AGENTS.md`.

**Top recommendation: Candidate A.** It is the only candidate that removes an *interface* from the
`app.js` module (the implicit DOM contract), and it converts a 15-file change into a 1-file change —
the clearest locality win available. Candidate B is a close second and is already half-done as a side
effect of the B-07 fix.

Per the skill, this pass stops here and asks which candidate to explore — see Question Q-7. No
interfaces were proposed and no ADRs were written.

---

## 3. Fixes applied (complete change set)

| File | Change |
|---|---|
| `site/js/app.js` | **B-01** defined `window.toggleSearch`; **B-02** random picks deep items only; **B-03** category map spelling; **B-04/B-05** scope tests accept `saved` and skip the category filter for tag scope; **B-06** explicit category→colour table; **B-07** search uses `search_blob`, display uses `content`; **B-08** category filter actually applied; **B-09** removed redundant filter re-init + one-shot guard; **B-11** dynamic spotlight copy label; **B-12** toast `pointer-events: none`; **B-13** clipboard capability guard + `.catch` |
| `scripts/sync_site.py` | **B-07** emits `content` (raw) alongside `search_blob` (search text); **B-10** three new regexes keep the landing page's title, meta description and signup copy in sync with the real item count |
| `site/index.html` | **B-10** regenerated: `354` → `391` in title, meta description and signup line |
| `site/search-index.json` | Regenerated with the new `content` + `search_blob` schema |

**Verification after the fixes:** `node --check` clean; `sync_site.py` runs with zero warnings;
full 281-path route sweep → **0 failures**; all interactions in §1.4 re-confirmed in a real browser;
no regression in the close-search restore path.

**Scratch artefacts:** two temporary audit files were created and **deleted** (per `AGENTS.md`).
The only untracked path remaining is the pre-existing `.freebuff/`.

---

## 4. Open questions

| # | Question | Why it matters |
|---|---|---|
| **Q-1** | Should the 14 body-less entries in `organized-data/Prompts/` (external prompt *libraries*: Shift AI database, CRO prompts, Superhuman libraries…) stay in `Prompts`, or move to a link-oriented category such as `Resources`? | Verified fact: 165 of the 179 entries under `Prompts` are prompts; the 14 link entries render as Quick View link cards, which is a different interaction from the copy-paste cards around them. This is a content-modelling call, not a code fix. |
| **Q-2** | Which Vercel config is actually live — repo-root `rewards/vercel.json` or `site/vercel.json`? And is the project Root Directory set to `site`? | The two files disagree. If the root is `site/`, the `/`, `/home` and `/saved` rewrites in the other file never run, and `/saved` only works because `saved.html` self-redirects. Worth resolving so the deploy config is honest. |
| **Q-3** | Should the 6 unlinked bundle pages be surfaced (e.g. a "All bundles" section on `rewards.html`), or deliberately left out of the UI? | They return 200 and are in the sitemap, so search engines will index pages no human can navigate to from the site. Either link them or de-list them. |
| **Q-4** | Is `owgt-rewards-logo.png` meant to be a distinct logo, or is the favicon knowingly reused as the header mark? | Verified fact: the two files are byte-identical (MD5 `adff3005…`). If a real logo exists, it needs adding; if not, the duplicate file and the `?v=3` cache-buster can go. |
| **Q-5** | The header has no saved-items count badge even though `.nav__badge` CSS exists. Was a badge intended? | The audit checklist asked about "count updates"; the only count today is the text on `/bookmarks`. If a badge was intended, that is unimplemented work (B-19). |
| **Q-6** | Should `scripts/verify_routing.py` be repaired or deleted? | It currently asserts four routes that do not exist (`/home`, `/index`, `/act-as-a-skeptical-senior`, `/bundle-cold-outreach-stack`). Run as-is against a healthy site, it reports failure — worse than no test. |
| **Q-7** | Which architecture candidate should be explored first — **A** (generated header, strongest), **B** (one dataset/one schema), **C** (single card module), **D** (scope as a value), or **E** (delete the dead subcategory dimension)? | The `/improve-codebase-architecture` skill stops at this question by design; the grilling loop starts once you pick. The visual report is at `%TEMP%\architecture-review-20260920-002531.html`. |
| **Q-8** | Are `patch_app.py` and `patch_search.py` (project root, one-time patch scripts) safe to delete? | `AGENTS.md` requires deleting one-time scripts after use; they were left untouched because they are not files this audit created. |

---

## 5. Bottom line

* **Data layer:** healthy — 391/391 files parse cleanly, no malformed URLs, no unbalanced fences, no
  missing descriptions.
* **Routing:** healthy — 281/281 routes return 200 locally; the *deployment* config is ambiguous
  (Q-2) and carries dead rewrites.
* **Links/assets:** no 404s anywhere; a handful of dead/duplicate files and two orphan templates.
* **Interactivity:** **13 real defects found and fixed**, five of them user-visible feature breakage
  (the `/` shortcut, the `R` shortcut's 404s, Cheat Sheets local search, the category filter, and
  Spotlight/Quick-View showing mangled text).
* **9 further discrepancies** are documented but intentionally left for a scoped follow-up, with
  reasons.
* **8 open questions** for the owner, chiefly around deployment config, bundle discoverability and
  the duplicated logo asset.

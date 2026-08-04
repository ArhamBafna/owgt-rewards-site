# OWGT Rewards

<p align="center">
  <img src="owgt-rewards-logo.png" alt="OWGT Rewards" width="140">
</p>

> A free, curated library of AI prompts, tools, guides, and resources — the subscriber reward that ships alongside the OWGT newsletter.

## What is this?

OWGT Rewards is the perks program for the OWGT newsletter. The newsletter is a sharp, no-hype weekly roundup of AI news for non-technical founders, operators, and solopreneurs. The Rewards library is the "so what" — 350+ copy-paste-ready AI resources that help readers actually *use* the AI they read about.

The site is a static, searchable library: browse by category, search everything, save bookmarks, and copy prompts in one click.

## What's inside

| Category | Items | What's in it |
|---|---|---|
| **Prompts** | ~148 | Copy-paste prompts for sales, writing, research, leadership, marketing, ops |
| **Tools** | ~82 | Curated AI tools for automation, coding, content, and productivity |
| **Learning** | ~54 | AI skills and lessons for getting from beginner to building |
| **Resources** | ~56 | Knowledge bases, frameworks, and references |
| **Guides** | ~25 | Step-by-step tutorials (e.g. build a cold-email generator, $10k/mo app) |
| **Frameworks, Cheat Sheets, Templates** | small | Decision systems, quick references, and Google Sheets templates |

> **Curated, not dumped.** Every item is hand-filtered, deduplicated, and reorganized for humans. Quality over quantity — nothing is there just to pad a number.

## Who it's for

Time-poor, hype-allergic professionals who want AI to do real work — outreach, content, research, automation. Not "the future is coming" readers; the "show me what works today" readers.

## Brand

- **Voice**: sharp, honest, plainspoken. No hype, no corporate jargon, no "revolutionary." Recommends the downside in the same breath as the upside.
- **Design**: "Hallmark Carnival" — bold, playful, premium. Warm accent palette, chunky display headings, tactile cards, playful micro-interactions (bounces, confetti on copy).

---

## Landing page brief (project-specific answers only)

### Hero — above the fold

**Headline** (pick one):
- "350+ ready-to-use AI prompts, tools, and guides. No fluff."

**Subheadline**:
"A curated library of copy-paste prompts, tools, and guides from real people. Free when you subscribe to an AI newsletter for founders and operators."

**Primary CTA text**:
- "Get the library free →"
- "Subscribe free, unlock all 350+ resources →"

**Social proof bar**:
"350+ resources • 8 categories • Read by [X] founders/operators"

### Problem section (empathy)

"You're busy. AI hype is exhausting. You don't need another 'top 100 tools' list — you need the 3 that actually work for *your* job."

### Solution / What you get (3 pillars)

1. **Copy-paste prompts that ship** — 148 prompts for cold email, content, research, leadership, sales. One click to copy.
2. **Tools that aren't vaporware** — 82 curated tools with descriptions, pricing (when known), and direct links.
3. **Guides that teach, not sell** — 25 step-by-step tutorials (build a cold-email generator, a $10k/mo app, an AI research system).

### Category cards (with live counts)

- Prompts (148)
- Tools (82)
- Learning (54)
- Resources (56)
- Guides (25)
- Frameworks
- Cheat Sheets
- Templates

(Shouldnt link to actual rewards when clicked. Should not be clickable)

### Spotlight (featured item)
Pick one of the best resources and spotlight it as an example (sneak peek).

### Use-case bundles (the library as workflows)

- **Cold Outreach Stack** — prompts + tools + guides for lead gen
- **Content Creation** — prompts + tools + guides for social/blog
- **Marketing Stack** — SOPs, prompt chains, tools to run your agency
- **No-Code Automation** — Zapier, Make, workflow builders
- **AI Research** — prompts + guides + tools for research workflows
- **Prompt Engineering** — cheat sheets + guides + skills
- **Video & Motion** — prompts + tools + guides for video
- **Career & Hiring** — prompts + guides + tools for hiring

(Shouldnt link to actual rewards when clicked. Should not be clickable)

### How it works (3 steps)

1. Enter email, subscribe to newsletter
2. Get instant access to the library
3. Search, copy, paste — ship work

### FAQ (objection handling)

- **Is it really free?** Yes. The library is a subscriber reward. The newsletter is free. No upsell.
- **What does the newsletter cover?** AI news worth your time — breakthroughs, model releases, things that change how you work. Not funding rounds, not rumors.
- **How often is the library updated?** New prompts, tools, and guides added regularly from the newsletter research.
- **Can I see the library before subscribing?** The category pages are public. Individual items are accessible. The full search/bookmarks experience is for subscribers.
- **What if I hate it?** Unsubscribe in one click. No hard feelings.

### Final CTA

"Get the library free →" or "Join [X] founders and operators using AI that works."

### Copywriting guardrails
- Short sentences. Address the reader as "you."
- Page should feel like the newsletter: honest, concrete, useful — not a sales page.

### Form - I will give later, just make space for now.

---

## Tech stack & structure

- **Plain HTML/CSS/JS** — no framework or build tooling beyond the generator.
- **Data flow**: `data/` (raw) → `organized-data/` (markdown library) → `build.py` → `data.json`, `search-index.json`, and static category/item HTML pages.
- **Existing pages**: category pages (`prompts.html`, `tools.html`, `resources.html`, etc.), item pages under `items/`, `rewards.html` (the library homepage), `tags.html`, `saved.html`, `bookmarks` via `js/app.js`.
- **Styling**: `css/tokens.css` (design tokens) + `css/base.css`. Shared layout partials in `_templates/`.
- **Assets**: `owgt-rewards-logo.png` (header logo), `favicon.png`.

## Run & deploy

```powershell
# Regenerate static pages from organized-data/
python build.py

# Local dev (clean URLs)
python serve.py    # http://localhost:8000
```

Deploys as static site.
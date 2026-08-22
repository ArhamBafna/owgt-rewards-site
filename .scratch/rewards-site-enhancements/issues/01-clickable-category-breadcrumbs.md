# 01: Clickable Category Breadcrumbs on Item Pages

**What to build:**
On every deep item standalone page, make the category eyebrow in the header a clickable link (e.g. `◆ LEARNING` links to `/learning`). Clicking it takes the user back to the category overview grid.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Category eyebrow in deep item header renders as `<a href="/{category_slug}">` with proper accent color styling
- [ ] Clicking the breadcrumb navigates to the matching category overview page
- [ ] Standalone HTML generation in `scripts/sync_site.py` generates the breadcrumb link for all deep item pages

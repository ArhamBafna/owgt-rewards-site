# 03: Automated Sitemap Generation via Online Tool

**What to build:**
Generate and maintain an up-to-date `sitemap.xml` in `rewards/site/` containing all live category pages, tag directory, and deep/shallow reward resource URLs using an online tool/crawler or automated API rather than building manually.

**Blocked by:** 01: Clickable Category Breadcrumbs on Item Pages, 02: Search Index Domain Keywords for Shallow Items

**Status:** ready-for-agent

- [ ] Online tool or automated crawler/API fetches the site structure and outputs standard XML sitemap
- [ ] Valid `sitemap.xml` placed in `rewards/site/sitemap.xml` with `<loc>`, `<lastmod>`, and `<priority>` elements
- [ ] `robots.txt` in `rewards/site/` references `https://rewards.owgt.com/sitemap.xml`

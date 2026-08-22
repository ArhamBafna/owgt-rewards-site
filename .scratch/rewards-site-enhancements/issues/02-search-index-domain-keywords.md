# 02: Search Index Domain Keywords for Shallow Items

**What to build:**
Enrich the search index payload in `search-index.json` for shallow redirect items by extracting domain and platform keywords from their URLs. When a user searches for "nvidia", "github", "linkedin", or other hostnames in the search bar, matching shallow courses, tools, and repositories appear in the search results.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] URL hostname and path keywords are extracted and appended to the indexed search body for shallow items
- [ ] Searching platform names (e.g. "nvidia", "github", "linkedin", "classcentral") in the search modal displays relevant shallow items
- [ ] `sync_site.py` builds the enriched `search-index.json` without slowing down sync execution

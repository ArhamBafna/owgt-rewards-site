/**
 * OWGT Rewards - Core Application Logic
 * Phase 6: Search, Bundles, Bookmarks & Utilities
 */

document.addEventListener('DOMContentLoaded', () => {
  initSearchSystem();
  initBookmarks();
  initShortcuts();
  initCopyEngine();
  initSpotlight();
  initExpandableCards();
  highlightActiveNav();
  if (typeof initFilterSystem === 'function') initFilterSystem();
});

/* ==========================================================================
   SEARCH SYSTEM
   ========================================================================== */
function initSearchSystem() {
  const triggerBtn = document.getElementById('searchTriggerBtn');
  const searchContainer = document.getElementById('headerSearchContainer');
  const scopeSelect = document.getElementById('searchScopeSelect');
  const inputWrapper = document.getElementById('searchInputWrapper');
  const scopeBtns = document.querySelectorAll('.scope-btn');
  const activeScopePill = document.getElementById('activeScopePill');
  const searchInput = document.getElementById('headerSearchInput');
  const executeBtn = document.getElementById('executeSearchBtn');
  const closeBtn = document.getElementById('closeSearchBtn');
  
  if (!triggerBtn || !searchContainer) return;

  let searchData = [];
  let currentScope = 'global'; // 'global' or category name
  let originalMainContent = null;
  const mainContentArea = document.querySelector('main');
  
  // Set Local Scope Button Text based on path
  const pathParts = window.location.pathname.split('/').filter(Boolean);
  let catSlug = pathParts.length > 0 ? pathParts[0] : '';
  if (catSlug === 'items' && pathParts.length > 1) {
    catSlug = pathParts[1];
  }
  const localScopeBtn = document.getElementById('localScopeBtn');
  let pageCategory = '';
  const catMap = {
    'prompts': 'Prompts',
    'tools': 'Tools',
    'guides': 'Guides',
    'resources': 'Resources',
    'tags': 'Tags',
    'bookmarks': 'Saved',
    'learning': 'Learning',
    'cheatsheets': 'Cheatsheets',
    'templates': 'Templates',
    'frameworks': 'Frameworks'
  };
  if (catMap[catSlug]) {
    pageCategory = catMap[catSlug];
    if(localScopeBtn) {
      localScopeBtn.textContent = pageCategory;
      localScopeBtn.style.display = 'inline-block';
    }
  } else {
    if(localScopeBtn) localScopeBtn.style.display = 'none';
  }

  fetch('/search-index.json')
    .then(res => res.json())
    .then(data => { searchData = data; })
    .catch(err => console.error('Could not load search index', err));

  const globalHeader = document.getElementById('globalHeader');

  triggerBtn.addEventListener('click', () => {
    const isCategoryPage = !!pageCategory;
    if (globalHeader) globalHeader.classList.add('search-active');
    if (!isCategoryPage) {
      // Direct open Global "All Rewards" search on homepage/global pages
      currentScope = 'global';
      activeScopePill.textContent = 'All Rewards';
      searchContainer.style.display = 'flex';
      scopeSelect.style.display = 'none';
      triggerBtn.style.display = 'none';
      inputWrapper.style.display = 'flex';
      searchInput.focus();
    } else {
      // Show scope options on category pages (e.g. Prompts, Tools, Guides, etc.)
      searchContainer.style.display = 'flex';
      scopeSelect.style.display = 'flex';
      inputWrapper.style.display = 'none';
    }
  });

  scopeBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const scopeType = e.target.getAttribute('data-scope');
      currentScope = scopeType === 'global' ? 'global' : pageCategory;
      activeScopePill.textContent = scopeType === 'global' ? 'All Rewards' : currentScope;
      
      // Hide scope selector, hide trigger button to avoid overlap
      scopeSelect.style.display = 'none';
      triggerBtn.style.display = 'none';
      
      // Show input wrapper and activate search-active class on header to fade out nav
      inputWrapper.style.display = 'flex';
      if (globalHeader) globalHeader.classList.add('search-active');
      
      searchInput.focus();
    });
  });

  const closeSearch = () => {
    if (globalHeader) globalHeader.classList.remove('search-active');
    triggerBtn.style.display = 'flex';
    searchContainer.style.display = 'none';
    inputWrapper.style.display = 'none';
    scopeSelect.style.display = 'none';
    searchInput.value = '';
    const cleanPath = window.location.pathname.toLowerCase().replace(/\/+$/, '');
    const parts = cleanPath.split('/').filter(Boolean);
    const lastSeg = parts.length > 0 ? parts[parts.length - 1] : '';
    const isHome = parts.length === 0 || lastSeg === 'home' || lastSeg === 'rewards' || lastSeg === 'rewards.html' || lastSeg === 'home.html' || lastSeg === 'index.html' || lastSeg === 'site';
    if (isHome) {
      const openFilterBtn = document.getElementById('openFilterDrawerBtn');
      if (openFilterBtn) openFilterBtn.style.display = 'none';
      if (typeof window.resetFilters === 'function') window.resetFilters();
    }
    if (originalMainContent && mainContentArea) {
      mainContentArea.innerHTML = originalMainContent;
      originalMainContent = null;
    }
  };

  closeBtn.addEventListener('click', closeSearch);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && searchContainer.style.display !== 'none') {
      closeSearch();
    }
  });

  const executeSearch = () => {
    const query = searchInput.value.toLowerCase().trim();
    if (!query) {
      closeSearch();
      return;
    }

    const cleanPath = window.location.pathname.toLowerCase().replace(/\/+$/, '');
    const parts = cleanPath.split('/').filter(Boolean);
    const lastSeg = parts.length > 0 ? parts[parts.length - 1] : '';
    const isHome = parts.length === 0 || lastSeg === 'home' || lastSeg === 'rewards' || lastSeg === 'rewards.html' || lastSeg === 'home.html' || lastSeg === 'index.html' || lastSeg === 'site';
    if (isHome) {
      const openFilterBtn = document.getElementById('openFilterDrawerBtn');
      if (openFilterBtn) openFilterBtn.style.display = 'inline-flex';
    }

    if (!originalMainContent && mainContentArea) {
      originalMainContent = mainContentArea.innerHTML;
    }

    const tokens = query.split(/\s+/).filter(Boolean);
    const isTagScope = currentScope.toLowerCase() === 'tags' || window.location.pathname.includes('/tags');
    const isBookmarkScope = currentScope.toLowerCase() === 'bookmarks';
    
    let bookmarks = [];
    if (isBookmarkScope) {
      bookmarks = JSON.parse(localStorage.getItem('owgt_bookmarks') || '[]').map(b => b.id);
    }

    const escapeRegExp = str => str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

    const scoredResults = searchData.map(item => {
      if (currentScope !== 'global' && !isBookmarkScope && item.category.toLowerCase() !== currentScope.toLowerCase()) return null;
      if (isBookmarkScope && !bookmarks.includes(item.id)) return null;

      let score = 0;
      let matchedSnippet = '';
      const matchedTokens = new Set();

      const searchInStr = (str, points, type) => {
        if (!str) return;
        const lowerStr = str.toLowerCase();

        // Exact phrase match bonus
        if (tokens.length > 1 && lowerStr.includes(query)) {
          score += points * 3;
        }

        tokens.forEach(token => {
          let idx = -1;
          let matchLen = token.length;

          if (token.length <= 3) {
            // Whole-word matching for short tokens (e.g. 'ai', 'ui', 'pdf')
            const regex = new RegExp(`\\b${escapeRegExp(token)}\\b`, 'i');
            const match = regex.exec(str);
            if (match) {
              idx = match.index;
              matchLen = match[0].length;
            }
          } else {
            idx = lowerStr.indexOf(token);
          }

          if (idx !== -1) {
            score += points;
            matchedTokens.add(token);
            if (!matchedSnippet && type !== 'tag') {
              const start = Math.max(0, idx - 40);
              const end = Math.min(str.length, idx + matchLen + 40);
              let snip = str.substring(start, end);
              const highlightRegex = token.length <= 3
                ? new RegExp(`\\b(${escapeRegExp(token)})\\b`, 'gi')
                : new RegExp(`(${escapeRegExp(token)})`, 'gi');
              snip = snip.replace(highlightRegex, match => `<mark>${match}</mark>`);
              matchedSnippet = (start > 0 ? '...' : '') + snip + (end < str.length ? '...' : '');
            }
          }
        });
      };

      searchInStr(item.name, 1000, 'name');
      searchInStr(item.description, 100, 'desc');
      searchInStr(item.content, 10, 'content');
      searchInStr(item.url, 50, 'url');
      
      const tagPoints = isTagScope ? 500 : 1;
      if (item.tags) {
        item.tags.forEach(tag => {
          tokens.forEach(token => {
            let matched = false;
            if (token.length <= 3) {
              const regex = new RegExp(`\\b${escapeRegExp(token)}\\b`, 'i');
              matched = regex.test(tag);
            } else {
              matched = tag.toLowerCase().includes(token);
            }
            if (matched) {
              score += tagPoints;
              matchedTokens.add(token);
              if (!matchedSnippet) matchedSnippet = `Tag: <mark>${tag}</mark>`;
            }
          });
        });
      }

      // Requiring multi-token match when query has multiple tokens
      const minTokensRequired = tokens.length > 1 ? Math.min(tokens.length, 2) : 1;
      if (score > 0 && matchedTokens.size >= minTokensRequired) {
        const finalScore = score * (matchedTokens.size / tokens.length);
        return { item, score: finalScore, matchedSnippet };
      }
      return null;
    }).filter(r => r !== null).sort((a, b) => b.score - a.score);

    renderResults(scoredResults, query);
  };

  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      executeSearch();
    }
  });

  executeBtn.addEventListener('click', executeSearch);

  function renderResults(results, query) {
    if (!mainContentArea) return;
    
    const escapeHTML = str => {
      if (!str) return '';
      return String(str).replace(/[&<>'"]/g, tag => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
      }[tag]));
    };

    let html = `<div style="padding: var(--space-xl) var(--space-md); margin-top: var(--space-md);">`;
    html += `<h2 style="font-family: var(--font-display); text-transform: uppercase; margin-bottom: var(--space-lg);">Search Results for "${escapeHTML(query)}"</h2>`;
    
    if (results.length === 0) {
      html += `<p style="font-family: var(--font-outlier); color: var(--color-muted);">No items matched your search in this scope.</p>`;
    } else {
      html += `<div class="card-grid card-grid--4">`;
      results.forEach(res => {
        const item = res.item;
        const tagsStr = item.tags ? item.tags.slice(0, 3).map(t => '#' + t).join(' ') : '';
        if (item.is_shallow) {
          // Shallow Item Card matching site category card styling
          html += `
            <div class="card card--expandable" style="--cat-color: var(--color-accent-2);">
              <div class="card__accent-strip"></div>
              <div class="card__header" style="display: flex; justify-content: space-between; align-items: start;">
                <span class="tag" style="font-size: 9px; padding: 2px 6px;">${escapeHTML(item.category)}</span>
                <button class="btn--ghost" data-bookmark-id="${escapeHTML(item.id)}" data-title="${escapeHTML(item.name)}" data-path="${escapeHTML(item.path)}" data-category="${escapeHTML(item.category)}" style="border: 1px solid var(--color-ink); padding: 2px 6px; font-family: var(--font-outlier); font-size: 10px;">♡ Save</button>
              </div>
              <div class="card__body">
                <h3 class="card__title">${escapeHTML(item.name)}</h3>
                <p class="card__desc">${escapeHTML(item.description || '')}</p>
                ${res.matchedSnippet ? `<div class="search-snippet">${res.matchedSnippet}</div>` : ''}
              </div>
              <button class="card__expand-btn" aria-expanded="false" onclick="this.setAttribute('aria-expanded', this.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'); this.nextElementSibling.classList.toggle('is-open');">
                <span>Quick View</span>
                <span class="card__expand-arrow">↓</span>
              </button>
              <div class="card__expand-content">
                <p style="font-size: var(--text-sm); white-space: pre-line;">${escapeHTML(item.content || item.description || '')}</p>
                ${item.url ? `<a href="${escapeHTML(item.url)}" target="_blank" class="btn btn--primary" style="margin-top: var(--space-sm); width: 100%;">Visit Resource ↗</a>` : ''}
              </div>
            </div>
          `;
        } else {
          // Deep Item Card matching site category card styling
          html += `
            <a href="${item.path}" class="card" style="--cat-color: var(--color-cat-prompts); text-decoration: none;">
              <div class="card__accent-strip"></div>
              <div class="card__header" style="display: flex; justify-content: space-between; align-items: start;">
                <span class="tag" style="font-size: 9px; padding: 2px 6px;">${escapeHTML(item.subcategory || item.category)}</span>
                <button class="btn--ghost" data-bookmark-id="${escapeHTML(item.id)}" data-title="${escapeHTML(item.name)}" data-path="${escapeHTML(item.path)}" data-category="${escapeHTML(item.category)}" style="border: 1px solid var(--color-ink); padding: 2px 6px; font-family: var(--font-outlier); font-size: 10px;">♡ Save</button>
              </div>
              <div class="card__body">
                <h3 class="card__title">${escapeHTML(item.name)}</h3>
                <p class="card__desc">${escapeHTML(item.description || '')}</p>
                ${res.matchedSnippet ? `<div class="search-snippet">${res.matchedSnippet}</div>` : ''}
              </div>
              <div class="card__footer">
                <span class="meta">${escapeHTML(tagsStr)}</span>
                <span class="card__expand-arrow">→</span>
              </div>
            </a>
          `;
        }
      });
      html += `</div>`;
    }
    html += `</div>`;
    
    mainContentArea.innerHTML = html;
    initBookmarks();
    initExpandableCards();
    if (window.applyCurrentFilters) window.applyCurrentFilters();
  }
}

/* ==========================================================================
   BOOKMARKS
   ========================================================================== */
function initBookmarks() {
  window.toggleBookmark = (id, title, path, category) => {
    let bookmarks = JSON.parse(localStorage.getItem('owgt_bookmarks') || '[]');
    const exists = bookmarks.find(b => b.id === id);
    
    if (exists) {
      bookmarks = bookmarks.filter(b => b.id !== id);
      showToast('Removed from Vault');
    } else {
      bookmarks.push({ id, title, path, category, date: new Date().toISOString() });
      showToast('Saved to Vault');
    }
    
    localStorage.setItem('owgt_bookmarks', JSON.stringify(bookmarks));
    updateBookmarkUI(id, !exists);
  };
  
  // Initialize UI state on page load
  const bookmarks = JSON.parse(localStorage.getItem('owgt_bookmarks') || '[]');
  document.querySelectorAll('[data-bookmark-id]').forEach(btn => {
    const id = btn.getAttribute('data-bookmark-id');
    const isBookmarked = bookmarks.some(b => b.id === id);
    updateBookmarkUI(id, isBookmarked);
    
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      toggleBookmark(id, btn.getAttribute('data-title'), btn.getAttribute('data-path'), btn.getAttribute('data-category'));
    });
  });
}

function updateBookmarkUI(id, isBookmarked) {
  document.querySelectorAll(`[data-bookmark-id="${id}"]`).forEach(btn => {
    if (isBookmarked) {
      btn.innerHTML = '♥ Saved';
      btn.classList.add('is-saved');
      btn.style.background = '#ef4444';
      btn.style.color = '#fff';
    } else {
      btn.innerHTML = '♡ Save';
      btn.classList.remove('is-saved');
      btn.style.background = 'transparent';
      btn.style.color = 'inherit';
    }
  });
}

/* ==========================================================================
   GLOBAL KEYBOARD SHORTCUTS
   ========================================================================== */
function initShortcuts() {
  document.addEventListener('keydown', (e) => {
    // Ignore keyboard shortcuts if modifier keys (Ctrl, Meta, Alt) are pressed
    if (e.ctrlKey || e.metaKey || e.altKey) return;

    // Don't trigger if user is typing in an input
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
      if (e.key === 'Escape') toggleSearch();
      return;
    }

    switch(e.key.toLowerCase()) {
      case '/':
        e.preventDefault();
        toggleSearch();
        break;
      case 'b':
        // Try to bookmark the current page if it's a deep page
        const bBtn = document.querySelector('.bookmark-main-btn');
        if (bBtn) bBtn.click();
        break;
      case 'c':
        // Copy the main prompt if it exists
        const copyBtn = document.querySelector('.copy-main-btn');
        if (copyBtn) copyBtn.click();
        break;
      case 'r':
        // Randomizer
        loadRandomResource();
        break;
    }
  });
}

function loadRandomResource() {
  fetch('/search-index.json')
    .then(res => res.json())
    .then(data => {
      if (data.length > 0) {
        const randomItem = data[Math.floor(Math.random() * data.length)];
        window.location.href = `${randomItem.path}`;
      }
    });
}

/* ==========================================================================
   COPY ENGINE
   ========================================================================== */
function initCopyEngine() {
  window.copyToClipboard = (textToCopy, btnElement) => {
    navigator.clipboard.writeText(textToCopy).then(() => {
      const originalHTML = btnElement.innerHTML;
      btnElement.classList.add('is-copied');
      btnElement.style.background = "#22c55e";
      btnElement.style.color = "#fff";
      btnElement.style.borderColor = "#22c55e";
      btnElement.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
      
      setTimeout(() => {
        btnElement.classList.remove('is-copied');
        btnElement.innerHTML = originalHTML;
        btnElement.style.background = "";
        btnElement.style.color = "";
        btnElement.style.borderColor = "";
      }, 2000);
    });
  };
}

/* ==========================================================================
   TOAST NOTIFICATION
   ========================================================================== */
function showToast(message) {
  let toast = document.getElementById('owgt-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'owgt-toast';
    Object.assign(toast.style, {
      position: 'fixed', bottom: '2rem', left: '50%', transform: 'translateX(-50%)',
      background: 'var(--color-ink)', color: 'var(--color-paper)',
      padding: '0.75rem 1.5rem', fontFamily: 'var(--font-outlier)', textTransform: 'uppercase',
      fontSize: 'var(--text-xs)', zIndex: '9999', boxShadow: '4px 4px 0 var(--color-accent)',
      transition: 'opacity 0.3s', opacity: '0'
    });
    document.body.appendChild(toast);
  }
  
  toast.innerText = message;
  toast.style.opacity = '1';
  
  setTimeout(() => {
    toast.style.opacity = '0';
  }, 3000);
}

/* ==========================================================================
   SPOTLIGHT RESOURCE SYSTEM
   ========================================================================== */
function initSpotlight() {
  const titleEl = document.getElementById('spotlight-title');
  const catEl = document.getElementById('spotlight-category');
  const descEl = document.getElementById('spotlight-desc');
  const copyBtn = document.getElementById('spotlight-copy-btn');
  const shuffleBtn = document.getElementById('spotlight-shuffle-btn');
  const linkBtn = document.getElementById('spotlight-link-btn');

  if (!titleEl || !copyBtn || !shuffleBtn) return;

  let allData = [];
  let currentItem = null;

  const updateSpotlight = (item) => {
    currentItem = item;
    titleEl.textContent = item.name;
    catEl.textContent = `Category: ${item.category}`;
    descEl.textContent = item.description ? `"${item.description}"` : `"Curated AI resource from the vault."`;
    if (linkBtn) {
      if (item.is_shallow) {
        linkBtn.style.display = 'none';
      } else if (item.path) {
        linkBtn.href = `${item.path}`;
        linkBtn.style.display = 'inline-block';
      }
    }
  };

  const getRandomItem = () => {
    if (!allData || allData.length === 0) return;
    const randomIndex = Math.floor(Math.random() * allData.length);
    updateSpotlight(allData[randomIndex]);
  };

  fetch('/search-index.json')
    .then(res => res.json())
    .then(data => {
      allData = data;
      getRandomItem();
    })
    .catch(err => console.error('Error loading spotlight data:', err));

  shuffleBtn.addEventListener('click', () => {
    getRandomItem();
  });

  copyBtn.addEventListener('click', () => {
    if (!currentItem) return;
    const textToCopy = currentItem.description || currentItem.name;
    navigator.clipboard.writeText(textToCopy).then(() => {
      const origText = copyBtn.innerText;
      copyBtn.innerText = "✔ COPIED!";
      copyBtn.style.background = "#22c55e";
      copyBtn.style.color = "#fff";
      
      setTimeout(() => {
        copyBtn.innerText = origText;
        copyBtn.style.background = "";
        copyBtn.style.color = "";
      }, 2000);
    });
  });
}

/* ==========================================================================
   EXPANDABLE CARD FULL-CLICK (Fix #8)
   ========================================================================== */
function initExpandableCards() {
  document.querySelectorAll('.card--expandable').forEach(card => {
    card.style.cursor = 'pointer';
    card.addEventListener('click', (e) => {
      // Don't trigger if clicking a button, link, or bookmark
      if (e.target.closest('button, a, [data-bookmark-id]')) return;
      const expandBtn = card.querySelector('.card__expand-btn');
      if (expandBtn) expandBtn.click();
    });
  });
}

/* ==========================================================================
   ACTIVE NAV HIGHLIGHT (Fix #10)
   ========================================================================== */
function highlightActiveNav() {
  const path = window.location.pathname.replace(/^\//, '').replace(/\.html$/, '');
  document.querySelectorAll('.new-header-nav a, .mast-nav a').forEach(link => {
    const href = link.getAttribute('href').replace(/^\//, '').replace(/\.html$/, '');
    if (href === path) {
      link.classList.add('active');
    }
  });
}

// Global Header Scroll Logic
document.addEventListener('DOMContentLoaded', () => {
  const header = document.getElementById('globalHeader');
  if (!header) return;
  
  if (window.location.pathname === '/' || window.location.pathname.endsWith('/index.html') || window.location.pathname === '/home' || window.location.pathname.endsWith('/rewards.html') || window.location.pathname === '/rewards') {
    document.body.classList.add('is-home');
  }
});


/* ==========================================================================
   FILTER SYSTEM
   ========================================================================== */
function initFilterSystem() {
  const mainContentArea = document.querySelector('main');
  if (!mainContentArea) return;

  let activeFilters = {
    category: '',
    subcategory: '',
    tags: []
  };
  
  const drawerHTML = `
    <div class="filter-backdrop" id="filterBackdrop"></div>
    <div class="filter-drawer" id="filterDrawer">
      <div class="filter-drawer__header">
        <h3>Filters</h3>
        <button class="filter-drawer__close" id="closeFilterDrawer">✕</button>
      </div>
      <div class="filter-drawer__body">
        <div class="filter-group" id="categoryFilterGroup" style="display:none;">
          <label>Category</label>
          <select class="filter-select" id="filterCategorySelect">
            <option value="">All Categories</option>
          </select>
        </div>
        <div class="filter-group" id="subcategoryFilterGroup" style="display:none;">
          <label>Type</label>
          <select class="filter-select" id="filterSubcategorySelect">
            <option value="">All Types</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Tags</label>
          <div class="filter-tags-cloud" id="filterTagsCloud"></div>
        </div>
      </div>
      <div class="filter-drawer__footer">
        <button class="btn-reset-filters" id="resetFiltersBtn">Reset</button>
        <button class="btn-apply-filters" id="applyFiltersBtn">Apply Filters</button>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', drawerHTML);

  const filterBackdrop = document.getElementById('filterBackdrop');
  const filterDrawer = document.getElementById('filterDrawer');
  const closeFilterDrawer = document.getElementById('closeFilterDrawer');
  const categoryFilterGroup = document.getElementById('categoryFilterGroup');
  const filterCategorySelect = document.getElementById('filterCategorySelect');
  const subcategoryFilterGroup = document.getElementById('subcategoryFilterGroup');
  const filterSubcategorySelect = document.getElementById('filterSubcategorySelect');
  const filterTagsCloud = document.getElementById('filterTagsCloud');
  const resetFiltersBtn = document.getElementById('resetFiltersBtn');
  const applyFiltersBtn = document.getElementById('applyFiltersBtn');
  
  const cleanPath = window.location.pathname.toLowerCase().replace(/\/+$/, '');
  const parts = cleanPath.split('/').filter(Boolean);
  const lastSegment = parts.length > 0 ? parts[parts.length - 1] : '';
  const isHomePage = parts.length === 0 || lastSegment === 'home' || lastSegment === 'rewards' || lastSegment === 'rewards.html' || lastSegment === 'home.html' || lastSegment === 'index.html' || lastSegment === 'site';

  const headerContent = document.querySelector('.new-global-header') || document.querySelector('header');
  if (headerContent) {
    let triggerBtn = document.getElementById('openFilterDrawerBtn');
    if (!triggerBtn) {
      triggerBtn = document.createElement('button');
      triggerBtn.className = 'filter-trigger-btn';
      triggerBtn.id = 'openFilterDrawerBtn';
      triggerBtn.setAttribute('aria-label', 'Open Filters');
      triggerBtn.style.display = isHomePage ? 'none' : 'inline-flex';
      triggerBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
        <span class="filter-badge" id="filterActiveBadge">0</span>
      `;
      const searchContainer = document.getElementById('headerSearchContainer');
      if (searchContainer) {
         searchContainer.parentNode.insertBefore(triggerBtn, searchContainer.nextSibling);
      } else {
         headerContent.appendChild(triggerBtn);
      }
    } else {
      triggerBtn.style.display = isHomePage ? 'none' : 'inline-flex';
    }
    
    triggerBtn.addEventListener('click', openDrawer);
  }

  let allItems = [];
  fetch('/search-index.json').then(r => r.json()).then(data => {
    allItems = data;
    populateDrawer();
  }).catch(err => console.error('Filter load error', err));

  const pathParts = window.location.pathname.split('/').filter(Boolean);
  let catSlug = pathParts.length > 0 ? pathParts[0] : '';
  if (catSlug === 'items' && pathParts.length > 1) {
    catSlug = pathParts[1];
  }
  const catMap = {
    'prompts': 'Prompts', 'tools': 'Tools', 'guides': 'Guides',
    'resources': 'Resources', 'tags': 'Tags', 'bookmarks': 'Saved',
    'learning': 'Learning', 'cheatsheets': 'Cheat Sheets',
    'templates': 'Templates', 'frameworks': 'Frameworks'
  };
  const pageCategory = catMap[catSlug] || '';
  const isGlobal = !pageCategory;

  function updateSubcategories() {
    const currentCat = isGlobal ? activeFilters.category : pageCategory;
    let pool = allItems;
    if (currentCat) {
      pool = allItems.filter(i => (i.category || '').toLowerCase() === currentCat.toLowerCase());
    }
    const subcats = [...new Set(pool.map(i => i.subcategory).filter(Boolean))].sort();

    filterSubcategorySelect.innerHTML = '<option value="">All Types</option>';
    if (subcats.length > 0) {
      subcats.forEach(s => {
        filterSubcategorySelect.insertAdjacentHTML('beforeend', `<option value="${s}">${s}</option>`);
      });
      if (subcategoryFilterGroup) subcategoryFilterGroup.style.display = 'block';
    } else {
      if (subcategoryFilterGroup) subcategoryFilterGroup.style.display = 'none';
      activeFilters.subcategory = '';
    }
  }

  function populateDrawer() {
    if (!isGlobal) {
      categoryFilterGroup.style.display = 'none';
    } else {
      categoryFilterGroup.style.display = 'block';
      filterCategorySelect.innerHTML = '<option value="">All Categories</option>';
      const categories = [...new Set(allItems.map(i => i.category).filter(Boolean))].sort();
      categories.forEach(c => {
        filterCategorySelect.insertAdjacentHTML('beforeend', `<option value="${c}">${c}</option>`);
      });
    }

    updateSubcategories();

    // Populate ALL tags across the site so ALL tags appear in filter drawer
    const tags = new Set();
    allItems.forEach(item => {
      if (item.tags) item.tags.forEach(t => tags.add(t));
    });
    const sortedTags = [...tags].sort();
    
    filterTagsCloud.innerHTML = '';
    sortedTags.forEach(tag => {
      const btn = document.createElement('button');
      btn.className = 'filter-tag-pill';
      btn.dataset.tag = tag;
      btn.textContent = tag;
      btn.addEventListener('click', () => {
        btn.classList.toggle('is-active');
        const isActive = btn.classList.contains('is-active');
        if (isActive) activeFilters.tags.push(tag);
        else activeFilters.tags = activeFilters.tags.filter(t => t !== tag);
      });
      filterTagsCloud.appendChild(btn);
    });
  }

  function openDrawer() {
    filterBackdrop.classList.add('is-active');
    filterDrawer.classList.add('is-open');
  }

  function closeDrawer() {
    filterBackdrop.classList.remove('is-active');
    filterDrawer.classList.remove('is-open');
  }

  closeFilterDrawer.addEventListener('click', closeDrawer);
  filterBackdrop.addEventListener('click', closeDrawer);

  filterCategorySelect.addEventListener('change', (e) => {
    activeFilters.category = e.target.value;
    activeFilters.subcategory = '';
    updateSubcategories();
  });
  filterSubcategorySelect.addEventListener('change', (e) => activeFilters.subcategory = e.target.value);

  window.resetFilters = () => {
    activeFilters.category = '';
    activeFilters.subcategory = '';
    activeFilters.tags = [];
    filterCategorySelect.value = '';
    filterSubcategorySelect.value = '';
    document.querySelectorAll('.filter-tag-pill').forEach(btn => btn.classList.remove('is-active'));
    updateSubcategories();
    applyFilters();
  };

  resetFiltersBtn.addEventListener('click', () => {
    window.resetFilters();
  });

  applyFiltersBtn.addEventListener('click', () => {
    applyFilters();
    closeDrawer();
  });

  function applyFilters() {
    let count = activeFilters.tags.length;
    if (activeFilters.category) count++;
    if (activeFilters.subcategory) count++;
    
    const badge = document.getElementById('filterActiveBadge');
    if (badge) {
      badge.textContent = count;
      if (count > 0) badge.classList.add('has-count');
      else badge.classList.remove('has-count');
    }

    const evt = new CustomEvent('owgtFiltersApplied', { detail: activeFilters });
    document.dispatchEvent(evt);
    
    filterPageCards();
  }

  window.applyCurrentFilters = filterPageCards;
  function filterPageCards() {
    const cards = document.querySelectorAll('.card-grid .card');
    if (!cards.length) return;
    
    cards.forEach(card => {
       const headerTag = card.querySelector('.tag');
       const metaTags = card.querySelector('.meta');
       
       const cardSubcat = headerTag ? headerTag.textContent.trim().toLowerCase() : '';
       const cardTagsStr = metaTags ? metaTags.textContent.toLowerCase() : '';
       
       let show = true;
       if (activeFilters.subcategory && cardSubcat !== activeFilters.subcategory.toLowerCase()) {
         show = false;
       }
       if (show && activeFilters.tags.length > 0) {
          const hasAllTags = activeFilters.tags.every(tag => cardTagsStr.includes('#' + tag.toLowerCase()));
          if (!hasAllTags) show = false;
       }
       
       if (show) {
         card.style.display = 'flex';
       } else {
         card.style.display = 'none';
       }
    });
  }
}

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
  const pathParts = window.location.pathname.split('/');
  const catMatch = pathParts.length > 1 ? pathParts[1] : '';
  const localScopeBtn = document.getElementById('localScopeBtn');
  let pageCategory = '';
  if (['prompts', 'tools', 'guides', 'resources', 'tags', 'bookmarks', 'learning', 'cheatsheets', 'templates', 'frameworks'].includes(catMatch)) {
    pageCategory = catMatch.charAt(0).toUpperCase() + catMatch.slice(1);
    if(localScopeBtn) localScopeBtn.textContent = pageCategory;
  } else {
    if(localScopeBtn) localScopeBtn.style.display = 'none'; // hide if not in category
  }

  fetch('/search-index.json')
    .then(res => res.json())
    .then(data => { searchData = data; })
    .catch(err => console.error('Could not load search index', err));

  const globalHeader = document.getElementById('globalHeader');

  triggerBtn.addEventListener('click', () => {
    const isCategoryPage = !!pageCategory;
    if (!isCategoryPage) {
      // Direct open Global "All Rewards" search on homepage/global pages
      currentScope = 'global';
      activeScopePill.textContent = 'All Rewards';
      searchContainer.style.display = 'flex';
      scopeSelect.style.display = 'none';
      triggerBtn.style.display = 'none';
      inputWrapper.style.display = 'flex';
      if (globalHeader) globalHeader.classList.add('search-active');
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
    if (!query) return;

    if (!originalMainContent && mainContentArea) {
      originalMainContent = mainContentArea.innerHTML;
    }

    const tokens = query.split(/\s+/);
    const isTagScope = currentScope.toLowerCase() === 'tags' || window.location.pathname.includes('/tags');
    const isBookmarkScope = currentScope.toLowerCase() === 'bookmarks';
    
    let bookmarks = [];
    if (isBookmarkScope) {
      bookmarks = JSON.parse(localStorage.getItem('owgt_bookmarks') || '[]').map(b => b.id);
    }

    const scoredResults = searchData.map(item => {
      if (currentScope !== 'global' && !isBookmarkScope && item.category.toLowerCase() !== currentScope.toLowerCase()) return null;
      if (isBookmarkScope && !bookmarks.includes(item.id)) return null;

      let score = 0;
      let matchedSnippet = '';

      const searchInStr = (str, points, type) => {
        if (!str) return;
        const lowerStr = str.toLowerCase();
        let matched = false;
        tokens.forEach(token => {
          const idx = lowerStr.indexOf(token);
          if (idx !== -1) {
            score += points;
            if (!matchedSnippet && type !== 'tag') {
              const start = Math.max(0, idx - 40);
              const end = Math.min(str.length, idx + token.length + 40);
              let snip = str.substring(start, end);
              const regex = new RegExp(token, 'gi');
              snip = snip.replace(regex, match => `<mark>${match}</mark>`);
              matchedSnippet = (start > 0 ? '...' : '') + snip + (end < str.length ? '...' : '');
            }
          }
        });
      };

      searchInStr(item.name, 1000, 'name');
      searchInStr(item.description, 100, 'desc');
      searchInStr(item.content, 10, 'content');
      
      const tagPoints = isTagScope ? 500 : 1;
      if (item.tags) {
        item.tags.forEach(tag => {
          tokens.forEach(token => {
            if (tag.toLowerCase().includes(token)) {
              score += tagPoints;
              if (!matchedSnippet) matchedSnippet = `Tag: <mark>${tag}</mark>`;
            }
          });
        });
      }

      if (score > 0) {
        return { item, score, matchedSnippet };
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
    
    let html = `<div style="padding: var(--space-xl) var(--space-md);">`;
    html += `<h2 style="font-family: var(--font-display); text-transform: uppercase; margin-bottom: var(--space-lg);">Search Results for "${query}"</h2>`;
    
    if (results.length === 0) {
      html += `<p style="font-family: var(--font-outlier); color: var(--color-muted);">No items matched your search in this scope.</p>`;
    } else {
      html += `<div class="search-results-grid">`;
      results.forEach(res => {
        const item = res.item;
        html += `
          <a href="${item.path}" class="card" style="border: 1px solid var(--color-ink); padding: var(--space-md); text-decoration: none; color: var(--color-ink); display: flex; flex-direction: column; background: var(--color-paper);">
            <div style="font-size: 10px; font-family: var(--font-outlier); text-transform: uppercase; margin-bottom: 8px; color: var(--color-muted);">${item.category}</div>
            <h3 style="font-family: var(--font-display); font-size: var(--text-lg); margin: 0 0 8px 0; text-transform: uppercase;">${item.name}</h3>
            <p style="font-size: var(--text-sm); margin: 0 0 12px 0;">${item.description || ''}</p>
            <div class="search-snippet">${res.matchedSnippet}</div>
          </a>
        `;
      });
      html += `</div>`;
    }
    html += `</div>`;
    
    mainContentArea.innerHTML = html;
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
      const originalText = btnElement.innerText;
      btnElement.innerText = "✔ COPIED!";
      btnElement.style.background = "#22c55e";
      btnElement.style.color = "#fff";
      
      setTimeout(() => {
        btnElement.innerText = originalText;
        btnElement.style.background = "";
        btnElement.style.color = "";
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
      link.style.color = 'var(--color-accent)';
    }
  });
}

// Global Header Scroll Logic
document.addEventListener('DOMContentLoaded', () => {
  const header = document.getElementById('globalHeader');
  if (!header) return;
  
  if (window.location.pathname === '/' || window.location.pathname.endsWith('/index.html') || window.location.pathname === '/home') {
    document.body.classList.add('is-home');
    header.classList.add('hidden-on-home');
    
    const target = document.querySelector('.hero-marquee'); // Using hero section
    if (target) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) {
            header.classList.remove('hidden-on-home');
            header.classList.add('visible-on-home');
          } else {
            header.classList.add('hidden-on-home');
            header.classList.remove('visible-on-home');
          }
        });
      }, { threshold: 0.1 });
      observer.observe(target);
    }
  }
});

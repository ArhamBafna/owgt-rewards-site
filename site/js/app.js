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
  // Inject Search Overlay into DOM
  const overlayHtml = `
    <div id="search-overlay" class="search-overlay" style="display: none;">
      <div class="search-modal">
        <div class="search-header">
          <input type="text" id="search-input-main" placeholder="Search the vault... (Esc to close)" autocomplete="off">
        </div>
        <div id="search-results" class="search-results">
          <!-- Results populated here -->
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', overlayHtml);
  
  // Inject minimal CSS for search overlay
  const style = document.createElement('style');
  style.textContent = `
    .search-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.8); z-index: 9999; display: flex; justify-content: center; padding-top: 10vh; backdrop-filter: blur(4px); }
    .search-modal { background: var(--color-paper); width: 100%; max-width: 600px; border: 2px solid var(--color-ink); box-shadow: 8px 8px 0 var(--color-ink); max-height: 80vh; display: flex; flex-direction: column; }
    .search-header { border-bottom: 2px solid var(--color-ink); padding: var(--space-sm); }
    #search-input-main { width: 100%; padding: var(--space-md); font-family: var(--font-display); font-size: var(--text-2xl); border: none; background: transparent; outline: none; }
    .search-results { padding: var(--space-md); overflow-y: auto; display: flex; flex-direction: column; gap: var(--space-sm); }
    .search-result-item { padding: var(--space-sm); border: 1px solid var(--color-ink); text-decoration: none; color: var(--color-ink); display: block; transition: all 0.1s; }
    .search-result-item:hover, .search-result-item.active { background: var(--color-accent); color: var(--color-accent-ink); transform: translate(-2px, -2px); box-shadow: 4px 4px 0 var(--color-ink); }
    .search-result-title { font-family: var(--font-display); font-size: var(--text-lg); text-transform: uppercase; }
    .search-result-meta { font-family: var(--font-outlier); font-size: var(--text-xs); margin-top: 4px; opacity: 0.8; }
  `;
  document.head.appendChild(style);

  const overlay = document.getElementById('search-overlay');
  const input = document.getElementById('search-input-main');
  const resultsContainer = document.getElementById('search-results');
  
  let searchData = [];
  
  // Load index asynchronously
  fetch('search-index.json')
    .then(res => res.json())
    .then(data => { searchData = data; })
    .catch(err => console.error('Could not load search index', err));

  // Toggle Search
  window.toggleSearch = () => {
    if (overlay.style.display === 'none') {
      overlay.style.display = 'flex';
      input.focus();
    } else {
      overlay.style.display = 'none';
      input.value = '';
      resultsContainer.innerHTML = '';
    }
  };

  // Close on background click
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) toggleSearch();
  });

  // Search Logic (As you type)
  input.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase();
    if (!query) {
      resultsContainer.innerHTML = '';
      return;
    }
    
    const results = searchData.filter(item => {
      return item.name.toLowerCase().includes(query) || 
             (item.description && item.description.toLowerCase().includes(query)) ||
             (item.tags && item.tags.some(tag => tag.toLowerCase().includes(query)));
    }).slice(0, 8); // Top 8 results
    
    if (results.length === 0) {
      resultsContainer.innerHTML = '<p style="font-family: var(--font-outlier); padding: 1rem;">No results found.</p>';
      return;
    }

    const escapeHTML = str => {
      if (!str) return '';
      return String(str).replace(/[&<>'"]/g, tag => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        "'": '&#39;',
        '"': '&quot;'
      }[tag]));
    };

    resultsContainer.innerHTML = results.map(item => `
      <a href="${escapeHTML(item.path)}" class="search-result-item">
        <div class="search-result-title">${escapeHTML(item.name)}</div>
        <div class="search-result-meta">${escapeHTML(item.category)} ${item.tags.length ? '· ' + item.tags.map(t=>'#'+escapeHTML(t)).join(' ') : ''}</div>
      </a>
    `).join('');
  });
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

  fetch('search-index.json')
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
  document.querySelectorAll('.mast-nav a').forEach(link => {
    const href = link.getAttribute('href').replace(/^\//, '').replace(/\.html$/, '');
    if (href === path) {
      link.classList.add('active');
      link.style.color = 'var(--color-accent)';
    }
  });
}

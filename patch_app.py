import sys

with open('site/js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '  highlightActiveNav();\n});',
    '  highlightActiveNav();\n  if (typeof initFilterSystem === \'function\') initFilterSystem();\n});'
)

filter_code = """

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
        <div class="filter-group">
          <label>Subcategory</label>
          <select class="filter-select" id="filterSubcategorySelect">
            <option value="">All Subcategories</option>
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
  const filterSubcategorySelect = document.getElementById('filterSubcategorySelect');
  const filterTagsCloud = document.getElementById('filterTagsCloud');
  const resetFiltersBtn = document.getElementById('resetFiltersBtn');
  const applyFiltersBtn = document.getElementById('applyFiltersBtn');
  
  const headerContent = document.querySelector('.header-content') || document.querySelector('header');
  if (headerContent) {
    const triggerBtn = document.createElement('button');
    triggerBtn.className = 'filter-trigger-btn';
    triggerBtn.id = 'openFilterDrawerBtn';
    triggerBtn.innerHTML = `
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
      Filter
      <span class="filter-badge" id="filterActiveBadge">0</span>
    `;
    const searchContainer = document.getElementById('headerSearchContainer');
    if (searchContainer) {
       searchContainer.parentNode.insertBefore(triggerBtn, searchContainer.nextSibling);
    } else {
       headerContent.appendChild(triggerBtn);
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
    'resources': 'Resources', 'tags': 'Tags', 'bookmarks': 'Bookmarks',
    'learning': 'Learning', 'cheatsheets': 'Cheat Sheets',
    'templates': 'Templates', 'frameworks': 'Frameworks'
  };
  const pageCategory = catMap[catSlug] || '';
  const isGlobal = !pageCategory;

  function populateDrawer() {
    let itemsToProcess = allItems;
    if (!isGlobal) {
      itemsToProcess = allItems.filter(i => (i.category || '').toLowerCase() === pageCategory.toLowerCase());
      categoryFilterGroup.style.display = 'none';
    } else {
      categoryFilterGroup.style.display = 'block';
      const categories = [...new Set(allItems.map(i => i.category).filter(Boolean))].sort();
      categories.forEach(c => {
        filterCategorySelect.insertAdjacentHTML('beforeend', `<option value="${c}">${c}</option>`);
      });
    }

    const subcats = [...new Set(itemsToProcess.map(i => i.subcategory).filter(Boolean))].sort();
    subcats.forEach(s => {
      filterSubcategorySelect.insertAdjacentHTML('beforeend', `<option value="${s}">${s}</option>`);
    });

    const tags = new Set();
    itemsToProcess.forEach(item => {
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

  filterCategorySelect.addEventListener('change', (e) => activeFilters.category = e.target.value);
  filterSubcategorySelect.addEventListener('change', (e) => activeFilters.subcategory = e.target.value);

  resetFiltersBtn.addEventListener('click', () => {
    activeFilters.category = '';
    activeFilters.subcategory = '';
    activeFilters.tags = [];
    filterCategorySelect.value = '';
    filterSubcategorySelect.value = '';
    document.querySelectorAll('.filter-tag-pill').forEach(btn => btn.classList.remove('is-active'));
    applyFilters();
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
"""

content = content + filter_code

with open('site/js/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')

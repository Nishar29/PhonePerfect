/**
 * PhonePerfect – App Logic
 * Weighted recommendation engine + UI interactions + Favorites + Compare
 */

// ─── STATE ───────────────────────────────────────────────────────────────────
let userWeights = { durability:7, camera:7, battery:7, charging:7, display:7, sound:7, ipRating:7 };
let budgetCategory = 5; // 0–5 (5 = no limit)
let currentSort = 'overall';
let currentSearch = '';
let currentBrandFilter = 'All';
let advFilters = {
  ram: 'any',
  processor: 'any',
  has5g: false,
  hasNfc: false,
  hasWireless: false
};
let showFavoritesOnly = false;
let currentTheme = 'dark'; // dark, light, amoled

let allPhonesSorted = [...PHONES];

// LocalStorage for Favorites
let favorites = JSON.parse(localStorage.getItem('phonePerfectFavs') || '[]');
// Compare List
let compareList = []; // Max 3 IDs

// ─── INIT ─────────────────────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  updateWeightsFromTags();
  renderBrandFilters();
  renderAllPhonesGrid();
  setupNavScroll();
  updateFavoritesCount();
  populateUpgradeSelect();
  
  const countEls = document.querySelectorAll('.stat-num');
  if (countEls[0]) countEls[0].textContent = PHONES.length + '+';
});

// ─── NAVBAR SCROLL ────────────────────────────────────────────────────────────
function setupNavScroll() {
  window.addEventListener('scroll', () => {
    const nav = document.getElementById('navbar');
    if (window.scrollY > 40) {
      nav.style.boxShadow = '0 4px 32px rgba(0,0,0,0.5)';
    } else {
      nav.style.boxShadow = 'none';
    }
  });
}

// ─── SLIDERS ──────────────────────────────────────────────────────────────────
let selectedPriorities = [];

function togglePriority(key, element) {
  const index = selectedPriorities.indexOf(key);
  
  if (index > -1) {
    // Remove if already selected
    selectedPriorities.splice(index, 1);
    element.classList.remove('active');
  } else {
    // Add if less than 3 are selected
    if (selectedPriorities.length >= 3) {
      // Remove the oldest one
      const oldest = selectedPriorities.shift();
      const oldEl = document.querySelector(`.priority-tag[onclick*="${oldest}"]`);
      if (oldEl) oldEl.classList.remove('active');
    }
    selectedPriorities.push(key);
    element.classList.add('active');
  }
  
  updateWeightsFromTags();
}

function updateWeightsFromTags() {
  // Reset all to base weight of 3
  CRITERIA.forEach(c => {
    userWeights[c.key] = 3; 
  });
  
  // Apply heavy weight to selected priorities
  selectedPriorities.forEach(key => {
    userWeights[key] = 10;
  });
  
  // Re-calculate UI if results are showing
  // But wait, the app recalculates live on button click. 
}

// ─── BUDGET ───────────────────────────────────────────────────────────────────
function updateBudget(val) {
  budgetCategory = parseInt(val);
  document.getElementById('budget-display').textContent = BUDGET_LABELS[budgetCategory];
  const slider = document.getElementById('budget-range');
  const pct = (val / 5) * 100;
  slider.style.background = `linear-gradient(to right, #06b6d4 ${pct}%, rgba(255,255,255,0.08) ${pct}%)`;
}

// ─── HELPERS ──────────────────────────────────────────────────────────────────
function getBatteryMah(phone) {
  const m = phone.specs.battery.match(/([\d,]+)\s*mAh/);
  return m ? m[1] : '–';
}

function getIPShort(phone) {
  return phone.specs.ip.split('–')[0].split(' ').slice(0,2).join(' ').trim();
}

function getChargingShort(phone) {
  return phone.specs.charging.split(',')[0].trim();
}

// ─── SCORING ENGINE ───────────────────────────────────────────────────────────
function computeScore(phone) {
  let totalWeight = 0;
  let weightedSum = 0;
  CRITERIA.forEach(c => {
    const w = userWeights[c.key];
    totalWeight += w;
    weightedSum += (phone.scores[c.key] || 0) * w;
  });
  if (totalWeight === 0) {
    const sum = CRITERIA.reduce((acc, c) => acc + (phone.scores[c.key] || 0), 0);
    return +(sum / CRITERIA.length).toFixed(2);
  }
  return +(weightedSum / totalWeight).toFixed(2);
}

function filterAndScore(phones) {
  return phones
    .filter(p => budgetCategory === 5 || p.priceCategory <= budgetCategory)
    .map(p => ({ ...p, _score: computeScore(p) }))
    .sort((a, b) => b._score - a._score);
}

// ─── RECOMMENDATIONS ─────────────────────────────────────────────────────────
function generateRecommendations() {
  const btn = document.getElementById('recommend-btn');
  btn.innerHTML = '<span>Analyzing ' + PHONES.length + ' phones...</span> ⏳';
  btn.disabled = true;

  setTimeout(() => {
    const scored = filterAndScore(PHONES);

    btn.innerHTML = `<span>Get Recommendations</span><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`;
    btn.disabled = false;

    const resultsSection = document.getElementById('results-section');
    resultsSection.style.display = 'block';
    setTimeout(() => resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);

    const bestCriteria = Object.entries(userWeights).sort((a,b)=>b[1]-a[1])[0];
    const criterionLabel = CRITERIA.find(c=>c.key===bestCriteria[0])?.label || '';
    document.getElementById('results-subtitle').textContent =
      `Top priority: ${criterionLabel} · ${scored.length} phones analyzed`;

    renderPodium(scored.slice(0, 3));
    renderRankedList(scored);
  }, 900);
}

// ─── PODIUM ───────────────────────────────────────────────────────────────────
const RANK_MEDALS = ['🥇', '🥈', '🥉'];
const RANK_CLASSES = ['rank-1', 'rank-2', 'rank-3'];

function renderPodium(top3) {
  const podium = document.getElementById('podium');
  const order = top3.length >= 3 ? [top3[1], top3[0], top3[2]] : top3;
  const classes = top3.length >= 3 ? ['rank-2','rank-1','rank-3'] : RANK_CLASSES;
  const medals = top3.length >= 3 ? [RANK_MEDALS[1], RANK_MEDALS[0], RANK_MEDALS[2]] : RANK_MEDALS;

  podium.innerHTML = order.map((phone, i) => {
    const mah = getBatteryMah(phone);
    return `
      <div class="podium-card ${classes[i]}" onclick="openModal('${phone.id}')">
        <div class="podium-rank">${medals[i]}</div>
        <div class="podium-img-placeholder">${phone.emoji}</div>
        <div class="podium-brand">${phone.brand}</div>
        <div class="podium-name">${phone.name}</div>
        <div class="podium-score-ring">${phone._score}</div>
        <div class="podium-price">${phone.price}</div>
        <div class="podium-mah">🔋 ${mah} mAh</div>
        <div class="podium-unique">${phone.uniqueFeature.split('+')[0].trim()}</div>
        <div class="podium-bars">
          ${CRITERIA.map(c => `
            <div class="podium-bar-row">
              <span class="podium-bar-label">${c.icon} ${c.label.split(' ')[0]}</span>
              <div class="podium-bar-track">
                <div class="podium-bar-fill" style="width: ${phone.scores[c.key] * 10}%"></div>
              </div>
            </div>
          `).join('')}
        </div>
        <button class="podium-detail-btn">View Full Specs →</button>
      </div>
    `;
  }).join('');
}

// ─── RANKED LIST ──────────────────────────────────────────────────────────────
function renderRankedList(scored) {
  const list = document.getElementById('ranked-list');
  list.innerHTML = scored.map((phone, i) => {
    const mah = getBatteryMah(phone);
    return `
      <div class="ranked-item" onclick="openModal('${phone.id}')" style="animation-delay: ${i*0.03}s">
        <span class="ranked-num ${i < 3 ? 'top3' : ''}">${i + 1}</span>
        <div class="ranked-phone-info">
          <div class="ranked-phone-name">${phone.emoji} ${phone.name}</div>
          <div class="ranked-phone-brand">${phone.brand} · ${phone.price} · 🔋 ${mah} mAh</div>
        </div>
        <div class="ranked-mini-bars">
          ${CRITERIA.map(c => `
            <div class="mini-bar" title="${c.label}: ${phone.scores[c.key]}/10">
              <div class="mini-bar-fill" style="height: ${phone.scores[c.key] * 10}%"></div>
            </div>
          `).join('')}
        </div>
        <span class="ranked-score">${phone._score}</span>
      </div>
    `;
  }).join('');
}

// ─── BRAND FILTERS ────────────────────────────────────────────────────────────
function renderBrandFilters() {
  const row = document.getElementById('brand-filters');
  if (!row) return;
  // Get unique brands
  const brands = [...new Set(PHONES.map(p => p.brand))].sort();
  brands.unshift('All');
  
  row.innerHTML = brands.map(b => `
    <button class="brand-chip ${currentBrandFilter === b ? 'active' : ''}" onclick="setBrandFilter('${b}')">${b}</button>
  `).join('');
}

function setBrandFilter(brand) {
  currentBrandFilter = brand;
  renderBrandFilters();
  renderAllPhonesGrid();
}

// ─── FAVORITES ────────────────────────────────────────────────────────────────
function toggleFavorite(e, id) {
  e.stopPropagation(); // Prevent opening modal
  const idx = favorites.indexOf(id);
  if (idx > -1) {
    favorites.splice(idx, 1);
  } else {
    favorites.push(id);
  }
  localStorage.setItem('phonePerfectFavs', JSON.stringify(favorites));
  updateFavoritesCount();
  renderAllPhonesGrid(); // re-render hearts
}

function updateFavoritesCount() {
  const badge = document.getElementById('fav-count');
  if (badge) badge.textContent = favorites.length;
}

function toggleFavoritesView() {
  showFavoritesOnly = !showFavoritesOnly;
  const btn = document.getElementById('nav-favorites-bottom');
  const textSpan = document.getElementById('bottom-fav-text');
  if (btn && textSpan) {
    if (showFavoritesOnly) {
      btn.classList.add('active-fav');
      textSpan.innerHTML = `All (<span id="fav-count">${favorites.length}</span>)`;
    } else {
      btn.classList.remove('active-fav');
      textSpan.innerHTML = `Favs (<span id="fav-count">${favorites.length}</span>)`;
    }
  }
  
  const searchInput = document.getElementById('phone-search');
  if (searchInput) {
    searchInput.style.display = showFavoritesOnly ? 'none' : 'block';
  }

  // Clear brand active
  document.querySelectorAll('.brand-chip').forEach(c => c.classList.remove('active'));
  const allBtn = document.querySelector('.brand-chip[onclick*="\'all\'"]');
  if (allBtn) allBtn.classList.add('active');
  activeBrand = 'all';

  renderAllPhonesGrid();
}


// ─── COMPARE MODE ─────────────────────────────────────────────────────────────
function toggleCompare(e, id) {
  e.stopPropagation();
  const idx = compareList.indexOf(id);
  if (idx > -1) {
    compareList.splice(idx, 1);
  } else {
    if (compareList.length >= 3) {
      alert("You can only compare up to 3 phones at once.");
      return;
    }
    compareList.push(id);
  }
  
  updateCompareBar();
  renderAllPhonesGrid(); // update checkboxes
}

function updateCompareBar() {
  const bar = document.getElementById('compare-bar');
  const count = document.getElementById('compare-count');
  if (!bar || !count) return;
  count.textContent = compareList.length;
  if (compareList.length > 0) {
    bar.classList.add('show');
  } else {
    bar.classList.remove('show');
  }
}

function clearCompare() {
  compareList = [];
  updateCompareBar();
  renderAllPhonesGrid();
}

function openCompareModal() {
  if (compareList.length === 0) return;
  const phonesToCompare = compareList.map(id => PHONES.find(p => p.id === id));
  
  const content = document.getElementById('compare-content');
  
  content.innerHTML = `
    <h2 class="compare-title">Compare Phones</h2>
    <div class="compare-grid" style="grid-template-columns: repeat(${phonesToCompare.length}, 1fr)">
      ${phonesToCompare.map(p => `
        <div class="compare-col-header">
          <div class="compare-emoji">${p.emoji}</div>
          <div class="compare-name">${p.name}</div>
          <div class="compare-brand">${p.brand}</div>
          <div class="compare-price">${p.price}</div>
        </div>
      `).join('')}
    </div>
    
    <div class="radar-chart-wrap" style="margin: 32px 0;">
      <canvas class="radar-canvas" id="compare-radar-canvas" width="400" height="400"></canvas>
    </div>
    
    <div class="compare-specs-table">
      ${Object.keys(phonesToCompare[0].specs).map(specKey => `
        <div class="compare-spec-row">
          <div class="compare-spec-label">${formatSpecKey(specKey)}</div>
          <div class="compare-spec-values" style="grid-template-columns: repeat(${phonesToCompare.length}, 1fr)">
            ${phonesToCompare.map(p => `
              <div class="compare-spec-val">${p.specs[specKey]}</div>
            `).join('')}
          </div>
        </div>
      `).join('')}
      
      <!-- Added Numeric Comparisons -->
      <div class="compare-spec-row">
        <div class="compare-spec-label">RAM</div>
        <div class="compare-spec-values" style="grid-template-columns: repeat(${phonesToCompare.length}, 1fr)">
          ${phonesToCompare.map(p => `
            <div class="compare-spec-val ${p.ram_gb === Math.max(...phonesToCompare.map(x=>x.ram_gb||0)) ? 'compare-winner' : ''}">${p.ram_gb || '?'} GB</div>
          `).join('')}
        </div>
      </div>
      <div class="compare-spec-row">
        <div class="compare-spec-label">Screen Size</div>
        <div class="compare-spec-values" style="grid-template-columns: repeat(${phonesToCompare.length}, 1fr)">
          ${phonesToCompare.map(p => `
            <div class="compare-spec-val ${p.screen_size === Math.max(...phonesToCompare.map(x=>x.screen_size||0)) ? 'compare-winner' : ''}">${p.screen_size || '?'} inches</div>
          `).join('')}
        </div>
      </div>
      <div class="compare-spec-row">
        <div class="compare-spec-label">Price</div>
        <div class="compare-spec-values" style="grid-template-columns: repeat(${phonesToCompare.length}, 1fr)">
          ${phonesToCompare.map(p => `
            <div class="compare-spec-val ${p.price_numeric === Math.min(...phonesToCompare.map(x=>x.price_numeric||9999999)) ? 'compare-winner' : ''}">₹${p.price_numeric ? p.price_numeric.toLocaleString() : '?'}</div>
          `).join('')}
        </div>
      </div>
    </div>
  `;
  
  document.getElementById('compare-modal-overlay').classList.add('open');
  document.body.style.overflow = 'hidden';
  
  // Draw radar with multiple phones
  setTimeout(() => drawCompareRadarChart(phonesToCompare), 100);
}

function closeCompareModal(e) {
  if (e && e.target !== document.getElementById('compare-modal-overlay')) return;
  document.getElementById('compare-modal-overlay').classList.remove('open');
  document.body.style.overflow = '';
}


// ─── ALL PHONES GRID ─────────────────────────────────────────────────────────
function renderAllPhonesGrid() {
  const grid = document.getElementById('phones-grid');
  let phones = [...PHONES];

  // Apply Favorites Filter
  if (showFavoritesOnly) {
    phones = phones.filter(p => favorites.includes(p.id));
  }

  // Apply Brand Filter
  if (currentBrandFilter !== 'All') {
    phones = phones.filter(p => p.brand === currentBrandFilter);
  }

  // Apply Advanced Filters
  if (advFilters.ram !== 'any') {
    phones = phones.filter(p => p.ram_gb >= parseInt(advFilters.ram));
  }
  if (advFilters.processor !== 'any') {
    phones = phones.filter(p => p.processor_brand === advFilters.processor);
  }
  if (advFilters.has5g) phones = phones.filter(p => p.has_5g);
  if (advFilters.hasNfc) phones = phones.filter(p => p.has_nfc);
  if (advFilters.hasWireless) phones = phones.filter(p => p.has_wireless_charging);

  if (currentSearch) {
    const q = currentSearch.toLowerCase();
    phones = phones.filter(p =>
      p.name.toLowerCase().includes(q) ||
      p.brand.toLowerCase().includes(q) ||
      (p.uniqueFeature && p.uniqueFeature.toLowerCase().includes(q))
    );
  }

  if (currentSort === 'overall') {
    phones.sort((a, b) => getOverallScore(b) - getOverallScore(a));
  } else {
    phones.sort((a, b) => b.scores[currentSort] - a.scores[currentSort]);
  }

  allPhonesSorted = phones;

  if (phones.length === 0) {
    grid.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding: 40px; color: var(--text-3);">No phones match your filters.</div>`;
    return;
  }

  grid.innerHTML = phones.map(p => {
    const overall = getOverallScore(p);
    const s = p.scores;
    const ipLabel = p.specs.ip.split('–')[0].split(' ').slice(0,2).join(' ').trim();
    const mah = getBatteryMah(p);
    const uniqueShort = p.uniqueFeature.split('+')[0].trim();
    
    const isFav = favorites.includes(p.id);
    const isComp = compareList.includes(p.id);
    
    return `
      <div class="phone-card" onclick="openModal('${p.id}')">
        <!-- Actions row (Fav + Compare) -->
        <div class="phone-actions">
          <button class="compare-check ${isComp ? 'checked' : ''}" onclick="toggleCompare(event, '${p.id}')">
            ${isComp ? '✓ Added' : '+ Compare'}
          </button>
          <button class="fav-btn ${isFav ? 'active' : ''}" onclick="toggleFavorite(event, '${p.id}')">
            ${isFav ? '❤️' : '🤍'}
          </button>
        </div>
        
        <div class="phone-card-ip">${ipLabel}</div>
        <div class="phone-card-brand">${p.brand}</div>
        <div class="phone-card-name">${p.emoji} ${p.name}</div>
        <div class="phone-card-price">${p.price}</div>
        <div class="phone-card-battery-row">
          <span class="battery-mah-badge">🔋 ${mah} mAh</span>
        </div>
        <div class="phone-card-unique">⭐ ${uniqueShort}</div>
        <div class="phone-card-scores">
          <div class="score-chip">
            <span class="score-chip-val ${scoreColor(s.camera)}">${s.camera}</span>
            <span class="score-chip-label">📸</span>
          </div>
          <div class="score-chip">
            <span class="score-chip-val ${scoreColor(s.battery)}">${s.battery}</span>
            <span class="score-chip-label">🔋</span>
          </div>
          <div class="score-chip">
            <span class="score-chip-val ${scoreColor(s.display)}">${s.display}</span>
            <span class="score-chip-label">🖥️</span>
          </div>
          <div class="score-chip">
            <span class="score-chip-val ${scoreColor(s.durability)}">${s.durability}</span>
            <span class="score-chip-label">🛡️</span>
          </div>
        </div>
        <div class="phone-card-overall">
          <span class="overall-label">Overall Score</span>
          <span class="overall-score">${overall}</span>
        </div>
      </div>
    `;
  }).join('');
}

function getOverallScore(phone) {
  const sum = CRITERIA.reduce((acc, c) => acc + (phone.scores[c.key] || 0), 0);
  return +(sum / CRITERIA.length).toFixed(1);
}

function scoreColor(val) {
  if (val >= 9) return 'score-high';
  if (val >= 7) return 'score-mid';
  return 'score-low';
}

function updateCarouselDots(container) {
  const scrollPos = container.scrollLeft;
  const itemWidth = container.clientWidth;
  const activeIndex = Math.round(scrollPos / itemWidth);
  const dots = container.nextElementSibling.querySelectorAll('.carousel-dot');
  dots.forEach((dot, i) => dot.classList.toggle('active', i === activeIndex));
}

function filterPhones(query) {
  currentSearch = query;
  renderAllPhonesGrid();
}

function sortPhones(key, btn) {
  currentSort = key;
  document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderAllPhonesGrid();
}

// ─── MODAL ────────────────────────────────────────────────────────────────────
function openModal(phoneId) {
  const phone = PHONES.find(p => p.id === phoneId);
  if (!phone) return;

  const overall = getOverallScore(phone);
  const s = phone.scores;
  const mah = getBatteryMah(phone);
  const ipShort = getIPShort(phone);
  const chargingShort = getChargingShort(phone);

  const basePriceNum = getPhonePrice(phone);
  const livePriceNum = typeof getLivePrice === 'function' ? getLivePrice(phone) : basePriceNum;
  const priceDiff = livePriceNum - basePriceNum;
  let priceIndicator = '';
  if (priceDiff > 0) priceIndicator = `<span style="color:#ef4444;font-size:0.8rem;margin-left:8px;">↑ ₹${priceDiff.toLocaleString('en-IN')} (Live)</span>`;
  else if (priceDiff < 0) priceIndicator = `<span style="color:#10b981;font-size:0.8rem;margin-left:8px;">↓ ₹${Math.abs(priceDiff).toLocaleString('en-IN')} (Live)</span>`;
  else priceIndicator = `<span style="color:#8b5cf6;font-size:0.8rem;margin-left:8px;">(Live)</span>`;

  const displayPrice = `₹${livePriceNum.toLocaleString('en-IN')}`;

  document.getElementById('modal-content').innerHTML = `
    <div class="modal-phone-header">
      <div class="modal-phone-emoji">${phone.emoji}</div>
      <div class="modal-phone-meta">
        <div class="modal-phone-brand">${phone.brand}</div>
        <div class="modal-phone-name">${phone.name}</div>
        <div class="modal-phone-price" style="display:flex;align-items:center;">${displayPrice} ${priceIndicator}</div>
        <div class="modal-phone-ip">${ipShort}</div>
      </div>
      </div>
      <div class="modal-actions" style="display: flex; flex-direction: column; align-items: flex-end; gap: 8px;">
        <div class="modal-overall-score">
          <span class="modal-score-num">${overall}</span>
          <span class="modal-score-label">/ 10</span>
        </div>
        <button class="compare-btn-primary" style="padding: 6px 12px; font-size: 0.8rem; background: #25D366; color: white; border: none; cursor: pointer; display: flex; align-items: center;" onclick="shareToWhatsApp('${phone.id}')">
          <svg style="width:14px; height:14px; margin-right: 6px;" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"/></svg> Share
        </button>
      </div>
    </div>

    ${phone.images && phone.images.length > 0 ? `
    <div class="modal-carousel-container">
      <div class="modal-carousel" onscroll="updateCarouselDots(this)">
        ${phone.images.map(img => `
          <img src="${img}" class="carousel-img" loading="lazy" />
        `).join('')}
      </div>
      <div class="carousel-dots">
        ${phone.images.map((_, i) => `<div class="carousel-dot ${i===0?'active':''}"></div>`).join('')}
      </div>
    </div>
    ` : ''}

    <div class="modal-unique-feature">
      <span class="unique-feature-icon">⭐</span>
      <div>
        <div class="unique-feature-title">What Makes It Special</div>
        <div class="unique-feature-text">${phone.uniqueFeature}</div>
      </div>
    </div>

    <div class="modal-battery-highlight">
      <div class="battery-highlight-item">
        <span class="battery-highlight-icon">🔋</span>
        <div>
          <div class="battery-highlight-val">${mah} mAh</div>
          <div class="battery-highlight-label">Battery Capacity</div>
        </div>
      </div>
      <div class="battery-highlight-item">
        <span class="battery-highlight-icon">⚡</span>
        <div>
          <div class="battery-highlight-val">${chargingShort}</div>
          <div class="battery-highlight-label">Max Charging</div>
        </div>
      </div>
      <div class="battery-highlight-item">
        <span class="battery-highlight-icon">💧</span>
        <div>
          <div class="battery-highlight-val">${ipShort}</div>
          <div class="battery-highlight-label">Water Resistance</div>
        </div>
      </div>
    </div>

    <!-- PROS AND CONS -->
    <div class="pros-cons-container" style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
      <div class="pros-card" style="background: rgba(16,185,129,0.05); border: 1px solid rgba(16,185,129,0.2); padding: 16px; border-radius: 12px;">
        <h4 style="color: #10b981; margin: 0 0 12px 0; font-size: 1rem;">✅ Pros</h4>
        <ul style="margin: 0; padding-left: 20px; color: var(--text-2); font-size: 0.9rem; line-height: 1.6;">
          ${phone.pros ? phone.pros.map(p => `<li>${p}</li>`).join('') : '<li>Great overall performance</li><li>Good battery life</li><li>Solid build quality</li>'}
        </ul>
      </div>
      <div class="cons-card" style="background: rgba(239,68,68,0.05); border: 1px solid rgba(239,68,68,0.2); padding: 16px; border-radius: 12px;">
        <h4 style="color: #ef4444; margin: 0 0 12px 0; font-size: 1rem;">⚠️ Cons</h4>
        <ul style="margin: 0; padding-left: 20px; color: var(--text-2); font-size: 0.9rem; line-height: 1.6;">
          ${phone.cons ? phone.cons.map(c => `<li>${c}</li>`).join('') : '<li>Premium price tag</li><li>Average low-light camera</li>'}
        </ul>
      </div>
    </div>

    <!-- PRICE TRACKER -->
    <div class="price-tracker-container" style="background: var(--bg-main); border: 1px solid var(--border); padding: 16px; border-radius: 12px; margin-bottom: 24px;">
      <h4 style="margin: 0 0 12px 0; font-size: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
        <span>📉 30-Day Price Trend</span>
        <div style="display: flex; gap: 8px;">
          <a href="https://www.amazon.in/s?k=${encodeURIComponent(phone.brand + ' ' + phone.name)}" target="_blank" class="compare-btn-outline" style="padding: 4px 12px; font-size: 0.8rem; text-decoration: none; display: inline-flex; align-items: center; color: #ff9900; border-color: #ff9900;">🛒 Amazon Search</a>
          <button class="compare-btn-outline" style="padding: 4px 12px; font-size: 0.8rem;" onclick="togglePriceAlert('${phone.id}')" id="alert-btn-${phone.id}">🔔 Set Alert</button>
        </div>
      </h4>
      <canvas id="priceChart-${phone.id}" width="400" height="100" style="width: 100%; height: 100px; display: block;"></canvas>
    </div>

    <div class="modal-radar-section">
      <div class="modal-radar-title">📊 Performance Radar</div>
      <div class="radar-chart-wrap">
        <canvas class="radar-canvas" id="radar-canvas" width="300" height="300"></canvas>
      </div>
    </div>

    <div class="modal-criteria">
      ${CRITERIA.map(c => `
        <div class="criteria-row">
          <div class="criteria-row-header">
            <span class="criteria-row-name">${c.icon} ${c.label}</span>
            <span class="criteria-row-score">${s[c.key]}/10</span>
          </div>
          <div class="criteria-bar-track">
            <div class="criteria-bar-fill" style="width: ${s[c.key] * 10}%"></div>
          </div>
        </div>
      `).join('')}
    </div>

    <div class="modal-specs-title">🔧 Full Specifications</div>
    <div class="modal-specs-grid">
      ${Object.entries(phone.specs).map(([k, v]) => `
        <div class="spec-item">
          <div class="spec-key">${formatSpecKey(k)}</div>
          <div class="spec-val">${v}</div>
        </div>
      `).join('')}
    </div>
    
    ${renderRatingUI(phone.id)}
  `;

  document.getElementById('modal-overlay').classList.add('open');
  document.body.style.overflow = 'hidden';

  // Render Price Chart
  setTimeout(() => {
    if (typeof getPriceHistory === 'function' && typeof renderSparkline === 'function') {
      const history = getPriceHistory(phone, 30);
      const canvas = document.getElementById(`priceChart-${phone.id}`);
      if (canvas) renderSparkline(canvas, history, '#10b981');
    }
    if (typeof updateAlertBtnState === 'function') {
      updateAlertBtnState(phone.id);
    }
  }, 200);
  setTimeout(() => drawRadarChart(phone), 50);
}

function closeModal(e) {
  if (e && e.target !== document.getElementById('modal-overlay')) return;
  document.getElementById('modal-overlay').classList.remove('open');
  document.body.style.overflow = '';
}

function shareToWhatsApp(phoneId) {
  const phone = PHONES.find(p => p.id === phoneId);
  if (!phone) return;
  const overall = getOverallScore(phone);
  let text = `Check out the ${phone.brand} ${phone.name} on PhonePerfect!\n\n`;
  text += `⭐ Rating: ${overall}/10\n`;
  text += `💰 Price: ${phone.price}\n\n`;
  if (phone.pros && phone.pros.length > 0) {
    text += `✅ Pros: ${phone.pros.join(', ')}\n`;
  }
  text += `\nFind it here: ${window.location.href.split('#')[0]}`;
  const encodedText = encodeURIComponent(text);
  window.open(`https://wa.me/?text=${encodedText}`, '_blank');
}

function formatSpecKey(key) {
  const map = {
    display: 'Display',
    processor: 'Processor',
    ram: 'RAM',
    battery: 'Battery',
    charging: 'Charging',
    camera: 'Camera',
    sound: 'Sound',
    ip: 'IP Rating',
    weight: 'Weight',
    build: 'Build'
  };
  return map[key] || key;
}

// ─── RADAR CHART (Canvas) ─────────────────────────────────────────────────────
function drawRadarChart(phone) {
  const canvas = document.getElementById('radar-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width;
  const H = canvas.height;
  const cx = W / 2;
  const cy = H / 2;
  const R = Math.min(W, H) / 2 - 40;

  ctx.clearRect(0, 0, W, H);

  const n = CRITERIA.length;
  const angles = CRITERIA.map((_, i) => (i / n) * Math.PI * 2 - Math.PI / 2);

  // Grid rings
  for (let level = 1; level <= 5; level++) {
    const r = (level / 5) * R;
    ctx.beginPath();
    angles.forEach((a, i) => {
      const x = cx + Math.cos(a) * r;
      const y = cy + Math.sin(a) * r;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.closePath();
    ctx.strokeStyle = 'rgba(255,255,255,0.07)';
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  // Axes
  angles.forEach(a => {
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + Math.cos(a) * R, cy + Math.sin(a) * R);
    ctx.strokeStyle = 'rgba(255,255,255,0.1)';
    ctx.lineWidth = 1;
    ctx.stroke();
  });

  // Data polygon
  ctx.beginPath();
  CRITERIA.forEach((c, i) => {
    const val = phone.scores[c.key] / 10;
    const r = val * R;
    const x = cx + Math.cos(angles[i]) * r;
    const y = cy + Math.sin(angles[i]) * r;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.closePath();
  const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, R);
  grad.addColorStop(0, 'rgba(139,92,246,0.5)');
  grad.addColorStop(1, 'rgba(6,182,212,0.2)');
  ctx.fillStyle = grad;
  ctx.fill();
  ctx.strokeStyle = '#8b5cf6';
  ctx.lineWidth = 2;
  ctx.stroke();

  // Dots
  CRITERIA.forEach((c, i) => {
    const val = phone.scores[c.key] / 10;
    const r = val * R;
    const x = cx + Math.cos(angles[i]) * r;
    const y = cy + Math.sin(angles[i]) * r;
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fillStyle = '#a78bfa';
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 1.5;
    ctx.stroke();
  });

  // Labels
  ctx.font = '600 11px Outfit, sans-serif';
  ctx.fillStyle = 'rgba(255,255,255,0.7)';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  CRITERIA.forEach((c, i) => {
    const labelR = R + 24;
    const x = cx + Math.cos(angles[i]) * labelR;
    const y = cy + Math.sin(angles[i]) * labelR;
    ctx.fillText(c.icon + ' ' + c.label.split(' ')[0], x, y);
  });
}

// ─── COMPARE RADAR CHART ─────────────────────────────────────────────────────
const COMPARE_COLORS = [
  { fill: 'rgba(139,92,246,0.3)', stroke: '#8b5cf6', dot: '#a78bfa' }, // Purple
  { fill: 'rgba(6,182,212,0.3)', stroke: '#06b6d4', dot: '#67e8f9' },  // Cyan
  { fill: 'rgba(245,158,11,0.3)', stroke: '#f59e0b', dot: '#fcd34d' }  // Amber
];

function drawCompareRadarChart(phones) {
  const canvas = document.getElementById('compare-radar-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width;
  const H = canvas.height;
  const cx = W / 2;
  const cy = H / 2;
  const R = Math.min(W, H) / 2 - 50;

  ctx.clearRect(0, 0, W, H);

  const n = CRITERIA.length;
  const angles = CRITERIA.map((_, i) => (i / n) * Math.PI * 2 - Math.PI / 2);

  // Grid rings
  for (let level = 1; level <= 5; level++) {
    const r = (level / 5) * R;
    ctx.beginPath();
    angles.forEach((a, i) => {
      const x = cx + Math.cos(a) * r;
      const y = cy + Math.sin(a) * r;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.closePath();
    ctx.strokeStyle = 'rgba(255,255,255,0.07)';
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  // Axes
  angles.forEach(a => {
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + Math.cos(a) * R, cy + Math.sin(a) * R);
    ctx.strokeStyle = 'rgba(255,255,255,0.1)';
    ctx.lineWidth = 1;
    ctx.stroke();
  });

  // Data polygons for each phone
  phones.forEach((phone, pIdx) => {
    const colors = COMPARE_COLORS[pIdx % COMPARE_COLORS.length];
    
    ctx.beginPath();
    CRITERIA.forEach((c, i) => {
      const val = phone.scores[c.key] / 10;
      const r = val * R;
      const x = cx + Math.cos(angles[i]) * r;
      const y = cy + Math.sin(angles[i]) * r;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.closePath();
    ctx.fillStyle = colors.fill;
    ctx.fill();
    ctx.strokeStyle = colors.stroke;
    ctx.lineWidth = 2;
    ctx.stroke();

    // Dots
    CRITERIA.forEach((c, i) => {
      const val = phone.scores[c.key] / 10;
      const r = val * R;
      const x = cx + Math.cos(angles[i]) * r;
      const y = cy + Math.sin(angles[i]) * r;
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fillStyle = colors.dot;
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    });
  });

  // Labels
  ctx.font = '600 12px Outfit, sans-serif';
  ctx.fillStyle = 'rgba(255,255,255,0.8)';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  CRITERIA.forEach((c, i) => {
    const labelR = R + 25;
    const x = cx + Math.cos(angles[i]) * labelR;
    const y = cy + Math.sin(angles[i]) * labelR;
    ctx.fillText(c.icon + ' ' + c.label.split(' ')[0], x, y);
  });
}

// ─── KEYBOARD ESCAPE FOR MODAL ────────────────────────────────────────────────
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    closeModal(null);
    closeCompareModal(null);
  }
});

// ─── SMOOTH ANCHOR LINKS ─────────────────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(a.getAttribute('href'));
    if (target) target.scrollIntoView({ behavior: 'smooth' });
  });
});

// ─── THEME TOGGLE ────────────────────────────────────────────────────────────
function toggleTheme() {
  const themes = ['dark', 'light', 'amoled'];
  const icons = { 'dark': '🌙', 'light': '☀️', 'amoled': '⚫' };
  
  let idx = themes.indexOf(currentTheme);
  idx = (idx + 1) % themes.length;
  currentTheme = themes[idx];
  
  if (currentTheme === 'dark') {
    document.documentElement.removeAttribute('data-theme');
  } else {
    document.documentElement.setAttribute('data-theme', currentTheme);
  }
  
  const btn = document.getElementById('theme-toggle');
  if (btn) btn.textContent = icons[currentTheme];
}

// ─── UPGRADE ADVISOR ──────────────────────────────────────────────────────────
function populateUpgradeSelect() {
  const select = document.getElementById('current-phone-select');
  if (!select) return;
  PHONES.forEach(p => {
    const opt = document.createElement('option');
    opt.value = p.id;
    opt.textContent = `${p.brand} ${p.name}`;
    select.appendChild(opt);
  });
}

function generateUpgradeReportUI() {
  const select = document.getElementById('current-phone-select');
  const resultsDiv = document.getElementById('upgrade-results');
  if (!select || !resultsDiv || !select.value) return;
  
  const currentPhone = PHONES.find(p => p.id === select.value);
  if (!currentPhone) return;
  
  const currentAvg = CRITERIA.reduce((a, c) => a + (currentPhone.scores[c.key] || 0), 0) / CRITERIA.length;
  
  const upgrades = PHONES.filter(p => {
    const avg = CRITERIA.reduce((a, c) => a + (p.scores[c.key] || 0), 0) / CRITERIA.length;
    return avg > currentAvg && p.id !== currentPhone.id;
  }).sort((a, b) => {
    const sa = CRITERIA.reduce((acc, c) => acc + (a.scores[c.key] || 0), 0) / CRITERIA.length;
    const sb = CRITERIA.reduce((acc, c) => acc + (b.scores[c.key] || 0), 0) / CRITERIA.length;
    return sb - sa;
  }).slice(0, 3);
  
  resultsDiv.style.display = 'grid';
  resultsDiv.innerHTML = '';
  
  if (upgrades.length === 0) {
    resultsDiv.innerHTML = `<div style="text-align:center; padding: 20px;">You already have one of the best phones! No significant upgrades found. 🎉</div>`;
    return;
  }
  
  upgrades.forEach((p, i) => {
    const avg = CRITERIA.reduce((a, c) => a + (p.scores[c.key] || 0), 0) / CRITERIA.length;
    const gains = [];
    const losses = [];
    CRITERIA.forEach(c => {
      const diff = (p.scores[c.key] || 0) - (currentPhone.scores[c.key] || 0);
      if (diff >= 1) gains.push(`+${diff.toFixed(1)} ${c.label.split(' ')[0]}`);
      if (diff <= -1) losses.push(`${diff.toFixed(1)} ${c.label.split(' ')[0]}`);
    });
    
    const gainStr = gains.length > 0 ? `✅ Gains: ${gains.join(', ')}` : '✅ Minor overall improvements';
    const lossStr = losses.length > 0 ? `⚠️ Trade-offs: ${losses.join(', ')}` : '';
    
    resultsDiv.innerHTML += `
      <div class="upgrade-result-card" onclick="openModal('${p.id}')" style="cursor:pointer">
        <div class="upgrade-result-details">
          <h4>${['🥇','🥈','🥉'][i]} ${p.brand} ${p.name}</h4>
          <div class="upgrade-gains">${gainStr}</div>
          <div class="upgrade-losses">${lossStr}</div>
        </div>
        <div>
          <button class="cta-btn"><span>View Specs</span></button>
        </div>
      </div>
    `;
  });
}

// ─── ADVANCED FILTERS ─────────────────────────────────────────────────────────
function toggleFilterPanel() {
  const body = document.getElementById('filter-body');
  const chevron = document.getElementById('filter-chevron');
  if (body.style.display === 'none') {
    body.style.display = 'block';
    chevron.textContent = '▲';
  } else {
    body.style.display = 'none';
    chevron.textContent = '▼';
  }
}

function applyAdvancedFilters() {
  advFilters.ram = document.getElementById('filter-ram').value;
  advFilters.processor = document.getElementById('filter-processor').value;
  advFilters.has5g = document.getElementById('filter-5g').checked;
  advFilters.hasNfc = document.getElementById('filter-nfc').checked;
  advFilters.hasWireless = document.getElementById('filter-wireless').checked;
  renderAllPhonesGrid();
}

function resetAdvancedFilters() {
  document.getElementById('filter-ram').value = 'any';
  document.getElementById('filter-processor').value = 'any';
  document.getElementById('filter-5g').checked = false;
  document.getElementById('filter-nfc').checked = false;
  document.getElementById('filter-wireless').checked = false;
  applyAdvancedFilters();
}

// ─── EXPORT & ANIMATIONS ──────────────────────────────────────────────────────
function exportResults() {
  const target = document.getElementById('exportable-results');
  if (!target) return;
  
  // Temporarily tweak styles for a cleaner image
  target.style.background = currentTheme === 'dark' ? '#0f1422' : (currentTheme === 'light' ? '#ffffff' : '#000000');
  target.style.padding = '30px';
  target.style.borderRadius = '20px';
  
  html2canvas(target, {
    backgroundColor: currentTheme === 'dark' ? '#0f1422' : (currentTheme === 'light' ? '#ffffff' : '#000000'),
    scale: 2
  }).then(canvas => {
    // Revert temporary styles
    target.style.background = '';
    target.style.padding = '';
    target.style.borderRadius = '';
    
    // Trigger download
    const link = document.createElement('a');
    link.download = 'PhonePerfect-Recommendations.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
    
    showToast('Image saved! Ready to share.');
  });
}

// Add a global toast UI since we referenced it earlier
function showToast(message) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.className = 'toast-notification';
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}

// Modify generateRecommendations to include confetti!
const originalGenerateRecommendations = generateRecommendations;
generateRecommendations = function() {
  originalGenerateRecommendations();
  // Wait for rendering to complete before confetti
  setTimeout(() => {
    if (typeof confetti === 'function') {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#8b5cf6', '#d946ef', '#10b981']
      });
    }
  }, 950);
};


// Voice Search Implementation
function startVoiceSearch() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert('Voice search is not supported in this browser.');
    return;
  }
  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.lang = 'en-US'; // We will change this for regional languages later
  recognition.interimResults = false;

  const btn = document.getElementById('voice-search-btn');
  const originalIcon = btn.innerText;
  btn.innerText = '??';

  recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    const searchInput = document.getElementById('phone-search');
    searchInput.value = transcript;
    filterPhones(transcript);
    btn.innerText = originalIcon;
  };

  recognition.onerror = function(event) {
    console.error('Speech recognition error', event.error);
    btn.innerText = originalIcon;
  };

  recognition.onend = function() {
    btn.innerText = originalIcon;
  };

  recognition.start();
}

// Language Support
const translations = {
  en: { find: 'Find', phones: 'Phones', recommend: 'Get Recommendations', searchPlaceholder: '?? Search phone name...' },
  hi: { find: '?????', phones: '????', recommend: '????????? ??????? ????', searchPlaceholder: '?? ???? ?? ??? ?????...' },
  ta: { find: '????', phones: '???????', recommend: '?????????????? ?????????', searchPlaceholder: '?? ???? ????? ???...' },
  te: { find: '???????', phones: '??????', recommend: '??????????? ???????', searchPlaceholder: '?? ???? ???? ???????...' }
};

function changeLanguage(lang) {
  const t = translations[lang] || translations.en;
  document.querySelector('a[href="#finder"] .bottom-nav-text').innerText = t.find;
  document.querySelector('a[href="#phones-list"] .bottom-nav-text').innerText = t.phones;
  const recBtn = document.querySelector('#recommend-btn span');
  if(recBtn) recBtn.innerText = t.recommend;
  const searchInput = document.getElementById('phone-search');
  if(searchInput) searchInput.placeholder = t.searchPlaceholder;
}


// User Ratings System
function renderRatingUI(phoneId) {
  const savedRating = localStorage.getItem('rating_' + phoneId) || 0;
  let starsHtml = '';
  for (let i = 1; i <= 5; i++) {
    starsHtml += `<span style='cursor:pointer; font-size:1.5rem; color:${i <= savedRating ? '#f59e0b' : 'var(--border)'};' onclick='saveRating("${phoneId}", ${i})'>★</span>`;
  }
  return `<div style='margin-top: 20px; text-align: center; background: var(--bg-card); padding: 16px; border-radius: 12px; border: 1px solid var(--border);'>
    <div style='font-size: 0.9rem; color: var(--text-2); margin-bottom: 8px;'>Your Rating</div>
    <div id='rating-stars-${phoneId}'>${starsHtml}</div>
  </div>`;
}

function saveRating(phoneId, rating) {
  localStorage.setItem('rating_' + phoneId, rating);
  const starsDiv = document.getElementById('rating-stars-' + phoneId);
  if(starsDiv) {
    let starsHtml = '';
    for (let i = 1; i <= 5; i++) {
      starsHtml += `<span style='cursor:pointer; font-size:1.5rem; color:${i <= rating ? '#f59e0b' : 'var(--border)'};' onclick='saveRating("${phoneId}", ${i})'>★</span>`;
    }
    starsDiv.innerHTML = starsHtml;
  }
}

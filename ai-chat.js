/**
 * PhonePerfect 2.0 – AI Chat Assistant
 * Local NLP engine for natural language phone queries
 */

// ─── CHAT STATE ──────────────────────────────────────────────────────────────
let chatHistory = [];
let chatOpen = false;

// ─── INTENT DETECTION ────────────────────────────────────────────────────────
const INTENTS = {
  COMPARE: ['compare', 'vs', 'versus', 'between', 'difference'],
  BEST: ['best', 'top', 'recommend', 'suggest', 'which', 'ideal', 'perfect'],
  CHEAPEST: ['cheapest', 'affordable', 'budget', 'lowest price', 'cheap'],
  EXPENSIVE: ['expensive', 'premium', 'flagship', 'high-end', 'costly'],
  SPECS: ['specs', 'specification', 'details', 'features', 'info', 'about'],
  LIST: ['list', 'show', 'all', 'every', 'give me'],
  BATTERY: ['battery', 'mah', 'charge', 'charging', 'endurance', 'backup'],
  CAMERA: ['camera', 'photo', 'megapixel', 'mp', 'photography', 'video', 'zoom'],
  GAMING: ['gaming', 'game', 'processor', 'performance', 'fps', 'snapdragon', 'chipset'],
  DISPLAY: ['display', 'screen', 'amoled', 'oled', 'refresh', 'hz', 'bright'],
  DURABILITY: ['durable', 'rugged', 'drop', 'water', 'ip68', 'tough', 'build'],
  UPGRADE: ['upgrade', 'replace', 'switch', 'move from', 'currently using']
};

const PRICE_KEYWORDS = {
  'under 10k': [0, 10000], 'below 10k': [0, 10000], 'under 10000': [0, 10000],
  'under 15k': [0, 15000], 'below 15k': [0, 15000], 'under 15000': [0, 15000],
  'under 20k': [0, 20000], 'below 20k': [0, 20000], 'under 20000': [0, 20000],
  'under 25k': [0, 25000], 'below 25k': [0, 25000], 'under 25000': [0, 25000],
  'under 30k': [0, 30000], 'below 30k': [0, 30000], 'under 30000': [0, 30000],
  'under 35k': [0, 35000], 'below 35k': [0, 35000], 'under 35000': [0, 35000],
  'under 40k': [0, 40000], 'below 40k': [0, 40000], 'under 40000': [0, 40000],
  'under 50k': [0, 50000], 'below 50k': [0, 50000], 'under 50000': [0, 50000],
  'under 60k': [0, 60000], 'under 70k': [0, 70000], 'under 80k': [0, 80000],
  'under 1 lakh': [0, 100000], 'under 100k': [0, 100000],
  '20k to 30k': [20000, 30000], '20-30k': [20000, 30000], '20000 to 30000': [20000, 30000],
  '30k to 50k': [30000, 50000], '30-50k': [30000, 50000],
  '50k to 70k': [50000, 70000], '50-70k': [50000, 70000],
  '70k to 1 lakh': [70000, 100000], '70-100k': [70000, 100000],
  'above 1 lakh': [100000, 999999], 'above 100k': [100000, 999999],
};

const BRAND_KEYWORDS = ['apple', 'iphone', 'samsung', 'galaxy', 'google', 'pixel', 'xiaomi', 'redmi', 'poco', 'oneplus', 'vivo', 'iqoo', 'oppo', 'motorola', 'moto', 'realme', 'nothing'];

function detectIntent(query) {
  const q = query.toLowerCase();
  const intents = [];
  
  for (const [intent, keywords] of Object.entries(INTENTS)) {
    if (keywords.some(kw => q.includes(kw))) {
      intents.push(intent);
    }
  }
  
  return intents.length > 0 ? intents : ['BEST']; // Default to BEST
}

function extractPriceRange(query) {
  const q = query.toLowerCase().replace(/,/g, '').replace(/₹/g, '');
  for (const [pattern, range] of Object.entries(PRICE_KEYWORDS)) {
    if (q.includes(pattern)) return range;
  }
  // Try to extract numbers
  const nums = q.match(/(\d+)\s*k/g);
  if (nums && nums.length >= 2) {
    const n1 = parseInt(nums[0]) * 1000;
    const n2 = parseInt(nums[1]) * 1000;
    return [Math.min(n1, n2), Math.max(n1, n2)];
  }
  if (nums && nums.length === 1) {
    const n = parseInt(nums[0]) * 1000;
    if (q.includes('under') || q.includes('below') || q.includes('within')) {
      return [0, n];
    }
    if (q.includes('above') || q.includes('over')) {
      return [n, 999999];
    }
  }
  return null;
}

function extractBrands(query) {
  const q = query.toLowerCase();
  const brands = [];
  const brandMap = {
    'apple': 'Apple', 'iphone': 'Apple',
    'samsung': 'Samsung', 'galaxy': 'Samsung',
    'google': 'Google', 'pixel': 'Google',
    'xiaomi': 'Xiaomi', 'redmi': 'Xiaomi', 'poco': 'Xiaomi',
    'oneplus': 'OnePlus', 'one plus': 'OnePlus',
    'vivo': 'Vivo', 'iqoo': 'Vivo',
    'oppo': 'Oppo',
    'motorola': 'Motorola', 'moto': 'Motorola'
  };
  for (const [kw, brand] of Object.entries(brandMap)) {
    if (q.includes(kw) && !brands.includes(brand)) brands.push(brand);
  }
  return brands;
}

function findPhoneByName(query) {
  const q = query.toLowerCase();
  return PHONES.filter(p => {
    const name = (p.brand + ' ' + p.name).toLowerCase();
    return q.includes(name.toLowerCase()) || name.includes(q);
  });
}

function getPhonePrice(phone) {
  if (phone.price_numeric) return phone.price_numeric;
  const m = phone.price.replace(/[₹,]/g, '').match(/\d+/);
  return m ? parseInt(m[0]) : 50000;
}

// ─── RESPONSE GENERATOR ─────────────────────────────────────────────────────
function generateResponse(query) {
  const intents = detectIntent(query);
  const priceRange = extractPriceRange(query);
  const brands = extractBrands(query);
  const q = query.toLowerCase();

  // Filter phones by price and brand
  let pool = [...PHONES];
  if (priceRange) {
    pool = pool.filter(p => {
      const price = getPhonePrice(p);
      return price >= priceRange[0] && price <= priceRange[1];
    });
  }
  if (brands.length > 0) {
    pool = pool.filter(p => brands.includes(p.brand));
  }

  // ── COMPARE ──
  if (intents.includes('COMPARE')) {
    // Try to find two phone names
    const allNames = PHONES.map(p => ({ phone: p, name: (p.brand + ' ' + p.name).toLowerCase() }));
    const found = [];
    for (const entry of allNames) {
      if (q.includes(entry.name) || q.includes(entry.phone.name.toLowerCase())) {
        found.push(entry.phone);
      }
    }
    if (found.length >= 2) {
      return generateCompareResponse(found[0], found[1]);
    }
    if (found.length === 1 && pool.length > 0) {
      const other = pool.find(p => p.id !== found[0].id);
      if (other) return generateCompareResponse(found[0], other);
    }
    return { text: "I'd love to compare phones for you! Please mention two specific phone names, like:\n\n*\"Compare iPhone 16 Pro vs Galaxy S24 Ultra\"*", type: 'info' };
  }

  // ── SPECS / INFO ──
  if (intents.includes('SPECS')) {
    const found = findPhoneByName(q);
    if (found.length > 0) {
      return generateSpecsResponse(found[0]);
    }
  }

  // ── UPGRADE ──
  if (intents.includes('UPGRADE')) {
    const found = findPhoneByName(q);
    if (found.length > 0) {
      return generateUpgradeResponse(found[0]);
    }
    return { text: "I can help you find an upgrade! Tell me which phone you currently use, like:\n\n*\"I'm using iPhone 13, should I upgrade?\"*", type: 'info' };
  }

  // ── CATEGORY QUERIES ──
  let sortKey = 'overall';
  let categoryLabel = '';
  
  if (intents.includes('CAMERA')) { sortKey = 'camera'; categoryLabel = '📸 Camera'; }
  else if (intents.includes('BATTERY')) { sortKey = 'battery'; categoryLabel = '🔋 Battery'; }
  else if (intents.includes('GAMING')) { sortKey = 'processor'; categoryLabel = '🎮 Gaming/Processor'; }
  else if (intents.includes('DISPLAY')) { sortKey = 'display'; categoryLabel = '🖥️ Display'; }
  else if (intents.includes('DURABILITY')) { sortKey = 'durability'; categoryLabel = '🛡️ Durability'; }

  if (sortKey !== 'overall') {
    pool.sort((a, b) => (b.scores[sortKey] || 0) - (a.scores[sortKey] || 0));
  } else {
    pool.sort((a, b) => {
      const sa = CRITERIA.reduce((acc, c) => acc + (a.scores[c.key] || 0), 0) / CRITERIA.length;
      const sb = CRITERIA.reduce((acc, c) => acc + (b.scores[c.key] || 0), 0) / CRITERIA.length;
      return sb - sa;
    });
  }

  // ── CHEAPEST ──
  if (intents.includes('CHEAPEST')) {
    pool.sort((a, b) => getPhonePrice(a) - getPhonePrice(b));
    categoryLabel = '💰 Most Affordable';
  }

  // ── EXPENSIVE ──
  if (intents.includes('EXPENSIVE')) {
    pool.sort((a, b) => getPhonePrice(b) - getPhonePrice(a));
    categoryLabel = '💎 Premium';
  }

  if (pool.length === 0) {
    return { text: "I couldn't find any phones matching your criteria. Try a different price range or brand!", type: 'warning' };
  }

  const top = pool.slice(0, 5);
  const priceLabel = priceRange ? ` (₹${(priceRange[0]/1000).toFixed(0)}K – ₹${(priceRange[1]/1000).toFixed(0)}K)` : '';
  const brandLabel = brands.length > 0 ? ` from ${brands.join(', ')}` : '';
  
  let title = categoryLabel ? `${categoryLabel} picks${brandLabel}${priceLabel}` : `Top picks${brandLabel}${priceLabel}`;
  
  let response = `**${title}**\n\n`;
  top.forEach((p, i) => {
    const score = sortKey !== 'overall' 
      ? `${sortKey}: ${p.scores[sortKey]}/10`
      : `Overall: ${(CRITERIA.reduce((acc, c) => acc + (p.scores[c.key] || 0), 0) / CRITERIA.length).toFixed(1)}/10`;
    response += `${['🥇','🥈','🥉','4️⃣','5️⃣'][i]} **${p.brand} ${p.name}** — ${p.price}\n   ${score} · ${p.uniqueFeature}\n\n`;
  });
  
  response += `\n_Tap any phone name in the Phones tab for full details!_`;
  
  return { text: response, type: 'success', phones: top };
}

function generateCompareResponse(p1, p2) {
  let text = `**⚔️ ${p1.brand} ${p1.name} vs ${p2.brand} ${p2.name}**\n\n`;
  text += `| Spec | ${p1.name} | ${p2.name} | Winner |\n`;
  text += `|------|----------|----------|--------|\n`;
  
  CRITERIA.forEach(c => {
    const s1 = p1.scores[c.key] || 0;
    const s2 = p2.scores[c.key] || 0;
    const winner = s1 > s2 ? `✅ ${p1.name}` : s2 > s1 ? `✅ ${p2.name}` : '🤝 Tie';
    text += `| ${c.icon} ${c.label} | ${s1}/10 | ${s2}/10 | ${winner} |\n`;
  });
  
  text += `\n**Price:** ${p1.price} vs ${p2.price}\n`;
  
  const avg1 = CRITERIA.reduce((a, c) => a + (p1.scores[c.key] || 0), 0) / CRITERIA.length;
  const avg2 = CRITERIA.reduce((a, c) => a + (p2.scores[c.key] || 0), 0) / CRITERIA.length;
  
  text += `\n**Overall:** ${p1.name} (${avg1.toFixed(1)}) vs ${p2.name} (${avg2.toFixed(1)})\n`;
  text += avg1 > avg2 
    ? `\n🏆 **${p1.brand} ${p1.name}** wins overall!`
    : avg2 > avg1 
      ? `\n🏆 **${p2.brand} ${p2.name}** wins overall!`
      : `\n🤝 It's a tie! Choose based on your priorities.`;
  
  return { text, type: 'compare' };
}

function generateSpecsResponse(phone) {
  let text = `**📋 ${phone.brand} ${phone.name}**\n\n`;
  text += `💰 Price: ${phone.price}\n`;
  text += `📱 Display: ${phone.specs.display}\n`;
  text += `⚙️ Processor: ${phone.specs.processor}\n`;
  text += `💾 RAM: ${phone.specs.ram}\n`;
  text += `🔋 Battery: ${phone.specs.battery}\n`;
  text += `⚡ Charging: ${phone.specs.charging}\n`;
  text += `📸 Camera: ${phone.specs.camera}\n`;
  text += `💧 IP Rating: ${phone.specs.ip}\n`;
  text += `⚖️ Weight: ${phone.specs.weight}\n`;
  text += `\n⭐ ${phone.uniqueFeature}`;
  
  return { text, type: 'specs' };
}

function generateUpgradeResponse(currentPhone) {
  // Find phones that score higher overall
  const currentAvg = CRITERIA.reduce((a, c) => a + (currentPhone.scores[c.key] || 0), 0) / CRITERIA.length;
  const upgrades = PHONES.filter(p => {
    const avg = CRITERIA.reduce((a, c) => a + (p.scores[c.key] || 0), 0) / CRITERIA.length;
    return avg > currentAvg && p.id !== currentPhone.id;
  }).sort((a, b) => {
    const sa = CRITERIA.reduce((acc, c) => acc + (a.scores[c.key] || 0), 0) / CRITERIA.length;
    const sb = CRITERIA.reduce((acc, c) => acc + (b.scores[c.key] || 0), 0) / CRITERIA.length;
    return sb - sa;
  }).slice(0, 3);
  
  if (upgrades.length === 0) {
    return { text: `**${currentPhone.brand} ${currentPhone.name}** is already one of the best phones in our database! No significant upgrades available. 🎉`, type: 'success' };
  }
  
  let text = `**📈 Upgrade from ${currentPhone.brand} ${currentPhone.name}**\n\n`;
  text += `Your current phone scores: **${currentAvg.toFixed(1)}/10** overall\n\n`;
  text += `**Top upgrade picks:**\n\n`;
  
  upgrades.forEach((p, i) => {
    const avg = CRITERIA.reduce((a, c) => a + (p.scores[c.key] || 0), 0) / CRITERIA.length;
    const gains = [];
    const losses = [];
    CRITERIA.forEach(c => {
      const diff = (p.scores[c.key] || 0) - (currentPhone.scores[c.key] || 0);
      if (diff >= 1) gains.push(`${c.icon} +${diff.toFixed(1)} ${c.label}`);
      if (diff <= -1) losses.push(`${c.icon} ${diff.toFixed(1)} ${c.label}`);
    });
    
    text += `${['🥇','🥈','🥉'][i]} **${p.brand} ${p.name}** — ${p.price} (${avg.toFixed(1)}/10)\n`;
    if (gains.length > 0) text += `   ✅ Gains: ${gains.join(', ')}\n`;
    if (losses.length > 0) text += `   ⚠️ Trade-offs: ${losses.join(', ')}\n`;
    text += '\n';
  });
  
  return { text, type: 'upgrade' };
}

// ─── CHAT UI ─────────────────────────────────────────────────────────────────
function toggleChat() {
  const panel = document.getElementById('chat-panel');
  chatOpen = !chatOpen;
  panel.classList.toggle('open', chatOpen);
  if (chatOpen && chatHistory.length === 0) {
    addBotMessage("👋 Hi! I'm **PhonePerfect AI**. Ask me anything about phones!\n\nTry:\n• *\"Best camera phone under 30K\"*\n• *\"Compare iPhone 16 Pro vs Galaxy S24\"*\n• *\"I have Pixel 8, should I upgrade?\"*\n• *\"Show me gaming phones\"*");
  }
}

function addBotMessage(text) {
  chatHistory.push({ role: 'bot', text, time: new Date() });
  renderChat();
}

function addUserMessage(text) {
  chatHistory.push({ role: 'user', text, time: new Date() });
  renderChat();
}

function sendChatMessage() {
  const input = document.getElementById('chat-input');
  const text = input.value.trim();
  if (!text) return;
  
  input.value = '';
  addUserMessage(text);
  
  // Show typing indicator
  const chatMessages = document.getElementById('chat-messages');
  const typingDiv = document.createElement('div');
  typingDiv.className = 'chat-msg bot typing-indicator';
  typingDiv.innerHTML = '<div class="chat-bubble bot"><span class="typing-dots"><span>.</span><span>.</span><span>.</span></span></div>';
  chatMessages.appendChild(typingDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  
  // Simulate thinking delay
  setTimeout(() => {
    typingDiv.remove();
    const response = generateResponse(text);
    addBotMessage(response.text);
  }, 600 + Math.random() * 800);
}

function handleChatKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendChatMessage();
  }
}

function renderChat() {
  const container = document.getElementById('chat-messages');
  container.innerHTML = chatHistory.map(msg => {
    const isBot = msg.role === 'bot';
    // Simple markdown-like rendering
    let html = msg.text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>')
      .replace(/\|(.+)\|/g, (match) => {
        // Simple table rendering
        return `<span class="chat-table-row">${match}</span>`;
      });
    
    return `
      <div class="chat-msg ${isBot ? 'bot' : 'user'}">
        <div class="chat-bubble ${isBot ? 'bot' : 'user'}">
          ${isBot ? '<div class="chat-avatar">🤖</div>' : ''}
          <div class="chat-text">${html}</div>
        </div>
      </div>
    `;
  }).join('');
  
  container.scrollTop = container.scrollHeight;
}

// Quick suggestion chips
function askSuggestion(text) {
  document.getElementById('chat-input').value = text;
  sendChatMessage();
}

/**
 * PhonePerfect 2.0 – Price Tracker & Sparkline Charts
 * Simulated price history with visual sparklines
 */

function renderSparkline(canvas, data, color = '#8b5cf6') {
  if (!canvas || !data || data.length === 0) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width;
  const H = canvas.height;
  const pad = 4;
  
  ctx.clearRect(0, 0, W, H);
  
  const min = Math.min(...data) * 0.98;
  const max = Math.max(...data) * 1.02;
  const range = max - min || 1;
  
  const points = data.map((v, i) => ({
    x: pad + (i / (data.length - 1)) * (W - pad * 2),
    y: pad + (1 - (v - min) / range) * (H - pad * 2)
  }));
  
  // Gradient fill
  const gradient = ctx.createLinearGradient(0, 0, 0, H);
  gradient.addColorStop(0, color + '40');
  gradient.addColorStop(1, color + '05');
  
  ctx.beginPath();
  ctx.moveTo(points[0].x, H);
  points.forEach(p => ctx.lineTo(p.x, p.y));
  ctx.lineTo(points[points.length - 1].x, H);
  ctx.closePath();
  ctx.fillStyle = gradient;
  ctx.fill();
  
  // Line
  ctx.beginPath();
  points.forEach((p, i) => {
    if (i === 0) ctx.moveTo(p.x, p.y);
    else {
      // Smooth curve
      const prev = points[i - 1];
      const cpx = (prev.x + p.x) / 2;
      ctx.bezierCurveTo(cpx, prev.y, cpx, p.y, p.x, p.y);
    }
  });
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.stroke();
  
  // Current price dot
  const last = points[points.length - 1];
  ctx.beginPath();
  ctx.arc(last.x, last.y, 3, 0, Math.PI * 2);
  ctx.fillStyle = color;
  ctx.fill();
  ctx.strokeStyle = '#fff';
  ctx.lineWidth = 1.5;
  ctx.stroke();
}

// Generate simulated price history if not present
function getPriceHistory(phone) {
  if (phone.price_history && phone.price_history.length > 0) {
    return phone.price_history;
  }
  // Generate from price
  const price = getPhonePrice(phone);
  const cat = phone.priceCategory;
  let decayRates;
  if (cat >= 4) { // Flagship
    decayRates = [1, 0.98, 0.95, 0.92, 0.88, 0.85];
  } else if (cat >= 2) { // Mid-range
    decayRates = [1, 0.97, 0.93, 0.88, 0.82, 0.78];
  } else { // Budget
    decayRates = [1, 0.95, 0.90, 0.85, 0.80, 0.75];
  }
  return decayRates.map(r => Math.round(price * r));
}

// Price alert system using localStorage
function getPriceAlerts() {
  return JSON.parse(localStorage.getItem('phonePerfectAlerts') || '{}');
}

function setPriceAlert(phoneId, targetPrice) {
  const alerts = getPriceAlerts();
  alerts[phoneId] = { targetPrice, setAt: Date.now() };
  localStorage.setItem('phonePerfectAlerts', JSON.stringify(alerts));
}

function removePriceAlert(phoneId) {
  const alerts = getPriceAlerts();
  delete alerts[phoneId];
  localStorage.setItem('phonePerfectAlerts', JSON.stringify(alerts));
}

function hasPriceAlert(phoneId) {
  return !!getPriceAlerts()[phoneId];
}

function togglePriceAlert(phoneId) {
  if (hasPriceAlert(phoneId)) {
    removePriceAlert(phoneId);
    showToast('🔕 Price alert removed');
  } else {
    // Request notification permission if needed
    if ("Notification" in window && Notification.permission !== "granted" && Notification.permission !== "denied") {
      Notification.requestPermission().then(function (permission) {
        if (permission === "granted") {
          setAlertForPhone(phoneId);
        } else {
          showToast('⚠️ Notifications denied. Alert will only work while app is open.');
          setAlertForPhone(phoneId);
        }
      });
    } else {
      setAlertForPhone(phoneId);
    }
  }
}

function setAlertForPhone(phoneId) {
  const phone = PHONES.find(p => p.id === phoneId);
  if (phone) {
    const price = getPhonePrice(phone);
    const target = Math.round(price * 0.9); // Alert at 10% drop
    setPriceAlert(phoneId, target);
    showToast(`🔔 Alert set! We'll notify when price drops below ₹${(target/1000).toFixed(0)}K`);
    
    // Test notification immediately if granted
    if ("Notification" in window && Notification.permission === "granted") {
      new Notification("Alert Set!", {
        body: `We will notify you when ${phone.name} drops below ₹${(target/1000).toFixed(0)}K.`,
        icon: phone.images && phone.images.length > 0 ? phone.images[0] : null
      });
    }
  }
}

function showToast(message) {
  // Remove existing toast
  const existing = document.querySelector('.toast-notification');
  if (existing) existing.remove();
  
  const toast = document.createElement('div');
  toast.className = 'toast-notification';
  toast.innerHTML = message;
  document.body.appendChild(toast);
  
  requestAnimationFrame(() => toast.classList.add('show'));
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

with open('app.js', 'a', encoding='utf-8') as f:
    f.write("""

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
""")

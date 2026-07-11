import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"

# 1. Create track.html
track_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SafeHer - Live Tracking Link</title>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
  
  <!-- FontAwesome Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
  
  <!-- Leaflet.js CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  
  <!-- Leaflet.js JavaScript -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>

  <style>
    :root {
      --bg-primary: #090D16;
      --bg-secondary: #121824;
      --border-color: rgba(255, 255, 255, 0.08);
      --text-primary: #FFFFFF;
      --text-secondary: #8E9AA8;
      --color-green: #34C759;
      --color-blue: #007AFF;
      --font-display: 'Outfit', sans-serif;
      --font-body: 'Inter', sans-serif;
    }
    
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    
    body {
      font-family: var(--font-body);
      background-color: var(--bg-primary);
      color: var(--text-primary);
      height: 100vh;
      width: 100vw;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    header {
      background-color: var(--bg-secondary);
      border-bottom: 1px solid var(--border-color);
      padding: 16px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }

    .logo-section {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .logo-icon {
      color: #FF3B30;
      font-size: 20px;
    }

    header h1 {
      font-family: var(--font-display);
      font-size: 18px;
      font-weight: 700;
    }

    .status-badge {
      background-color: rgba(52, 199, 89, 0.1);
      border: 1px solid rgba(52, 199, 89, 0.2);
      color: var(--color-green);
      padding: 6px 12px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .status-badge.inactive {
      background-color: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
    }

    .pulse-dot {
      width: 6px;
      height: 6px;
      background-color: var(--color-green);
      border-radius: 50%;
      box-shadow: 0 0 6px var(--color-green);
      animation: pulse 1.2s infinite alternate;
    }

    .status-badge.inactive .pulse-dot {
      background-color: var(--text-secondary);
      box-shadow: none;
      animation: none;
    }

    #track-map {
      flex: 1;
      width: 100%;
      height: 100%;
      background-color: #0d121c;
    }

    /* Floating card for details */
    .user-info-card {
      position: absolute;
      top: 90px;
      left: 20px;
      background: rgba(18, 24, 36, 0.85);
      backdrop-filter: blur(10px);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.5);
      z-index: 1000;
      max-width: 300px;
    }

    .user-info-card h3 {
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 700;
      margin-bottom: 4px;
    }

    .user-info-card p {
      font-size: 12px;
      color: var(--text-secondary);
      line-height: 1.4;
      margin-bottom: 8px;
    }

    .coords-display {
      background-color: rgba(0, 0, 0, 0.3);
      padding: 6px 10px;
      border-radius: 6px;
      font-family: monospace;
      font-size: 11px;
      color: var(--text-secondary);
    }

    .user-marker {
      width: 16px;
      height: 16px;
      background-color: var(--color-blue);
      border: 2px solid #FFFFFF;
      border-radius: 50%;
      box-shadow: 0 0 10px var(--color-blue);
    }

    @keyframes pulse {
      0% { opacity: 0.4; }
      100% { opacity: 1; }
    }
  </style>
</head>
<body>

  <header>
    <div class="logo-section">
      <i class="fa-solid fa-shield-halved logo-icon"></i>
      <h1>SafeHer Live Tracker</h1>
    </div>
    <div class="status-badge" id="live-status">
      <span class="pulse-dot"></span>
      <span id="status-text">LIVE STREAM ACTIVE</span>
    </div>
  </header>

  <div class="user-info-card">
    <h3 id="card-username">User Location</h3>
    <p id="card-desc">Waiting for coordinates...</p>
    <div class="coords-display">
      Lat: <span id="lat-val">-</span> | Lng: <span id="lng-val">-</span>
    </div>
  </div>

  <div id="track-map"></div>

  <script>
    // Global state
    let map = null;
    let userMarker = null;
    let currentCoords = { lat: 40.7128, lng: -74.0060 };
    let username = "SafeHer User";

    // Read URL params
    const urlParams = new URLSearchParams(window.location.search);
    const urlLat = parseFloat(urlParams.get('lat'));
    const urlLng = parseFloat(urlParams.get('lng'));
    const urlCity = urlParams.get('city');

    // Load initial info from LocalStorage or URL
    try {
      const storedUser = localStorage.getItem('safeher_user');
      if (storedUser) {
        username = JSON.parse(storedUser).name;
      }
    } catch(e) {}

    document.getElementById('card-username').textContent = username + "'s Path";

    if (!isNaN(urlLat) && !isNaN(urlLng)) {
      currentCoords.lat = urlLat;
      currentCoords.lng = urlLng;
    } else {
      // Check localStorage as fallback
      try {
        const storedSim = localStorage.getItem('safeher_sim_coords');
        if (storedSim) {
          const c = JSON.parse(storedSim);
          currentCoords.lat = c.lat;
          currentCoords.lng = c.lng;
        }
      } catch(e) {}
    }

    // Initialize Map
    map = L.map('track-map', {
      zoomControl: true,
      attributionControl: false
    }).setView([currentCoords.lat, currentCoords.lng], 15);

    // Dark Map Tiles
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      maxZoom: 20
    }).addTo(map);

    // Initial User Marker
    const userIcon = L.divIcon({
      className: 'user-marker-container',
      html: '<div class="user-marker"></div>',
      iconSize: [20, 20],
      iconAnchor: [10, 10]
    });
    userMarker = L.marker([currentCoords.lat, currentCoords.lng], { icon: userIcon }).addTo(map);

    // Breadcrumb trail
    const pathCoordinates = [[currentCoords.lat, currentCoords.lng]];
    const breadcrumbTrail = L.polyline(pathCoordinates, {
      color: '#007AFF',
      weight: 4,
      opacity: 0.7,
      lineCap: 'round'
    }).addTo(map);

    function updateLocation(lat, lng, city) {
      currentCoords.lat = lat;
      currentCoords.lng = lng;
      
      document.getElementById('lat-val').textContent = lat.toFixed(4);
      document.getElementById('lng-val').textContent = lng.toFixed(4);
      document.getElementById('card-desc').textContent = "Last active position centered in " + (city || "Map View") + ".";

      const latlng = [lat, lng];
      userMarker.setLatLng(latlng);
      map.panTo(latlng);
      
      // Update breadcrumb
      pathCoordinates.push(latlng);
      breadcrumbTrail.setLatLngs(pathCoordinates);
    }

    // Initialize display values
    updateLocation(currentCoords.lat, currentCoords.lng, urlCity);

    // Real-time synchronization via LocalStorage events
    window.addEventListener('storage', (e) => {
      if (e.key === 'safeher_sim_coords' && e.newValue) {
        try {
          const data = JSON.parse(e.newValue);
          updateLocation(data.lat, data.lng, data.city);
          
          // Flash live stream badge green
          const badge = document.getElementById('live-status');
          badge.className = "status-badge";
          document.getElementById('status-text').textContent = "LIVE STREAM ACTIVE";
        } catch(err) {}
      }
    });
  </script>
</body>
</html>
"""

with open(os.path.join(workspace_dir, "track.html"), "w", encoding="utf-8") as f:
    f.write(track_html)
print("Created track.html successfully.")

# 2. Update app.js
js_path = os.path.join(workspace_dir, "app.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Replace share link builder to make it dynamic
target_link_1 = "const mapLink = `https://safeher.live/track/usr9203?lat=${state.currentCoords.lat.toFixed(5)}&lng=${state.currentCoords.lng.toFixed(5)}`;"
replacement_link_1 = "const mapLink = `${window.location.origin}/track.html?lat=${state.currentCoords.lat.toFixed(5)}&lng=${state.currentCoords.lng.toFixed(5)}&city=${encodeURIComponent(state.currentCoords.city)}`;"

target_link_2 = "linkInput.value = `https://safeher.live/track/usr9203?lat=${state.currentCoords.lat.toFixed(5)}&lng=${state.currentCoords.lng.toFixed(5)}&city=${encodeURIComponent(state.currentCoords.city)}`;"
replacement_link_2 = "linkInput.value = `${window.location.origin}/track.html?lat=${state.currentCoords.lat.toFixed(5)}&lng=${state.currentCoords.lng.toFixed(5)}&city=${encodeURIComponent(state.currentCoords.city)}`;"

# Replace coordinate update points to also write to LocalStorage
target_coord_1 = """      state.currentCoords.lat = lat;
      state.currentCoords.lng = lng;
      state.currentCoords.city = city;"""

replacement_coord_1 = """      state.currentCoords.lat = lat;
      state.currentCoords.lng = lng;
      state.currentCoords.city = city;

      // Sync coordinate state to localStorage for real-time tracking page connection
      localStorage.setItem('safeher_sim_coords', JSON.stringify({
        lat: lat,
        lng: lng,
        city: city,
        timestamp: Date.now()
      }));"""

target_coord_2 = """      // Step delta (~50m each interval)
      state.currentCoords.lat += 0.0004;
      state.currentCoords.lng += 0.0004;"""

replacement_coord_2 = """      // Step delta (~50m each interval)
      state.currentCoords.lat += 0.0004;
      state.currentCoords.lng += 0.0004;

      // Sync simulated movement coordinate state
      localStorage.setItem('safeher_sim_coords', JSON.stringify({
        lat: state.currentCoords.lat,
        lng: state.currentCoords.lng,
        city: state.currentCoords.city,
        timestamp: Date.now()
      }));"""

if target_link_1 in js_content:
    js_content = js_content.replace(target_link_1, replacement_link_1)
    print("Replaced link building in SOS sequence.")

if target_link_2 in js_content:
    js_content = js_content.replace(target_link_2, replacement_link_2)
    print("Replaced link building in sharing screen render.")

if target_coord_1 in js_content:
    js_content = js_content.replace(target_coord_1, replacement_coord_1)
    print("Replaced coordinator jump sync.")

if target_coord_2 in js_content:
    js_content = js_content.replace(target_coord_2, replacement_coord_2)
    print("Replaced location simulator loop sync.")

# Write updated javascript file back
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)
print("Updated app.js successfully.")

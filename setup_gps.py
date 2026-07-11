import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"

# 1. Update index.html to add "Use Real GPS" button in simulator coordinates section
html_path = os.path.join(workspace_dir, "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

target_html = """          <div class="sim-button-group">
            <button class="btn-sim-loc active" data-lat="40.7128" data-lng="-74.0060" data-city="New York City">New York</button>
            <button class="btn-sim-loc" data-lat="51.5074" data-lng="-0.1278" data-city="London">London</button>
            <button class="btn-sim-loc" data-lat="12.9716" data-lng="77.5946" data-city="Bangalore">Bangalore</button>
            <button class="btn-sim-loc" data-lat="-33.8688" data-lng="151.2093" data-city="Sydney">Sydney</button>
          </div>"""

replacement_html = """          <div class="sim-button-group">
            <button class="btn-sim-loc active" data-lat="40.7128" data-lng="-74.0060" data-city="New York City">New York</button>
            <button class="btn-sim-loc" data-lat="51.5074" data-lng="-0.1278" data-city="London">London</button>
            <button class="btn-sim-loc" data-lat="12.9716" data-lng="77.5946" data-city="Bangalore">Bangalore</button>
            <button class="btn-sim-loc" data-lat="-33.8688" data-lng="151.2093" data-city="Sydney">Sydney</button>
          </div>
          <button class="btn-sim-action" id="btn-use-real-gps" style="margin-top: 8px; width: 100%; border-color: rgba(52, 199, 89, 0.25); color: var(--color-green); background-color: rgba(52, 199, 89, 0.05);">
            <i class="fa-solid fa-location-arrow"></i> Fetch My Real GPS Location
          </button>"""

if target_html in html_content:
    html_content = html_content.replace(target_html, replacement_html)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Updated index.html successfully.")
else:
    print("WARNING: index.html pattern not found.")

# 2. Update app.js
js_path = os.path.join(workspace_dir, "app.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Add fetchRealLocation definition in app.js
geolocation_functions = """
// --- REAL GPS GEOLOCATION FETCH ---
function fetchRealLocation() {
  addSimLog("[GPS STATUS] Querying browser geolocation...", "system");
  
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        
        state.currentCoords.lat = lat;
        state.currentCoords.lng = lng;
        state.currentCoords.city = "My Location";

        document.getElementById('sim-city-name').textContent = "My Location (Real GPS)";
        document.getElementById('sim-lat').textContent = lat.toFixed(4);
        document.getElementById('sim-lng').textContent = lng.toFixed(4);

        // Deactivate mock city buttons
        document.querySelectorAll('.btn-sim-loc').forEach(btn => btn.classList.remove('active'));

        addSimLog(`[GPS FETCH] Successfully acquired real coordinates: ${lat.toFixed(5)}, ${lng.toFixed(5)}`, 'system');

        // Sync coordinate state to localStorage for tracking page
        localStorage.setItem('safeher_sim_coords', JSON.stringify({
          lat: lat,
          lng: lng,
          city: "My Location",
          timestamp: Date.now()
        }));

        // If Leaflet map is loaded, update it
        if (state.map) {
          state.map.setView([lat, lng], 15);
          updateUserMarkerOnMap();
          loadNearbyPlaces();
        }

        // Update tracking screen text
        if (document.getElementById('screen-tracking').classList.contains('active')) {
          renderTrackingState();
        }
      },
      (error) => {
        addSimLog(`[GPS FAIL] Geolocation fetch failed: ${error.message} (using simulation default)`, 'system');
        alert("Failed to access your location. Using default simulation coordinates (New York). Please enable location permissions.");
      },
      { enableHighAccuracy: true, timeout: 8000, maximumAge: 0 }
    );
  } else {
    addSimLog("[GPS FAIL] Geolocation not supported by this browser.", 'system');
    alert("Geolocation is not supported by your browser.");
  }
}
"""

# Insert the geolocation function and hook it into DOMContentLoaded
target_dom_load = """  // Render layout depending on whether user is logged in
  if (state.user) {
    document.getElementById('display-user-name').textContent = state.user.name;
    showScreen('screen-home');
  } else {
    showScreen('screen-onboarding');
  }
});"""

replacement_dom_load = """  // Render layout depending on whether user is logged in
  if (state.user) {
    document.getElementById('display-user-name').textContent = state.user.name;
    showScreen('screen-home');
  } else {
    showScreen('screen-onboarding');
  }
  
  // Auto-fetch real location on launch
  fetchRealLocation();
});"""

# Modify loadNearbyPlaces to generate dynamic mock elements around user's real coords
target_load_places = """  const currentFilter = document.querySelector('.filter-tab.active').getAttribute('data-filter');
  const cityPlaces = nearbyPlacesData[state.currentCoords.city] || nearbyPlacesData['New York City'];
  const places = cityPlaces[currentFilter] || [];"""

replacement_load_places = """  const currentFilter = document.querySelector('.filter-tab.active').getAttribute('data-filter');
  let places = [];
  
  if (state.currentCoords.city === "My Location") {
    // Generate dynamic mock locations around user's actual location
    const isPolice = currentFilter === 'police';
    const placeType = isPolice ? "Police Station" : "Hospital";
    const placePrefix = isPolice ? "Local Area" : "Emergency Care";
    const localPhone = isPolice ? "+91 100 / 112" : "+91 102 / 108";
    
    places = [
      {
        name: `${placePrefix} ${placeType} Alpha`,
        lat: state.currentCoords.lat + 0.0042,
        lng: state.currentCoords.lng + 0.0035,
        address: `Sector 3 Safety Lane, ${state.currentCoords.city}`,
        phone: localPhone
      },
      {
        name: `${placePrefix} ${placeType} Beta`,
        lat: state.currentCoords.lat - 0.0031,
        lng: state.currentCoords.lng + 0.0051,
        address: `Avenue 7 Guardian Road, ${state.currentCoords.city}`,
        phone: localPhone
      },
      {
        name: `${placePrefix} ${placeType} Gamma`,
        lat: state.currentCoords.lat + 0.0028,
        lng: state.currentCoords.lng - 0.0045,
        address: `Ring Road Crossing, ${state.currentCoords.city}`,
        phone: localPhone
      }
    ];
  } else {
    const cityPlaces = nearbyPlacesData[state.currentCoords.city] || nearbyPlacesData['New York City'];
    places = cityPlaces[currentFilter] || [];
  }"""

# Hook up the simulator button for GPS
target_sim_init = """function initSimulatorControls() {
  const panel = document.getElementById('simulation-panel');
  const toggleBtn = document.getElementById('sim-toggle-btn');"""

replacement_sim_init = """function initSimulatorControls() {
  const panel = document.getElementById('simulation-panel');
  const toggleBtn = document.getElementById('sim-toggle-btn');
  
  // Real GPS fetch button
  document.getElementById('btn-use-real-gps').addEventListener('click', () => {
    fetchRealLocation();
  });"""

# Assemble all updates
js_content += geolocation_functions

if target_dom_load in js_content:
    js_content = js_content.replace(target_dom_load, replacement_dom_load)
    print("Hooked fetchRealLocation into DOM load.")

if target_load_places in js_content:
    js_content = js_content.replace(target_load_places, replacement_load_places)
    print("Updated loadNearbyPlaces for dynamic user coordinates.")

if target_sim_init in js_content:
    js_content = js_content.replace(target_sim_init, replacement_sim_init)
    print("Hooked simulator GPS button listener.")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)
print("Updated app.js successfully.")

import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"

# 1. Update index.html
html_path = os.path.join(workspace_dir, "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Remove Nearby Help card from quick-grid
target_grid_card = """                <!-- Quick Navigation Grid -->
                <div class="quick-grid">
                  <button class="grid-card card-blue" id="btn-nav-map">
                    <div class="card-icon"><i class="fa-solid fa-map-location-dot"></i></div>
                    <div class="card-info">
                      <h4>Nearby Help</h4>
                      <p>Police & Hospitals</p>
                    </div>
                  </button>
                  
                  <button class="grid-card card-purple" id="btn-nav-contacts">"""

replacement_grid_card = """                <!-- Quick Navigation Grid -->
                <div class="quick-grid">
                  <button class="grid-card card-purple" id="btn-nav-contacts">"""

html_content = html_content.replace(target_grid_card, replacement_grid_card)

# Remove screen-map division completely
target_screen_map = """            <!-- SCREEN 3: MAP / NEARBY HELP -->
            <div class="app-screen map-screen" id="screen-map">
              <div class="app-header-bar flex-row">
                <button class="btn-back" id="map-back-btn"><i class="fa-solid fa-chevron-left"></i></button>
                <h3>Nearby Help</h3>
                <div style="width: 28px;"></div> <!-- Spacer for centering -->
              </div>
              
              <!-- Mandatory sharing banner -->
              <div class="mandatory-sharing-banner" id="map-sharing-banner">
                <span class="pulse-beacon"></span>
                <i class="fa-solid fa-share-nodes"></i> Mandatory Live Sharing Active
              </div>
              
              <!-- Filter Tabs -->
              <div class="map-filters">
                <button class="filter-tab active" data-filter="police">
                  <i class="fa-solid fa-building-shield"></i> Police
                </button>
                <button class="filter-tab" data-filter="hospitals">
                  <i class="fa-solid fa-house-medical"></i> Hospitals
                </button>
              </div>
              
              <div class="map-container-wrapper">
                <div id="safety-map"></div>
                
                <!-- Slide up overlay with details about selected marker -->
                <div class="place-details-card" id="place-details-card">
                  <div class="card-handle"></div>
                  <div class="place-info">
                    <h4 id="place-name">Selected Station</h4>
                    <p id="place-address"><i class="fa-solid fa-location-dot"></i> Street address goes here</p>
                    <div class="place-stats">
                      <span id="place-distance"><i class="fa-solid fa-person-walking"></i> 0.5 km away</span>
                      <span id="place-phone"><i class="fa-solid fa-phone"></i> +1 800 123 456</span>
                    </div>
                  </div>
                  <div class="place-actions">
                    <a href="#" class="btn-primary" id="btn-get-directions">
                      <i class="fa-solid fa-diamond-turn-right"></i> Navigate
                    </a>
                    <a href="#" class="btn-secondary" id="btn-call-place">
                      <i class="fa-solid fa-phone"></i> Call
                    </a>
                  </div>
                </div>
              </div>
            </div>"""

if target_screen_map in html_content:
    html_content = html_content.replace(target_screen_map, "")
    print("Removed map-screen div from index.html.")
else:
    # Try finding fallback structure if slightly different due to previous edit
    print("WARNING: Direct screen-map target not matched. Searching for generic screen-map...")
    # Let's write a robust search for screen-map and extract it
    start_idx = html_content.find('<!-- SCREEN 3: MAP / NEARBY HELP -->')
    if start_idx != -1:
        # find the end of this screen
        end_tag = '</div>\n            \n            <!-- SCREEN 4: CONTACTS MANAGEMENT -->'
        end_idx = html_content.find(end_tag)
        if end_idx != -1:
            html_content = html_content[:start_idx] + html_content[end_idx + len('</div>\n            \n'):]
            print("Extracted screen-map via index matching successfully.")

# Remove Nearby item from bottom nav bar
target_nav_item = """              <button class="nav-item" data-target="screen-map">
                <i class="fa-solid fa-map-location-dot"></i>
                <span>Nearby</span>
              </button>"""

html_content = html_content.replace(target_nav_item, "")

# Save index.html
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)
print("Updated index.html files successfully.")


# 2. Update style.css (Modify quick-grid for 2 items)
css_path = os.path.join(workspace_dir, "style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

# Make quick-grid display two columns for visual balance
target_css_grid = """/* Quick Navigation Grid */
.quick-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
  width: 100%;
}"""

replacement_css_grid = """/* Quick Navigation Grid (Balanced 2 Columns) */
.quick-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  width: 100%;
}"""

css_content = css_content.replace(target_css_grid, replacement_css_grid)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css_content)
print("Updated style.css layout successfully.")


# 3. Update app.js (Remove map, route listeners and data)
js_path = os.path.join(workspace_dir, "app.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# We can simply truncate map related variables and functions
target_state = """  map: null,
  userMarker: null,
  placesMarkers: [],
  navigationRoute: null"""

replacement_state = """  // Map variables are not used in main app (only track.html utilizes Leaflet)"""

js_content = js_content.replace(target_state, replacement_state)

# Remove router showScreen map code block
target_js_show = """  // Screen specific hooks
  if (screenId === 'screen-map') {
    // Mandatory Location Sharing activation
    if (!state.isSharingLocation) {
      state.isSharingLocation = true;
      addSimLog("[MANDATORY TRIGGER] Live Location Sharing enabled automatically to query Nearby Help.", "location");
    }
    initLeafletMap();
  } else if (screenId === 'screen-contacts') {"""

replacement_js_show = """  // Screen specific hooks
  if (screenId === 'screen-contacts') {"""

js_content = js_content.replace(target_js_show, replacement_js_show)

# Remove map listeners from app router
target_js_route = """  // Action button routing on home screen
  document.getElementById('btn-nav-map').addEventListener('click', () => showScreen('screen-map'));
  document.getElementById('btn-nav-contacts').addEventListener('click', () => showScreen('screen-contacts'));
  document.getElementById('btn-nav-tracking').addEventListener('click', () => showScreen('screen-tracking'));

  // Back buttons
  document.getElementById('map-back-btn').addEventListener('click', () => showScreen('screen-home'));
  document.getElementById('contacts-back-btn').addEventListener('click', () => showScreen('screen-home'));"""

replacement_js_route = """  // Action button routing on home screen
  document.getElementById('btn-nav-contacts').addEventListener('click', () => showScreen('screen-contacts'));
  document.getElementById('btn-nav-tracking').addEventListener('click', () => showScreen('screen-tracking'));

  // Back buttons
  document.getElementById('contacts-back-btn').addEventListener('click', () => showScreen('screen-home'));"""

js_content = js_content.replace(target_js_route, replacement_js_route)

# Remove shareBtn map check inside click
target_js_check = """    // Check if user is currently browsing the Map screen, where sharing is mandatory
    const mapActive = document.getElementById('screen-map').classList.contains('active');
    if (mapActive && state.isSharingLocation) {
      addSimLog("[SIMULATOR BLOCK] Cannot disable sharing while viewing Nearby Help (Mandatory requirement).", "system");
      alert("Live location sharing is mandatory while viewing nearby emergency stations.");
      return;
    }"""

js_content = js_content.replace(target_js_check, "")

# Ensure SOS button automatically triggers location sharing
target_sos_activate = """function activateSOS() {
  state.isSOSActive = true;
  
  // Update indicator UI
  const statusDot = document.getElementById('home-status-dot');
  const statusLbl = document.getElementById('home-status-lbl');
  const statusInd = document.querySelector('.system-status-indicator');
  
  if (statusDot && statusLbl && statusInd) {
    statusDot.className = "status-dot red";
    statusLbl.textContent = "SOS ACTIVE";
    statusInd.classList.add('sos-mode');
  }

  // 1. Get primary contact"""

replacement_sos_activate = """function activateSOS() {
  state.isSOSActive = true;
  
  // Force location sharing to be active during SOS
  state.isSharingLocation = true;
  addSimLog("[SOS SHARING] Live Location Sharing enabled automatically due to SOS trigger.", "location");
  
  // Update indicator UI
  const statusDot = document.getElementById('home-status-dot');
  const statusLbl = document.getElementById('home-status-lbl');
  const statusInd = document.querySelector('.system-status-indicator');
  
  if (statusDot && statusLbl && statusInd) {
    statusDot.className = "status-dot red";
    statusLbl.textContent = "SOS ACTIVE";
    statusInd.classList.add('sos-mode');
  }

  // 1. Get primary contact"""

js_content = js_content.replace(target_sos_activate, replacement_sos_activate)

# Remove unused functions from end of app.js (NearbyPlaces details, distance functions, routing functions, Leaflet handlers)
# Let's search and remove Leaflet functions cleanly or just print message.
# We will do a string slice search or replace.
# Let's search for "function initLeafletMap()" and cut until "function initSimulatorControls()"
map_func_start = js_content.find("function initLeafletMap()")
sim_func_start = js_content.find("function initSimulatorControls()")
if map_func_start != -1 and sim_func_start != -1:
    js_content = js_content[:map_func_start] + js_content[sim_func_start:]
    print("Removed Leaflet map helper functions from app.js successfully.")

# Remove nearbyPlacesData definition
places_data_start = js_content.find("const nearbyPlacesData = {")
if places_data_start != -1:
    # Find the next global function or route definition to slice
    clock_start = js_content.find("// --- INITIALIZE APP ON LOAD ---")
    if clock_start != -1:
        js_content = js_content[:places_data_start] + js_content[clock_start:]
        print("Removed nearbyPlacesData block successfully.")

# Write updated javascript file back
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)
print("Updated app.js successfully.")

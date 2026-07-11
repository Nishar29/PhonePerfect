import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"

# 1. Read index.html and insert mandatory sharing banner
html_path = os.path.join(workspace_dir, "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

target_html = """            <!-- SCREEN 3: MAP / NEARBY HELP -->
            <div class="app-screen map-screen" id="screen-map">
              <div class="app-header-bar flex-row">
                <button class="btn-back" id="map-back-btn"><i class="fa-solid fa-chevron-left"></i></button>
                <h3>Nearby Help</h3>
                <div style="width: 28px;"></div> <!-- Spacer for centering -->
              </div>"""

replacement_html = """            <!-- SCREEN 3: MAP / NEARBY HELP -->
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
              </div>"""

if target_html in html_content:
    html_content = html_content.replace(target_html, replacement_html)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Updated index.html successfully.")
else:
    print("WARNING: index.html target pattern not found.")

# 2. Read style.css and append banner styling
css_path = os.path.join(workspace_dir, "style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

css_append = """
/* Mandatory location sharing banner */
.mandatory-sharing-banner {
  background-color: rgba(255, 59, 48, 0.15);
  border-bottom: 1px solid rgba(255, 59, 48, 0.25);
  color: #FF3B30;
  padding: 8px 16px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  z-index: 10;
}

.pulse-beacon {
  width: 8px;
  height: 8px;
  background-color: #FF3B30;
  border-radius: 50%;
  box-shadow: 0 0 6px #FF3B30;
  animation: heartBeat 1s infinite alternate;
}
"""

if ".mandatory-sharing-banner" not in css_content:
    css_content += css_append
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)
    print("Updated style.css successfully.")
else:
    print("WARNING: style.css banner styles already exist.")

# 3. Read app.js and modify screen-map hook in showScreen & toggle share button click
js_path = os.path.join(workspace_dir, "app.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

target_js_show = """  // Screen specific hooks
  if (screenId === 'screen-map') {
    initLeafletMap();"""

replacement_js_show = """  // Screen specific hooks
  if (screenId === 'screen-map') {
    // Mandatory Location Sharing activation
    if (!state.isSharingLocation) {
      state.isSharingLocation = true;
      addSimLog("[MANDATORY TRIGGER] Live Location Sharing enabled automatically to query Nearby Help.", "location");
    }
    initLeafletMap();"""

target_js_click = """  // Start Sharing Toggle
  shareBtn.onclick = () => {
    state.isSharingLocation = !state.isSharingLocation;
    if (state.isSharingLocation) {
      addSimLog(`Location sharing enabled by user. Shared Link: ${linkInput.value}`, 'location');
    } else {
      addSimLog(`Location sharing disabled by user. Broadcast stopped.`, 'location');
    }
    renderTrackingState();
  };"""

replacement_js_click = """  // Start Sharing Toggle
  shareBtn.onclick = () => {
    // Check if user is currently browsing the Map screen, where sharing is mandatory
    const mapActive = document.getElementById('screen-map').classList.contains('active');
    if (mapActive && state.isSharingLocation) {
      addSimLog("[SIMULATOR BLOCK] Cannot disable sharing while viewing Nearby Help (Mandatory requirement).", "system");
      alert("Live location sharing is mandatory while viewing nearby emergency stations.");
      return;
    }

    state.isSharingLocation = !state.isSharingLocation;
    if (state.isSharingLocation) {
      addSimLog(`Location sharing enabled by user. Shared Link: ${linkInput.value}`, 'location');
    } else {
      addSimLog(`Location sharing disabled by user. Broadcast stopped.`, 'location');
    }
    renderTrackingState();
  };"""

if target_js_show in js_content:
    js_content = js_content.replace(target_js_show, replacement_js_show)
    print("Replaced showScreen pattern in app.js.")
else:
    print("WARNING: showScreen pattern in app.js not found.")

if target_js_click in js_content:
    js_content = js_content.replace(target_js_click, replacement_js_click)
    print("Replaced shareBtn click pattern in app.js.")
else:
    print("WARNING: shareBtn click pattern in app.js not found.")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)
print("Updated app.js successfully.")

import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"
js_path = os.path.join(workspace_dir, "app.js")

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Replace map view checking in quick jump coordinator buttons
target_ref_1 = """      // Update map immediately if screen is active
      if (document.getElementById('screen-map').classList.contains('active')) {
        initLeafletMap();
      }"""

# Since map doesn't exist, we don't update anything in main app map view
js_content = js_content.replace(target_ref_1, "")

# Replace map updating in geolocation callback
target_ref_2 = """        // If Leaflet map is loaded, update it
        if (state.map) {
          state.map.setView([lat, lng], 15);
          updateUserMarkerOnMap();
          loadNearbyPlaces();
        }"""
js_content = js_content.replace(target_ref_2, "")

# Replace user marker updating and nearby places loading in simulated movement loop
target_ref_3 = """      // Update Map Marker
      updateUserMarkerOnMap();"""
js_content = js_content.replace(target_ref_3, "")

# Replace reset button map updating
target_ref_4 = """    updateUserMarkerOnMap();
    if (document.getElementById('screen-map').classList.contains('active')) {
      loadNearbyPlaces();
    }"""
js_content = js_content.replace(target_ref_4, "")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)
print("Cleaned up map references in app.js simulator code successfully.")

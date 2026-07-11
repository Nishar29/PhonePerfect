import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"
js_path = os.path.join(workspace_dir, "app.js")

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Define the storage wrapper
storage_wrapper = """
// --- SAFE STORAGE HELPER (Resilient to privacy blocks / WebView restrictions) ---
const storage = {
  getItem(key) {
    try {
      return localStorage.getItem(key);
    } catch (e) {
      console.warn("localStorage read blocked, using runtime fallback:", e);
      return this._fallback[key] || null;
    }
  },
  setItem(key, value) {
    try {
      localStorage.setItem(key, value);
    } catch (e) {
      console.warn("localStorage write blocked, using runtime fallback:", e);
      this._fallback[key] = value;
    }
  },
  _fallback: {}
};
"""

# Insert storage_wrapper at the top of app.js (e.g. after the global state definition)
state_end_idx = js_content.find("  navigationRoute: null\n};")
if state_end_idx == -1:
    # Look for fallback end-state string
    state_end_idx = js_content.find("};\n\n// --- MOCK DATABASE OF PLACES ---")

if state_end_idx != -1:
    # Insert just after the state object definition
    insert_pos = js_content.find("\n", state_end_idx) + 1
    js_content = js_content[:insert_pos] + storage_wrapper + js_content[insert_pos:]
    print("Inserted storage wrapper definition.")
else:
    # Fallback to appending at the top
    js_content = storage_wrapper + js_content
    print("Appended storage wrapper definition at the top.")

# Replace all occurrences of localStorage
js_content = js_content.replace("localStorage.getItem", "storage.getItem")
js_content = js_content.replace("localStorage.setItem", "storage.setItem")
print("Replaced all direct localStorage calls with safe storage helper.")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)
print("Updated app.js successfully.")

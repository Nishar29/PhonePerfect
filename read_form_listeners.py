import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"
js_path = os.path.join(workspace_dir, "app.js")

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Let's find initFormListeners
start_idx = js_content.find("function initFormListeners()")
if start_idx != -1:
    # Print 3000 characters from start_idx
    print(js_content[start_idx:start_idx+3000])
else:
    print("WARNING: initFormListeners not found.")

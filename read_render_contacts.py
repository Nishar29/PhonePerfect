import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"
js_path = os.path.join(workspace_dir, "app.js")

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Find renderContactsList
start_idx = js_content.find("function renderContactsList()")
if start_idx != -1:
    print(js_content[start_idx:start_idx+2500])
else:
    print("WARNING: renderContactsList not found.")

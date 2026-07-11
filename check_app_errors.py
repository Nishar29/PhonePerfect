import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"
js_path = os.path.join(workspace_dir, "app.js")

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Check for deleted function calls
functions_to_check = [
    "initLeafletMap",
    "updateUserMarkerOnMap",
    "loadNearbyPlaces",
    "drawDirectionsRoute",
    "calculateDistance"
]

print("Checking for leftover map references in app.js:")
for func in functions_to_check:
    count = js_content.count(func)
    print(f"- '{func}': found {count} times")
    if count > 0:
        # Find where it occurs
        idx = 0
        while True:
            idx = js_content.find(func, idx)
            if idx == -1:
                break
            # print context of 100 chars around it
            start = max(0, idx - 60)
            end = min(len(js_content), idx + 80)
            print(f"  Context: {js_content[start:end].strip().replace('\\n', ' ')}")
            idx += len(func)

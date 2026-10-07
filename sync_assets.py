import os
import shutil

src_dir = r"c:\Users\nisha\.gemini\antigravity\scratch"
dest_dir = os.path.join(src_dir, "android-app", "app", "src", "main", "assets")

os.makedirs(dest_dir, exist_ok=True)

files_to_sync = [
    "index.html",
    "style.css",
    "app.js",
    "phones.js",
    "price-tracker.js",
    "ai-chat.js",
    "auto-updater.js",
    "manifest.json"
]

for filename in files_to_sync:
    src_path = os.path.join(src_dir, filename)
    dest_path = os.path.join(dest_dir, filename)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"Copied {filename} to Android assets.")
    else:
        print(f"Skipped {filename} (not found in source).")

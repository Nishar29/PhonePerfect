import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni\safeher-android"
main_activity_path = os.path.join(workspace_dir, "app", "src", "main", "java", "com", "example", "safeher", "MainActivity.kt")

with open(main_activity_path, "r", encoding="utf-8") as f:
    print(f.read())

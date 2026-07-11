import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni\safeher-android"

found_files = []
for root, dirs, files in os.walk(workspace_dir):
    for f in files:
        if f.endswith(".kt") or f.endswith(".java") or f.endswith(".xml"):
            found_files.append(os.path.join(root, f))

print("Found Android source/manifest files:")
for f in found_files:
    # print relative path
    rel = os.path.relpath(f, workspace_dir)
    print(f"- {rel}")

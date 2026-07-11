import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni\safeher-android"

def list_files(startpath):
    print(f"Listing structure of: {startpath}")
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        # only show files up to depth 3 to avoid spam
        if level <= 3:
            for f in files:
                print(f"{subindent}{f}")

list_files(workspace_dir)

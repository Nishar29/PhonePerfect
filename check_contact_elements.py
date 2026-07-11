import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"
html_path = os.path.join(workspace_dir, "index.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

elements_to_check = [
    'id="add-contact-modal"',
    'id="btn-show-add-contact-modal"',
    'id="btn-close-contact-modal"',
    'id="add-contact-form"',
    'id="new-contact-name"',
    'id="new-contact-phone"',
    'id="set-as-primary"',
    'id="contacts-list"',
    'id="contact-count"'
]

print("Checking DOM element IDs in index.html:")
for el in elements_to_check:
    present = el in html
    print(f"- '{el}': {'PRESENT' if present else 'MISSING!'}")

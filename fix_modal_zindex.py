import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"
css_path = os.path.join(workspace_dir, "style.css")

with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

target_modal_css = """/* Add Contact modal */
.add-contact-modal {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(3, 6, 12, 0.7);
  backdrop-filter: blur(8px);
  z-index: 100;"""

replacement_modal_css = """/* Add Contact modal */
.add-contact-modal {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(3, 6, 12, 0.7);
  backdrop-filter: blur(8px);
  z-index: 200;"""

if target_modal_css in css_content:
    css_content = css_content.replace(target_modal_css, replacement_modal_css)
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)
    print("Updated style.css modal z-index successfully.")
else:
    print("WARNING: modal z-index target not found in style.css.")

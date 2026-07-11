import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"
js_path = os.path.join(workspace_dir, "app.js")

with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

target_storage = """function loadStateFromStorage() {
  const storedUser = localStorage.getItem('safeher_user');
  const storedContacts = localStorage.getItem('safeher_contacts');
  
  if (storedUser) {
    state.user = JSON.parse(storedUser);
  }
  
  if (storedContacts) {
    state.contacts = JSON.parse(storedContacts);
  } else {
    // Inject mock contacts for instant testing
    state.contacts = [
      { id: '1', name: 'Mom', phone: '+1 (555) 902-1209', isPrimary: true },
      { id: '2', name: 'Dad', phone: '+1 (555) 304-4920', isPrimary: false },
      { id: '3', name: 'Sister', phone: '+1 (555) 728-1123', isPrimary: false }
    ];
    saveContactsToStorage();
  }
}"""

replacement_storage = """function loadStateFromStorage() {
  const storedUser = localStorage.getItem('safeher_user');
  const storedContacts = localStorage.getItem('safeher_contacts');
  
  if (storedUser) {
    try {
      state.user = JSON.parse(storedUser);
    } catch (e) {
      state.user = null;
    }
  }
  
  if (storedContacts) {
    try {
      const parsed = JSON.parse(storedContacts);
      if (Array.isArray(parsed)) {
        state.contacts = parsed;
      } else {
        throw new Error("Stored contacts is not an array");
      }
    } catch (e) {
      console.warn("Invalid contacts stored, recovering default database", e);
      loadDefaultContacts();
    }
  } else {
    loadDefaultContacts();
  }
}

function loadDefaultContacts() {
  state.contacts = [
    { id: '1', name: 'Mom', phone: '+1 (555) 902-1209', isPrimary: true },
    { id: '2', name: 'Dad', phone: '+1 (555) 304-4920', isPrimary: false },
    { id: '3', name: 'Sister', phone: '+1 (555) 728-1123', isPrimary: false }
  ];
  saveContactsToStorage();
}"""

if target_storage in js_content:
    js_content = js_content.replace(target_storage, replacement_storage)
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print("Updated loadStateFromStorage successfully.")
else:
    print("WARNING: loadStateFromStorage target not found.")

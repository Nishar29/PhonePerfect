import os
import shutil

moni_dir = r"c:\Users\nisha\.gemini\antigravity\moni"
android_dir = os.path.join(moni_dir, "safeher-android")
assets_dir = os.path.join(android_dir, "app", "src", "main", "assets")

# Ensure assets directory exists
os.makedirs(assets_dir, exist_ok=True)

# Copy index.html, style.css, track.html from workspace root to assets
shutil.copy2(os.path.join(moni_dir, "index.html"), os.path.join(assets_dir, "index.html"))
shutil.copy2(os.path.join(moni_dir, "style.css"), os.path.join(assets_dir, "style.css"))
shutil.copy2(os.path.join(moni_dir, "track.html"), os.path.join(assets_dir, "track.html"))
print("Synced index.html, style.css, and track.html to assets.")

# Copy app.js and inject AndroidBridge SMS support
with open(os.path.join(moni_dir, "app.js"), "r", encoding="utf-8") as f:
    app_js = f.read()

target_sms = """  state.contacts.forEach(contact => {
    addSimLog(`[SMS SENT] To: ${contact.name} (${contact.phone}) - Msg: "${smsBody}"`, 'sms');
  });"""

replacement_sms = """  state.contacts.forEach(contact => {
    addSimLog(`[SMS SENT] To: ${contact.name} (${contact.phone}) - Msg: "${smsBody}"`, 'sms');
    
    // Call Android Bridge to send real SMS
    if (typeof AndroidBridge !== 'undefined' && AndroidBridge.sendSMS) {
      const cleanPhone = contact.phone.replace(/[^+\\d]/g, '');
      AndroidBridge.sendSMS(cleanPhone, smsBody);
    }
  });"""

if target_sms in app_js:
    app_js = app_js.replace(target_sms, replacement_sms)
    print("Injected AndroidBridge SMS call in assets/app.js.")
else:
    # Check if already injected
    if "AndroidBridge.sendSMS" in app_js:
        print("AndroidBridge SMS call already present in app.js.")
    else:
        print("WARNING: Target SMS pattern not found in app.js.")

with open(os.path.join(assets_dir, "app.js"), "w", encoding="utf-8") as f:
    f.write(app_js)
print("Synced app.js to assets.")

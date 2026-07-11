import os
import shutil

moni_dir = r"c:\Users\nisha\.gemini\antigravity\moni"
android_dir = os.path.join(moni_dir, "safeher-android")

# 1. Create assets directory
assets_dir = os.path.join(android_dir, "app", "src", "main", "assets")
os.makedirs(assets_dir, exist_ok=True)
print("Created assets directory.")

# 2. Copy index.html, style.css, track.html, app.js
shutil.copy2(os.path.join(moni_dir, "index.html"), os.path.join(assets_dir, "index.html"))
shutil.copy2(os.path.join(moni_dir, "style.css"), os.path.join(assets_dir, "style.css"))
shutil.copy2(os.path.join(moni_dir, "track.html"), os.path.join(assets_dir, "track.html"))

# 3. Read and modify app.js to include SMS Bridge call, then write to assets
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
    print("Injected AndroidBridge SMS call in app.js.")
else:
    print("WARNING: Target SMS pattern not found in app.js.")

with open(os.path.join(assets_dir, "app.js"), "w", encoding="utf-8") as f:
    f.write(app_js)
print("Copied and modified app.js into assets folder.")

# 4. Modify AndroidManifest.xml
manifest_path = os.path.join(android_dir, "app", "src", "main", "AndroidManifest.xml")
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = f.read()

permission_tag = '<uses-permission android:name="android.permission.SEND_SMS" />'
if permission_tag not in manifest:
    # Insert permission just under <manifest ...>
    insert_idx = manifest.find("<manifest")
    insert_end = manifest.find(">", insert_idx) + 1
    manifest = manifest[:insert_end] + f"\n    {permission_tag}" + manifest[insert_end:]
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest)
    print("Added SEND_SMS permission to AndroidManifest.xml.")
else:
    print("SEND_SMS permission already present in AndroidManifest.xml.")

# 5. Rewrite MainActivity.kt
main_activity_path = os.path.join(android_dir, "app", "src", "main", "java", "com", "example", "safeher", "MainActivity.kt")

new_main_activity = """package com.example.safeher

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.telephony.SmsManager
import android.util.Log
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : ComponentActivity() {
    private val SMS_PERMISSION_CODE = 101

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        enableEdgeToEdge()
        
        // Request SMS Permission on startup
        checkSmsPermission()

        setContent {
            AndroidView(
                factory = { context ->
                    WebView(context).apply {
                        settings.javaScriptEnabled = true
                        settings.domStorageEnabled = true
                        settings.allowFileAccess = true
                        settings.allowContentAccess = true
                        
                        webViewClient = object : WebViewClient() {
                            override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
                                if (url != null && url.startsWith("tel:")) {
                                    // Trigger native dialer dial intent
                                    val intent = Intent(Intent.ACTION_DIAL, Uri.parse(url))
                                    context.startActivity(intent)
                                    return true
                                }
                                return super.shouldOverrideUrlLoading(view, url)
                            }
                        }
                        
                        webChromeClient = WebChromeClient()
                        
                        // Add Javascript Interface
                        addJavascriptInterface(AndroidBridge(context), "AndroidBridge")
                        
                        loadUrl("file:///android_asset/index.html")
                    }
                },
                modifier = Modifier.fillMaxSize()
            )
        }
    }

    private fun checkSmsPermission() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.SEND_SMS) 
            != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(
                this, 
                arrayOf(Manifest.permission.SEND_SMS), 
                SMS_PERMISSION_CODE
            )
        }
    }
}

class AndroidBridge(private val context: Context) {
    @JavascriptInterface
    fun sendSMS(phoneNumber: String, message: String) {
        try {
            val smsManager = context.getSystemService(SmsManager::class.java)
            smsManager.sendTextMessage(phoneNumber, null, message, null, null)
            Log.d("SafeHerBridge", "SMS sent to " + phoneNumber + " successfully.")
        } catch (e: Exception) {
            Log.e("SafeHerBridge", "Failed to send SMS", e)
        }
    }
}
"""

with open(main_activity_path, "w", encoding="utf-8") as f:
    f.write(new_main_activity)
print("Updated MainActivity.kt successfully with WebView and SMS Bridge.")

import os

workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"
android_dir = os.path.join(workspace_dir, "safeher-android")
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
import android.webkit.GeolocationPermissions
import android.webkit.JavascriptInterface
import android.webkit.JsResult
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
    private val PERMISSIONS_REQUEST_CODE = 101

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        enableEdgeToEdge()
        
        // Request all permissions on startup
        checkAndRequestPermissions()
        
        // Enable Chrome remote debugging for the WebView
        WebView.setWebContentsDebuggingEnabled(true)

        setContent {
            AndroidView(
                factory = { context ->
                    WebView(context).apply {
                        settings.javaScriptEnabled = true
                        settings.domStorageEnabled = true
                        settings.allowFileAccess = true
                        settings.allowContentAccess = true
                        // Enable geolocation inside WebView
                        settings.setGeolocationEnabled(true)
                        
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
                        
                        // Custom WebChromeClient to handle WebView geolocation and JS Alerts
                        webChromeClient = object : WebChromeClient() {
                            override fun onGeolocationPermissionsShowPrompt(
                                origin: String?,
                                callback: GeolocationPermissions.Callback?
                            ) {
                                // Automatically grant permission to WebView assets origin
                                callback?.invoke(origin, true, false)
                            }

                            override fun onJsAlert(
                                view: WebView?,
                                url: String?,
                                message: String?,
                                result: JsResult?
                            ): Boolean {
                                Log.d("SafeHerWebView", "JS Alert intercepted: " + message)
                                // Confirm the alert automatically to prevent JS thread locking
                                result?.confirm()
                                return true
                            }
                        }
                        
                        // Add Javascript Interface
                        addJavascriptInterface(AndroidBridge(context), "AndroidBridge")
                        
                        loadUrl("file:///android_asset/index.html")
                    }
                },
                modifier = Modifier.fillMaxSize()
            )
        }
    }

    private fun checkAndRequestPermissions() {
        val permissionsNeeded = mutableListOf<String>()

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.SEND_SMS) 
            != PackageManager.PERMISSION_GRANTED) {
            permissionsNeeded.add(Manifest.permission.SEND_SMS)
        }

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) 
            != PackageManager.PERMISSION_GRANTED) {
            permissionsNeeded.add(Manifest.permission.ACCESS_FINE_LOCATION)
        }

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) 
            != PackageManager.PERMISSION_GRANTED) {
            permissionsNeeded.add(Manifest.permission.ACCESS_COARSE_LOCATION)
        }

        if (permissionsNeeded.isNotEmpty()) {
            ActivityCompat.requestPermissions(
                this, 
                permissionsNeeded.toTypedArray(), 
                PERMISSIONS_REQUEST_CODE
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
print("Updated MainActivity.kt successfully with onJsAlert override and WebView debugging.")

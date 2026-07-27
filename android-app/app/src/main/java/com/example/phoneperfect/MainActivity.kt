package com.example.phoneperfect

import android.annotation.SuppressLint
import android.os.Bundle
import android.view.KeyEvent
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.enableEdgeToEdge

class MainActivity : ComponentActivity() {
    private lateinit var webView: WebView

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        enableEdgeToEdge()
        
        webView = WebView(this)
        
        // Enable hardware acceleration
        webView.setLayerType(WebView.LAYER_TYPE_HARDWARE, null)
        
        val settings: WebSettings = webView.settings
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true
        
        // Caching
        settings.cacheMode = WebSettings.LOAD_DEFAULT
        settings.databaseEnabled = true
        
        // Mobile fit
        settings.useWideViewPort = true
        settings.loadWithOverviewMode = true
        
        webView.webViewClient = WebViewClient()
        webView.webChromeClient = WebChromeClient()
        
        webView.loadUrl("file:///android_asset/index.html")
        
        setContentView(webView)
    }

    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {
        // Handle back button for webview navigation
        if (keyCode == KeyEvent.KEYCODE_BACK && webView.canGoBack()) {
            webView.goBack()
            return true
        }
        return super.onKeyDown(keyCode, event)
    }
}

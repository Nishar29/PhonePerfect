import os

# Define the targets
workspace_dir = r"c:\Users\nisha\.gemini\antigravity\moni"

# Ensure the workspace directory exists
os.makedirs(workspace_dir, exist_ok=True)

# ----------------- index.html CONTENT -----------------
index_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SafeHer - Women's Safety & Emergency Assistance</title>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  
  <!-- FontAwesome Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
  
  <!-- Leaflet.js CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  
  <!-- Leaflet.js JavaScript -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  
  <!-- Custom Styling -->
  <link rel="stylesheet" href="style.css">
</head>
<body>

  <!-- Main Wrapper (Aligns Mock Phone and Simulation Drawer side-by-side on desktop) -->
  <div class="app-wrapper">
    
    <!-- Smartphone Mockup Container -->
    <div class="phone-mockup">
      <div class="phone-case">
        <!-- Speaker / Notch -->
        <div class="phone-notch"></div>
        
        <!-- Screen Content Area -->
        <div class="phone-screen">
          
          <!-- Mock Phone Status Bar -->
          <div class="phone-status-bar">
            <span class="status-time" id="status-time">17:15</span>
            <div class="status-icons">
              <i class="fa-solid fa-signal"></i>
              <i class="fa-solid fa-wifi"></i>
              <i class="fa-solid fa-battery-three-quarters"></i>
            </div>
          </div>
          
          <!-- MAIN APP WINDOW -->
          <div class="app-body" id="app-body">
            
            <!-- SCREEN 1: ONBOARDING / SETUP -->
            <div class="app-screen onboarding-screen active" id="screen-onboarding">
              <div class="screen-header onboarding-header">
                <div class="logo-area">
                  <div class="shield-logo">
                    <i class="fa-solid fa-shield-halved"></i>
                  </div>
                  <h1>SafeHer</h1>
                  <p>Your Personal Safety Companion</p>
                </div>
              </div>
              
              <div class="screen-content onboarding-content">
                <form id="onboarding-form" class="form-container">
                  <div class="form-group">
                    <label for="user-name">Your Name</label>
                    <input type="text" id="user-name" placeholder="Enter your name" required>
                  </div>
                  
                  <div class="form-group">
                    <label for="user-phone">Your Phone Number</label>
                    <input type="tel" id="user-phone" placeholder="Enter your phone number" required>
                  </div>
                  
                  <div class="divider-text"><span>Primary Emergency Contact</span></div>
                  
                  <div class="form-group">
                    <label for="primary-contact-name">Contact Name</label>
                    <input type="text" id="primary-contact-name" placeholder="e.g., Mom, Husband, Friend" required>
                  </div>
                  
                  <div class="form-group">
                    <label for="primary-contact-phone">Contact Phone Number</label>
                    <input type="tel" id="primary-contact-phone" placeholder="Emergency mobile number" required>
                  </div>
                  
                  <button type="submit" class="btn-primary" id="btn-finish-setup">
                    Complete Setup <i class="fa-solid fa-arrow-right"></i>
                  </button>
                </form>
              </div>
            </div>
            
            <!-- SCREEN 2: HOME DASHBOARD -->
            <div class="app-screen home-screen" id="screen-home">
              <div class="app-header-bar">
                <div class="user-greeting">
                  <p class="sub-greeting">Welcome back,</p>
                  <h3 id="display-user-name">User Name</h3>
                </div>
                <div class="system-status-indicator">
                  <span class="status-dot green" id="home-status-dot"></span>
                  <span class="status-lbl" id="home-status-lbl">System Ready</span>
                </div>
              </div>
              
              <div class="screen-content home-content">
                <!-- SOS Pulse Button Container -->
                <div class="sos-trigger-container">
                  <p class="sos-hint">DOUBLE TAP TO ACTIVATE SOS</p>
                  <button class="sos-button" id="sos-button">
                    <div class="sos-ring ring-1"></div>
                    <div class="sos-ring ring-2"></div>
                    <div class="sos-ring ring-3"></div>
                    <div class="sos-inner">
                      <span class="sos-text">SOS</span>
                      <span class="sos-sub-text">EMERGENCY</span>
                    </div>
                  </button>
                  <p class="sos-warning-desc">Instantly alerts family & calls primary contact</p>
                </div>
                
                <!-- Quick Navigation Grid -->
                <div class="quick-grid">
                  <button class="grid-card card-blue" id="btn-nav-map">
                    <div class="card-icon"><i class="fa-solid fa-map-location-dot"></i></div>
                    <div class="card-info">
                      <h4>Nearby Help</h4>
                      <p>Police & Hospitals</p>
                    </div>
                  </button>
                  
                  <button class="grid-card card-purple" id="btn-nav-contacts">
                    <div class="card-icon"><i class="fa-solid fa-user-shield"></i></div>
                    <div class="card-info">
                      <h4>My Contacts</h4>
                      <p>Emergency Network</p>
                    </div>
                  </button>
                  
                  <button class="grid-card card-teal" id="btn-nav-tracking">
                    <div class="card-icon"><i class="fa-solid fa-share-nodes"></i></div>
                    <div class="card-info">
                      <h4>Live Tracking</h4>
                      <p>Share Location Link</p>
                    </div>
                  </button>
                </div>
              </div>
            </div>
            
            <!-- SCREEN 3: MAP / NEARBY HELP -->
            <div class="app-screen map-screen" id="screen-map">
              <div class="app-header-bar flex-row">
                <button class="btn-back" id="map-back-btn"><i class="fa-solid fa-chevron-left"></i></button>
                <h3>Nearby Help</h3>
                <div style="width: 28px;"></div> <!-- Spacer for centering -->
              </div>
              
              <!-- Filter Tabs -->
              <div class="map-filters">
                <button class="filter-tab active" data-filter="police">
                  <i class="fa-solid fa-building-shield"></i> Police
                </button>
                <button class="filter-tab" data-filter="hospitals">
                  <i class="fa-solid fa-house-medical"></i> Hospitals
                </button>
              </div>
              
              <div class="map-container-wrapper">
                <div id="safety-map"></div>
                
                <!-- Slide up overlay with details about selected marker -->
                <div class="place-details-card" id="place-details-card">
                  <div class="card-handle"></div>
                  <div class="place-info">
                    <h4 id="place-name">Selected Station</h4>
                    <p id="place-address"><i class="fa-solid fa-location-dot"></i> Street address goes here</p>
                    <div class="place-stats">
                      <span id="place-distance"><i class="fa-solid fa-person-walking"></i> 0.5 km away</span>
                      <span id="place-phone"><i class="fa-solid fa-phone"></i> +1 800 123 456</span>
                    </div>
                  </div>
                  <div class="place-actions">
                    <a href="#" class="btn-primary" id="btn-get-directions">
                      <i class="fa-solid fa-diamond-turn-right"></i> Navigate
                    </a>
                    <a href="#" class="btn-secondary" id="btn-call-place">
                      <i class="fa-solid fa-phone"></i> Call
                    </a>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- SCREEN 4: CONTACTS MANAGEMENT -->
            <div class="app-screen contacts-screen" id="screen-contacts">
              <div class="app-header-bar flex-row">
                <button class="btn-back" id="contacts-back-btn"><i class="fa-solid fa-chevron-left"></i></button>
                <h3>Emergency Contacts</h3>
                <div style="width: 28px;"></div>
              </div>
              
              <div class="screen-content contacts-content">
                <div class="primary-contact-display" id="primary-contact-card">
                  <span class="badge-primary">PRIMARY CALL RECEIVER</span>
                  <div class="avatar-row">
                    <div class="contact-avatar"><i class="fa-solid fa-user-large"></i></div>
                    <div class="contact-meta">
                      <h4 id="pc-display-name">Name</h4>
                      <p id="pc-display-phone">Phone number</p>
                    </div>
                    <i class="fa-solid fa-star star-icon"></i>
                  </div>
                </div>
                
                <div class="contacts-list-container">
                  <div class="list-header">
                    <h4>Other Trusted Contacts</h4>
                    <span class="contact-count" id="contact-count">(0)</span>
                  </div>
                  <div class="contacts-list" id="contacts-list">
                    <!-- Dynamic contacts injected here -->
                  </div>
                </div>
                
                <button class="btn-add-contact" id="btn-show-add-contact-modal">
                  <i class="fa-solid fa-plus"></i> Add Trusted Contact
                </button>
              </div>
              
              <!-- Add Contact Slide Up Form -->
              <div class="add-contact-modal" id="add-contact-modal">
                <div class="modal-content-wrapper">
                  <div class="modal-header">
                    <h4>Add Contact</h4>
                    <button class="btn-close-modal" id="btn-close-contact-modal"><i class="fa-solid fa-xmark"></i></button>
                  </div>
                  <form id="add-contact-form">
                    <div class="form-group">
                      <label for="new-contact-name">Contact Name</label>
                      <input type="text" id="new-contact-name" placeholder="Enter contact name" required>
                    </div>
                    <div class="form-group">
                      <label for="new-contact-phone">Phone Number</label>
                      <input type="tel" id="new-contact-phone" placeholder="Enter mobile number" required>
                    </div>
                    <div class="form-group checkbox-group">
                      <input type="checkbox" id="set-as-primary">
                      <label for="set-as-primary">Set as Primary Emergency Contact</label>
                    </div>
                    <button type="submit" class="btn-primary">Save Contact</button>
                  </form>
                </div>
              </div>
            </div>
            
            <!-- SCREEN 5: OUTGOING CALL SCREEN (SOS ACTIVATION TRIGGERED) -->
            <div class="app-screen call-screen" id="screen-call">
              <div class="call-glow-effect"></div>
              
              <div class="call-header">
                <div class="sos-active-badge"><i class="fa-solid fa-triangle-exclamation"></i> SOS ACTIVE</div>
                <div class="call-timer" id="call-timer">00:00</div>
              </div>
              
              <div class="call-user-info">
                <div class="calling-avatar">
                  <i class="fa-solid fa-user"></i>
                  <div class="avatar-ripple r1"></div>
                  <div class="avatar-ripple r2"></div>
                </div>
                <h2 id="calling-contact-name">Primary Contact</h2>
                <p id="calling-status">Calling...</p>
                <div class="gps-dispatched">
                  <i class="fa-solid fa-location-crosshairs fa-spin"></i> GPS details dispatched via SMS
                </div>
              </div>
              
              <div class="call-controls">
                <div class="control-row">
                  <button class="call-btn-circle" disabled><i class="fa-solid fa-microphone-slash"></i><span>Mute</span></button>
                  <button class="call-btn-circle active" disabled><i class="fa-solid fa-volume-high"></i><span>Speaker</span></button>
                  <button class="call-btn-circle" disabled><i class="fa-solid fa-keyboard"></i><span>Keypad</span></button>
                </div>
                
                <button class="btn-hangup" id="btn-end-call">
                  <i class="fa-solid fa-phone-slash"></i>
                </button>
                <p class="end-call-hint">Tap to hang up and return home</p>
              </div>
            </div>
            
            <!-- SCREEN 6: LIVE TRACKING / SHARE SCREEN -->
            <div class="app-screen tracking-screen" id="screen-tracking">
              <div class="app-header-bar flex-row">
                <button class="btn-back" id="tracking-back-btn"><i class="fa-solid fa-chevron-left"></i></button>
                <h3>Location Sharing</h3>
                <div style="width: 28px;"></div>
              </div>
              
              <div class="screen-content tracking-content">
                <div class="tracking-status-card">
                  <div class="sharing-animation" id="sharing-animation">
                    <span class="ping-circle"></span>
                    <i class="fa-solid fa-share-nodes"></i>
                  </div>
                  <h4 id="tracking-title">GPS Sharing: Inactive</h4>
                  <p class="tracking-text" id="tracking-desc">Keep your loved ones informed. Share your real-time path updates.</p>
                </div>
                
                <div class="link-share-box">
                  <label>Shareable SafeHer Link</label>
                  <div class="input-copy-group">
                    <input type="text" id="share-link-input" value="https://safeher.live/track/usr9203" readonly>
                    <button id="btn-copy-link"><i class="fa-solid fa-copy"></i></button>
                  </div>
                </div>
                
                <div class="tracking-controls">
                  <button class="btn-primary" id="btn-toggle-share-active">
                    <i class="fa-solid fa-play"></i> Start Sharing Location
                  </button>
                </div>
                
                <div class="alert-box info-box">
                  <i class="fa-solid fa-circle-info"></i>
                  <p>When sharing is active, emergency contacts can open the link in any browser to watch your movement on a map in real-time.</p>
                </div>
              </div>
            </div>
            
            <!-- SOS TRIGGER COUNTDOWN MODAL OVERLAY -->
            <div class="countdown-modal" id="sos-countdown-modal">
              <div class="countdown-card">
                <h3>Calling Contact in</h3>
                <div class="countdown-number" id="countdown-number">5</div>
                <p>Alert SMS will be dispatched immediately and a phone call placed.</p>
                <button class="btn-cancel-sos" id="btn-cancel-sos">
                  CANCEL SOS
                </button>
              </div>
            </div>
            
            <!-- BOTTOM TAB NAVIGATION BAR (hidden on onboarding and calling screens) -->
            <nav class="bottom-nav" id="bottom-nav">
              <button class="nav-item active" data-target="screen-home">
                <i class="fa-solid fa-house"></i>
                <span>Home</span>
              </button>
              <button class="nav-item" data-target="screen-map">
                <i class="fa-solid fa-map-location-dot"></i>
                <span>Nearby</span>
              </button>
              <button class="nav-item" data-target="screen-contacts">
                <i class="fa-solid fa-user-shield"></i>
                <span>Contacts</span>
              </button>
              <button class="nav-item" data-target="screen-tracking">
                <i class="fa-solid fa-share-nodes"></i>
                <span>Share</span>
              </button>
            </nav>
            
            <!-- Home Swipe Bar for iOS styling -->
            <div class="phone-home-bar"></div>
            
          </div> <!-- App Body -->
        </div> <!-- Phone Screen -->
      </div> <!-- Phone Case -->
    </div> <!-- Phone Mockup -->
    
    <!-- Collapsible Simulation Control Center (Only visible/meaningful in browser for testing) -->
    <div class="simulation-panel collapsed" id="simulation-panel">
      <button class="sim-toggle-btn" id="sim-toggle-btn">
        <i class="fa-solid fa-gears"></i>
        <span>SIMULATOR</span>
      </button>
      
      <div class="sim-panel-content">
        <div class="sim-header">
          <h3>Simulation Control Panel</h3>
          <p>Test the app's location-based and emergency services below.</p>
        </div>
        
        <div class="sim-section">
          <h4><i class="fa-solid fa-location-crosshairs"></i> Set Mock Coordinates</h4>
          <p class="sim-desc">Changes the simulated phone GPS position. Safety search centers on this point.</p>
          <div class="sim-button-group">
            <button class="btn-sim-loc active" data-lat="40.7128" data-lng="-74.0060" data-city="New York City">New York</button>
            <button class="btn-sim-loc" data-lat="51.5074" data-lng="-0.1278" data-city="London">London</button>
            <button class="btn-sim-loc" data-lat="12.9716" data-lng="77.5946" data-city="Bangalore">Bangalore</button>
            <button class="btn-sim-loc" data-lat="-33.8688" data-lng="151.2093" data-city="Sydney">Sydney</button>
          </div>
          <div class="coords-display">
            <strong>City:</strong> <span id="sim-city-name">New York City</span><br>
            <strong>Lat:</strong> <span id="sim-lat">40.7128</span> | 
            <strong>Lng:</strong> <span id="sim-lng">-74.0060</span>
          </div>
        </div>
        
        <div class="sim-section">
          <h4><i class="fa-solid fa-person-walking-arrow-right"></i> Location Path Simulation</h4>
          <p class="sim-desc">Simulate traveling along a route to test the live tracking sharing updates.</p>
          <div class="sim-control-row">
            <button class="btn-sim-action" id="btn-sim-play-movement">
              <i class="fa-solid fa-play"></i> Start Walk
            </button>
            <button class="btn-sim-action btn-danger" id="btn-sim-reset-movement" disabled>
              <i class="fa-solid fa-rotate-left"></i> Reset
            </button>
          </div>
          <div class="sim-status-label">
            Status: <span id="sim-movement-status" class="status-inactive">Inactive</span>
          </div>
        </div>
        
        <div class="sim-section flex-grow">
          <h4><i class="fa-solid fa-network-wired"></i> Network Dispatch Logs</h4>
          <p class="sim-desc">Verifies SMS notifications and call outputs sent by SafeHer.</p>
          <div class="log-output-container" id="log-output">
            <div class="log-entry system">[SYSTEM] Simulator Ready. Setup emergency contacts to test SMS.</div>
          </div>
        </div>
      </div>
    </div>
    
  </div>

  <!-- Custom Javascript -->
  <script src="app.js"></script>
</body>
</html>
"""

# ----------------- style.css CONTENT -----------------
style_css = """/* ==========================================================================
   SafeHer Styling - Premium Theme and Responsive Smartphone Mockup
   ========================================================================== */

:root {
  /* Premium Dark Mode Colors */
  --bg-primary: #090D16;
  --bg-secondary: #121824;
  --bg-card: rgba(26, 34, 50, 0.75);
  --border-color: rgba(255, 255, 255, 0.08);
  
  --color-crimson: #FF3B30;
  --color-crimson-hover: #E03026;
  --color-green: #34C759;
  --color-blue: #007AFF;
  --color-purple: #AF52DE;
  --color-teal: #5AC8FA;
  --color-orange: #FF9500;
  
  --text-primary: #FFFFFF;
  --text-secondary: #8E9AA8;
  --text-muted: #566373;
  
  --font-display: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  
  --shadow-premium: 0 12px 30px rgba(0, 0, 0, 0.5), 0 4px 12px rgba(0, 0, 0, 0.3);
  --shadow-glow-red: 0 0 25px rgba(255, 59, 48, 0.6);
  --shadow-glass: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
  --radius-lg: 20px;
  --radius-md: 14px;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  -webkit-tap-highlight-color: transparent;
}

body {
  font-family: var(--font-body);
  background-color: #03060c;
  color: var(--text-primary);
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* App Wrapper for Layout Alignment */
.app-wrapper {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 40px;
  width: 100%;
  height: 100%;
  max-width: 1200px;
  padding: 20px;
  position: relative;
}

/* ==========================================================================
   Smartphone Mockup Frame
   ========================================================================== */
.phone-mockup {
  position: relative;
  width: 375px;
  height: 812px;
  background-color: #000;
  border-radius: 40px;
  padding: 12px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 0 0 0 4px #262930;
  flex-shrink: 0;
  overflow: hidden;
  z-index: 10;
}

.phone-case {
  position: relative;
  width: 100%;
  height: 100%;
  background-color: var(--bg-primary);
  border-radius: 32px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
  border: 1px solid rgba(255,255,255,0.05);
}

.phone-notch {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 150px;
  height: 25px;
  background-color: #000;
  border-bottom-left-radius: 18px;
  border-bottom-right-radius: 18px;
  z-index: 999;
}

.phone-screen {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.phone-status-bar {
  height: 38px;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  font-size: 12px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  z-index: 990;
  pointer-events: none;
  font-family: var(--font-body);
}

.status-icons {
  display: flex;
  gap: 6px;
  align-items: center;
}

.status-icons i {
  font-size: 11px;
}

.phone-home-bar {
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 5px;
  background-color: rgba(255, 255, 255, 0.35);
  border-radius: 3px;
  z-index: 999;
  pointer-events: none;
}

/* ==========================================================================
   Main Application Body & Screen Router
   ========================================================================== */
.app-body {
  flex: 1;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: calc(100% - 38px);
}

.app-screen {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  pointer-events: none;
  display: flex;
  flex-direction: column;
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1), transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform: scale(0.96);
  z-index: 1;
}

.app-screen.active {
  opacity: 1;
  pointer-events: auto;
  transform: scale(1);
  z-index: 5;
}

.screen-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  overflow-x: hidden;
  padding-bottom: 90px; /* Space for Bottom Nav */
}

/* Hide scrollbar for layout purity */
.screen-content::-webkit-scrollbar {
  width: 0px;
}

/* App Header Bar (Shared for inner views) */
.app-header-bar {
  padding: 15px 20px;
  background: linear-gradient(180deg, var(--bg-primary) 0%, rgba(9, 13, 22, 0.8) 100%);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 10;
}

.app-header-bar h3 {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.flex-row {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.btn-back {
  background: rgba(255, 255, 255, 0.08);
  border: none;
  color: var(--text-primary);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-back:hover {
  background: rgba(255, 255, 255, 0.15);
}

/* System status indicator */
.system-status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(52, 199, 89, 0.1);
  padding: 4px 10px;
  border-radius: 12px;
  border: 1px solid rgba(52, 199, 89, 0.2);
}

.system-status-indicator.sos-mode {
  background: rgba(255, 59, 48, 0.1);
  border: 1px solid rgba(255, 59, 48, 0.25);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-dot.green {
  background-color: var(--color-green);
  box-shadow: 0 0 8px var(--color-green);
}

.status-dot.red {
  background-color: var(--color-crimson);
  box-shadow: 0 0 8px var(--color-crimson);
  animation: heartBeat 1s infinite alternate;
}

.status-lbl {
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--color-green);
}

.system-status-indicator.sos-mode .status-lbl {
  color: var(--color-crimson);
}

/* ==========================================================================
   Screen 1: Onboarding / Setup
   ========================================================================== */
.onboarding-screen {
  background: linear-gradient(135deg, #090d16 0%, #06182c 100%);
  display: flex;
  flex-direction: column;
}

.onboarding-header {
  padding: 60px 20px 20px;
  text-align: center;
}

.shield-logo {
  font-size: 48px;
  color: var(--color-crimson);
  margin-bottom: 12px;
  filter: drop-shadow(0 0 15px rgba(255, 59, 48, 0.3));
}

.logo-area h1 {
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -0.5px;
  margin-bottom: 4px;
}

.logo-area p {
  color: var(--text-secondary);
  font-size: 14px;
}

.onboarding-content {
  display: flex;
  flex-direction: column;
  padding: 0 24px 40px;
  overflow-y: auto;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-secondary);
}

.form-group input[type="text"],
.form-group input[type="tel"] {
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  padding: 12px 16px;
  border-radius: var(--radius-md);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s, background-color 0.2s;
}

.form-group input:focus {
  border-color: var(--color-crimson);
  background-color: rgba(255, 255, 255, 0.08);
}

.divider-text {
  text-align: center;
  position: relative;
  margin: 15px 0 5px;
}

.divider-text::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 1px;
  background-color: var(--border-color);
  z-index: 1;
}

.divider-text span {
  position: relative;
  background-color: #080f1b;
  padding: 0 12px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-crimson);
  letter-spacing: 1px;
  z-index: 2;
}

.btn-primary {
  background: linear-gradient(135deg, var(--color-crimson) 0%, #D31A11 100%);
  color: #FFF;
  border: none;
  padding: 14px;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  box-shadow: var(--shadow-glow-red);
  transition: opacity 0.2s, transform 0.1s;
  font-family: var(--font-display);
}

.btn-primary:active {
  transform: scale(0.98);
}

/* ==========================================================================
   Screen 2: Home Dashboard
   ========================================================================== */
.home-screen {
  background-color: var(--bg-primary);
}

.user-greeting .sub-greeting {
  font-size: 12px;
  color: var(--text-secondary);
}

.user-greeting h3 {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
}

.home-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
  gap: 20px;
}

.sos-trigger-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 15px 0;
  position: relative;
}

.sos-hint {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: var(--text-secondary);
  margin-bottom: 15px;
  opacity: 0.8;
  animation: pulseOpacity 1.5s infinite alternate;
}

/* Glowing Pulse SOS Button */
.sos-button {
  position: relative;
  width: 170px;
  height: 170px;
  border-radius: 50%;
  border: none;
  outline: none;
  background: none;
  cursor: pointer;
  z-index: 10;
}

.sos-inner {
  position: absolute;
  top: 5px;
  left: 5px;
  right: 5px;
  bottom: 5px;
  background: radial-gradient(circle, var(--color-crimson) 0%, #B81810 100%);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4), inset 0 4px 10px rgba(255, 255, 255, 0.3);
  border: 4px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.1s;
}

.sos-button:active .sos-inner {
  transform: scale(0.95);
}

.sos-text {
  font-family: var(--font-display);
  font-size: 38px;
  font-weight: 900;
  letter-spacing: -0.5px;
  color: #FFFFFF;
  line-height: 1;
}

.sos-sub-text {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2px;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 4px;
}

/* Pulsing outer rings */
.sos-ring {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 50%;
  background-color: var(--color-crimson);
  opacity: 0;
  z-index: 1;
  pointer-events: none;
}

.ring-1 { animation: sosPulseRing 3s cubic-bezier(0.215, 0.61, 0.355, 1) infinite; }
.ring-2 { animation: sosPulseRing 3s cubic-bezier(0.215, 0.61, 0.355, 1) 1s infinite; }
.ring-3 { animation: sosPulseRing 3s cubic-bezier(0.215, 0.61, 0.355, 1) 2s infinite; }

.sos-warning-desc {
  font-size: 11px;
  color: var(--text-secondary);
  margin-top: 20px;
  text-align: center;
  max-width: 220px;
}

/* Quick Navigation Grid */
.quick-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
  width: 100%;
}

.grid-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  text-align: left;
  transition: transform 0.2s, border-color 0.2s, background-color 0.2s;
  width: 100%;
}

.grid-card:hover {
  border-color: rgba(255, 255, 255, 0.15);
  background-color: rgba(26, 34, 50, 0.9);
}

.grid-card:active {
  transform: scale(0.98);
}

.card-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
}

.card-blue .card-icon { background-color: rgba(0, 122, 255, 0.15); color: var(--color-blue); }
.card-purple .card-icon { background-color: rgba(175, 82, 222, 0.15); color: var(--color-purple); }
.card-teal .card-icon { background-color: rgba(90, 200, 250, 0.15); color: var(--color-teal); }

.card-info h4 {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.card-info p {
  font-size: 11px;
  color: var(--text-secondary);
}

/* ==========================================================================
   Screen 3: Map / Nearby Help
   ========================================================================== */
.map-filters {
  display: grid;
  grid-template-columns: 1fr 1fr;
  padding: 8px 12px;
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  z-index: 10;
  gap: 8px;
}

.filter-tab {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid transparent;
  color: var(--text-secondary);
  padding: 8px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.filter-tab.active {
  background-color: rgba(0, 122, 255, 0.15);
  color: var(--color-blue);
  border-color: rgba(0, 122, 255, 0.25);
}

.map-container-wrapper {
  flex: 1;
  position: relative;
  width: 100%;
  height: 100%;
}

#safety-map {
  width: 100%;
  height: 100%;
  background-color: #0d121c;
}

/* Override Leaflet Dark styles */
.leaflet-container {
  font-family: var(--font-body);
}

/* Place details overlay slide-up */
.place-details-card {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--bg-secondary);
  border-top-left-radius: var(--radius-lg);
  border-top-right-radius: var(--radius-lg);
  border-top: 1px solid var(--border-color);
  padding: 16px;
  box-shadow: 0 -8px 24px rgba(0, 0, 0, 0.4);
  z-index: 1000;
  transform: translateY(105%);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.place-details-card.active {
  transform: translateY(0);
}

.card-handle {
  width: 40px;
  height: 4px;
  background-color: rgba(255, 255, 255, 0.15);
  border-radius: 2px;
  margin: -8px auto 12px;
}

.place-info h4 {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 4px;
}

.place-address {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.place-stats {
  display: flex;
  gap: 15px;
  font-size: 11px;
  color: var(--text-muted);
  margin: 8px 0 16px;
}

.place-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.place-actions {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 10px;
}

.place-actions a {
  text-decoration: none;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  padding: 10px;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  transition: background-color 0.2s;
  font-family: var(--font-display);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.12);
}

/* Custom map marker styles */
.user-marker {
  width: 14px;
  height: 14px;
  background-color: var(--color-blue);
  border: 2px solid #FFFFFF;
  border-radius: 50%;
  box-shadow: 0 0 10px var(--color-blue);
}

/* ==========================================================================
   Screen 4: Contacts Management
   ========================================================================== */
.contacts-screen {
  background-color: var(--bg-primary);
}

.contacts-content {
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.primary-contact-display {
  background: linear-gradient(135deg, rgba(255, 59, 48, 0.15) 0%, rgba(26, 34, 50, 0.4) 100%);
  border: 1px solid rgba(255, 59, 48, 0.25);
  border-radius: var(--radius-lg);
  padding: 16px;
  position: relative;
  box-shadow: var(--shadow-glass);
}

.badge-primary {
  position: absolute;
  top: -8px;
  right: 16px;
  background-color: var(--color-crimson);
  color: #fff;
  font-size: 9px;
  font-weight: 800;
  padding: 2px 8px;
  border-radius: 8px;
  letter-spacing: 0.5px;
}

.avatar-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.contact-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
}

.primary-contact-display .contact-avatar {
  border-color: rgba(255, 59, 48, 0.3);
  color: var(--color-crimson);
  background: rgba(255, 59, 48, 0.1);
}

.contact-meta h4 {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
}

.contact-meta p {
  font-size: 13px;
  color: var(--text-secondary);
}

.star-icon {
  margin-left: auto;
  color: var(--color-crimson);
  font-size: 18px;
}

.contacts-list-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.list-header h4 {
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-secondary);
}

.contact-count {
  font-size: 12px;
  color: var(--text-muted);
}

.contacts-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.contact-card {
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 12px 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  transition: background-color 0.2s;
}

.contact-card:hover {
  background-color: rgba(26, 34, 50, 0.9);
}

.card-actions {
  margin-left: auto;
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 14px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s;
}

.btn-icon:hover {
  background-color: rgba(255, 255, 255, 0.08);
  color: var(--text-primary);
}

.btn-icon.delete:hover {
  color: var(--color-crimson);
  background-color: rgba(255, 59, 48, 0.1);
}

.btn-add-contact {
  background-color: rgba(255, 255, 255, 0.04);
  border: 1px dashed var(--border-color);
  color: var(--text-secondary);
  padding: 12px;
  border-radius: var(--radius-md);
  font-family: var(--font-display);
  font-weight: 600;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-add-contact:hover {
  background-color: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.2);
  color: var(--text-primary);
}

/* Add Contact modal */
.add-contact-modal {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(3, 6, 12, 0.7);
  backdrop-filter: blur(8px);
  z-index: 100;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s;
  display: flex;
  align-items: flex-end;
}

.add-contact-modal.active {
  opacity: 1;
  pointer-events: auto;
}

.modal-content-wrapper {
  width: 100%;
  background-color: var(--bg-secondary);
  border-top-left-radius: var(--radius-lg);
  border-top-right-radius: var(--radius-lg);
  border-top: 1px solid var(--border-color);
  padding: 24px;
  transform: translateY(100%);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.add-contact-modal.active .modal-content-wrapper {
  transform: translateY(0);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h4 {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
}

.btn-close-modal {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 20px;
  cursor: pointer;
}

.checkbox-group {
  flex-direction: row;
  align-items: center;
  gap: 10px;
  margin: 5px 0 15px;
}

.checkbox-group input {
  width: 18px;
  height: 18px;
  accent-color: var(--color-crimson);
}

.checkbox-group label {
  font-size: 13px;
  color: var(--text-primary);
  text-transform: none;
  letter-spacing: 0px;
  cursor: pointer;
}

/* ==========================================================================
   Screen 5: Outgoing Call Interface (SOS Activated)
   ========================================================================== */
.call-screen {
  background: radial-gradient(circle at center, #1b0a0a 0%, #090303 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 40px 24px 60px;
  z-index: 100;
}

.call-glow-effect {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at top, rgba(255, 59, 48, 0.15) 0%, transparent 70%);
  z-index: 1;
  pointer-events: none;
}

.call-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  z-index: 5;
}

.sos-active-badge {
  background-color: rgba(255, 59, 48, 0.2);
  color: var(--color-crimson);
  border: 1px solid rgba(255, 59, 48, 0.4);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 1px;
  padding: 4px 12px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  animation: pulseOpacity 1s infinite alternate;
}

.call-timer {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 500;
  color: #fff;
  opacity: 0.9;
}

.call-user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 5;
}

.calling-avatar {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 40px;
  color: #FFF;
  margin-bottom: 24px;
}

.avatar-ripple {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 50%;
  border: 2px solid rgba(255, 59, 48, 0.35);
  opacity: 0;
  pointer-events: none;
}

.r1 { animation: callRipple 2s infinite; }
.r2 { animation: callRipple 2s infinite 1s; }

.call-user-info h2 {
  font-family: var(--font-display);
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 6px;
  text-align: center;
}

.call-user-info p {
  color: var(--text-secondary);
  font-size: 14px;
}

.gps-dispatched {
  background: rgba(0, 122, 255, 0.12);
  border: 1px solid rgba(0, 122, 255, 0.2);
  color: var(--color-blue);
  padding: 6px 14px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 15px;
}

.call-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
  z-index: 5;
}

.control-row {
  display: flex;
  justify-content: center;
  gap: 30px;
}

.call-btn-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  border: none;
  color: #FFF;
  font-size: 18px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: not-allowed;
  opacity: 0.6;
}

.call-btn-circle span {
  font-size: 9px;
  margin-top: 6px;
  opacity: 0.8;
  font-family: var(--font-body);
}

.call-btn-circle.active {
  background: rgba(255, 255, 255, 0.2);
  opacity: 1;
}

.btn-hangup {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  background-color: var(--color-crimson);
  border: none;
  color: #FFF;
  font-size: 28px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: 0 10px 25px rgba(255, 59, 48, 0.4);
  transition: transform 0.2s, background-color 0.2s;
}

.btn-hangup:active {
  transform: scale(0.9);
  background-color: var(--color-crimson-hover);
}

.end-call-hint {
  font-size: 11px;
  color: var(--text-muted);
}

/* ==========================================================================
   Screen 6: Live Location Tracking
   ========================================================================== */
.tracking-screen {
  background-color: var(--bg-primary);
}

.tracking-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.tracking-status-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  box-shadow: var(--shadow-glass);
}

.sharing-animation {
  position: relative;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  transition: all 0.3s;
}

.sharing-animation.active {
  color: var(--color-green);
  border-color: rgba(52, 199, 89, 0.3);
  background-color: rgba(52, 199, 89, 0.1);
}

.ping-circle {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 50%;
  border: 2px solid rgba(52, 199, 89, 0.5);
  opacity: 0;
  display: none;
}

.sharing-animation.active .ping-circle {
  display: block;
  animation: callRipple 1.5s infinite;
}

.tracking-status-card h4 {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
}

.tracking-text {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.link-share-box {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.link-share-box label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-secondary);
}

.input-copy-group {
  display: flex;
  background-color: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.input-copy-group input {
  flex: 1;
  background: none;
  border: none;
  color: var(--text-primary);
  padding: 12px 14px;
  font-size: 12px;
  outline: none;
  font-family: var(--font-body);
}

.input-copy-group button {
  background-color: rgba(255, 255, 255, 0.06);
  border: none;
  border-left: 1px solid var(--border-color);
  color: var(--text-primary);
  width: 46px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.input-copy-group button:hover {
  background-color: rgba(255, 255, 255, 0.12);
}

.alert-box {
  display: flex;
  gap: 12px;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  font-size: 12px;
  line-height: 1.5;
}

.info-box {
  background-color: rgba(0, 122, 255, 0.08);
  border: 1px solid rgba(0, 122, 255, 0.15);
  color: var(--text-secondary);
}

.info-box i {
  color: var(--color-blue);
  font-size: 15px;
  margin-top: 1px;
}

/* ==========================================================================
   SOS Countdown Modal Overlays
   ========================================================================== */
.countdown-modal {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(3, 6, 12, 0.85);
  backdrop-filter: blur(12px);
  z-index: 900;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s;
}

.countdown-modal.active {
  opacity: 1;
  pointer-events: auto;
}

.countdown-card {
  background-color: var(--bg-secondary);
  border: 1px solid rgba(255, 59, 48, 0.2);
  border-radius: var(--radius-lg);
  padding: 30px 24px;
  width: 85%;
  text-align: center;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6);
  transform: scale(0.9);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.countdown-modal.active .countdown-card {
  transform: scale(1);
}

.countdown-card h3 {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 15px;
}

.countdown-number {
  font-family: var(--font-display);
  font-size: 72px;
  font-weight: 800;
  color: var(--color-crimson);
  text-shadow: 0 0 15px rgba(255, 59, 48, 0.3);
  margin: 10px 0 15px;
  line-height: 1;
}

.countdown-card p {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: 24px;
}

.btn-cancel-sos {
  background-color: rgba(255, 255, 255, 0.08);
  border: 1px solid var(--border-color);
  color: #FFF;
  width: 100%;
  padding: 12px;
  border-radius: var(--radius-md);
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-cancel-sos:hover {
  background-color: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.2);
}

/* ==========================================================================
   Bottom Tab Navigation Bar
   ========================================================================== */
.bottom-nav {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 70px;
  background-color: rgba(18, 24, 36, 0.85);
  backdrop-filter: blur(20px);
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding-bottom: 12px; /* Leaves room for iOS Home Bar */
  z-index: 100;
  transition: transform 0.2s;
}

.nav-item {
  background: none;
  border: none;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  width: 60px;
  font-family: var(--font-body);
  transition: color 0.2s;
}

.nav-item i {
  font-size: 18px;
}

.nav-item span {
  font-size: 9px;
  font-weight: 500;
}

.nav-item.active {
  color: var(--color-blue);
}

/* ==========================================================================
   Animations
   ========================================================================== */
@keyframes sosPulseRing {
  0% { transform: scale(0.95); opacity: 0.6; }
  100% { transform: scale(2.2); opacity: 0; }
}

@keyframes callRipple {
  0% { transform: scale(1); opacity: 0.8; }
  100% { transform: scale(1.8); opacity: 0; }
}

@keyframes pulseOpacity {
  0% { opacity: 0.5; }
  100% { opacity: 1; }
}

@keyframes heartBeat {
  0% { transform: scale(1); }
  50% { transform: scale(1.15); }
  100% { transform: scale(1); }
}

/* ==========================================================================
   Simulation Control Panel (Side Drawer)
   ========================================================================== */
.simulation-panel {
  position: relative;
  width: 380px;
  height: 812px;
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-premium);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 9;
}

.sim-toggle-btn {
  display: none; /* Only used on mobile layout, hidden on desktop side-by-side */
}

.sim-panel-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 24px;
}

.sim-header {
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 16px;
  margin-bottom: 20px;
}

.sim-header h3 {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.sim-header p {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.sim-section {
  margin-bottom: 24px;
}

.sim-section h4 {
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--text-primary);
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.sim-desc {
  font-size: 11px;
  color: var(--text-secondary);
  margin-bottom: 12px;
  line-height: 1.4;
}

.sim-button-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 12px;
}

.btn-sim-loc {
  background-color: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: 8px;
  font-size: 11px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-sim-loc:hover {
  background-color: rgba(255, 255, 255, 0.08);
  color: var(--text-primary);
}

.btn-sim-loc.active {
  background-color: rgba(0, 122, 255, 0.12);
  color: var(--color-blue);
  border-color: rgba(0, 122, 255, 0.25);
}

.coords-display {
  background-color: rgba(0, 0, 0, 0.25);
  border-radius: 8px;
  padding: 8px 12px;
  font-family: monospace;
  font-size: 11px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.sim-control-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 10px;
}

.btn-sim-action {
  background-color: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  padding: 10px;
  font-size: 12px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.btn-sim-action:hover:not(:disabled) {
  background-color: rgba(255, 255, 255, 0.12);
}

.btn-sim-action.btn-danger {
  color: var(--color-crimson);
}

.btn-sim-action.btn-danger:hover:not(:disabled) {
  background-color: rgba(255, 59, 48, 0.12);
}

.btn-sim-action:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.sim-status-label {
  font-size: 11px;
  color: var(--text-secondary);
}

.sim-status-label span {
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
}

.status-inactive { background-color: rgba(255, 255, 255, 0.08); color: var(--text-secondary); }
.status-active { background-color: rgba(52, 199, 89, 0.15); color: var(--color-green); }

.flex-grow {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.log-output-container {
  flex: 1;
  background-color: #03060c;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 12px;
  font-family: monospace;
  font-size: 11px;
  line-height: 1.5;
  overflow-y: auto;
  color: #c4d1e2;
  min-height: 150px;
  max-height: 280px;
}

.log-entry {
  margin-bottom: 8px;
  padding-bottom: 6px;
  border-bottom: 1px dashed rgba(255,255,255,0.03);
  word-break: break-all;
}

.log-entry.system { color: #8e9aa8; }
.log-entry.sms { color: #ffbc42; }
.log-entry.call { color: #34c759; }
.log-entry.location { color: #007aff; }

/* ==========================================================================
   Responsive Adaptations
   ========================================================================== */
@media (max-width: 820px) {
  .app-wrapper {
    flex-direction: column;
    padding: 0;
    gap: 0;
    height: 100vh;
    width: 100vw;
  }
  
  .phone-mockup {
    width: 100%;
    height: 100%;
    border-radius: 0;
    padding: 0;
    box-shadow: none;
  }
  
  .phone-case {
    border-radius: 0;
    border: none;
  }
  
  .phone-notch, .phone-home-bar {
    display: none;
  }
  
  .phone-status-bar {
    padding: 10px 16px 0;
    height: 44px;
    background-color: var(--bg-primary);
  }
  
  /* Mobile Floating simulation toggle */
  .simulation-panel {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 60%;
    z-index: 1001;
    transform: translateY(100%);
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    border-bottom: none;
  }
  
  .simulation-panel.expanded {
    transform: translateY(0);
  }
  
  .sim-toggle-btn {
    display: flex;
    position: absolute;
    top: -50px;
    right: 20px;
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    color: var(--text-primary);
    padding: 8px 16px;
    border-radius: 20px 20px 0 0;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    align-items: center;
    gap: 6px;
    z-index: 1002;
    border-bottom: none;
  }
}
"""

# ----------------- app.js CONTENT -----------------
app_js = """/* ==========================================================================
   SafeHer Core Application Logic
   ========================================================================== */

// --- GLOBAL APPLICATION STATE ---
const state = {
  user: null, // { name, phone }
  contacts: [], // Array of { id, name, phone, isPrimary }
  currentCoords: { lat: 40.7128, lng: -74.0060, city: 'New York City' }, // Default
  isSharingLocation: false,
  isSOSActive: false,
  countdownTimer: null,
  callTimer: null,
  callSeconds: 0,
  pathSimulationInterval: null,
  pathIndex: 0,
  mockPath: [],
  map: null,
  userMarker: null,
  placesMarkers: [],
  navigationRoute: null
};

// --- MOCK DATABASE OF PLACES ---
const nearbyPlacesData = {
  'New York City': {
    police: [
      { name: "Midtown South Precinct", lat: 40.7516, lng: -73.9892, address: "357 W 35th St, New York", phone: "+1 212-695-3811" },
      { name: "17th Precinct Police Station", lat: 40.7562, lng: -73.9710, address: "167 E 51st St, New York", phone: "+1 212-826-3211" },
      { name: "Precinct 14 Police Station", lat: 40.7505, lng: -73.9909, address: "234 W 35th St, New York", phone: "+1 212-239-1800" }
    ],
    hospitals: [
      { name: "Mount Sinai West Emergency Room", lat: 40.7690, lng: -73.9875, address: "1000 10th Ave, New York", phone: "+1 212-523-4000" },
      { name: "NYU Langone Health Emergency", lat: 40.7423, lng: -73.9739, address: "550 1st Ave, New York", phone: "+1 212-263-5555" },
      { name: "Bellevue Hospital Emergency", lat: 40.7385, lng: -73.9750, address: "462 1st Ave, New York", phone: "+1 212-562-4141" }
    ]
  },
  'London': {
    police: [
      { name: "Charing Cross Police Station", lat: 51.5085, lng: -0.1261, address: "Agar St, London WC2N 4JP", phone: "+44 20 7240 1212" },
      { name: "Belgravia Police Station", lat: 51.4988, lng: -0.1502, address: "202-206 Buckingham Palace Rd, London", phone: "+44 20 7730 1212" }
    ],
    hospitals: [
      { name: "St Thomas' Hospital Emergency", lat: 51.4989, lng: -0.1182, address: "Westminster Bridge Rd, London SE1 7EH", phone: "+44 20 7188 7188" },
      { name: "University College Hospital A&E", lat: 51.5249, lng: -0.1340, address: "235 Euston Rd, London NW1 2BU", phone: "+44 20 3456 7890" }
    ]
  },
  'Bangalore': {
    police: [
      { name: "Cubbon Park Police Station", lat: 12.9779, lng: 77.5952, address: "Kasturba Rd, Shanthala Nagar, Bangalore", phone: "+91 80 2294 2583" },
      { name: "High Grounds Police Station", lat: 12.9904, lng: 77.5901, address: "Millers Rd, Vasanth Nagar, Bangalore", phone: "+91 80 2294 2581" }
    ],
    hospitals: [
      { name: "Mallya Hospital Emergency Care", lat: 12.9691, lng: 77.5960, address: "2 Vittal Mallya Rd, Bangalore", phone: "+91 80 2227 7979" },
      { name: "Fortis Hospital Emergency", lat: 12.9926, lng: 77.5977, address: "Cunningham Rd, Vasanth Nagar, Bangalore", phone: "+91 80 4199 4444" }
    ]
  },
  'Sydney': {
    police: [
      { name: "Sydney City Police Station", lat: -33.8762, lng: 151.2045, address: "192 Day St, Sydney NSW 2000", phone: "+61 2 9265 6499" },
      { name: "Surry Hills Police Station", lat: -33.8860, lng: 151.2110, address: "31-43 Goulburn St, Surry Hills", phone: "+61 2 9265 4122" }
    ],
    hospitals: [
      { name: "St Vincent's Hospital Emergency", lat: -33.8795, lng: 151.2205, address: "390 Victoria St, Darlinghurst NSW 2010", phone: "+61 2 8382 1111" },
      { name: "Sydney Hospital Emergency Dept", lat: -33.8679, lng: 151.2132, address: "8 Macquarie St, Sydney NSW 2000", phone: "+61 2 9382 7111" }
    ]
  }
};

// --- INITIALIZE APP ON LOAD ---
document.addEventListener('DOMContentLoaded', () => {
  initStatusBarTime();
  loadStateFromStorage();
  initAppRouter();
  initFormListeners();
  initSimulatorControls();
  
  // Render layout depending on whether user is logged in
  if (state.user) {
    document.getElementById('display-user-name').textContent = state.user.name;
    showScreen('screen-home');
  } else {
    showScreen('screen-onboarding');
  }
});

// --- CLOCK STATUS BAR ---
function initStatusBarTime() {
  const timeEl = document.getElementById('status-time');
  const updateClock = () => {
    const now = new Date();
    let hours = now.getHours();
    let minutes = now.getMinutes();
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    timeEl.textContent = `${hours}:${minutes}`;
  };
  updateClock();
  setInterval(updateClock, 60000);
}

// --- STATE STORAGE ---
function loadStateFromStorage() {
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
}

function saveContactsToStorage() {
  localStorage.setItem('safeher_contacts', JSON.stringify(state.contacts));
}

// --- ROUTER (SPA VISIBILITY) ---
function initAppRouter() {
  // Navigation Tabs at the bottom
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      const target = item.getAttribute('data-target');
      showScreen(target);
    });
  });

  // Action button routing on home screen
  document.getElementById('btn-nav-map').addEventListener('click', () => showScreen('screen-map'));
  document.getElementById('btn-nav-contacts').addEventListener('click', () => showScreen('screen-contacts'));
  document.getElementById('btn-nav-tracking').addEventListener('click', () => showScreen('screen-tracking'));

  // Back buttons
  document.getElementById('map-back-btn').addEventListener('click', () => showScreen('screen-home'));
  document.getElementById('contacts-back-btn').addEventListener('click', () => showScreen('screen-home'));
  document.getElementById('tracking-back-btn').addEventListener('click', () => showScreen('screen-home'));
}

function showScreen(screenId) {
  // Prevent changes while calling
  if (state.isSOSActive && screenId !== 'screen-call') {
    return;
  }

  document.querySelectorAll('.app-screen').forEach(s => s.classList.remove('active'));
  document.getElementById(screenId).classList.add('active');
  
  const bottomNav = document.getElementById('bottom-nav');
  if (screenId === 'screen-onboarding' || screenId === 'screen-call') {
    bottomNav.style.display = 'none';
  } else {
    bottomNav.style.display = 'flex';
    // Highlight correct icon
    document.querySelectorAll('.nav-item').forEach(item => {
      if (item.getAttribute('data-target') === screenId) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });
  }

  // Screen specific hooks
  if (screenId === 'screen-map') {
    initLeafletMap();
  } else if (screenId === 'screen-contacts') {
    renderContactsList();
  } else if (screenId === 'screen-tracking') {
    renderTrackingState();
  }
}

// --- FORMS & CONTACTS MANAGEMENT ---
function initFormListeners() {
  // Onboarding Setup Form
  const onboardingForm = document.getElementById('onboarding-form');
  onboardingForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const nameVal = document.getElementById('user-name').value;
    const phoneVal = document.getElementById('user-phone').value;
    
    const pcName = document.getElementById('primary-contact-name').value;
    const pcPhone = document.getElementById('primary-contact-phone').value;

    state.user = { name: nameVal, phone: phoneVal };
    localStorage.setItem('safeher_user', JSON.stringify(state.user));

    // Clear and set primary contact
    state.contacts = [
      { id: Date.now().toString(), name: pcName, phone: pcPhone, isPrimary: true }
    ];
    saveContactsToStorage();

    // Update greeting
    document.getElementById('display-user-name').textContent = nameVal;
    
    // Add simulator log
    addSimLog(`User registration complete: ${nameVal} (${phoneVal})`, 'system');
    addSimLog(`Primary emergency contact set to: ${pcName} (${pcPhone})`, 'system');

    showScreen('screen-home');
  });

  // Modal display listeners
  const addModal = document.getElementById('add-contact-modal');
  document.getElementById('btn-show-add-contact-modal').addEventListener('click', () => {
    addModal.classList.add('active');
  });

  const closeModal = () => {
    addModal.classList.remove('active');
    document.getElementById('add-contact-form').reset();
  };

  document.getElementById('btn-close-contact-modal').addEventListener('click', closeModal);

  // Add Contact Form Submit
  const addContactForm = document.getElementById('add-contact-form');
  addContactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('new-contact-name').value;
    const phone = document.getElementById('new-contact-phone').value;
    const isPrimary = document.getElementById('set-as-primary').checked;

    if (isPrimary) {
      // Demote existing primary contact
      state.contacts.forEach(c => c.isPrimary = false);
    }

    const newContact = {
      id: Date.now().toString(),
      name: name,
      phone: phone,
      isPrimary: isPrimary
    };

    state.contacts.push(newContact);
    saveContactsToStorage();
    renderContactsList();
    closeModal();
    addSimLog(`Added emergency contact: ${name} (${phone})`, 'system');
  });
}

function renderContactsList() {
  const primaryCard = document.getElementById('primary-contact-card');
  const contactsList = document.getElementById('contacts-list');
  const countSpan = document.getElementById('contact-count');

  // Find primary
  const primaryContact = state.contacts.find(c => c.isPrimary);
  if (primaryContact) {
    document.getElementById('pc-display-name').textContent = primaryContact.name;
    document.getElementById('pc-display-phone').textContent = primaryContact.phone;
    primaryCard.style.display = 'block';
  } else {
    primaryCard.style.display = 'none';
  }

  // Find others
  const others = state.contacts.filter(c => !c.isPrimary);
  countSpan.textContent = `(${others.length})`;
  contactsList.innerHTML = '';

  if (others.length === 0) {
    contactsList.innerHTML = `<div class="empty-list-desc">No secondary contacts added. Click below to expand your safety network.</div>`;
  } else {
    others.forEach(c => {
      const card = document.createElement('div');
      card.className = 'contact-card';
      card.innerHTML = `
        <div class="contact-avatar"><i class="fa-solid fa-user"></i></div>
        <div class="contact-meta">
          <h4>${c.name}</h4>
          <p>${c.phone}</p>
        </div>
        <div class="card-actions">
          <button class="btn-icon make-primary" data-id="${c.id}" title="Set as primary"><i class="fa-solid fa-star"></i></button>
          <button class="btn-icon delete" data-id="${c.id}" title="Delete contact"><i class="fa-solid fa-trash-can"></i></button>
        </div>
      `;

      // Set primary click
      card.querySelector('.make-primary').addEventListener('click', () => {
        state.contacts.forEach(temp => temp.isPrimary = (temp.id === c.id));
        saveContactsToStorage();
        renderContactsList();
        addSimLog(`Promoted ${c.name} to Primary Call Receiver`, 'system');
      });

      // Delete click
      card.querySelector('.delete').addEventListener('click', () => {
        state.contacts = state.contacts.filter(temp => temp.id !== c.id);
        saveContactsToStorage();
        renderContactsList();
        addSimLog(`Removed contact: ${c.name}`, 'system');
      });

      contactsList.appendChild(card);
    });
  }
}

// --- SOS TRIGGER SEQUENCE ---
const sosButton = document.getElementById('sos-button');
let doubleTapTimeout = null;

// Double tap detector
sosButton.addEventListener('click', () => {
  if (doubleTapTimeout === null) {
    doubleTapTimeout = setTimeout(() => {
      doubleTapTimeout = null;
    }, 300); // 300ms window
  } else {
    clearTimeout(doubleTapTimeout);
    doubleTapTimeout = null;
    triggerSOSCountdown();
  }
});

function triggerSOSCountdown() {
  const modal = document.getElementById('sos-countdown-modal');
  const countEl = document.getElementById('countdown-number');
  modal.classList.add('active');
  
  let countdownVal = 5;
  countEl.textContent = countdownVal;

  state.countdownTimer = setInterval(() => {
    countdownVal--;
    countEl.textContent = countdownVal;

    if (countdownVal <= 0) {
      clearInterval(state.countdownTimer);
      modal.classList.remove('active');
      activateSOS();
    }
  }, 1000);
}

document.getElementById('btn-cancel-sos').addEventListener('click', () => {
  if (state.countdownTimer) {
    clearInterval(state.countdownTimer);
    state.countdownTimer = null;
  }
  document.getElementById('sos-countdown-modal').classList.remove('active');
  addSimLog("SOS Sequence Cancelled by user.", "system");
});

function activateSOS() {
  state.isSOSActive = true;
  
  // Update indicator UI
  const statusDot = document.getElementById('home-status-dot');
  const statusLbl = document.getElementById('home-status-lbl');
  const statusInd = document.querySelector('.system-status-indicator');
  
  if (statusDot && statusLbl && statusInd) {
    statusDot.className = "status-dot red";
    statusLbl.textContent = "SOS ACTIVE";
    statusInd.classList.add('sos-mode');
  }

  // 1. Get primary contact
  const primaryContact = state.contacts.find(c => c.isPrimary) || { name: 'Emergency Services', phone: '911' };
  
  // 2. Dispatch simulated GPS SMS to all contacts
  const mapLink = `https://safeher.live/track/usr9203?lat=${state.currentCoords.lat.toFixed(5)}&lng=${state.currentCoords.lng.toFixed(5)}`;
  const smsBody = `SAFEHER SOS ALERT! I need help. My current location is: ${mapLink}`;
  
  state.contacts.forEach(contact => {
    addSimLog(`[SMS SENT] To: ${contact.name} (${contact.phone}) - Msg: "${smsBody}"`, 'sms');
  });

  // 3. Initiate actual/mock phone call to primary contact
  addSimLog(`[CALL OUTGOING] Dialing Primary Contact: ${primaryContact.name} (${primaryContact.phone})`, 'call');
  
  // Inside the browser/webview, trigger tel link to open native system dialer
  const dialerHref = `tel:${primaryContact.phone.replace(/[^+\d]/g, '')}`;
  
  // Render call UI overlay inside mockup
  document.getElementById('calling-contact-name').textContent = primaryContact.name;
  document.getElementById('calling-status').textContent = "Calling...";
  showScreen('screen-call');

  // Start Call Timer
  state.callSeconds = 0;
  document.getElementById('call-timer').textContent = "00:00";
  
  // Simulate call connection after 3 seconds
  let connectTimeout = setTimeout(() => {
    document.getElementById('calling-status').textContent = "Connected (0:00)";
    addSimLog(`[CALL CONNECTED] Emergency line active with ${primaryContact.name}`, 'call');
    
    state.callTimer = setInterval(() => {
      state.callSeconds++;
      let mins = Math.floor(state.callSeconds / 60);
      let secs = state.callSeconds % 60;
      mins = mins < 10 ? '0' + mins : mins;
      secs = secs < 10 ? '0' + secs : secs;
      
      document.getElementById('call-timer').textContent = `${mins}:${secs}`;
      document.getElementById('calling-status').textContent = `Connected (${mins}:${secs})`;
    }, 1000);
  }, 3000);

  // Bind hang up action
  const endCallBtn = document.getElementById('btn-end-call');
  const handleHangup = () => {
    clearTimeout(connectTimeout);
    if (state.callTimer) {
      clearInterval(state.callTimer);
      state.callTimer = null;
    }
    
    state.isSOSActive = false;
    addSimLog(`[CALL DISCONNECTED] Call duration: ${state.callSeconds} seconds`, 'call');
    
    // Reset home indicators
    if (statusDot && statusLbl && statusInd) {
      statusDot.className = "status-dot green";
      statusLbl.textContent = "System Ready";
      statusInd.classList.remove('sos-mode');
    }
    
    showScreen('screen-home');
    endCallBtn.removeEventListener('click', handleHangup);
  };
  
  endCallBtn.addEventListener('click', handleHangup);
  
  // Trigger system link (does not block JS thread, opens dialer asynchronously)
  window.location.href = dialerHref;
}

// --- LIVE SHARER STATE ---
function renderTrackingState() {
  const shareBtn = document.getElementById('btn-toggle-share-active');
  const anim = document.getElementById('sharing-animation');
  const title = document.getElementById('tracking-title');
  const desc = document.getElementById('tracking-desc');
  const linkInput = document.getElementById('share-link-input');

  const updateLink = () => {
    linkInput.value = `https://safeher.live/track/usr9203?lat=${state.currentCoords.lat.toFixed(5)}&lng=${state.currentCoords.lng.toFixed(5)}&city=${encodeURIComponent(state.currentCoords.city)}`;
  };
  updateLink();

  if (state.isSharingLocation) {
    shareBtn.innerHTML = `<i class="fa-solid fa-stop"></i> Stop Sharing Location`;
    shareBtn.className = "btn-secondary";
    anim.classList.add('active');
    title.textContent = "GPS Sharing: ACTIVE";
    desc.innerHTML = `Your location link is actively broadcasting. Move coordinates in the Simulator to watch updates.`;
  } else {
    shareBtn.innerHTML = `<i class="fa-solid fa-play"></i> Start Sharing Location`;
    shareBtn.className = "btn-primary";
    anim.classList.remove('active');
    title.textContent = "GPS Sharing: Inactive";
    desc.textContent = `Keep your loved ones informed. Share your real-time path updates.`;
  }

  // Start Sharing Toggle
  shareBtn.onclick = () => {
    state.isSharingLocation = !state.isSharingLocation;
    if (state.isSharingLocation) {
      addSimLog(`Location sharing enabled by user. Shared Link: ${linkInput.value}`, 'location');
    } else {
      addSimLog(`Location sharing disabled by user. Broadcast stopped.`, 'location');
    }
    renderTrackingState();
  };

  // Copy Link
  document.getElementById('btn-copy-link').onclick = () => {
    linkInput.select();
    navigator.clipboard.writeText(linkInput.value);
    
    const copyBtn = document.getElementById('btn-copy-link');
    copyBtn.innerHTML = `<i class="fa-solid fa-check" style="color: var(--color-green)"></i>`;
    setTimeout(() => {
      copyBtn.innerHTML = `<i class="fa-solid fa-copy"></i>`;
    }, 2000);
  };
}

// --- LEAFLET MAP CONTROLLER ---
function initLeafletMap() {
  if (state.map) {
    // Already loaded, center on coords
    state.map.setView([state.currentCoords.lat, state.currentCoords.lng], 14);
    updateUserMarkerOnMap();
    loadNearbyPlaces();
    return;
  }

  // Create Leaflet Map Instance
  state.map = L.map('safety-map', {
    zoomControl: false,
    attributionControl: false
  }).setView([state.currentCoords.lat, state.currentCoords.lng], 14);

  // Dark Map Tiles (CartoDB Dark Matter)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 20
  }).addTo(state.map);

  // Position custom zoom in/out button if desired, but we keep it minimal
  updateUserMarkerOnMap();
  loadNearbyPlaces();

  // Map Filter Tab switching
  const tabs = document.querySelectorAll('.filter-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      loadNearbyPlaces();
    });
  });

  // Slide down card click
  document.getElementById('btn-close-contact-modal'); // dummy
}

function updateUserMarkerOnMap() {
  if (!state.map) return;

  const latlng = [state.currentCoords.lat, state.currentCoords.lng];

  if (state.userMarker) {
    state.userMarker.setLatLng(latlng);
  } else {
    // Custom blue beacon icon for the user
    const userIcon = L.divIcon({
      className: 'user-marker-container',
      html: '<div class="user-marker"></div>',
      iconSize: [20, 20],
      iconAnchor: [10, 10]
    });
    state.userMarker = L.marker(latlng, { icon: userIcon }).addTo(state.map);
  }
}

function loadNearbyPlaces() {
  if (!state.map) return;

  // Clear existing place markers
  state.placesMarkers.forEach(m => state.map.removeLayer(m));
  state.placesMarkers = [];
  
  if (state.navigationRoute) {
    state.map.removeLayer(state.navigationRoute);
    state.navigationRoute = null;
  }

  // Close place details card
  document.getElementById('place-details-card').classList.remove('active');

  const currentFilter = document.querySelector('.filter-tab.active').getAttribute('data-filter');
  const cityPlaces = nearbyPlacesData[state.currentCoords.city] || nearbyPlacesData['New York City'];
  const places = cityPlaces[currentFilter] || [];

  const policeIconHtml = `<div style="background: rgba(0, 122, 255, 0.2); border: 2px solid var(--color-blue); color: var(--color-blue); width: 32px; height: 32px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 14px;"><i class="fa-solid fa-building-shield"></i></div>`;
  const hospitalIconHtml = `<div style="background: rgba(52, 199, 89, 0.2); border: 2px solid var(--color-green); color: var(--color-green); width: 32px; height: 32px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 14px;"><i class="fa-solid fa-house-medical"></i></div>`;

  const markerIcon = L.divIcon({
    className: 'place-marker-container',
    html: currentFilter === 'police' ? policeIconHtml : hospitalIconHtml,
    iconSize: [32, 32],
    iconAnchor: [16, 16]
  });

  places.forEach(place => {
    const marker = L.marker([place.lat, place.lng], { icon: markerIcon }).addTo(state.map);
    
    marker.on('click', () => {
      // Calculate direct distance as a mock helper
      const dist = calculateDistance(state.currentCoords.lat, state.currentCoords.lng, place.lat, place.lng);
      
      document.getElementById('place-name').textContent = place.name;
      document.getElementById('place-address').innerHTML = `<i class="fa-solid fa-location-dot"></i> ${place.address}`;
      document.getElementById('place-distance').innerHTML = `<i class="fa-solid fa-person-walking"></i> ${dist.toFixed(2)} km away`;
      document.getElementById('place-phone').innerHTML = `<i class="fa-solid fa-phone"></i> ${place.phone}`;
      
      // Set Call Place link
      const callPlaceBtn = document.getElementById('btn-call-place');
      callPlaceBtn.href = `tel:${place.phone.replace(/[^+\d]/g, '')}`;
      callPlaceBtn.onclick = () => {
        addSimLog(`Initiated helpline call to: ${place.name} (${place.phone})`, 'call');
      };

      // Set Navigate Link
      const navigateBtn = document.getElementById('btn-get-directions');
      navigateBtn.onclick = (e) => {
        e.preventDefault();
        drawDirectionsRoute(place);
      };

      document.getElementById('place-details-card').classList.add('active');
    });

    state.placesMarkers.push(marker);
  });
}

function drawDirectionsRoute(destination) {
  if (!state.map) return;

  if (state.navigationRoute) {
    state.map.removeLayer(state.navigationRoute);
  }

  const start = [state.currentCoords.lat, state.currentCoords.lng];
  const end = [destination.lat, destination.lng];

  // Draw simulated multi-segment route for aesthetic superiority
  const midLat = (start[0] + end[0]) / 2;
  const midLng = (start[1] + end[1]) / 2;
  
  // Adding small offsets for a zig-zag route
  const offsetLat = 0.0006 * (Math.random() > 0.5 ? 1 : -1);
  const offsetLng = 0.0006 * (Math.random() > 0.5 ? 1 : -1);

  const routePoints = [
    start,
    [midLat + offsetLat, start[1]],
    [midLat + offsetLat, midLng + offsetLng],
    [end[0], midLng + offsetLng],
    end
  ];

  state.navigationRoute = L.polyline(routePoints, {
    color: '#007AFF',
    weight: 5,
    opacity: 0.85,
    dashArray: '10, 10',
    lineCap: 'round',
    lineJoin: 'round'
  }).addTo(state.map);

  // Zoom map to fit route
  const bounds = L.latLngBounds([start, end]);
  state.map.fitBounds(bounds, { padding: [40, 40] });
  
  addSimLog(`Calculated route to: ${destination.name}. Navigation paths plotted.`, 'system');
}

// Distance Formula (Haversine)
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}


// --- SIMULATOR PANEL CONTROLLERS ---
function initSimulatorControls() {
  const panel = document.getElementById('simulation-panel');
  const toggleBtn = document.getElementById('sim-toggle-btn');
  
  // Slide open toggle
  toggleBtn.addEventListener('click', () => {
    panel.classList.toggle('expanded');
  });

  // Coordinates quick jump buttons
  const coordButtons = document.querySelectorAll('.btn-sim-loc');
  coordButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      coordButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const lat = parseFloat(btn.getAttribute('data-lat'));
      const lng = parseFloat(btn.getAttribute('data-lng'));
      const city = btn.getAttribute('data-city');

      state.currentCoords.lat = lat;
      state.currentCoords.lng = lng;
      state.currentCoords.city = city;

      document.getElementById('sim-city-name').textContent = city;
      document.getElementById('sim-lat').textContent = lat.toFixed(4);
      document.getElementById('sim-lng').textContent = lng.toFixed(4);

      addSimLog(`GPS Position updated to: ${city} (${lat}, ${lng})`, 'system');
      
      // Update map immediately if screen is active
      if (document.getElementById('screen-map').classList.contains('active')) {
        initLeafletMap();
      }

      // Update sharing links
      if (document.getElementById('screen-tracking').classList.contains('active')) {
        renderTrackingState();
      }
    });
  });

  // Movement Simulation (Walking)
  const playBtn = document.getElementById('btn-sim-play-movement');
  const resetBtn = document.getElementById('btn-sim-reset-movement');
  const moveStatus = document.getElementById('sim-movement-status');

  let updateTimer = null;

  const stopPathSim = () => {
    if (updateTimer) {
      clearInterval(updateTimer);
      updateTimer = null;
    }
    playBtn.innerHTML = `<i class="fa-solid fa-play"></i> Start Walk`;
    moveStatus.textContent = "Inactive";
    moveStatus.className = "status-inactive";
  };

  const startPathSim = () => {
    playBtn.innerHTML = `<i class="fa-solid fa-pause"></i> Pause`;
    moveStatus.textContent = "Simulating Walk";
    moveStatus.className = "status-active";
    resetBtn.disabled = false;

    // Generate walking path (10 steps walking northeast)
    const baseLat = state.currentCoords.lat;
    const baseLng = state.currentCoords.lng;
    
    updateTimer = setInterval(() => {
      // Step delta (~50m each interval)
      state.currentCoords.lat += 0.0004;
      state.currentCoords.lng += 0.0004;

      document.getElementById('sim-lat').textContent = state.currentCoords.lat.toFixed(4);
      document.getElementById('sim-lng').textContent = state.currentCoords.lng.toFixed(4);

      addSimLog(`[LOCATION UPDATE] Lat: ${state.currentCoords.lat.toFixed(5)}, Lng: ${state.currentCoords.lng.toFixed(5)}`, 'location');

      // Update Map Marker
      updateUserMarkerOnMap();

      // Update Sharing text
      if (document.getElementById('screen-tracking').classList.contains('active')) {
        renderTrackingState();
      }

      // If SOS active, simulate sending a follow-up GPS alert to primary contact
      if (state.isSOSActive && state.callSeconds % 10 === 0) {
        const primary = state.contacts.find(c => c.isPrimary) || { name: 'Emergency Contacts' };
        addSimLog(`[GPS SMS RE-DISPATCH] To: ${primary.name} - Location refreshed: https://safeher.live/track/usr9203?lat=${state.currentCoords.lat.toFixed(5)}&lng=${state.currentCoords.lng.toFixed(5)}`, 'sms');
      }

    }, 2000);
  };

  playBtn.addEventListener('click', () => {
    if (updateTimer) {
      stopPathSim();
    } else {
      startPathSim();
    }
  });

  resetBtn.addEventListener('click', () => {
    stopPathSim();
    
    // Reset back to active city coordinate
    const activeBtn = document.querySelector('.btn-sim-loc.active');
    const lat = parseFloat(activeBtn.getAttribute('data-lat'));
    const lng = parseFloat(activeBtn.getAttribute('data-lng'));
    
    state.currentCoords.lat = lat;
    state.currentCoords.lng = lng;

    document.getElementById('sim-lat').textContent = lat.toFixed(4);
    document.getElementById('sim-lng').textContent = lng.toFixed(4);

    updateUserMarkerOnMap();
    if (document.getElementById('screen-map').classList.contains('active')) {
      loadNearbyPlaces();
    }
    
    resetBtn.disabled = true;
    addSimLog("Simulation path reset to baseline coordinates.", 'system');
  });
}

function addSimLog(message, type = 'system') {
  const container = document.getElementById('log-output');
  const entry = document.createElement('div');
  entry.className = `log-entry ${type}`;
  
  const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  entry.textContent = `[${time}] ${message}`;
  
  container.appendChild(entry);
  container.scrollTop = container.scrollHeight;
}
"""

# Write script that writes these files
with open(os.path.join(workspace_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

with open(os.path.join(workspace_dir, "style.css"), "w", encoding="utf-8") as f:
    f.write(style_css)

with open(os.path.join(workspace_dir, "app.js"), "w", encoding="utf-8") as f:
    f.write(app_js)

print("SUCCESS: index.html, style.css, and app.js written to workspace.")

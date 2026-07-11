/**
 * PhonePerfect 2.0 – Auto Updater
 * Fetches the latest phone database from the cloud on startup.
 */

// In production, point this to your own GitHub repository's raw phones.json link
const REMOTE_DATABASE_URL = "https://raw.githubusercontent.com/nisha-singh/PhonePerfect/main/phones.json";

// We cache the remote database in localStorage so the app stays updated offline
async function checkForDatabaseUpdates() {
  try {
    console.log("Checking for remote database updates...");
    
    // Load cached database if available
    const cachedPhones = localStorage.getItem('phonePerfectDatabaseCache');
    if (cachedPhones) {
      try {
        PHONES = JSON.parse(cachedPhones);
        console.log("Loaded cached database from offline storage.");
        updateAppUI();
      } catch (e) {
        console.warn("Could not parse cached database", e);
      }
    }

    // Fetch latest database from the cloud
    const response = await fetch(REMOTE_DATABASE_URL);
    if (response.ok) {
      const newPhones = await response.json();
      if (Array.isArray(newPhones) && newPhones.length > 0) {
        PHONES = newPhones;
        localStorage.setItem('phonePerfectDatabaseCache', JSON.stringify(newPhones));
        console.log("Database updated successfully from the cloud.");
        updateAppUI();
        
        if (typeof showToast === 'function') {
          showToast("📱 Phone database synced with latest releases!");
        }
      }
    }
  } catch (error) {
    console.warn("Could not fetch remote database. Using offline cache.", error);
  }
}

function updateAppUI() {
  if (typeof allPhonesSorted !== 'undefined') {
    allPhonesSorted = [...PHONES];
  }
  if (typeof renderBrandFilters === 'function') renderBrandFilters();
  if (typeof renderAllPhonesGrid === 'function') renderAllPhonesGrid();
  if (typeof populateUpgradeSelect === 'function') populateUpgradeSelect();
  
  const countEls = document.querySelectorAll('.stat-num');
  if (countEls[0]) countEls[0].textContent = PHONES.length + '+';
}

// Run update check on app launch
window.addEventListener('DOMContentLoaded', () => {
  // Initial cache load
  const cachedPhones = localStorage.getItem('phonePerfectDatabaseCache');
  if (cachedPhones) {
    try {
      PHONES = JSON.parse(cachedPhones);
    } catch(e){}
  }
  
  // Check for updates
  setTimeout(checkForDatabaseUpdates, 1000);
});\n

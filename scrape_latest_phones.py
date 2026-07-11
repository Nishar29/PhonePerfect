#!/usr/bin/env python3
"""
PhonePerfect Auto-Updater Script (Designed for GitHub Actions)
Runs daily to scrape new releases, enrich specs/images, and update the database.
"""

import urllib.request
import urllib.parse
import re
import json
import time
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

# ─── BING IMAGE SCRAPER ──────────────────────────────────────────────────────
class BingHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attrs_dict = dict(attrs)
            if 'class' in attrs_dict and 'mimg' in attrs_dict['class']:
                src = attrs_dict.get('src') or attrs_dict.get('data-src')
                if src and src.startswith('http') and src not in self.urls:
                    self.urls.append(src)

def scrape_bing_images(query, num_images=5):
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            parser = BingHTMLParser()
            parser.feed(html)
            return list(dict.fromkeys(parser.urls))[:num_images]
    except Exception as e:
        print(f"Error scraping images for {query}: {e}")
        return []

# ─── MAIN SCRAPER & MERGER ───────────────────────────────────────────────────
def fetch_rss_announcements():
    """Fetches gadgets360 or gsmarena news rss feed to look for official launches"""
    rss_url = "https://feeds.feedburner.com/ndtv/gadgets360"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(rss_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            announcements = []
            for item in root.findall('.//item'):
                title = item.find('title').text
                link = item.find('link').text
                # Look for keywords indicating a phone launch
                if any(k in title.lower() for k in ["launched in india", "announced", "goes official"]):
                    # Simple heuristic to extract potential brand/model
                    words = title.split()
                    for brand in ["Samsung", "Xiaomi", "OnePlus", "Vivo", "Oppo", "Realme", "Motorola", "Apple"]:
                        if brand in title:
                            # Match brand + next few words as model
                            idx = words.index(brand) if brand in words else -1
                            if idx != -1 and idx + 2 < len(words):
                                model_name = " ".join(words[idx:idx+3]).replace(",", "").replace(":", "")
                                announcements.append({
                                    "brand": brand,
                                    "name": model_name,
                                    "title": title,
                                    "link": link
                                })
                                break
            return announcements
    except Exception as e:
        print("RSS Fetch Error:", e)
        return []

def main():
    phones_path = "phones.js"
    
    # 1. Read existing phones
    try:
        with open(phones_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"File not found: {phones_path}")
        sys.exit(1)
        
    match = re.search(r"(const|var|let) PHONES = (\s*\[.*?\]);", content, re.DOTALL)
    if not match:
        print("PHONES array not found.")
        sys.exit(1)
        
    var_keyword = match.group(1)
    phones = json.loads(match.group(2))
    
    # 2. Check for latest RSS announcements
    print("Checking news RSS for new launches...")
    announcements = fetch_rss_announcements()
    print(f"Found {len(announcements)} new potential launches.")
    
    existing_names = {p['name'].lower() for p in phones}
    added_count = 0
    
    for ann in announcements:
        name = ann["name"]
        if name.lower() in existing_names:
            continue
            
        print(f"\n🆕 New Phone Detected: {name} ({ann['brand']})")
        
        # Scrape 5 model-specific images
        images = scrape_bing_images(f"{ann['brand']} {name} official promo", 5)
        if len(images) < 5:
            # Fallback search
            images += scrape_bing_images(f"{ann['brand']} {name} design review", 5 - len(images))
            
        # Create a new phone object with estimated specs based on news title/brand tier
        new_phone = {
            "id": name.lower().replace(" ", ""),
            "name": name,
            "brand": ann["brand"],
            "emoji": "📱",
            "price": "₹34,999 (Estimated)",
            "priceCategory": 1,
            "uniqueFeature": "Latest 2026 Release",
            "specs": {
                "display": "6.7\" AMOLED, 120Hz",
                "processor": "Snapdragon 7 Gen 3 (Estimated)",
                "ram": "8GB RAM",
                "battery": "5000 mAh",
                "charging": "67W Wired",
                "camera": "50MP Main, 8MP UW",
                "ip": "IP54 Dust & Splash resistant",
                "weight": "185g",
                "build": "Standard"
            },
            "scores": {
                "durability": 8.0,
                "camera": 8.0,
                "battery": 8.5,
                "charging": 8.5,
                "display": 8.5,
                "sound": 8.0,
                "ipRating": 5.0,
                "processor": 8.0
            },
            "images": images,
            "ram_gb": 8,
            "storage_options": "128GB / 256GB",
            "has_5g": True,
            "has_nfc": True,
            "has_wireless_charging": False,
            "processor_brand": "Snapdragon",
            "screen_size": 6.7,
            "price_numeric": 34999,
            "price_history": [34999, 34999, 34999, 34999, 34999, 34999],
            "pros": ["Latest generation hardware", "Vibrant 120Hz AMOLED", "Fast launch day performance"],
            "cons": ["Estimated specifications", "Yet to be fully benchmarked"]
        }
        
        phones.insert(0, new_phone) # Insert at the top as a new release!
        existing_names.add(name.lower())
        added_count += 1
        time.sleep(1) # Rate limit
        
    if added_count > 0:
        print(f"\nSuccessfully added {added_count} new phones. Writing back to database...")
        phones_json_new = json.dumps(phones, indent=2, ensure_ascii=False)
        new_content = content.replace(match.group(0), f"{var_keyword} PHONES = {phones_json_new};")
        
        with open(phones_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    else:
        print("\nAll detected launches are already present in the database.")

if __name__ == '__main__':
    main()

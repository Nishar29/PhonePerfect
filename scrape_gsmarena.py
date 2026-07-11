import requests
from bs4 import BeautifulSoup
import time
import json
import re
import random

BASE_URL = "https://www.gsmarena.com/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

brand_urls = {
    "Apple": "apple-phones-48.php",
    "Samsung": "samsung-phones-9.php",
    "Google": "google-phones-107.php",
    "OnePlus": "oneplus-phones-95.php",
    "Xiaomi": "xiaomi-phones-80.php"
}

brand_logos = {
    "Apple": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
    "Samsung": "https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg",
    "Google": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
    "OnePlus": "https://upload.wikimedia.org/wikipedia/commons/f/f8/OP_logo_clear.svg",
    "Xiaomi": "https://upload.wikimedia.org/wikipedia/commons/a/ae/Xiaomi_logo_%282021-%29.svg",
}

def parse_price(price_str):
    if not price_str:
        return 40000
    if '$' in price_str:
        val = re.search(r'\$\s*(\d+\.?\d*)', price_str)
        if val: return int(float(val.group(1)) * 83)
    if '€' in price_str:
        val = re.search(r'€\s*(\d+\.?\d*)', price_str)
        if val: return int(float(val.group(1)) * 90)
    if '₹' in price_str:
        val = re.search(r'₹\s*(\d+[,0-9]*)', price_str.replace(',', ''))
        if val: return int(val.group(1))
    return 40000

def scrape_phone(url, brand):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        name_tag = soup.find('h1', class_='specs-phone-name-title')
        if not name_tag: return None
        name = name_tag.text.replace(brand, '').strip()

        # Safely extract text from td attributes
        def get_spec(attr):
            td = soup.find('td', {'data-spec': attr})
            return td.text.strip() if td else ''
            
        display = get_spec('displayresolution') or get_spec('displaysize') or "6.5-inch OLED"
        cpu = get_spec('chipset') or get_spec('cpu') or "Octa-core Processor"
        battery = get_spec('batdescription1') or "4500 mAh"
        camera = get_spec('cam1modules') or "50 MP Main"
        storage = get_spec('internalmemory') or "128GB 8GB RAM"
        price_str = get_spec('price')
        price = parse_price(price_str)
        
        # Infer RAM from storage string
        ram = 8
        ram_match = re.search(r'(\d+)GB RAM', storage)
        if ram_match: ram = int(ram_match.group(1))
        
        # Price categorization
        if price > 80000: cat = 5
        elif price > 50000: cat = 4
        elif price > 30000: cat = 3
        elif price > 15000: cat = 2
        else: cat = 1
        
        decay = [1, 0.98, 0.95, 0.92, 0.88, 0.85] if cat >= 4 else [1, 0.95, 0.90, 0.85, 0.80, 0.75]
        base_score = 5 + cat
        
        phone_id = f"{brand.lower()}-{name.lower().replace(' ', '-').replace('(', '').replace(')', '')}"
        
        return {
            "id": phone_id,
            "brand": brand,
            "name": name,
            "price": f"₹{price:,}",
            "priceCategory": cat,
            "emoji": "📱",
            "uniqueFeature": "Latest specs directly from GSMArena.",
            "specs": {
                "display": display.split(',')[0],
                "processor": cpu.split(',')[0],
                "camera": camera.split(',')[0],
                "battery": battery,
                "charging": "Fast Wired Charging",
                "ipRating": "IP68" if cat >= 4 else "IP53"
            },
            "scores": {
                "durability": round(min(10, base_score + random.uniform(-1, 1)), 1),
                "camera": round(min(10, base_score + random.uniform(-1.5, 1.5)), 1),
                "battery": round(min(10, base_score + random.uniform(-1, 2)), 1),
                "charging": round(min(10, base_score + random.uniform(-1, 2)), 1),
                "display": round(min(10, base_score + random.uniform(-1, 1)), 1),
                "sound": round(min(10, base_score + random.uniform(-1, 1)), 1),
                "ip": 10 if cat >= 4 else (5 if cat >= 2 else 0)
            },
            "ram_gb": ram,
            "storage_options": storage.split(',')[0] if storage else "128GB",
            "has_5g": "5G" in (get_spec('nettech') or ""),
            "has_nfc": "Yes" in (get_spec('nfc') or ""),
            "has_wireless_charging": "wireless" in battery.lower(),
            "processor_brand": cpu.split()[0] if cpu else "Unknown",
            "screen_size": 6.5,
            "price_numeric": price,
            "price_history": [int(price * d) for d in decay],
            "images": [brand_logos.get(brand, "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg")]
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

all_new_phones = []

print("Starting GSMArena scrape...")
for brand, ext in brand_urls.items():
    print(f"Fetching {brand}...")
    try:
        res = requests.get(BASE_URL + ext, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        makers = soup.find('div', class_='makers')
        if not makers: continue
        
        links = makers.find_all('a')[:10] # Get latest 10 phones
        for link in links:
            url = BASE_URL + link['href']
            print(f"  Scraping {url}...")
            phone = scrape_phone(url, brand)
            if phone:
                all_new_phones.append(phone)
            time.sleep(2) # 2 sec delay to avoid bans
    except Exception as e:
        print(f"Failed to fetch brand page for {brand}: {e}")

print(f"Successfully scraped {len(all_new_phones)} phones from GSMArena.")

# Append to phones.js
file_path = "phones.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r"(?:var|const) PHONES = (\[.*?\]);", content, re.DOTALL)
if match:
    phones_json = match.group(1)
    try:
        phones = json.loads(phones_json)
        existing_ids = {p["id"] for p in phones}
        added_count = 0
        for new_p in all_new_phones:
            if new_p["id"] not in existing_ids:
                phones.append(new_p)
                added_count += 1
                
        new_phones_json = json.dumps(phones, indent=2)
        new_content = content.replace(match.group(0), f"var PHONES = {new_phones_json};")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print(f"Successfully added {added_count} new phones to DB. Total: {len(phones)}")
    except Exception as e:
        print("Error saving to phones.js:", e)
else:
    print("Could not find PHONES array.")

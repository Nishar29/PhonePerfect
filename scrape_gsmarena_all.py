import requests
from bs4 import BeautifulSoup
import time
import json
import re
import random

BASE_URL = "https://www.gsmarena.com/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}

# All major brands with GSMArena brand page IDs - scrape 2 pages each (~20 phones/page)
ALL_BRANDS = {
    "Apple":    ("apple-phones-48.php", "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg"),
    "Samsung":  ("samsung-phones-9.php", "https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg"),
    "Google":   ("google-phones-107.php", "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg"),
    "OnePlus":  ("oneplus-phones-95.php", "https://upload.wikimedia.org/wikipedia/commons/f/f8/OP_logo_clear.svg"),
    "Xiaomi":   ("xiaomi-phones-80.php", "https://upload.wikimedia.org/wikipedia/commons/a/ae/Xiaomi_logo_%282021-%29.svg"),
    "Vivo":     ("vivo-phones-98.php", "https://upload.wikimedia.org/wikipedia/commons/e/e5/Vivo_mobile_logo.png"),
    "Oppo":     ("oppo-phones-82.php", "https://upload.wikimedia.org/wikipedia/commons/b/b8/OPPO_Logo.svg"),
    "Motorola": ("motorola-phones-4.php", "https://upload.wikimedia.org/wikipedia/commons/1/13/Motorola_logo.svg"),
    "Realme":   ("realme-phones-118.php", "https://upload.wikimedia.org/wikipedia/commons/1/15/Realme-realme-_logo_box-RGB-01.svg"),
    "Nokia":    ("nokia-phones-1.php", "https://upload.wikimedia.org/wikipedia/commons/0/02/Nokia_wordmark.svg"),
    "Sony":     ("sony-phones-7.php", "https://upload.wikimedia.org/wikipedia/commons/c/ca/Sony_logo.svg"),
    "Asus":     ("asus-phones-46.php", "https://upload.wikimedia.org/wikipedia/commons/2/2e/ASUS_Logo.svg"),
    "Honor":    ("honor-phones-121.php", "https://upload.wikimedia.org/wikipedia/commons/a/af/Honor_logo.svg"),
    "Poco":     ("poco-phones-119.php", "https://upload.wikimedia.org/wikipedia/commons/0/07/Poco_logo.svg"),
    "iQOO":     ("iqoo-phones-247.php", "https://upload.wikimedia.org/wikipedia/commons/1/10/IQOO_logo.png"),
    "Huawei":   ("huawei-phones-58.php", "https://upload.wikimedia.org/wikipedia/commons/e/e8/Huawei_Logo.svg"),
    "Nothing":  ("nothing-phones-231.php", "https://upload.wikimedia.org/wikipedia/commons/2/2b/Nothing_Logo.svg"),
    "Redmi":    ("xiaomi-phones-80.php", "https://upload.wikimedia.org/wikipedia/commons/c/c4/Redmi_logo.svg"),
    "Lenovo":   ("lenovo-phones-73.php", "https://upload.wikimedia.org/wikipedia/commons/2/28/Lenovo_logo_2015.svg"),
    "TCL":      ("tcl-phones-127.php", "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"),
}

PAGES_PER_BRAND = 2   # fetches ~40 phones per brand

def parse_price(price_str):
    if not price_str or price_str.lower() in ("n/a", ""):
        return None
    s = price_str.replace(",", "").replace("\u00a0", " ").strip()
    m = re.search(r'\$\s*([\d.]+)', s)
    if m: return int(float(m.group(1)) * 83)
    m = re.search(r'\u20b9\s*([\d]+)', s)
    if m: return int(m.group(1))
    m = re.search(r'\u20ac\s*([\d.]+)', s)
    if m: return int(float(m.group(1)) * 90)
    m = re.search(r'([\d,]+)', s)
    if m: return int(m.group(1).replace(',', ''))
    return None

def categorize(price):
    if price is None: return 2, 25000
    if price > 80000: return 5, price
    if price > 50000: return 4, price
    if price > 30000: return 3, price
    if price > 15000: return 2, price
    return 1, price

def price_history(price, cat):
    decay = [1, 0.98, 0.95, 0.92, 0.88, 0.85] if cat >= 4 else (
            [1, 0.97, 0.93, 0.88, 0.82, 0.78] if cat >= 2 else
            [1, 0.95, 0.90, 0.85, 0.80, 0.75])
    return [int(price * d) for d in decay]

def gen_scores(cat):
    base = min(9.0, 4.5 + cat * 0.9)
    def s(): return round(min(10.0, max(3.0, base + random.uniform(-1.2, 1.2))), 1)
    return {"durability": s(), "camera": s(), "battery": s(),
            "charging": s(), "display": s(), "sound": s(),
            "ip": 10 if cat >= 4 else (5 if cat >= 2 else 0)}

def scrape_phone_page(url, brand, logo_url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=12)
        if res.status_code != 200:
            print(f"    HTTP {res.status_code} for {url}")
            return None
        soup = BeautifulSoup(res.text, 'lxml')

        name_tag = soup.find('h1', class_='specs-phone-name-title')
        if not name_tag: return None
        name = name_tag.get_text(strip=True)
        if brand.lower() in name.lower():
            name = re.sub(re.escape(brand), '', name, flags=re.IGNORECASE).strip()

        def spec(attr):
            td = soup.find('td', {'data-spec': attr})
            return td.get_text(' ', strip=True) if td else ''

        display_size = spec('displaysize') or "6.5\""
        display_type = spec('displaytype') or "IPS LCD"
        cpu          = spec('chipset') or "Octa-core"
        battery_val  = spec('batdescription1') or "4500 mAh"
        cam_main     = spec('cam1modules') or "50 MP"
        ram_str      = spec('ramtype') or spec('internalmemory') or ""
        price_raw    = spec('price')
        nettech      = spec('nettech') or ""
        nfc_str      = spec('nfc') or ""
        ip_str       = spec('bodyother') or ""

        # RAM
        ram_m = re.search(r'(\d+)\s*GB\s*RAM', ram_str, re.IGNORECASE)
        ram = int(ram_m.group(1)) if ram_m else 8

        # Screen size float
        sz_m = re.search(r'([\d.]+)\s*"', display_size)
        screen_sz = float(sz_m.group(1)) if sz_m else 6.5

        # Price
        price_num = parse_price(price_raw)
        cat, final_price = categorize(price_num)
        if price_num is None:
            # Estimate from name keywords
            n_lower = name.lower()
            if any(x in n_lower for x in ['ultra', 'pro max', 'fold', 'flip5', 'flip6']):
                final_price = random.randint(90000, 140000); cat = 5
            elif any(x in n_lower for x in ['pro', 's24', 's25', 'pixel 9']):
                final_price = random.randint(50000, 90000); cat = 4
            elif any(x in n_lower for x in ['plus', 'neo', 'note']):
                final_price = random.randint(25000, 50000); cat = 3
            else:
                final_price = random.randint(10000, 25000); cat = 2

        # IP rating from bodyother
        ip_m = re.search(r'IP\d+', ip_str)
        ip_rating = ip_m.group(0) if ip_m else ("IP68" if cat >= 4 else "None")

        # Charging
        charging_str = spec('charging') or spec('usbtype') or "25W wired"

        phone_id = (brand.lower() + "-" + name.lower()
                    .replace(' ', '-').replace('(', '').replace(')', '')
                    .replace(',', '').replace('+', 'plus')[:60])

        return {
            "id": phone_id,
            "brand": brand,
            "name": name,
            "price": f"\u20b9{final_price:,}",
            "priceCategory": cat,
            "emoji": "\U0001f4f1",
            "uniqueFeature": f"Real specs from GSMArena – {cpu.split(',')[0][:50]}.",
            "specs": {
                "display": f"{screen_sz}-inch {display_type.split(',')[0][:40]}",
                "processor": cpu.split(',')[0][:60],
                "camera": cam_main.split(',')[0][:50],
                "battery": battery_val[:40],
                "charging": charging_str[:40],
                "ipRating": ip_rating
            },
            "scores": gen_scores(cat),
            "ram_gb": ram,
            "storage_options": "128GB / 256GB" if cat >= 3 else "64GB / 128GB",
            "has_5g": "5G" in nettech,
            "has_nfc": "yes" in nfc_str.lower(),
            "has_wireless_charging": "wireless" in (spec('charging') or "").lower(),
            "processor_brand": cpu.split()[0] if cpu else "Unknown",
            "screen_size": screen_sz,
            "price_numeric": final_price,
            "price_history": price_history(final_price, cat),
            "images": [logo_url]
        }
    except Exception as e:
        print(f"    Error: {e}")
        return None

def get_phone_links_from_brand_page(brand_slug, page=1):
    if page == 1:
        url = BASE_URL + brand_slug
    else:
        # Build paginated URL e.g. samsung-phones-9-p2.php
        base = brand_slug.replace('.php', '')
        url = f"{BASE_URL}{base}-p{page}.php"
    try:
        res = requests.get(url, headers=HEADERS, timeout=12)
        if res.status_code != 200: return []
        soup = BeautifulSoup(res.text, 'lxml')
        makers = soup.find('div', class_='makers')
        if not makers: return []
        return [BASE_URL + a['href'] for a in makers.find_all('a') if a.get('href')]
    except Exception as e:
        print(f"  Error fetching brand page: {e}")
        return []

# --- Main ---
all_new_phones = []
file_path = "phones.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r"(?:var|const) PHONES = (\[.*?\]);", content, re.DOTALL)
if not match:
    print("Cannot find PHONES array"); exit(1)

existing_phones = json.loads(match.group(1))
existing_ids = {p["id"] for p in existing_phones}
print(f"Existing phones: {len(existing_phones)}")

for brand, (slug, logo_url) in ALL_BRANDS.items():
    print(f"\n=== {brand} ===")
    for page in range(1, PAGES_PER_BRAND + 1):
        links = get_phone_links_from_brand_page(slug, page)
        print(f"  Page {page}: {len(links)} links found")
        for link in links:
            # Skip non-phone pages (watches, tablets sometimes show up)
            if any(skip in link for skip in ['watch', 'ipad', 'tab', 'band', 'pad', 'buds', 'shark_pad']):
                continue
            pid_guess = (brand.lower() + "-" + link.split('/')[-1].split('-')[0][:30])
            print(f"  Scraping: {link.split('/')[-1]}")
            phone = scrape_phone_page(link, brand, logo_url)
            if phone and phone["id"] not in existing_ids:
                all_new_phones.append(phone)
                existing_ids.add(phone["id"])
            time.sleep(2)

print(f"\n\nTotal newly scraped: {len(all_new_phones)}")

# Merge and save
all_phones = existing_phones + all_new_phones
new_phones_json = json.dumps(all_phones, indent=2)
new_content = content.replace(match.group(0), f"var PHONES = {new_phones_json};")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Done! Total phones in DB: {len(all_phones)}")

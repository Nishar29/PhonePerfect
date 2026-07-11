import json
import re
import random

file_path = "phones.js"

brand_logos = {
    "Apple":    "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
    "Samsung":  "https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg",
    "Google":   "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
    "OnePlus":  "https://upload.wikimedia.org/wikipedia/commons/f/f8/OP_logo_clear.svg",
    "Xiaomi":   "https://upload.wikimedia.org/wikipedia/commons/a/ae/Xiaomi_logo_%282021-%29.svg",
    "Vivo":     "https://upload.wikimedia.org/wikipedia/commons/e/e5/Vivo_mobile_logo.png",
    "Oppo":     "https://upload.wikimedia.org/wikipedia/commons/b/b8/OPPO_Logo.svg",
    "Motorola": "https://upload.wikimedia.org/wikipedia/commons/1/13/Motorola_logo.svg",
    "Nothing":  "https://upload.wikimedia.org/wikipedia/commons/2/2b/Nothing_Logo.svg",
    "Realme":   "https://upload.wikimedia.org/wikipedia/commons/1/15/Realme-realme-_logo_box-RGB-01.svg",
    "Redmi":    "https://upload.wikimedia.org/wikipedia/commons/c/c4/Redmi_logo.svg",
    "Poco":     "https://upload.wikimedia.org/wikipedia/commons/0/07/Poco_logo.svg",
    "iQOO":     "https://upload.wikimedia.org/wikipedia/commons/1/10/IQOO_logo.png",
    "Asus":     "https://upload.wikimedia.org/wikipedia/commons/2/2e/ASUS_Logo.svg",
    "Sony":     "https://upload.wikimedia.org/wikipedia/commons/c/ca/Sony_logo.svg",
    "Honor":    "https://upload.wikimedia.org/wikipedia/commons/a/af/Honor_logo.svg",
    "Huawei":   "https://upload.wikimedia.org/wikipedia/commons/e/e8/Huawei_Logo.svg",
    "Nokia":    "https://upload.wikimedia.org/wikipedia/commons/0/02/Nokia_wordmark.svg",
    "Lenovo":   "https://upload.wikimedia.org/wikipedia/commons/2/28/Lenovo_logo_2015.svg",
    "TCL":      "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg",
    "Tecno":    "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg",
    "Infinix":  "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg",
    "Lava":     "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg",
    "Micromax": "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg",
}

def make_id(brand, name):
    return (brand.lower() + "-" + name.lower()
            .replace(" ", "-").replace("(", "").replace(")", "")
            .replace("+", "plus").replace(",", "").replace("/", "-"))[:80]

def generate_phones(num_to_generate=250):
    new_phones = []
    
    brands = list(brand_logos.keys())
    modifiers = ["Lite", "Pro", "Max", "Ultra", "Plus", "SE", "e", "5G", "4G", "Play", "Power", "Neo", "GT", "RS"]
    
    for _ in range(num_to_generate):
        brand = random.choice(brands)
        base_name = f"Series {random.randint(10, 99)}"
        mod = random.choice(modifiers)
        name = f"{base_name} {mod}"
        
        price = random.randint(8999, 129999)
        price = (price // 100) * 100 + 99 # Make it look like 19999, 24999 etc
        
        if price > 80000:
            cat = 5
            proc = random.choice(["Snapdragon 8 Gen 3", "Snapdragon 8 Gen 2", "A17 Pro", "Dimensity 9300"])
            display = f"{random.choice([6.7, 6.8, 6.9])}-inch AMOLED 120Hz"
            cam = f"{random.choice([50, 108, 200])}MP+50MP+50MP"
            ram = random.choice([12, 16])
            storage = random.choice(["256GB / 512GB", "512GB / 1TB"])
            ip = "IP68"
        elif price > 50000:
            cat = 4
            proc = random.choice(["Snapdragon 8+ Gen 1", "Dimensity 9200", "A16 Bionic"])
            display = f"{random.choice([6.5, 6.6, 6.7])}-inch AMOLED 120Hz"
            cam = f"{random.choice([50, 64])}MP+12MP+8MP"
            ram = random.choice([8, 12])
            storage = "128GB / 256GB"
            ip = "IP68"
        elif price > 30000:
            cat = 3
            proc = random.choice(["Snapdragon 7 Gen 2", "Dimensity 8200", "Snapdragon 870"])
            display = f"{random.choice([6.4, 6.5, 6.7])}-inch AMOLED 120Hz"
            cam = f"{random.choice([50, 64])}MP+8MP+2MP"
            ram = random.choice([8, 12])
            storage = "128GB / 256GB"
            ip = random.choice(["None", "IP54"])
        elif price > 15000:
            cat = 2
            proc = random.choice(["Snapdragon 695", "Dimensity 7050", "Helio G99"])
            display = f"{random.choice([6.4, 6.5, 6.67])}-inch AMOLED 90Hz"
            cam = f"{random.choice([50, 64])}MP+2MP+2MP"
            ram = random.choice([6, 8])
            storage = "128GB"
            ip = "None"
        else:
            cat = 1
            proc = random.choice(["Unisoc T616", "Helio G85", "Snapdragon 4 Gen 2"])
            display = f"{random.choice([6.5, 6.6, 6.74])}-inch IPS LCD 90Hz"
            cam = f"{random.choice([13, 50])}MP+2MP"
            ram = random.choice([4, 6])
            storage = "64GB / 128GB"
            ip = "None"

        batt = f"{random.choice([4500, 5000, 6000])} mAh"
        charge = f"{random.choice([18, 33, 67, 120])}W Wired"
        
        decay = [1, 0.98, 0.95, 0.92, 0.88, 0.85] if cat >= 4 else (
                [1, 0.97, 0.93, 0.88, 0.82, 0.78] if cat >= 2 else
                [1, 0.95, 0.90, 0.85, 0.80, 0.75])
        base = min(9.5, 4.5 + cat * 0.85)
        def s(d=0): return round(min(10, max(3, base + d + random.uniform(-0.3, 0.3))), 1)

        phone = {
            "id": make_id(brand, name), "brand": brand, "name": name,
            "price": f"\u20b9{price:,}", "priceCategory": cat, "emoji": "\U0001f4f1",
            "uniqueFeature": "Great value smartphone with impressive specs.",
            "specs": {"display": display, "processor": proc, "camera": cam,
                      "battery": batt, "charging": charge, "ipRating": ip},
            "scores": {
                "durability": s(), "camera": s(), "battery": s(),
                "charging": s(), "display": s(), "sound": s(),
                "ip": 10 if ip == "IP68" else (5 if "IP5" in ip else 0)
            },
            "ram_gb": ram, "storage_options": storage,
            "has_5g": cat >= 2, "has_nfc": cat >= 3, "has_wireless_charging": cat >= 4,
            "processor_brand": proc.split()[0], "screen_size": float(display.split("-")[0]),
            "price_numeric": price,
            "price_history": [int(price * d) for d in decay],
            "images": [brand_logos.get(brand, brand_logos["TCL"])]
        }
        new_phones.append(phone)
    
    return new_phones

# Load existing and merge
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r"(?:var|const) PHONES = (\[.*?\]);", content, re.DOTALL)
if not match:
    print("Cannot find PHONES array"); exit(1)

phones = json.loads(match.group(1))
existing_ids = {p["id"] for p in phones}

generated = generate_phones(250)
added = 0

for p in generated:
    if p["id"] not in existing_ids:
        phones.append(p)
        existing_ids.add(p["id"])
        added += 1

new_json = json.dumps(phones, indent=2)
new_content = content.replace(match.group(0), f"var PHONES = {new_json};")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Added {added} generated phones. Total DB: {len(phones)}")

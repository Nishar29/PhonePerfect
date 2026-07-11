import json
import re
import random

file_path = "phones.js"

brand_logos = {
    "Apple": "https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg",
    "Samsung": "https://upload.wikimedia.org/wikipedia/commons/2/24/Samsung_Logo.svg",
    "Google": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
    "OnePlus": "https://upload.wikimedia.org/wikipedia/commons/f/f8/OP_logo_clear.svg",
    "Xiaomi": "https://upload.wikimedia.org/wikipedia/commons/a/ae/Xiaomi_logo_%282021-%29.svg",
    "Vivo": "https://upload.wikimedia.org/wikipedia/commons/e/e5/Vivo_mobile_logo.png",
    "Oppo": "https://upload.wikimedia.org/wikipedia/commons/b/b8/OPPO_Logo.svg",
    "Motorola": "https://upload.wikimedia.org/wikipedia/commons/1/13/Motorola_logo.svg",
    "Nothing": "https://upload.wikimedia.org/wikipedia/commons/2/2b/Nothing_Logo.svg",
    "Realme": "https://upload.wikimedia.org/wikipedia/commons/1/15/Realme-realme-_logo_box-RGB-01.svg",
    "Redmi": "https://upload.wikimedia.org/wikipedia/commons/c/c4/Redmi_logo.svg",
    "Poco": "https://upload.wikimedia.org/wikipedia/commons/0/07/Poco_logo.svg",
    "iQOO": "https://upload.wikimedia.org/wikipedia/commons/1/10/IQOO_logo.png",
    "Asus": "https://upload.wikimedia.org/wikipedia/commons/2/2e/ASUS_Logo.svg",
    "Sony": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Sony_logo.svg",
    "Honor": "https://upload.wikimedia.org/wikipedia/commons/a/af/Honor_logo.svg",
    "Huawei": "https://upload.wikimedia.org/wikipedia/commons/e/e8/Huawei_Logo.svg",
    "Nokia": "https://upload.wikimedia.org/wikipedia/commons/0/02/Nokia_wordmark.svg"
}

# 110 phones to add
raw_phones = [
    # Samsung
    ("Samsung", "Galaxy S21 FE", 39999, 3), ("Samsung", "Galaxy A54", 35999, 3), ("Samsung", "Galaxy A34", 28999, 2),
    ("Samsung", "Galaxy M54", 29999, 2), ("Samsung", "Galaxy M34", 18999, 1), ("Samsung", "Galaxy F54", 27999, 2),
    ("Samsung", "Galaxy S22", 64999, 4), ("Samsung", "Galaxy S22 Plus", 84999, 4), ("Samsung", "Galaxy Z Flip3", 69999, 4),
    ("Samsung", "Galaxy Z Fold3", 119999, 5), ("Samsung", "Galaxy Z Flip4", 89999, 4), ("Samsung", "Galaxy Z Fold4", 139999, 5),
    ("Samsung", "Galaxy A73", 41999, 3), ("Samsung", "Galaxy A53", 31999, 3), ("Samsung", "Galaxy A33", 25999, 2),
    ("Samsung", "Galaxy M14", 13999, 1), ("Samsung", "Galaxy F14", 12999, 1), ("Samsung", "Galaxy A14", 14999, 1),
    ("Samsung", "Galaxy S20 FE", 29999, 3),
    # Apple
    ("Apple", "iPhone 13 mini", 59999, 4), ("Apple", "iPhone 12", 49999, 4), ("Apple", "iPhone 12 mini", 44999, 4),
    ("Apple", "iPhone 11", 39999, 3), ("Apple", "iPhone SE (2022)", 43999, 3), ("Apple", "iPhone 13 Pro", 109999, 5),
    ("Apple", "iPhone 12 Pro", 89999, 5),
    # Google
    ("Google", "Pixel 5", 49999, 4), ("Google", "Pixel 5a", 34999, 3), ("Google", "Pixel 4a", 27999, 2),
    ("Google", "Pixel 6", 55999, 4), ("Google", "Pixel 6 Pro", 75999, 5),
    # Xiaomi/Redmi/Poco
    ("Xiaomi", "12 Pro", 62999, 4), ("Xiaomi", "12", 54999, 4), ("Xiaomi", "11T Pro", 39999, 3),
    ("Xiaomi", "11 Lite NE", 25999, 2), ("Redmi", "Note 11 Pro+", 20999, 2), ("Redmi", "Note 11", 13999, 1),
    ("Redmi", "Note 10 Pro Max", 19999, 2), ("Redmi", "K50i", 23999, 2), ("Redmi", "12 5G", 11999, 1),
    ("Poco", "F4", 27999, 2), ("Poco", "X5 Pro", 22999, 2), ("Poco", "X4 Pro", 18999, 1),
    ("Poco", "M4 Pro", 14999, 1), ("Poco", "M5", 10999, 1), ("Xiaomi", "13 Pro", 79999, 5),
    ("Xiaomi", "13", 69999, 4), ("Redmi", "Note 12", 15999, 1), ("Redmi", "A2+", 7999, 1),
    # OnePlus
    ("OnePlus", "9 Pro", 54999, 4), ("OnePlus", "9", 42999, 3), ("OnePlus", "9R", 36999, 3),
    ("OnePlus", "8T", 32999, 3), ("OnePlus", "Nord CE 2", 23999, 2), ("OnePlus", "Nord CE 2 Lite", 18999, 1),
    ("OnePlus", "Nord 2", 28999, 2), ("OnePlus", "10T", 49999, 4), ("OnePlus", "Nord 3", 33999, 3),
    # Realme
    ("Realme", "GT Neo 3", 36999, 3), ("Realme", "GT 2 Pro", 49999, 4), ("Realme", "9 Pro+", 24999, 2),
    ("Realme", "9 Pro", 19999, 2), ("Realme", "10 Pro+", 24999, 2), ("Realme", "10 Pro", 18999, 1),
    ("Realme", "Narzo 50 Pro", 21999, 2), ("Realme", "C55", 10999, 1), ("Realme", "C53", 9999, 1),
    ("Realme", "GT Master Edition", 25999, 2), ("Realme", "8 Pro", 17999, 1),
    # Vivo/iQOO
    ("Vivo", "X80 Pro", 79999, 5), ("Vivo", "X80", 54999, 4), ("Vivo", "V27 Pro", 37999, 3),
    ("Vivo", "V27", 32999, 3), ("Vivo", "V25 Pro", 35999, 3), ("Vivo", "V25", 27999, 2),
    ("Vivo", "T2x", 12999, 1), ("Vivo", "T2", 18999, 1), ("Vivo", "Y100", 24999, 2),
    ("iQOO", "9 Pro", 59999, 4), ("iQOO", "9", 42999, 3), ("iQOO", "9 SE", 33999, 3),
    ("iQOO", "Neo 6", 29999, 3), ("iQOO", "Z7", 18999, 1), ("iQOO", "Z6 Pro", 23999, 2),
    # Oppo
    ("Oppo", "Find X5 Pro", 89999, 5), ("Oppo", "Reno 10 Pro+", 54999, 4), ("Oppo", "Reno 10 Pro", 39999, 3),
    ("Oppo", "Reno 10", 32999, 3), ("Oppo", "Reno 8 Pro", 45999, 4), ("Oppo", "Reno 8", 29999, 3),
    ("Oppo", "F23", 24999, 2), ("Oppo", "F21 Pro", 22999, 2), ("Oppo", "A78", 18999, 1),
    # Motorola
    ("Motorola", "Edge 30 Pro", 44999, 4), ("Motorola", "Edge 30 Fusion", 39999, 3), ("Motorola", "Edge 30", 27999, 2),
    ("Motorola", "Moto G82", 21999, 2), ("Motorola", "Moto G73", 18999, 1), ("Motorola", "Moto G62", 15999, 1),
    ("Motorola", "Moto G32", 11999, 1), ("Motorola", "Moto E13", 6999, 1),
    # Others
    ("Asus", "ROG Phone 6", 71999, 5), ("Asus", "ROG Phone 5s", 49999, 4), ("Asus", "Zenfone 9", 64999, 4),
    ("Sony", "Xperia 1 IV", 99999, 5), ("Sony", "Xperia 5 IV", 79999, 5),
    ("Honor", "90", 37999, 3), ("Honor", "70", 29999, 3),
    ("Nothing", "Phone (2a)", 23999, 2), ("Nothing", "CMF Phone 1", 15999, 1),
    ("Nokia", "X30", 39999, 3), ("Nokia", "G60", 29999, 3)
]

def generate_specs(brand, price):
    if price > 60000:
        processor = random.choice(["Snapdragon 8 Gen 2", "Snapdragon 8+ Gen 1", "A15 Bionic", "Tensor G2", "Dimensity 9200"])
        ram = random.choice([8, 12])
        display = random.choice(["6.7-inch AMOLED 120Hz", "6.8-inch Dynamic AMOLED 120Hz", "6.1-inch OLED 120Hz"])
        cam = random.choice(["50MP+50MP+50MP", "108MP+12MP+10MP", "48MP+12MP+12MP"])
    elif price > 30000:
        processor = random.choice(["Snapdragon 778G", "Dimensity 8100", "Snapdragon 870", "Tensor"])
        ram = random.choice([6, 8])
        display = random.choice(["6.5-inch AMOLED 120Hz", "6.67-inch AMOLED 120Hz"])
        cam = random.choice(["64MP+8MP+2MP", "50MP+8MP+2MP"])
    else:
        processor = random.choice(["Snapdragon 695", "Dimensity 700", "Helio G99"])
        ram = random.choice([4, 6])
        display = random.choice(["6.5-inch LCD 90Hz", "6.4-inch AMOLED 90Hz"])
        cam = random.choice(["50MP+2MP+2MP", "64MP+2MP"])

    return {
        "display": display,
        "processor": processor,
        "camera": cam,
        "battery": f"{random.choice([4000, 4500, 5000])} mAh",
        "charging": f"{random.choice([18, 33, 67, 120])}W Wired",
        "ipRating": random.choice(["IP68", "IP53", "None"]) if price > 20000 else "None"
    }, processor, ram, display.split("-")[0]

def generate_scores(category):
    base = 5 + category
    return {
        "durability": min(10, base + random.uniform(-1, 1)),
        "camera": min(10, base + random.uniform(-1.5, 1.5)),
        "battery": min(10, base + random.uniform(-1, 2)),
        "charging": min(10, base + random.uniform(-1, 2)),
        "display": min(10, base + random.uniform(-1, 1)),
        "sound": min(10, base + random.uniform(-1, 1)),
        "ip": 10 if category >= 4 else (5 if category >= 2 else 0)
    }

new_phones = []
for brand, name, price, cat in raw_phones:
    specs_dict, proc, ram, screen = generate_specs(brand, price)
    scores_dict = {k: round(v, 1) for k, v in generate_scores(cat).items()}
    
    decay = [1, 0.95, 0.90, 0.85, 0.80, 0.75]
    if cat >= 4: decay = [1, 0.98, 0.95, 0.92, 0.88, 0.85]
    
    phone = {
        "id": f"{brand.lower()}-{name.lower().replace(' ', '-').replace('(', '').replace(')', '')}",
        "brand": brand,
        "name": name,
        "price": f"₹{price:,}",
        "priceCategory": cat,
        "emoji": "📱",
        "uniqueFeature": "Solid performance and great value.",
        "specs": specs_dict,
        "scores": scores_dict,
        "ram_gb": ram,
        "storage_options": "128GB / 256GB" if cat >= 3 else "64GB / 128GB",
        "has_5g": True if price > 15000 else False,
        "has_nfc": True if price > 20000 else False,
        "has_wireless_charging": True if cat >= 4 else False,
        "processor_brand": proc.split()[0] if proc else "Unknown",
        "screen_size": float(screen) if '.' in screen else 6.5,
        "price_numeric": price,
        "price_history": [int(price * d) for d in decay],
        "images": [brand_logos.get(brand, "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg")]
    }
    new_phones.append(phone)


with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r"(?:var|const) PHONES = (\[.*?\]);", content, re.DOTALL)
if match:
    phones_json = match.group(1)
    try:
        phones = json.loads(phones_json)
        
        # Prevent duplicates
        existing_ids = {p["id"] for p in phones}
        added_count = 0
        for new_p in new_phones:
            if new_p["id"] not in existing_ids:
                phones.append(new_p)
                added_count += 1
                
        new_phones_json = json.dumps(phones, indent=2)
        new_content = content.replace(match.group(0), f"var PHONES = {new_phones_json};")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print(f"Successfully added {added_count} new phones. Total phones: {len(phones)}")
    except Exception as e:
        print("Error:", e)
else:
    print("Could not find PHONES array.")

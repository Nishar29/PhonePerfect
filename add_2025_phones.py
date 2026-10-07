import json
import random
import re

NEW_PHONES_DATA = [
    ("Apple", "iPhone 17 Pro Max", 169900, 5, "🍎", "Apple Intelligence Max", 6.9, 12, "Apple", True, True, True, [9.5, 9.9, 9.0, 7.8, 9.8, 9.5, 10.0, 10.0]),
    ("Apple", "iPhone 17 Pro", 144900, 5, "🍎", "Apple Intelligence", 6.3, 12, "Apple", True, True, True, [9.4, 9.8, 8.7, 7.8, 9.8, 9.4, 10.0, 10.0]),
    ("Apple", "iPhone 17 Air", 119900, 5, "🍎", "Ultra-thin design", 6.6, 8, "Apple", True, True, True, [8.5, 9.2, 8.2, 7.5, 9.5, 8.8, 9.5, 9.6]),
    ("Apple", "iPhone 17", 89900, 5, "🍎", "Standard perfection", 6.1, 8, "Apple", True, True, True, [9.0, 9.0, 8.5, 7.5, 9.3, 8.8, 10.0, 9.6]),
    
    ("Samsung", "Galaxy S25 Ultra", 134999, 5, "📱", "S-Pen & Galaxy AI", 6.8, 16, "Snapdragon", True, True, True, [9.6, 9.8, 9.2, 8.5, 9.9, 9.3, 10.0, 10.0]),
    ("Samsung", "Galaxy S25+", 104999, 5, "📱", "Galaxy AI Plus", 6.7, 12, "Snapdragon", True, True, True, [9.3, 9.4, 9.0, 8.5, 9.7, 9.0, 10.0, 9.8]),
    ("Samsung", "Galaxy S25", 84999, 5, "📱", "Compact AI", 6.2, 12, "Snapdragon", True, True, True, [9.2, 9.2, 8.6, 8.5, 9.6, 8.8, 10.0, 9.8]),
    ("Samsung", "Galaxy Z Fold 7", 164999, 5, "📱", "Ultimate foldable", 7.6, 16, "Snapdragon", True, True, True, [8.0, 9.0, 8.5, 8.0, 9.5, 9.0, 9.0, 9.8]),
    ("Samsung", "Galaxy Z Flip 7", 99999, 5, "📱", "Stylish flip", 6.7, 12, "Snapdragon", True, True, True, [8.2, 8.8, 8.3, 8.0, 9.4, 8.5, 9.0, 9.6]),
    ("Samsung", "Galaxy A56", 34999, 3, "📱", "Premium Mid-range", 6.6, 8, "Exynos", True, True, False, [8.8, 8.4, 8.8, 8.0, 9.0, 8.2, 9.5, 8.2]),
    ("Samsung", "Galaxy A36", 26999, 2, "📱", "Balanced value", 6.6, 8, "Exynos", True, True, False, [8.5, 7.8, 8.8, 7.5, 8.8, 8.0, 9.5, 7.8]),

    ("Google", "Pixel 10 Pro XL", 114999, 5, "📱", "Tensor G5 AI", 6.8, 16, "Tensor", True, True, True, [9.2, 9.9, 8.8, 8.0, 9.8, 9.0, 10.0, 9.5]),
    ("Google", "Pixel 10 Pro", 99999, 5, "📱", "Compact Pro AI", 6.3, 16, "Tensor", True, True, True, [9.2, 9.9, 8.5, 8.0, 9.7, 8.9, 10.0, 9.5]),
    ("Google", "Pixel 10", 79999, 4, "📱", "Tensor G5", 6.3, 12, "Tensor", True, True, True, [9.0, 9.6, 8.5, 7.8, 9.5, 8.6, 10.0, 9.2]),
    ("Google", "Pixel 9a", 44999, 3, "📱", "Affordable AI", 6.1, 8, "Tensor", True, True, True, [8.5, 9.0, 8.2, 7.5, 9.0, 8.0, 9.0, 8.5]),

    ("OnePlus", "13", 69999, 4, "📱", "Hasselblad perfection", 6.82, 16, "Snapdragon", True, True, True, [9.5, 9.4, 9.6, 9.8, 9.7, 9.2, 10.0, 9.9]),
    ("OnePlus", "13R", 42999, 3, "📱", "Flagship killer", 6.78, 12, "Snapdragon", True, True, False, [9.0, 8.5, 9.5, 9.8, 9.5, 8.8, 9.0, 9.5]),
    ("OnePlus", "Nord 5", 31999, 3, "📱", "Smooth mid-range", 6.74, 12, "Snapdragon", True, True, False, [8.8, 8.2, 9.2, 9.5, 9.0, 8.5, 8.5, 8.6]),
    ("OnePlus", "Nord CE 5 Lite", 19999, 2, "📱", "Entry OnePlus", 6.72, 8, "Snapdragon", True, False, False, [8.0, 7.5, 9.0, 9.0, 8.5, 8.0, 0, 7.5]),

    ("Xiaomi", "15 Ultra", 119999, 5, "📱", "Leica Photography", 6.73, 16, "Snapdragon", True, True, True, [9.3, 10.0, 9.2, 9.5, 9.7, 9.4, 10.0, 9.8]),
    ("Xiaomi", "15 Pro", 89999, 5, "📱", "Leica Pro", 6.73, 16, "Snapdragon", True, True, True, [9.2, 9.7, 9.2, 9.5, 9.6, 9.2, 10.0, 9.8]),
    ("Xiaomi", "15", 74999, 4, "📱", "Compact Flagship", 6.36, 12, "Snapdragon", True, True, True, [9.2, 9.4, 8.8, 9.2, 9.5, 9.0, 10.0, 9.8]),
    ("Xiaomi", "Redmi Note 14 Pro+", 32999, 3, "📱", "200MP Master", 6.67, 12, "MediaTek", True, True, False, [8.8, 8.8, 9.4, 9.8, 9.2, 8.8, 10.0, 8.5]),
    ("POCO", "F7 Pro", 35999, 3, "📱", "Gaming beast", 6.67, 12, "Snapdragon", True, True, False, [8.5, 8.0, 9.2, 9.8, 9.3, 8.5, 8.0, 9.6]),

    ("Motorola", "Edge 60 Pro", 84999, 5, "📱", "Moto AI", 6.7, 12, "Snapdragon", True, True, True, [9.2, 9.2, 8.8, 9.6, 9.6, 9.0, 10.0, 9.6]),
    ("Motorola", "Edge 60 Fusion", 24999, 2, "📱", "Curved beauty", 6.7, 8, "Snapdragon", True, True, False, [8.5, 8.0, 9.0, 9.2, 9.0, 8.5, 9.5, 8.0]),
    ("Motorola", "Razr 60 Ultra", 99999, 5, "📱", "Premium Flip", 6.9, 12, "Snapdragon", True, True, True, [8.2, 8.8, 8.2, 8.5, 9.5, 8.5, 9.0, 9.4]),

    ("Realme", "GT 7 Pro", 64999, 4, "📱", "Performance Core", 6.78, 16, "Snapdragon", True, True, False, [9.0, 8.8, 9.6, 10.0, 9.5, 9.0, 9.5, 9.9]),
    ("Realme", "Narzo 80 Pro", 21999, 2, "📱", "Budget gamer", 6.67, 8, "MediaTek", True, False, False, [8.2, 7.8, 9.0, 9.2, 8.8, 8.2, 8.0, 8.4]),

    ("iQOO", "13", 64999, 4, "📱", "E-sports legend", 6.78, 16, "Snapdragon", True, True, False, [9.0, 8.5, 9.5, 10.0, 9.6, 9.0, 9.5, 10.0]),
    ("iQOO", "Neo 10 Pro", 38999, 3, "📱", "Flagship killer", 6.78, 12, "MediaTek", True, True, False, [8.8, 8.2, 9.4, 9.8, 9.4, 8.8, 8.5, 9.6]),

    ("Nothing", "Phone (3)", 44999, 3, "📱", "Glyph Interface 3.0", 6.7, 12, "Snapdragon", True, True, True, [9.0, 8.8, 9.0, 8.5, 9.2, 8.5, 9.0, 9.2]),

    ("Vivo", "X200 Pro", 89999, 5, "📱", "Zeiss Imaging", 6.78, 16, "MediaTek", True, True, True, [9.2, 9.9, 9.4, 9.5, 9.6, 9.0, 10.0, 9.8]),
    ("Vivo", "V50 Pro", 42999, 3, "📱", "Portrait master", 6.78, 12, "MediaTek", True, True, False, [8.8, 9.2, 9.2, 9.2, 9.3, 8.5, 9.0, 8.8])
]

# (brand, name, price_num, category, emoji, unique, screen, ram_gb, proc_brand, 5g, nfc, wireless, [dur, cam, bat, chg, dis, snd, ip, proc])

def make_phone(data):
    brand, name, price, cat, emoji, unique, screen, ram, proc, h5g, nfc, wless, scores = data
    id_str = re.sub(r'[^a-z0-9]', '', f"{brand} {name}".lower())
    
    # generate price history
    phist = [price]
    for i in range(5):
        phist.append(int(phist[-1] * random.uniform(0.96, 0.99)))
        
    return {
        "id": id_str,
        "name": name,
        "brand": brand,
        "emoji": emoji,
        "price": f"₹{price:,}",
        "priceCategory": cat,
        "uniqueFeature": unique,
        "specs": {
            "display": f"{screen}\" AMOLED",
            "processor": proc,
            "ram": f"{ram}GB RAM",
            "battery": "5000 mAh" if "Pro Max" not in name and "Ultra" not in name else "5500 mAh",
            "charging": "Fast Wired",
            "camera": "Multiple Lenses",
            "ip": "IP68" if scores[6] >= 9 else "IP65",
            "weight": "200g",
            "build": "Premium"
        },
        "scores": {
            "durability": scores[0],
            "camera": scores[1],
            "battery": scores[2],
            "charging": scores[3],
            "display": scores[4],
            "sound": scores[5],
            "ipRating": scores[6],
            "processor": scores[7]
        },
        "images": ["https://upload.wikimedia.org/wikipedia/commons/3/3a/Mobile_phone_icon.png"],
        "ram_gb": ram,
        "storage_options": "256GB / 512GB",
        "has_5g": h5g,
        "has_nfc": nfc,
        "has_wireless_charging": wless,
        "processor_brand": proc,
        "screen_size": screen,
        "price_numeric": price,
        "price_history": phist,
        "pros": ["Great performance", "Modern design", "Good display"],
        "cons": ["Pricey" if price > 80000 else "Average cameras", "No charger in box" if brand in ["Apple", "Samsung", "Google", "Nothing"] else "Bloatware"]
    }

def main():
    try:
        with open("phones.js", "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Read error: {e}")
        return

    array_start = content.find("var PHONES = ") + len("var PHONES = ")
    array_end = content.find("];", array_start) + 1
    array_json = content[array_start:array_end]

    try:
        phones = json.loads(array_json)
    except Exception as e:
        print(f"JSON decode error: {e}")
        return

    existing_ids = {p['id'] for p in phones}
    
    added_count = 0
    for p_data in NEW_PHONES_DATA:
        p_obj = make_phone(p_data)
        if p_obj['id'] not in existing_ids:
            phones.append(p_obj)
            existing_ids.add(p_obj['id'])
            added_count += 1
            
    print(f"Added {added_count} new 2025/2026 phones.")
    
    new_array_json = json.dumps(phones, indent=2, ensure_ascii=False)
    new_content = content[:array_start] + new_array_json + ";" + content[array_end + 1:]

    with open("phones.js", "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("phones.js updated successfully.")

if __name__ == "__main__":
    main()

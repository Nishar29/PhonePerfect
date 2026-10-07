import json
import re

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
    "Huawei": "https://upload.wikimedia.org/wikipedia/commons/e/e8/Huawei_Logo.svg"
}

new_phones = [
    {
        "id": "iphone-13",
        "brand": "Apple",
        "name": "iPhone 13",
        "price": "₹52,999",
        "priceCategory": 4,
        "emoji": "📱",
        "uniqueFeature": "Classic iPhone reliability with Cinematic mode.",
        "specs": {
            "display": "6.1-inch Super Retina XDR OLED",
            "processor": "A15 Bionic",
            "camera": "12MP Wide, 12MP Ultra Wide",
            "battery": "3240 mAh",
            "charging": "20W Wired, 15W MagSafe",
            "ipRating": "IP68"
        },
        "scores": { "durability": 8, "camera": 8.5, "battery": 7.5, "charging": 6, "display": 8.5, "sound": 8, "ip": 10 },
        "ram_gb": 4,
        "storage_options": "128GB / 256GB / 512GB",
        "has_5g": True,
        "has_nfc": True,
        "has_wireless_charging": True,
        "processor_brand": "Apple",
        "screen_size": 6.1,
        "price_numeric": 52999,
        "price_history": [59999, 58000, 56000, 54000, 53500, 52999],
        "pros": ["Great OLED display", "Reliable performance", "Excellent video recording"],
        "cons": ["Only 60Hz display", "Slower charging"]
    },
    {
        "id": "samsung-s22-ultra",
        "brand": "Samsung",
        "name": "Galaxy S22 Ultra",
        "price": "₹84,999",
        "priceCategory": 5,
        "emoji": "🖊️",
        "uniqueFeature": "Built-in S Pen and powerful 100x Space Zoom.",
        "specs": {
            "display": "6.8-inch Dynamic AMOLED 2X, 120Hz",
            "processor": "Snapdragon 8 Gen 1",
            "camera": "108MP Main, 12MP UW, 2x 10MP Telephoto",
            "battery": "5000 mAh",
            "charging": "45W Wired, 15W Wireless",
            "ipRating": "IP68"
        },
        "scores": { "durability": 8, "camera": 9, "battery": 7.5, "charging": 7.5, "display": 9.5, "sound": 8.5, "ip": 10 },
        "ram_gb": 12,
        "storage_options": "256GB / 512GB",
        "has_5g": True,
        "has_nfc": True,
        "has_wireless_charging": True,
        "processor_brand": "Snapdragon",
        "screen_size": 6.8,
        "price_numeric": 84999,
        "price_history": [109999, 99999, 94999, 89999, 86999, 84999],
        "pros": ["S Pen included", "Incredible zoom cameras", "Stunning display"],
        "cons": ["Battery life is average", "Heavy and bulky"]
    },
    {
        "id": "google-pixel-6a",
        "brand": "Google",
        "name": "Pixel 6a",
        "price": "₹29,999",
        "priceCategory": 3,
        "emoji": "📸",
        "uniqueFeature": "Flagship camera processing in a compact size.",
        "specs": {
            "display": "6.1-inch OLED",
            "processor": "Google Tensor",
            "camera": "12.2MP Main, 12MP UW",
            "battery": "4410 mAh",
            "charging": "18W Wired",
            "ipRating": "IP67"
        },
        "scores": { "durability": 7, "camera": 9, "battery": 7, "charging": 5, "display": 7.5, "sound": 7.5, "ip": 9 },
        "ram_gb": 6,
        "storage_options": "128GB",
        "has_5g": True,
        "has_nfc": True,
        "has_wireless_charging": False,
        "processor_brand": "Tensor",
        "screen_size": 6.1,
        "price_numeric": 29999,
        "price_history": [43999, 39999, 34999, 31999, 30999, 29999],
        "pros": ["Best camera in its class", "Stock Android", "Compact size"],
        "cons": ["60Hz display", "Slow charging speed"]
    },
    {
        "id": "oneplus-10r",
        "brand": "OnePlus",
        "name": "10R 5G",
        "price": "₹32,999",
        "priceCategory": 3,
        "emoji": "⚡",
        "uniqueFeature": "Insane 150W SUPERVOOC charging.",
        "specs": {
            "display": "6.7-inch Fluid AMOLED, 120Hz",
            "processor": "MediaTek Dimensity 8100-Max",
            "camera": "50MP Main, 8MP UW, 2MP Macro",
            "battery": "4500 mAh",
            "charging": "150W Wired",
            "ipRating": "None"
        },
        "scores": { "durability": 6, "camera": 7, "battery": 7, "charging": 10, "display": 8.5, "sound": 8, "ip": 0 },
        "ram_gb": 12,
        "storage_options": "256GB",
        "has_5g": True,
        "has_nfc": True,
        "has_wireless_charging": False,
        "processor_brand": "MediaTek",
        "screen_size": 6.7,
        "price_numeric": 32999,
        "price_history": [38999, 36999, 34999, 33999, 33500, 32999],
        "pros": ["Lightning fast charging", "Smooth 120Hz display", "Good performance"],
        "cons": ["No official IP rating", "Average auxiliary cameras"]
    },
    {
        "id": "nothing-phone-1",
        "brand": "Nothing",
        "name": "Phone (1)",
        "price": "₹27,999",
        "priceCategory": 2,
        "emoji": "💡",
        "uniqueFeature": "Transparent back with unique Glyph interface.",
        "specs": {
            "display": "6.55-inch OLED, 120Hz",
            "processor": "Snapdragon 778G+",
            "camera": "50MP Main, 50MP UW",
            "battery": "4500 mAh",
            "charging": "33W Wired, 15W Wireless",
            "ipRating": "IP53"
        },
        "scores": { "durability": 7, "camera": 7.5, "battery": 7.5, "charging": 7, "display": 8.5, "sound": 8, "ip": 5 },
        "ram_gb": 8,
        "storage_options": "128GB / 256GB",
        "has_5g": True,
        "has_nfc": True,
        "has_wireless_charging": True,
        "processor_brand": "Snapdragon",
        "screen_size": 6.55,
        "price_numeric": 27999,
        "price_history": [32999, 30999, 29999, 28999, 28500, 27999],
        "pros": ["Unique Glyph interface", "Clean software", "Wireless charging in mid-range"],
        "cons": ["Average low-light camera", "Average battery life"]
    },
    {
        "id": "iqoo-neo-7",
        "brand": "iQOO",
        "name": "Neo 7",
        "price": "₹27,999",
        "priceCategory": 2,
        "emoji": "🎮",
        "uniqueFeature": "High-performance gaming on a budget.",
        "specs": {
            "display": "6.78-inch AMOLED, 120Hz",
            "processor": "MediaTek Dimensity 8200",
            "camera": "64MP Main, 2MP Macro, 2MP Depth",
            "battery": "5000 mAh",
            "charging": "120W Wired",
            "ipRating": "None"
        },
        "scores": { "durability": 6, "camera": 6.5, "battery": 8.5, "charging": 9.5, "display": 8, "sound": 7.5, "ip": 0 },
        "ram_gb": 8,
        "storage_options": "128GB / 256GB",
        "has_5g": True,
        "has_nfc": False,
        "has_wireless_charging": False,
        "processor_brand": "MediaTek",
        "screen_size": 6.78,
        "price_numeric": 27999,
        "price_history": [29999, 28999, 28500, 28000, 27999, 27999],
        "pros": ["Excellent gaming performance", "Super fast 120W charging", "Large battery"],
        "cons": ["No ultra-wide camera", "Funtouch OS bloatware"]
    },
    {
        "id": "poco-f5",
        "brand": "Poco",
        "name": "F5 5G",
        "price": "₹29,999",
        "priceCategory": 3,
        "emoji": "🏎️",
        "uniqueFeature": "Snapdragon 7+ Gen 2 flagship-level power.",
        "specs": {
            "display": "6.67-inch AMOLED, 120Hz",
            "processor": "Snapdragon 7+ Gen 2",
            "camera": "64MP Main, 8MP UW, 2MP Macro",
            "battery": "5000 mAh",
            "charging": "67W Wired",
            "ipRating": "IP53"
        },
        "scores": { "durability": 7, "camera": 7, "battery": 8.5, "charging": 8.5, "display": 8.5, "sound": 8, "ip": 5 },
        "ram_gb": 8,
        "storage_options": "256GB",
        "has_5g": True,
        "has_nfc": True,
        "has_wireless_charging": False,
        "processor_brand": "Snapdragon",
        "screen_size": 6.67,
        "price_numeric": 29999,
        "price_history": [29999, 29999, 29999, 29999, 29999, 29999],
        "pros": ["Outstanding performance", "Great display", "Thin and light"],
        "cons": ["Plastic build", "Average cameras"]
    },
    {
        "id": "motorola-edge-40",
        "brand": "Motorola",
        "name": "Edge 40",
        "price": "₹26,999",
        "priceCategory": 2,
        "emoji": "🌊",
        "uniqueFeature": "Slim design with IP68 rating and vegan leather.",
        "specs": {
            "display": "6.55-inch pOLED, 144Hz",
            "processor": "MediaTek Dimensity 8020",
            "camera": "50MP Main, 13MP UW",
            "battery": "4400 mAh",
            "charging": "68W Wired, 15W Wireless",
            "ipRating": "IP68"
        },
        "scores": { "durability": 8, "camera": 7.5, "battery": 7, "charging": 8.5, "display": 9, "sound": 8, "ip": 10 },
        "ram_gb": 8,
        "storage_options": "256GB",
        "has_5g": True,
        "has_nfc": True,
        "has_wireless_charging": True,
        "processor_brand": "MediaTek",
        "screen_size": 6.55,
        "price_numeric": 26999,
        "price_history": [29999, 28999, 27999, 27499, 26999, 26999],
        "pros": ["Beautiful curved display", "IP68 water resistance", "Clean UI"],
        "cons": ["Average battery life", "Software updates are slow"]
    },
    {
        "id": "realme-11-pro-plus",
        "brand": "Realme",
        "name": "11 Pro+ 5G",
        "price": "₹27,999",
        "priceCategory": 2,
        "emoji": "✨",
        "uniqueFeature": "200MP camera and luxury leather design.",
        "specs": {
            "display": "6.7-inch AMOLED, 120Hz",
            "processor": "MediaTek Dimensity 7050",
            "camera": "200MP Main, 8MP UW, 2MP Macro",
            "battery": "5000 mAh",
            "charging": "100W Wired",
            "ipRating": "None"
        },
        "scores": { "durability": 7, "camera": 8.5, "battery": 8.5, "charging": 9, "display": 8.5, "sound": 8, "ip": 0 },
        "ram_gb": 8,
        "storage_options": "256GB",
        "has_5g": True,
        "has_nfc": False,
        "has_wireless_charging": False,
        "processor_brand": "MediaTek",
        "screen_size": 6.7,
        "price_numeric": 27999,
        "price_history": [27999, 27999, 27999, 27999, 27999, 27999],
        "pros": ["Stunning design", "200MP camera", "Fast 100W charging"],
        "cons": ["Bloatware in UI", "No IP rating"]
    },
    {
        "id": "redmi-note-12-pro",
        "brand": "Redmi",
        "name": "Note 12 Pro 5G",
        "price": "₹20,999",
        "priceCategory": 2,
        "emoji": "📱",
        "uniqueFeature": "Sony IMX766 sensor with OIS on a budget.",
        "specs": {
            "display": "6.67-inch AMOLED, 120Hz",
            "processor": "MediaTek Dimensity 1080",
            "camera": "50MP Main, 8MP UW, 2MP Macro",
            "battery": "5000 mAh",
            "charging": "67W Wired",
            "ipRating": "IP53"
        },
        "scores": { "durability": 7, "camera": 8, "battery": 8.5, "charging": 8.5, "display": 8.5, "sound": 7.5, "ip": 5 },
        "ram_gb": 6,
        "storage_options": "128GB",
        "has_5g": True,
        "has_nfc": False,
        "has_wireless_charging": False,
        "processor_brand": "MediaTek",
        "screen_size": 6.67,
        "price_numeric": 20999,
        "price_history": [24999, 23999, 22999, 21999, 20999, 20999],
        "pros": ["Great main camera", "Vibrant OLED display", "Good battery life"],
        "cons": ["Still on Android 12 out of box", "Bloatware"]
    }
]

# Set the images to use brand logos
for phone in new_phones:
    brand = phone.get("brand", "")
    phone["images"] = [brand_logos.get(brand, "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg")]

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

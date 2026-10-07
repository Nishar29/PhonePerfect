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

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Match the PHONES array
match = re.search(r"(?:var|const) PHONES = (\[.*?\]);", content, re.DOTALL)
if match:
    phones_json = match.group(1)
    # The JSON might have trailing commas or JS-specific syntax, but we used json.dumps before
    # Let's try to load it
    try:
        phones = json.loads(phones_json)
        
        for phone in phones:
            brand = phone.get("brand", "")
            # Find matching logo
            logo_url = brand_logos.get(brand, "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg")
            phone["images"] = [logo_url]
            
        new_phones_json = json.dumps(phones, indent=2)
        new_content = content.replace(match.group(0), f"var PHONES = {new_phones_json};")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        print(f"Successfully replaced images for {len(phones)} phones.")
    except Exception as e:
        print("Failed to parse or save JSON:", e)
else:
    print("Could not find PHONES array.")

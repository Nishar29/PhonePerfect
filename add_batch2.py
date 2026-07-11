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

def build_phone(brand, name, price, cat, display, cpu, cam, batt, charge, ip,
                ram, storage, g5, nfc, wc, proc_brand, scrn, unique):
    decay = [1, 0.98, 0.95, 0.92, 0.88, 0.85] if cat >= 4 else (
            [1, 0.97, 0.93, 0.88, 0.82, 0.78] if cat >= 2 else
            [1, 0.95, 0.90, 0.85, 0.80, 0.75])
    base = min(9.5, 4.5 + cat * 0.85)
    def s(d=0): return round(min(10, max(3, base + d + random.uniform(-0.3, 0.3))), 1)
    return {
        "id": make_id(brand, name), "brand": brand, "name": name,
        "price": f"\u20b9{price:,}", "priceCategory": cat, "emoji": "\U0001f4f1",
        "uniqueFeature": unique,
        "specs": {"display": display, "processor": cpu, "camera": cam,
                  "battery": batt, "charging": charge, "ipRating": ip},
        "scores": {
            "durability": s(0.5 if ip != "None" else -0.3),
            "camera": s(0.8 if any(x in cam for x in ["200MP","108MP","50MP+50MP"]) else 0),
            "battery": s(0.5 if "5000" in batt or "6000" in batt else 0),
            "charging": s(1.0 if any(x in charge for x in ["100W","120W","150W","240W","80W"]) else 0),
            "display": s(0.5 if "AMOLED" in display or "OLED" in display else -0.3),
            "sound": s(0), "ip": 10 if ip == "IP68" else (5 if "IP5" in ip else 0)
        },
        "ram_gb": ram, "storage_options": storage,
        "has_5g": g5, "has_nfc": nfc, "has_wireless_charging": wc,
        "processor_brand": proc_brand, "screen_size": scrn,
        "price_numeric": price,
        "price_history": [int(price * d) for d in decay],
        "images": [brand_logos.get(brand, brand_logos["TCL"])]
    }

P = build_phone

phones_batch = [
    # ===== SAMSUNG (older + budget + mid) =====
    P("Samsung","Galaxy A55",34999,3,"6.6-inch AMOLED 120Hz","Exynos 1480","50MP+12MP+5MP","5000 mAh","25W Wired","IP67",8,"128GB/256GB",True,True,False,"Exynos",6.6,"Samsung's best mid-ranger with IP67."),
    P("Samsung","Galaxy A35",27999,2,"6.6-inch AMOLED 120Hz","Exynos 1380","50MP+8MP+5MP","5000 mAh","25W Wired","IP67",6,"128GB/256GB",True,True,False,"Exynos",6.6,"IP67 water resistance at mid-range price."),
    P("Samsung","Galaxy A25",16999,1,"6.5-inch AMOLED 120Hz","Exynos 1280","50MP+8MP+2MP","5000 mAh","25W Wired","IP67",6,"128GB",True,False,False,"Exynos",6.5,"IP67 in budget segment — Samsung exclusive."),
    P("Samsung","Galaxy A15",12999,1,"6.5-inch AMOLED 90Hz","MediaTek Helio G99","50MP+5MP+2MP","5000 mAh","25W Wired","None",4,"128GB",False,False,False,"MediaTek",6.5,"AMOLED display in ultra-budget."),
    P("Samsung","Galaxy A05s",9999,1,"6.7-inch PLS LCD","Snapdragon 680","50MP+2MP+2MP","5000 mAh","15W Wired","None",4,"64GB/128GB",False,False,False,"Snapdragon",6.7,"Large screen budget Samsung."),
    P("Samsung","Galaxy M55",29999,3,"6.7-inch AMOLED 120Hz","Snapdragon 7 Gen 1","50MP+8MP+2MP","5000 mAh","45W Wired","None",8,"128GB/256GB",True,True,False,"Snapdragon",6.7,"Snapdragon 7 Gen 1 M-series flagship."),
    P("Samsung","Galaxy M35",18999,2,"6.6-inch AMOLED 120Hz","Exynos 1380","50MP+8MP+2MP","6000 mAh","25W Wired","None",6,"128GB",True,False,False,"Exynos",6.6,"Monster 6000mAh battery."),
    P("Samsung","Galaxy M15",10999,1,"6.5-inch AMOLED 90Hz","MediaTek Dimensity 6100+","50MP+5MP+2MP","6000 mAh","25W Wired","None",4,"128GB",True,False,False,"MediaTek",6.5,"6000mAh battery with 5G under 11K."),
    P("Samsung","Galaxy F55",26999,2,"6.7-inch AMOLED 120Hz","Snapdragon 7 Gen 1","50MP+8MP+2MP","5000 mAh","45W Wired","None",8,"128GB/256GB",True,True,False,"Snapdragon",6.7,"Vegan leather back with flagship feel."),
    P("Samsung","Galaxy F34",16999,1,"6.5-inch AMOLED 120Hz","Exynos 1280","50MP+8MP+2MP","6000 mAh","25W Wired","None",6,"128GB",True,False,False,"Exynos",6.5,"6000mAh + AMOLED combo under 17K."),
    P("Samsung","Galaxy F15",11999,1,"6.5-inch AMOLED 90Hz","MediaTek Dimensity 6100+","50MP+5MP+2MP","6000 mAh","25W Wired","None",4,"128GB",True,False,False,"MediaTek",6.5,"Budget Samsung with massive battery."),
    P("Samsung","Galaxy S23",69999,4,"6.1-inch AMOLED 120Hz","Snapdragon 8 Gen 2","50MP+12MP+10MP","3900 mAh","25W Wired + 15W Wireless","IP68",8,"128GB/256GB",True,True,True,"Snapdragon",6.1,"Compact flagship with S8 Gen 2."),
    P("Samsung","Galaxy S23 Plus",89999,5,"6.6-inch AMOLED 120Hz","Snapdragon 8 Gen 2","50MP+12MP+10MP","4700 mAh","45W Wired + 15W Wireless","IP68",8,"256GB",True,True,True,"Snapdragon",6.6,"Larger S23 with bigger battery."),
    P("Samsung","Galaxy S23 Ultra",124999,5,"6.8-inch AMOLED 120Hz","Snapdragon 8 Gen 2","200MP+12MP+10MP+10MP","5000 mAh","45W Wired + 15W Wireless","IP68",12,"256GB/512GB/1TB",True,True,True,"Snapdragon",6.8,"200MP camera with S Pen and 100x zoom."),
    P("Samsung","Galaxy Z Flip5",99999,5,"6.7-inch AMOLED 120Hz Foldable","Snapdragon 8 Gen 2","12MP+12MP","3700 mAh","25W Wired + 15W Wireless","IPX8",8,"256GB/512GB",True,True,True,"Snapdragon",6.7,"Flip phone with large cover screen."),
    P("Samsung","Galaxy Z Fold5",154999,5,"7.6-inch AMOLED 120Hz Foldable","Snapdragon 8 Gen 2","50MP+12MP+10MP","4400 mAh","25W Wired + 15W Wireless","IPX8",12,"256GB/512GB/1TB",True,True,True,"Snapdragon",7.6,"Book-style foldable with S Pen support."),
    P("Samsung","Galaxy Z Flip6",109999,5,"6.7-inch AMOLED 120Hz Foldable","Snapdragon 8 Gen 3","50MP+12MP","4000 mAh","25W Wired + 15W Wireless","IP48",8,"256GB/512GB",True,True,True,"Snapdragon",6.7,"Latest flip phone with Galaxy AI features."),
    P("Samsung","Galaxy Z Fold6",164999,5,"7.6-inch AMOLED 120Hz Foldable","Snapdragon 8 Gen 3","50MP+12MP+10MP","4400 mAh","25W Wired + 15W Wireless","IP48",12,"256GB/512GB/1TB",True,True,True,"Snapdragon",7.6,"Slimmer foldable with Galaxy AI."),
    P("Samsung","Galaxy A24",18999,2,"6.5-inch AMOLED 90Hz","MediaTek Helio G99","50MP+5MP+2MP","5000 mAh","25W Wired","None",6,"128GB",False,False,False,"MediaTek",6.5,"Clean AMOLED mid-ranger from Samsung."),

    # ===== APPLE (older models) =====
    P("Apple","iPhone 13 Pro Max",129999,5,"6.7-inch OLED 120Hz ProMotion","A15 Bionic","12MP+12MP+12MP","4352 mAh","27W Wired + 15W MagSafe","IP68",6,"128GB/256GB/512GB/1TB",True,True,True,"Apple",6.7,"ProMotion display + cinematic mode."),
    P("Apple","iPhone 13 Pro",119999,5,"6.1-inch OLED 120Hz ProMotion","A15 Bionic","12MP+12MP+12MP","3095 mAh","27W Wired + 15W MagSafe","IP68",6,"128GB/256GB/512GB/1TB",True,True,True,"Apple",6.1,"Compact Pro with 120Hz ProMotion."),
    P("Apple","iPhone 13 mini",59999,4,"5.4-inch OLED","A15 Bionic","12MP+12MP","2438 mAh","20W Wired + 15W MagSafe","IP68",4,"128GB/256GB/512GB",True,True,True,"Apple",5.4,"Ultra-compact iPhone with flagship power."),
    P("Apple","iPhone 12 Pro Max",109999,5,"6.7-inch OLED","A14 Bionic","12MP+12MP+12MP","3687 mAh","20W Wired + 15W MagSafe","IP68",6,"128GB/256GB/512GB",True,True,True,"Apple",6.7,"The largest iPhone 12 with sensor-shift OIS."),
    P("Apple","iPhone 12 Pro",99999,5,"6.1-inch OLED","A14 Bionic","12MP+12MP+12MP","2815 mAh","20W Wired + 15W MagSafe","IP68",6,"128GB/256GB/512GB",True,True,True,"Apple",6.1,"LiDAR scanner + ProRAW photography."),
    P("Apple","iPhone 12",54999,4,"6.1-inch OLED","A14 Bionic","12MP+12MP","2815 mAh","20W Wired + 15W MagSafe","IP68",4,"64GB/128GB/256GB",True,True,True,"Apple",6.1,"First iPhone with MagSafe + Ceramic Shield."),
    P("Apple","iPhone 12 mini",44999,3,"5.4-inch OLED","A14 Bionic","12MP+12MP","2227 mAh","20W Wired + 15W MagSafe","IP68",4,"64GB/128GB/256GB",True,True,True,"Apple",5.4,"Tiniest 5G iPhone ever made."),
    P("Apple","iPhone 11",37999,3,"6.1-inch Liquid Retina LCD","A13 Bionic","12MP+12MP","3110 mAh","18W Wired","IP68",4,"64GB/128GB/256GB",True,True,False,"Apple",6.1,"Best-selling iPhone of its generation."),
    P("Apple","iPhone SE 3rd Gen",42999,3,"4.7-inch Retina LCD","A15 Bionic","12MP","2018 mAh","20W Wired + 7.5W Qi","IP67",4,"64GB/128GB/256GB",True,True,True,"Apple",4.7,"A15 Bionic power in a compact classic design."),
    P("Apple","iPhone 14 Plus",79999,4,"6.7-inch OLED","A15 Bionic","12MP+12MP","4325 mAh","20W Wired + 15W MagSafe","IP68",6,"128GB/256GB/512GB",True,True,True,"Apple",6.7,"Big-screen iPhone with all-day battery."),

    # ===== ONEPLUS =====
    P("OnePlus","12R",39999,3,"6.78-inch AMOLED 120Hz","Snapdragon 8 Gen 2","50MP+8MP+2MP","5500 mAh","100W Wired","None",8,"128GB/256GB",True,True,False,"Snapdragon",6.78,"100W SUPERVOOC + S8 Gen 2 at budget price."),
    P("OnePlus","11R",39999,3,"6.74-inch AMOLED 120Hz","Snapdragon 8+ Gen 1","50MP+8MP+2MP","5000 mAh","100W Wired","None",8,"128GB/256GB",True,True,False,"Snapdragon",6.74,"Flagship experience at mid-range price."),
    P("OnePlus","Nord CE 3",24999,2,"6.7-inch AMOLED 120Hz","Snapdragon 782G","50MP+8MP+2MP","5000 mAh","80W Wired","None",8,"128GB/256GB",True,True,False,"Snapdragon",6.7,"80W charging in compact Nord design."),
    P("OnePlus","Nord CE 3 Lite",19999,2,"6.72-inch IPS LCD 120Hz","Snapdragon 695","108MP+2MP+2MP","5000 mAh","67W Wired","None",8,"128GB",True,False,False,"Snapdragon",6.72,"108MP camera budget Nord."),
    P("OnePlus","Nord CE 4 Lite",19999,2,"6.67-inch AMOLED 120Hz","Snapdragon 695","50MP+2MP","5500 mAh","80W Wired","None",8,"128GB/256GB",True,False,False,"Snapdragon",6.67,"5500mAh + AMOLED in budget segment."),
    P("OnePlus","Nord 4",29999,3,"6.74-inch AMOLED 120Hz","Snapdragon 7+ Gen 3","50MP+8MP","5500 mAh","100W Wired","None",8,"128GB/256GB",True,True,False,"Snapdragon",6.74,"Metal unibody design — last of its kind."),
    P("OnePlus","Open",149999,5,"7.82-inch AMOLED 120Hz Foldable","Snapdragon 8 Gen 2","48MP+64MP+48MP","4805 mAh","67W Wired","IPX4",16,"512GB",True,True,False,"Snapdragon",7.82,"OnePlus's first foldable with Hasselblad cameras."),
    P("OnePlus","Ace 3V",24999,2,"6.74-inch AMOLED 120Hz","MediaTek Dimensity 7050","64MP+2MP","5500 mAh","100W Wired","None",8,"128GB/256GB",True,False,False,"MediaTek",6.74,"100W SUPERVOOC at budget price."),

    # ===== XIAOMI =====
    P("Xiaomi","14 Ultra",99999,5,"6.73-inch AMOLED 120Hz","Snapdragon 8 Gen 3","50MP+50MP+50MP+50MP Leica","5300 mAh","90W Wired + 50W Wireless","IP68",16,"512GB/1TB",True,True,True,"Snapdragon",6.73,"Quad 50MP Leica cameras — ultimate camera phone."),
    P("Xiaomi","14",64999,4,"6.36-inch AMOLED 120Hz","Snapdragon 8 Gen 3","50MP+50MP+50MP Leica","4610 mAh","90W Wired + 50W Wireless","IP68",12,"256GB/512GB",True,True,True,"Snapdragon",6.36,"Compact Leica flagship with IP68."),
    P("Xiaomi","14T Pro",54999,4,"6.67-inch AMOLED 144Hz","MediaTek Dimensity 9300+","50MP+50MP+12MP Leica","5000 mAh","120W Wired","IP68",12,"256GB/512GB/1TB",True,True,False,"MediaTek",6.67,"Leica cameras with 120W HyperCharge."),
    P("Xiaomi","14T",44999,3,"6.67-inch AMOLED 144Hz","MediaTek Dimensity 8300 Ultra","50MP+50MP+12MP Leica","5000 mAh","67W Wired","IP68",12,"256GB/512GB",True,True,False,"MediaTek",6.67,"Affordable Leica camera phone with IP68."),
    P("Xiaomi","13T Pro",49999,4,"6.67-inch AMOLED 144Hz","MediaTek Dimensity 9200+","50MP+50MP+12MP Leica","5000 mAh","120W Wired","IP68",12,"256GB/512GB",True,True,False,"MediaTek",6.67,"Leica cameras + 120W — unbeatable combo."),
    P("Xiaomi","13T",39999,3,"6.67-inch AMOLED 144Hz","MediaTek Dimensity 8200 Ultra","50MP+50MP+12MP Leica","5000 mAh","67W Wired","IP68",8,"256GB",True,True,False,"MediaTek",6.67,"Leica lens at mid-range price."),
    P("Xiaomi","13 Lite",29999,3,"6.55-inch AMOLED 120Hz","Snapdragon 7 Gen 1","50MP+8MP+2MP","4500 mAh","67W Wired","None",8,"128GB/256GB",True,True,False,"Snapdragon",6.55,"Slim and light with Snapdragon 7."),
    P("Xiaomi","12T Pro",44999,3,"6.67-inch AMOLED 120Hz","Snapdragon 8+ Gen 1","200MP+8MP+2MP","5000 mAh","120W Wired","None",8,"128GB/256GB",True,True,False,"Snapdragon",6.67,"200MP camera with 120W HyperCharge."),
    P("Xiaomi","12T",34999,3,"6.67-inch AMOLED 120Hz","MediaTek Dimensity 8100 Ultra","108MP+8MP+2MP","5000 mAh","120W Wired","None",8,"128GB/256GB",True,True,False,"MediaTek",6.67,"108MP + 120W at mid-range price."),
    P("Xiaomi","Mix Fold 4",149999,5,"7.98-inch AMOLED 120Hz Foldable","Snapdragon 8 Gen 3","50MP+10MP+50MP+12MP Leica","5100 mAh","67W Wired","IPX8",16,"512GB/1TB",True,True,False,"Snapdragon",7.98,"Ultra-thin foldable with Leica quad cameras."),

    # ===== REDMI =====
    P("Redmi","Note 14 Pro Plus",31999,3,"6.67-inch AMOLED 120Hz","Snapdragon 7s Gen 3","200MP+8MP+2MP","5110 mAh","90W Wired","IP68",8,"128GB/256GB",True,True,False,"Snapdragon",6.67,"200MP camera + IP68 budget flagship."),
    P("Redmi","Note 14 Pro",25999,2,"6.67-inch AMOLED 120Hz","MediaTek Dimensity 7300 Ultra","50MP+8MP+2MP","5500 mAh","45W Wired","IP54",8,"128GB/256GB",True,False,False,"MediaTek",6.67,"5500mAh battery king with AMOLED."),
    P("Redmi","Note 14",15999,1,"6.67-inch AMOLED 120Hz","MediaTek Dimensity 7025 Ultra","108MP+2MP","5110 mAh","33W Wired","IP54",6,"128GB/256GB",False,False,False,"MediaTek",6.67,"108MP AMOLED under 16K."),
    P("Redmi","14C",8999,1,"6.88-inch IPS LCD 120Hz","MediaTek Helio G81 Ultra","50MP","5160 mAh","18W Wired","None",4,"64GB/128GB",False,False,False,"MediaTek",6.88,"Large screen budget phone."),
    P("Redmi","13",12999,1,"6.79-inch IPS LCD 120Hz","Snapdragon 4 Gen 2","108MP+2MP","5030 mAh","33W Wired","None",6,"128GB/256GB",True,False,False,"Snapdragon",6.79,"5G with 108MP under 13K."),
    P("Redmi","13C",8999,1,"6.74-inch IPS LCD 90Hz","MediaTek Helio G85","50MP+2MP","5000 mAh","18W Wired","None",4,"64GB/128GB",False,False,False,"MediaTek",6.74,"Ultra-budget with big battery."),
    P("Redmi","Note 11 Pro Plus",22999,2,"6.67-inch AMOLED 120Hz","MediaTek Dimensity 920","108MP+8MP+2MP","5000 mAh","67W Wired","None",6,"128GB/256GB",True,True,False,"MediaTek",6.67,"108MP powerhouse with fast charging."),
    P("Redmi","Note 11S",16999,1,"6.43-inch AMOLED 90Hz","MediaTek Helio G96","108MP+8MP+2MP+2MP","5000 mAh","33W Wired","None",6,"64GB/128GB",False,False,False,"MediaTek",6.43,"108MP quad camera at budget price."),
    P("Redmi","Note 10 Pro",18999,2,"6.67-inch AMOLED 120Hz","Snapdragon 732G","108MP+8MP+5MP+2MP","5020 mAh","33W Wired","IP53",6,"64GB/128GB",False,True,False,"Snapdragon",6.67,"Game-changing AMOLED mid-ranger."),
    P("Redmi","K60",34999,3,"6.67-inch AMOLED 120Hz","Snapdragon 8+ Gen 1","64MP+8MP+2MP","5500 mAh","67W Wired + 30W Wireless","None",8,"128GB/256GB/512GB",True,True,True,"Snapdragon",6.67,"Flagship killer with wireless charging."),
    P("Redmi","Turbo 3",29999,3,"6.67-inch AMOLED 120Hz","Snapdragon 8s Gen 3","50MP+8MP","5000 mAh","90W Wired","None",8,"256GB/512GB",True,True,False,"Snapdragon",6.67,"Snapdragon 8s Gen 3 gaming mid-ranger."),

    # ===== VIVO =====
    P("Vivo","X200 Pro",94999,5,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 9400","50MP+50MP+200MP ZEISS","6000 mAh","90W Wired","IP69",16,"256GB/512GB",True,True,True,"MediaTek",6.78,"200MP ZEISS periscope with IP69 rating."),
    P("Vivo","X200",69999,4,"6.67-inch AMOLED 120Hz","MediaTek Dimensity 9400","50MP+50MP+50MP ZEISS","5800 mAh","90W Wired","IP68",12,"256GB/512GB",True,True,False,"MediaTek",6.67,"Dimensity 9400 camera flagship."),
    P("Vivo","V40 Pro",49999,4,"6.78-inch AMOLED 120Hz","Snapdragon 7 Gen 3","50MP+50MP ZEISS","5500 mAh","80W Wired","IP68",12,"256GB",True,True,False,"Snapdragon",6.78,"ZEISS optics in mid-range with IP68."),
    P("Vivo","V40",34999,3,"6.78-inch AMOLED 120Hz","Snapdragon 7 Gen 3","50MP+50MP ZEISS","5500 mAh","80W Wired","IP68",8,"128GB/256GB",True,True,False,"Snapdragon",6.78,"IP68 mid-ranger with ZEISS."),
    P("Vivo","V40e",27999,2,"6.77-inch AMOLED 120Hz","MediaTek Dimensity 7300","50MP+8MP","5500 mAh","80W Wired","IP64",8,"128GB/256GB",True,False,False,"MediaTek",6.77,"Slim AMOLED mid-ranger."),
    P("Vivo","T3 Pro",24999,2,"6.77-inch AMOLED 120Hz","Snapdragon 7 Gen 3","50MP+8MP","5500 mAh","80W Wired","IP68",8,"128GB/256GB",True,True,False,"Snapdragon",6.77,"IP68 + Snapdragon 7 Gen 3 under 25K."),
    P("Vivo","T3x",14999,1,"6.72-inch IPS LCD 120Hz","Snapdragon 6 Gen 1","50MP+2MP","6000 mAh","44W Wired","None",6,"128GB",True,False,False,"Snapdragon",6.72,"Massive 6000mAh battery in budget."),
    P("Vivo","T3 Ultra",32999,3,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 9200+","50MP+8MP","5500 mAh","80W Wired","IP68",8,"128GB/256GB",True,True,False,"MediaTek",6.78,"D9200+ flagship power at mid-range."),
    P("Vivo","Y300",20999,2,"6.67-inch AMOLED 120Hz","Snapdragon 4 Gen 2","50MP+2MP","5000 mAh","44W Wired","IP64",8,"128GB/256GB",True,False,False,"Snapdragon",6.67,"Affordable AMOLED with 5G."),
    P("Vivo","Y28",13999,1,"6.56-inch IPS LCD 90Hz","MediaTek Helio G85","50MP+2MP","6000 mAh","15W Wired","IP64",4,"128GB",False,False,False,"MediaTek",6.56,"6000mAh budget phone."),

    # ===== REALME =====
    P("Realme","GT 6",34999,3,"6.78-inch AMOLED 120Hz","Snapdragon 7+ Gen 3","50MP+8MP+2MP","5500 mAh","120W Wired","IP65",8,"128GB/256GB",True,True,False,"Snapdragon",6.78,"120W SUPERVOOC with IP65."),
    P("Realme","GT 6T",29999,3,"6.78-inch AMOLED 120Hz","Snapdragon 7+ Gen 3","50MP+2MP","5500 mAh","120W Wired","IP65",8,"128GB/256GB",True,True,False,"Snapdragon",6.78,"120W charging flagship killer."),
    P("Realme","P1 Pro",19999,2,"6.7-inch AMOLED 120Hz","Snapdragon 6 Gen 1","50MP+8MP","5000 mAh","45W Wired","IP65",8,"128GB/256GB",True,False,False,"Snapdragon",6.7,"IP65 mid-ranger with AMOLED."),
    P("Realme","P1",16999,1,"6.67-inch IPS LCD 120Hz","MediaTek Dimensity 7050","50MP+2MP","5000 mAh","45W Wired","None",6,"128GB/256GB",True,False,False,"MediaTek",6.67,"Budget 5G performer."),
    P("Realme","Narzo 70",14999,1,"6.72-inch AMOLED 120Hz","MediaTek Dimensity 7050","50MP+2MP","5000 mAh","45W Wired","None",6,"128GB",True,False,False,"MediaTek",6.72,"AMOLED in Narzo budget line."),
    P("Realme","Narzo 60",16999,1,"6.4-inch AMOLED 90Hz","MediaTek Dimensity 6020","64MP+2MP","5000 mAh","33W Wired","None",8,"128GB/256GB",True,False,False,"MediaTek",6.4,"Compact AMOLED with 5G."),
    P("Realme","12 Pro Plus",29999,3,"6.7-inch AMOLED 120Hz","Snapdragon 7s Gen 2","50MP+64MP+8MP","5000 mAh","67W Wired","None",8,"128GB/256GB",True,True,False,"Snapdragon",6.7,"Periscope zoom camera mid-ranger."),
    P("Realme","12 Pro",23999,2,"6.7-inch AMOLED 120Hz","Snapdragon 6 Gen 1","50MP+32MP+8MP","5000 mAh","67W Wired","None",8,"128GB/256GB",True,True,False,"Snapdragon",6.7,"Portrait camera specialist."),
    P("Realme","12",17999,1,"6.72-inch IPS LCD 90Hz","MediaTek Dimensity 6100+","108MP+2MP","5000 mAh","45W Wired","None",8,"128GB/256GB",True,False,False,"MediaTek",6.72,"108MP budget 5G phone."),

    # ===== OPPO =====
    P("Oppo","Find N3 Flip",89999,5,"6.8-inch AMOLED 120Hz Foldable","MediaTek Dimensity 9200","50MP+48MP+32MP","4300 mAh","44W Wired","IPX4",12,"256GB",True,True,False,"MediaTek",6.8,"Best cover screen on a flip phone."),
    P("Oppo","Reno 12 Pro",36999,3,"6.7-inch AMOLED 120Hz","MediaTek Dimensity 7300","50MP+8MP+2MP","5000 mAh","80W Wired","IP65",12,"256GB",True,True,False,"MediaTek",6.7,"AI features with IP65 mid-ranger."),
    P("Oppo","Reno 12",32999,3,"6.7-inch AMOLED 120Hz","MediaTek Dimensity 7300","50MP+8MP+2MP","5000 mAh","80W Wired","IP65",8,"128GB/256GB",True,True,False,"MediaTek",6.7,"AI portrait master."),
    P("Oppo","F27 Pro Plus",27999,2,"6.7-inch AMOLED 120Hz","MediaTek Dimensity 7050","64MP+2MP","5000 mAh","67W Wired","IP66/IP69",8,"128GB/256GB",True,False,False,"MediaTek",6.7,"IP69 Swiss Armor Edition."),
    P("Oppo","A3 Pro",17999,1,"6.67-inch AMOLED 120Hz","MediaTek Dimensity 6300","50MP+2MP","5100 mAh","45W Wired","IP66/IP69",8,"128GB",True,False,False,"MediaTek",6.67,"IP69 under 18K — unbeatable durability."),
    P("Oppo","A3",12999,1,"6.67-inch IPS LCD 90Hz","MediaTek Dimensity 6300","50MP+2MP","5100 mAh","45W Wired","IP54",6,"128GB",True,False,False,"MediaTek",6.67,"Budget 5G with IP54 protection."),
    P("Oppo","K12x",12999,1,"6.67-inch IPS LCD 120Hz","Snapdragon 4 Gen 2","50MP+2MP","5100 mAh","45W Wired","IP54",6,"128GB",True,False,False,"Snapdragon",6.67,"Snapdragon budget all-rounder."),

    # ===== MOTOROLA =====
    P("Motorola","Edge 50 Neo",23999,2,"6.36-inch pOLED 120Hz","MediaTek Dimensity 7300","50MP+13MP+10MP","4310 mAh","68W Wired","IP68",8,"256GB",True,True,False,"MediaTek",6.36,"Compact IP68 pOLED mid-ranger."),
    P("Motorola","Razr 50",59999,4,"6.9-inch pOLED 120Hz Foldable","MediaTek Dimensity 7300X","50MP+13MP","4200 mAh","30W Wired + 15W Wireless","IP52",8,"256GB",True,True,True,"MediaTek",6.9,"Most affordable flip phone with large cover display."),
    P("Motorola","G85",19999,2,"6.67-inch pOLED 120Hz","Snapdragon 6s Gen 3","50MP+8MP","5000 mAh","33W Wired","IP52",8,"128GB/256GB",True,False,False,"Snapdragon",6.67,"pOLED display under 20K."),
    P("Motorola","G55",12999,1,"6.49-inch IPS LCD 120Hz","MediaTek Dimensity 7025","50MP+2MP","5000 mAh","18W Wired","IP52",4,"128GB",True,False,False,"MediaTek",6.49,"Budget 5G with IP52."),
    P("Motorola","Edge 40 Neo",24999,2,"6.55-inch pOLED 144Hz","MediaTek Dimensity 7030","50MP+13MP","5000 mAh","68W Wired","IP68",8,"256GB",True,True,False,"MediaTek",6.55,"IP68 at sub-25K — amazing."),

    # ===== POCO =====
    P("Poco","F5 Pro",39999,3,"6.67-inch AMOLED 120Hz","Snapdragon 8+ Gen 1","64MP+8MP+2MP","5160 mAh","67W Wired","None",12,"256GB/512GB",True,True,False,"Snapdragon",6.67,"S8+ Gen 1 powerhouse."),
    P("Poco","X6 Neo",15999,1,"6.67-inch AMOLED 120Hz","MediaTek Dimensity 6080","108MP+2MP","5000 mAh","33W Wired","None",6,"128GB/256GB",True,False,False,"MediaTek",6.67,"AMOLED + 108MP under 16K."),
    P("Poco","M6 5G",11999,1,"6.74-inch IPS LCD 90Hz","Snapdragon 4 Gen 2","50MP+2MP","5000 mAh","18W Wired","None",4,"64GB/128GB",True,False,False,"Snapdragon",6.74,"Most affordable Poco 5G."),
    P("Poco","C65",7999,1,"6.74-inch IPS LCD 90Hz","MediaTek Helio G85","50MP+2MP","5000 mAh","18W Wired","None",4,"64GB/128GB",False,False,False,"MediaTek",6.74,"Ultra-budget Poco for essentials."),
    P("Poco","X5",17999,1,"6.67-inch AMOLED 120Hz","Snapdragon 695","48MP+8MP+2MP","5000 mAh","33W Wired","None",6,"128GB/256GB",True,False,False,"Snapdragon",6.67,"Budget AMOLED with decent specs."),

    # ===== iQOO =====
    P("iQOO","13",54999,4,"6.82-inch AMOLED 144Hz","Snapdragon 8 Elite","50MP+50MP+50MP","6000 mAh","120W Wired","IP68",12,"256GB/512GB",True,True,False,"Snapdragon",6.82,"Snapdragon 8 Elite with 6000mAh."),
    P("iQOO","Neo 7 Pro",34999,3,"6.78-inch AMOLED 120Hz","Snapdragon 8+ Gen 1","50MP+8MP+2MP","5000 mAh","120W Wired","None",8,"128GB/256GB",True,True,False,"Snapdragon",6.78,"S8+ Gen 1 budget powerhouse."),
    P("iQOO","Z9x",12999,1,"6.72-inch IPS LCD 120Hz","Snapdragon 6 Gen 1","50MP+2MP","6000 mAh","44W Wired","None",6,"128GB",True,False,False,"Snapdragon",6.72,"6000mAh monster battery under 13K."),
    P("iQOO","Z9",18999,2,"6.67-inch AMOLED 120Hz","MediaTek Dimensity 7200","50MP+2MP","5000 mAh","44W Wired","None",8,"128GB/256GB",True,False,False,"MediaTek",6.67,"AMOLED value champion."),

    # ===== NOTHING =====
    P("Nothing","Phone (2a) Plus Community Edition",27999,2,"6.7-inch AMOLED 120Hz","MediaTek Dimensity 7350 Pro","50MP+50MP","5000 mAh","50W Wired","IP54",12,"256GB",True,True,False,"MediaTek",6.7,"Community-designed edition."),

    # ===== HONOR =====
    P("Honor","200 Pro",57999,4,"6.78-inch AMOLED 120Hz","Snapdragon 8s Gen 3","50MP+50MP+12MP","5200 mAh","100W Wired","IP65",12,"256GB/512GB",True,True,False,"Snapdragon",6.78,"Studio Harcourt portrait camera flagship."),
    P("Honor","200",44999,3,"6.7-inch AMOLED 120Hz","Snapdragon 7 Gen 3","50MP+50MP+12MP","5200 mAh","100W Wired","IP65",12,"256GB/512GB",True,True,False,"Snapdragon",6.7,"100W charging with portrait AI."),
    P("Honor","X7b",14999,1,"6.7-inch IPS LCD 90Hz","MediaTek Helio G99","108MP+5MP+2MP","6000 mAh","35W Wired","None",8,"256GB",False,False,False,"MediaTek",6.7,"6000mAh monster with 108MP."),
    P("Honor","Magic 6 Pro",89999,5,"6.78-inch AMOLED 120Hz","Snapdragon 8 Gen 3","50MP+180MP+50MP","5600 mAh","80W Wired + 66W Wireless","IP68",16,"512GB",True,True,True,"Snapdragon",6.78,"180MP periscope + IP68 flagship."),

    # ===== TECNO =====
    P("Tecno","Camon 30 Pro",29999,3,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 8200","50MP+50MP+2MP","5000 mAh","70W Wired","None",12,"256GB",True,True,False,"MediaTek",6.78,"Vlog camera with dual 50MP."),
    P("Tecno","Camon 30",21999,2,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 7020","50MP+2MP","5000 mAh","33W Wired","None",8,"256GB",True,False,False,"MediaTek",6.78,"Budget AMOLED camera phone."),
    P("Tecno","Spark 20 Pro Plus",14999,1,"6.78-inch AMOLED 120Hz","MediaTek Helio G99","108MP+2MP","5000 mAh","33W Wired","None",8,"256GB",False,False,False,"MediaTek",6.78,"AMOLED + 108MP under 15K."),
    P("Tecno","Spark 20",10999,1,"6.56-inch IPS LCD 90Hz","MediaTek Helio G85","50MP+2MP","5000 mAh","18W Wired","None",8,"128GB",False,False,False,"MediaTek",6.56,"Affordable Tecno all-rounder."),
    P("Tecno","Phantom V Fold",89999,5,"7.85-inch AMOLED 120Hz Foldable","MediaTek Dimensity 9000+","50MP+13MP+50MP","5000 mAh","45W Wired","None",12,"256GB",True,True,False,"MediaTek",7.85,"Most affordable foldable phone."),
    P("Tecno","Pova 6 Pro",18999,2,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 6080","108MP+2MP","6000 mAh","33W Wired","None",8,"256GB",True,False,False,"MediaTek",6.78,"Gaming phone with 6000mAh."),

    # ===== INFINIX =====
    P("Infinix","GT 20 Pro",24999,2,"6.78-inch AMOLED 144Hz","MediaTek Dimensity 8200 Ultimate","108MP+2MP+2MP","5000 mAh","45W Wired","None",8,"256GB",True,False,False,"MediaTek",6.78,"Budget gaming phone with LED lights."),
    P("Infinix","Zero 40",24999,2,"6.78-inch AMOLED 144Hz","MediaTek Dimensity 8200","108MP+50MP+2MP","5000 mAh","45W Wired","None",12,"256GB",True,True,False,"MediaTek",6.78,"GoPro partnership for action camera."),
    P("Infinix","Note 40 Pro Plus",24999,2,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 7020","108MP+2MP+2MP","4600 mAh","100W Wired + 20W Wireless","None",12,"256GB",True,False,True,"MediaTek",6.78,"100W + wireless charging under 25K."),
    P("Infinix","Note 40 Pro",21999,2,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 7020","108MP+2MP","5000 mAh","100W Wired","None",8,"256GB",True,False,False,"MediaTek",6.78,"100W charging at budget price."),
    P("Infinix","Note 40",16999,1,"6.78-inch AMOLED 120Hz","MediaTek Helio G99","108MP+2MP","5000 mAh","45W Wired","None",8,"256GB",False,False,False,"MediaTek",6.78,"AMOLED + 108MP under 17K."),
    P("Infinix","Hot 50 Pro",11999,1,"6.78-inch IPS LCD 120Hz","MediaTek Helio G100","50MP+2MP","5000 mAh","33W Wired","None",8,"128GB/256GB",True,False,False,"MediaTek",6.78,"Budget 5G with big battery."),
    P("Infinix","Smart 8 Plus",7999,1,"6.6-inch IPS LCD 90Hz","Unisoc T606","50MP+2MP","5000 mAh","10W Wired","None",4,"64GB/128GB",False,False,False,"Unisoc",6.6,"Ultra-budget smartphone."),

    # ===== LAVA =====
    P("Lava","Agni 2",21999,2,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 7050","50MP+8MP+2MP","5000 mAh","66W Wired","None",8,"128GB/256GB",True,True,False,"MediaTek",6.78,"Premium Indian brand flagship."),
    P("Lava","Blaze Curve",12999,1,"6.67-inch AMOLED 120Hz","MediaTek Dimensity 6020","50MP+2MP","5000 mAh","33W Wired","None",8,"128GB",True,False,False,"MediaTek",6.67,"Curved AMOLED budget phone."),
    P("Lava","O2",8999,1,"6.5-inch IPS LCD 90Hz","Unisoc T606","50MP+2MP","5000 mAh","18W Wired","None",4,"64GB/128GB",False,False,False,"Unisoc",6.5,"Budget Indian-brand phone."),

    # ===== NOKIA =====
    P("Nokia","G310",14999,1,"6.56-inch IPS LCD 90Hz","Snapdragon 4 Gen 2","50MP+2MP","5000 mAh","20W Wired","IP52",4,"128GB",True,False,False,"Snapdragon",6.56,"Repairable 5G Nokia."),
    P("Nokia","C210",7999,1,"6.3-inch IPS LCD","Unisoc T606","8MP+2MP","4000 mAh","10W Wired","None",3,"64GB",False,False,False,"Unisoc",6.3,"Entry-level Nokia."),
    P("Nokia","XR21",44999,3,"6.49-inch IPS LCD 120Hz","Snapdragon 695","64MP+8MP","4800 mAh","33W Wired","IP68 MIL-STD-810H",6,"128GB",True,True,False,"Snapdragon",6.49,"Military-grade rugged phone."),

    # ===== GOOGLE =====
    P("Google","Pixel 7a",39999,3,"6.1-inch OLED 90Hz","Google Tensor G2","64MP+13MP","4385 mAh","20W Wired + 7.5W Wireless","IP67",8,"128GB",True,True,True,"Tensor",6.1,"Best camera under 40K."),
    P("Google","Pixel 7",49999,4,"6.3-inch OLED 90Hz","Google Tensor G2","50MP+12MP","4355 mAh","30W Wired + 21W Wireless","IP68",8,"128GB/256GB",True,True,True,"Tensor",6.3,"Pure Google with Tensor G2."),
    P("Google","Pixel 7 Pro",74999,5,"6.7-inch OLED 120Hz","Google Tensor G2","50MP+12MP+48MP","5000 mAh","30W Wired + 23W Wireless","IP68",12,"128GB/256GB",True,True,True,"Tensor",6.7,"30x zoom with Tensor G2."),
    P("Google","Pixel 8",59999,4,"6.2-inch OLED 120Hz","Google Tensor G3","50MP+12MP","4575 mAh","27W Wired + 18W Wireless","IP68",8,"128GB/256GB",True,True,True,"Tensor",6.2,"7 years of OS updates guaranteed."),
    P("Google","Pixel 8 Pro",89999,5,"6.7-inch OLED 120Hz","Google Tensor G3","50MP+48MP+48MP","5050 mAh","30W Wired + 23W Wireless","IP68",12,"128GB/256GB/512GB/1TB",True,True,True,"Tensor",6.7,"Temperature sensor + Pro cameras."),
    P("Google","Pixel 8a",44999,3,"6.1-inch OLED 120Hz","Google Tensor G3","64MP+13MP","4492 mAh","18W Wired + 7.5W Wireless","IP67",8,"128GB/256GB",True,True,True,"Tensor",6.1,"Flagship cameras at mid-range price."),

    # ===== SONY =====
    P("Sony","Xperia 1 VI",99999,5,"6.5-inch OLED 120Hz","Snapdragon 8 Gen 3","52MP+12MP+12MP","5000 mAh","30W Wired","IP68",12,"256GB/512GB",True,True,True,"Snapdragon",6.5,"Cinema-grade camera with Creator mode."),
    P("Sony","Xperia 5 VI",79999,5,"6.1-inch OLED 120Hz","Snapdragon 8 Gen 3","52MP+12MP","5000 mAh","30W Wired","IP68",8,"128GB/256GB",True,True,False,"Snapdragon",6.1,"Compact S8 Gen 3 flagship."),
    P("Sony","Xperia 10 VI",39999,3,"6.1-inch OLED 60Hz","Snapdragon 6 Gen 1","48MP+8MP","5000 mAh","30W Wired","IP68",6,"128GB",True,True,False,"Snapdragon",6.1,"Ultra-slim IP68 with 3.5mm jack."),

    # ===== HUAWEI =====
    P("Huawei","Mate 50 Pro",89999,5,"6.74-inch OLED 120Hz","Snapdragon 8+ Gen 1","50MP+13MP+64MP","4700 mAh","66W Wired + 50W Wireless","IP68",8,"256GB/512GB",False,True,True,"Snapdragon",6.74,"Ultra aperture XMAGE camera."),
    P("Huawei","Nova 12 Ultra",49999,4,"6.78-inch OLED 120Hz","Kirin 9000S","50MP+8MP","4600 mAh","100W Wired","None",12,"256GB/512GB",True,True,False,"Kirin",6.78,"100W HuaweiCharge with Kirin."),
    P("Huawei","Nova 12 SE",29999,3,"6.67-inch OLED 120Hz","Snapdragon 680","108MP+8MP+2MP","4500 mAh","66W Wired","None",8,"256GB",False,True,False,"Snapdragon",6.67,"Mid-range Huawei with fast charging."),

    # ===== ASUS =====
    P("Asus","ROG Phone 8",79999,5,"6.78-inch AMOLED 165Hz","Snapdragon 8 Gen 3","50MP+13MP+32MP","5500 mAh","65W Wired","IP54",16,"256GB/512GB",True,True,False,"Snapdragon",6.78,"Gaming powerhouse with 165Hz."),
    P("Asus","Zenfone 11 Ultra",69999,4,"6.78-inch AMOLED 120Hz","Snapdragon 8 Gen 3","50MP+13MP+32MP","5500 mAh","65W Wired","IP68",16,"256GB/512GB",True,True,False,"Snapdragon",6.78,"Zenfone goes big with 8 Gen 3."),

    # ===== LENOVO =====
    P("Lenovo","Legion Y70",44999,3,"6.67-inch AMOLED 144Hz","Snapdragon 8+ Gen 1","50MP+13MP+2MP","5100 mAh","68W Wired","None",12,"256GB",True,True,False,"Snapdragon",6.67,"Gaming phone that looks normal."),
]

# Load existing and merge
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r"(?:var|const) PHONES = (\[.*?\]);", content, re.DOTALL)
if not match:
    print("Cannot find PHONES array"); exit(1)

phones = json.loads(match.group(1))
existing_ids = {p["id"] for p in phones}

added = 0
for p in phones_batch:
    if p["id"] not in existing_ids:
        phones.append(p)
        existing_ids.add(p["id"])
        added += 1

new_json = json.dumps(phones, indent=2)
new_content = content.replace(match.group(0), f"var PHONES = {new_json};")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Added {added} new phones. Total DB: {len(phones)}")

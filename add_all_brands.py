import json
import re

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
}

def logo(brand):
    return brand_logos.get(brand, "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg")

def make_id(brand, name):
    return (brand.lower() + "-" + name.lower()
            .replace(" ", "-").replace("(", "").replace(")", "")
            .replace("+", "plus").replace(",", "").replace("/", "-"))[:80]

def ph(brand, name, price, cat, display, cpu, cam, battery, charging, ip,
       ram, storage, has5g, hasnfc, haswc, proc_brand, screen_sz,
       pros, cons, unique):
    decay = [1, 0.98, 0.95, 0.92, 0.88, 0.85] if cat >= 4 else (
            [1, 0.97, 0.93, 0.88, 0.82, 0.78] if cat >= 2 else
            [1, 0.95, 0.90, 0.85, 0.80, 0.75])
    base = min(9.5, 4.5 + cat * 0.85)
    def sc(delta=0): return round(min(10, max(3, base + delta)), 1)
    return {
        "id": make_id(brand, name),
        "brand": brand, "name": name,
        "price": f"\u20b9{price:,}", "priceCategory": cat, "emoji": "\U0001f4f1",
        "uniqueFeature": unique,
        "specs": {
            "display": display, "processor": cpu, "camera": cam,
            "battery": battery, "charging": charging, "ipRating": ip
        },
        "scores": {
            "durability": sc(0.5 if ip != "None" else -0.5),
            "camera": sc(0.8 if "200MP" in cam or "108MP" in cam else 0),
            "battery": sc(0.5 if "5000" in battery else 0),
            "charging": sc(1.0 if any(x in charging for x in ["100W","120W","150W","240W"]) else 0),
            "display": sc(0.5 if "AMOLED" in display or "OLED" in display else -0.3),
            "sound": sc(0), "ip": 10 if ip == "IP68" else (5 if "IP53" in ip else 0)
        },
        "ram_gb": ram, "storage_options": storage,
        "has_5g": has5g, "has_nfc": hasnfc, "has_wireless_charging": haswc,
        "processor_brand": proc_brand, "screen_size": screen_sz,
        "price_numeric": price,
        "price_history": [int(price * d) for d in decay],
        "pros": pros, "cons": cons,
        "images": [logo(brand)]
    }

# ======================== ALL NEW PHONES ========================
new_phones = [

    # ===== VIVO =====
    ph("Vivo","X100 Pro",89999,5,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 9300","50MP+50MP+64MP ZEISS","5400 mAh","100W Wired + 50W Wireless","IP68",16,"256GB / 512GB",True,True,True,"MediaTek",6.78,["ZEISS optics","Massive 5400mAh battery","Premium AMOLED display"],["Very expensive","Heavy build"],"ZEISS-certified periscope cameras with 100x zoom."),
    ph("Vivo","X100",69999,4,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 9300","50MP+50MP+50MP ZEISS","5000 mAh","120W Wired","IP54",12,"256GB",True,True,False,"MediaTek",6.78,["Excellent cameras","120W charging","Dimensity 9300 powerhouse"],["No wireless charging","Average ultrawide"],"Dimensity 9300 flagship with ZEISS triple camera."),
    ph("Vivo","X90 Pro",84999,5,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 9200 Plus","50MP+50MP+12MP ZEISS","4870 mAh","80W Wired + 50W Wireless","IP68",12,"256GB",True,True,True,"MediaTek",6.78,["ZEISS flagship camera","IP68 rated","Wireless charging"],["Older chipset now","Price is high"],"Professional ZEISS photography system with IP68."),
    ph("Vivo","V29 Pro",35999,3,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 8200","50MP+8MP+2MP","4600 mAh","80W Wired","IP54",12,"256GB",True,True,False,"MediaTek",6.78,["Aura light portrait","Slim design","120Hz AMOLED"],["No wireless charging","Average battery life"],"Aura light system for perfect portrait selfies."),
    ph("Vivo","V29",30999,3,"6.78-inch AMOLED 120Hz","Snapdragon 778G","50MP+8MP+2MP","4600 mAh","44W Wired","IP54",8,"128GB / 256GB",True,False,False,"Snapdragon",6.78,["Slim build","Good display","5G ready"],["Slow charging for price","Average cameras"],"Ultra-slim flagship-style mid-ranger."),
    ph("Vivo","V27 Pro",37999,3,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 8200","50MP+8MP+2MP","4600 mAh","80W Wired","IP54",12,"256GB",True,True,False,"MediaTek",6.78,["Aura light for selfies","Premium design","Fast charging"],["No wireless charging","Average main camera"],"Designed for portrait photography with Aura light."),
    ph("Vivo","T2 Pro",21999,2,"6.67-inch AMOLED 120Hz","MediaTek Dimensity 7200","64MP+8MP+2MP","4600 mAh","80W Wired","None",8,"128GB",True,False,False,"MediaTek",6.67,["Fast 80W charging","Bright AMOLED","Good performance"],["No IP rating","Plastic build"],"80W charging speed in mid-range segment."),
    ph("Vivo","Y100A",20999,2,"6.67-inch AMOLED 120Hz","Snapdragon 695","64MP+2MP+2MP","4500 mAh","44W Wired","None",8,"128GB",True,False,False,"Snapdragon",6.67,["AMOLED display","Good cameras","Reliable chipset"],["No IP rating","Basic design"],"Beautiful AMOLED mid-ranger with Snapdragon."),
    ph("Vivo","Y200e",15999,1,"6.67-inch AMOLED 120Hz","Snapdragon 4 Gen 1","50MP+2MP","5000 mAh","44W Wired","None",6,"128GB",True,False,False,"Snapdragon",6.67,["AMOLED at budget price","5000mAh battery","5G ready"],["Weak chipset","Basic cameras"],"Budget 5G with AMOLED display."),
    ph("Vivo","Y78 5G",19999,2,"6.64-inch IPS LCD 120Hz","Snapdragon 695","64MP+2MP+2MP","5000 mAh","44W Wired","None",8,"128GB",True,False,False,"Snapdragon",6.64,["Large battery","5G connectivity","Decent camera"],["LCD display","Average performance"],"Reliable 5G mid-ranger with solid battery."),

    # ===== iQOO =====
    ph("iQOO","12 5G",52999,4,"6.78-inch AMOLED 144Hz","Snapdragon 8 Gen 3","50MP+64MP+50MP","5000 mAh","120W Wired","None",12,"256GB / 512GB",True,True,False,"Snapdragon",6.78,["Snapdragon 8 Gen 3","144Hz AMOLED","Fastest charging flagship"],["No wireless charging","No IP rating","Gaming focused design"],"Snapdragon 8 Gen 3 gaming flagship at mid-range price."),
    ph("iQOO","11 5G",59999,4,"6.78-inch AMOLED 144Hz","Snapdragon 8 Gen 2","50MP+13MP+8MP","5000 mAh","120W Wired","None",16,"256GB",True,True,False,"Snapdragon",6.78,["Snapdragon 8 Gen 2","Great performance","144Hz display"],["No wireless charging","Average cameras"],"Performance beast with 120W charging."),
    ph("iQOO","Neo 9 Pro",35999,3,"6.78-inch AMOLED 144Hz","Snapdragon 8 Gen 2","50MP+8MP+2MP","5160 mAh","120W Wired","None",12,"256GB",True,True,False,"Snapdragon",6.78,["Flagship chipset","Huge battery","144Hz display"],["No wireless charging","Camera could be better"],"Snapdragon 8 Gen 2 in a budget-friendly package."),
    ph("iQOO","Neo 9",29999,2,"6.67-inch AMOLED 120Hz","MediaTek Dimensity 9300","50MP+2MP+2MP","5000 mAh","80W Wired","None",8,"128GB / 256GB",True,False,False,"MediaTek",6.67,["Dimensity 9300 value pick","5000mAh battery","80W charging"],["No ultrawide","No wireless charging"],"Dimensity 9300 at an unbeatable price."),
    ph("iQOO","Z9 Turbo",24999,2,"6.67-inch AMOLED 144Hz","Snapdragon 7 Gen 3","50MP+2MP","5000 mAh","80W Wired","None",8,"256GB",True,True,False,"Snapdragon",6.67,["Snapdragon 7 Gen 3","Fast 80W charging","Value pick"],["No ultra-wide camera","Plastic design"],"Best performance under 25K with Snapdragon 7 Gen 3."),
    ph("iQOO","Z9s",20999,2,"6.77-inch AMOLED 120Hz","MediaTek Dimensity 7300","50MP+2MP","5000 mAh","44W Wired","None",8,"128GB",True,False,False,"MediaTek",6.77,["AMOLED display","5000mAh battery","Good value"],["No fast charging","Average performance"],"Affordable AMOLED phone with large battery."),
    ph("iQOO","Z7 Pro",24999,2,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 7200","64MP+2MP+2MP","4500 mAh","67W Wired","None",8,"256GB",True,False,False,"MediaTek",6.78,["Premium AMOLED","Fast 67W charging","Slim design"],["Small battery","Average processor"],"Slim premium mid-ranger with bright AMOLED."),
    ph("iQOO","Z6 Lite",13999,1,"6.56-inch IPS LCD 90Hz","Snapdragon 4 Gen 1","50MP+2MP","5000 mAh","18W Wired","None",4,"64GB / 128GB",True,False,False,"Snapdragon",6.56,["5G connectivity","Large battery","Budget friendly"],["LCD display","Slow charging","Low RAM"],"Budget 5G with great battery life."),

    # ===== OPPO =====
    ph("Oppo","Find X6 Pro",89999,5,"6.82-inch AMOLED 120Hz","Snapdragon 8 Gen 2","50MP+50MP+6x Periscope Hasselblad","5000 mAh","100W Wired + 50W Wireless","IP68",12,"256GB",True,True,True,"Snapdragon",6.82,["Hasselblad cameras","IP68","100W charging"],["Very expensive","Heavy"],"Hasselblad-certified photography with 6x periscope zoom."),
    ph("Oppo","Find X5 Pro",84999,5,"6.7-inch AMOLED 120Hz","Snapdragon 8 Gen 1","50MP+50MP+13MP Hasselblad","5000 mAh","80W Wired + 50W Wireless","IP68",12,"256GB",True,True,True,"Snapdragon",6.7,["Hasselblad cameras","IP68","Wireless charging"],["Older chipset","Slightly bulky"],"Flagship photography with Hasselblad coloration."),
    ph("Oppo","Reno 11 Pro",39999,3,"6.7-inch AMOLED 120Hz","MediaTek Dimensity 8200","50MP+32MP+12MP","4600 mAh","80W Wired","None",12,"256GB",True,True,False,"MediaTek",6.7,["64MP portrait camera","Premium build","80W fast charging"],["No wireless charging","No IP rating"],"Portrait specialist with periscope-style zoom."),
    ph("Oppo","Reno 11",31999,3,"6.7-inch AMOLED 120Hz","MediaTek Dimensity 7050","50MP+8MP+2MP","5000 mAh","67W Wired","None",8,"128GB / 256GB",True,False,False,"MediaTek",6.7,["Beautiful design","67W charging","Good cameras"],["Average chipset","No wireless charging"],"Stylish mid-ranger with capable cameras."),
    ph("Oppo","Reno 10 Pro Plus",54999,4,"6.74-inch AMOLED 120Hz","Snapdragon 8 Plus Gen 1","50MP+32MP+5x Periscope","4700 mAh","100W Wired","None",12,"256GB",True,True,False,"Snapdragon",6.74,["5x periscope zoom","100W charging","Flagship chipset"],["No wireless charging","No IP rating"],"5x periscope zoom at a competitive price."),
    ph("Oppo","F25 Pro",24999,2,"6.7-inch AMOLED 120Hz","MediaTek Dimensity 7050","64MP+8MP+2MP","5000 mAh","67W Wired","IP65",8,"128GB",True,False,False,"MediaTek",6.7,["IP65 rating","64MP camera","5000mAh battery"],["Average chipset","No NFC"],"Water-resistant mid-ranger with 64MP camera."),
    ph("Oppo","F23",22999,2,"6.72-inch IPS LCD 90Hz","Snapdragon 695","64MP+2MP+2MP","5000 mAh","67W Wired","None",8,"128GB",True,False,False,"Snapdragon",6.72,["Fast 67W charging","Big battery","Good cameras"],["LCD display","No IP rating"],"Fast-charging budget phone with 64MP camera."),
    ph("Oppo","A79",17999,1,"6.72-inch IPS LCD 90Hz","MediaTek Helio G96","50MP+2MP","5000 mAh","33W Wired","None",4,"128GB",True,False,False,"MediaTek",6.72,["5G connectivity","5000mAh battery","Affordable"],["LCD display","Weak processor","Slow charging"],"Budget 5G with excellent battery backup."),
    ph("Oppo","A58",16999,1,"6.72-inch IPS LCD 90Hz","MediaTek Helio G85","50MP+2MP","5000 mAh","33W Wired","None",6,"128GB",False,False,False,"MediaTek",6.72,["Big screen","Large battery","Affordable"],["No 5G","Weak processor","Slow charging"],"Reliable budget phone for everyday tasks."),

    # ===== MOTOROLA =====
    ph("Motorola","Edge 50 Pro",31999,3,"6.7-inch pOLED 144Hz","Snapdragon 7s Gen 2","50MP+13MP+10MP","4500 mAh","125W Wired + 50W Wireless","IP68",12,"256GB",True,True,True,"Snapdragon",6.7,["125W charging","IP68","Wireless charging"],["Average cameras","Battery life suffers with 125W"],"125W TurboPower charging — 0 to 100% in 32 minutes."),
    ph("Motorola","Edge 50 Ultra",59999,4,"6.67-inch pOLED 144Hz","Snapdragon 8s Gen 3","50MP+50MP+10MP","4500 mAh","125W Wired + 50W Wireless","IP68",12,"512GB",True,True,True,"Snapdragon",6.67,["8s Gen 3 performance","125W charging","IP68"],["Average camera system","Smaller battery"],"Ultra-slim flagship with curved pOLED and IP68."),
    ph("Motorola","Edge 50 Fusion",21999,2,"6.67-inch pOLED 144Hz","Snapdragon 7s Gen 2","50MP+13MP","5000 mAh","68W Wired","IP68",8,"128GB / 256GB",True,True,False,"Snapdragon",6.67,["IP68 mid-ranger","Great display","Large battery"],["No wireless charging","Average processor speed"],"IP68-rated pOLED phone under 25K."),
    ph("Motorola","G84",18999,2,"6.55-inch pOLED 120Hz","Snapdragon 695","50MP+8MP","5000 mAh","33W Wired","IP52",12,"256GB",True,False,False,"Snapdragon",6.55,["pOLED display","Large RAM","Good battery"],["Average performance","Slow charging"],"pOLED display with 12GB RAM in budget segment."),
    ph("Motorola","G54",13999,1,"6.5-inch IPS LCD 120Hz","MediaTek Dimensity 7020","50MP+2MP","6000 mAh","20W Wired","None",8,"128GB / 256GB",True,False,False,"MediaTek",6.5,["6000mAh battery","5G connectivity","Affordable"],["LCD display","Slow charging","Average cameras"],"Massive 6000mAh battery for 2-day life."),
    ph("Motorola","G34",9999,1,"6.5-inch IPS LCD 120Hz","Snapdragon 695","50MP+2MP","5000 mAh","18W Wired","None",4,"128GB",True,False,False,"Snapdragon",6.5,["5G on budget","Decent performance","Snapdragon chipset"],["Low RAM","LCD display","Slow charging"],"Most affordable 5G phone in India."),
    ph("Motorola","G64",17999,1,"6.5-inch IPS LCD 120Hz","MediaTek Dimensity 7025","50MP+2MP","6000 mAh","33W Wired","None",8,"128GB / 256GB",True,False,False,"MediaTek",6.5,["6000mAh massive battery","5G","Affordable"],["LCD only","Average cameras"],"Budget 5G with industry-best battery life."),
    ph("Motorola","Razr 50 Ultra",89999,5,"6.9-inch pOLED 165Hz Foldable","Snapdragon 8s Gen 3","50MP+50MP","3800 mAh","45W Wired + 15W Wireless","IP48",12,"512GB",True,True,True,"Snapdragon",6.9,["Flip foldable","Huge cover screen","Premium design"],["Small battery for price","Expensive"],"Motorola's most premium flip phone with 3.6-inch cover screen."),

    # ===== REALME =====
    ph("Realme","GT 5 Pro",49999,4,"6.78-inch AMOLED 144Hz","Snapdragon 8 Gen 3","50MP+50MP+36MP","5400 mAh","100W Wired + 50W Wireless","None",16,"256GB / 512GB / 1TB",True,True,True,"Snapdragon",6.78,["Snapdragon 8 Gen 3","Massive storage options","Periscope zoom"],["No IP rating","No MicroSD"],"Snapdragon 8 Gen 3 with 1TB storage at mid-range price."),
    ph("Realme","GT Neo 5 SE",29999,3,"6.74-inch AMOLED 144Hz","Snapdragon 7+ Gen 2","50MP+8MP+2MP","5000 mAh","100W Wired","None",8,"256GB",True,False,False,"Snapdragon",6.74,["100W super charging","Snapdragon 7+ Gen 2","144Hz display"],["No wireless charging","No IP rating"],"100W charging fills up in just 29 minutes."),
    ph("Realme","GT Neo 5",36999,3,"6.74-inch AMOLED 144Hz","Snapdragon 8+ Gen 1","50MP+8MP+2MP","5000 mAh","150W Wired","None",16,"256GB",True,True,False,"Snapdragon",6.74,["150W fastest charging","Great performance","144Hz AMOLED"],["No IP rating","No wireless charging"],"150W charging — fully charged in 15 minutes!"),
    ph("Realme","GT Neo 3T",29999,3,"6.62-inch AMOLED 120Hz","Snapdragon 870","64MP+8MP+2MP","5000 mAh","80W Wired","None",8,"128GB / 256GB",True,True,False,"Snapdragon",6.62,["Snapdragon 870 power","80W charging","Good cameras"],["Older chipset","No IP"],"Flagship-grade Snapdragon 870 with 80W charging."),
    ph("Realme","C67",14999,1,"6.72-inch IPS LCD 120Hz","Snapdragon 685","108MP+2MP","5000 mAh","33W Wired","None",8,"128GB",False,False,False,"Snapdragon",6.72,["108MP camera","Large battery","Affordable"],["No 5G","LCD display","Slow charging"],"108MP camera for sharp photos on a budget."),
    ph("Realme","C65",10999,1,"6.67-inch IPS LCD 90Hz","MediaTek Helio G85","50MP+2MP","5000 mAh","45W Wired","None",4,"128GB",False,False,False,"MediaTek",6.67,["45W fast charging","5000mAh battery","Budget-friendly"],["No 5G","Very low RAM","Average camera"],"Fastest charging in budget segment at 45W."),
    ph("Realme","Narzo 70 Pro",19999,2,"6.67-inch AMOLED 120Hz","MediaTek Dimensity 7050","50MP+8MP+2MP","5000 mAh","45W Wired","None",8,"128GB",True,False,False,"MediaTek",6.67,["AMOLED display","5G connectivity","Large battery"],["No IP rating","Average cameras"],"AMOLED display with 5G at an affordable price."),
    ph("Realme","P2 Pro",22999,2,"6.7-inch AMOLED 120Hz","Snapdragon 7s Gen 2","50MP+8MP+2MP","5000 mAh","80W Wired","None",8,"128GB / 256GB",True,False,False,"Snapdragon",6.7,["Snapdragon 7s Gen 2","80W charging","AMOLED"],["No IP rating","Average design"],"Snapdragon 7s Gen 2 mid-ranger with fast charging."),

    # ===== NOKIA =====
    ph("Nokia","G42",14999,1,"6.56-inch IPS LCD 90Hz","Snapdragon 480+","50MP+2MP+2MP","4500 mAh","18W Wired","IP52",4,"128GB",True,False,False,"Snapdragon",6.56,["Repairable design","5G connectivity","IP52 dust resistant"],["Slow charging","Basic cameras","Low RAM"],"Sustainable phone with user-repairable design."),
    ph("Nokia","G60",22999,2,"6.58-inch IPS LCD 120Hz","Snapdragon 695","50MP+5MP+2MP","4500 mAh","20W Wired","IP52",6,"128GB",True,False,False,"Snapdragon",6.58,["3-year OS updates","IP52","5G connectivity"],["Slow charging","Average cameras","LCD"],"3 years of Android OS updates guaranteed."),
    ph("Nokia","X30",33999,3,"6.43-inch AMOLED 90Hz","Snapdragon 695","50MP+13MP","4200 mAh","33W Wired","IP67",6,"256GB",True,True,False,"Snapdragon",6.43,["IP67 water resistant","AMOLED","50MP camera"],["Small battery","Weaker processor"],"Eco-certified premium mid-ranger with IP67."),
    ph("Nokia","C32",8999,1,"6.52-inch IPS LCD","MediaTek Helio G37","50MP+2MP+2MP","5000 mAh","10W Wired","None",3,"64GB / 128GB",False,False,False,"MediaTek",6.52,["Huge battery","Affordable price","Large screen"],["Very slow charging","Very low RAM","No 5G"],"Ultra-affordable phone with 2-day battery life."),

    # ===== SONY =====
    ph("Sony","Xperia 1 V",109999,5,"6.5-inch 4K OLED 120Hz","Snapdragon 8 Gen 2","52MP+12MP+12MP","5000 mAh","30W Wired","IP68",12,"256GB",True,True,False,"Snapdragon",6.5,["4K OLED display","IP68","Pro cinema cameras"],["No wireless charging","Very expensive","Heavy"],"The world's first 4K OLED smartphone display."),
    ph("Sony","Xperia 5 V",84999,5,"6.1-inch AMOLED 120Hz","Snapdragon 8 Gen 2","52MP+12MP","5000 mAh","30W Wired","IP68",8,"256GB",True,True,False,"Snapdragon",6.1,["Compact flagship","IP68","Pro cameras"],["No wireless charging","Expensive","No ultrawide zoom"],"Compact flagship with cinema-grade cameras."),
    ph("Sony","Xperia 10 V",44999,3,"6.1-inch OLED 60Hz","Snapdragon 695","48MP+8MP+12MP","5000 mAh","30W Wired","IP68",6,"128GB",True,True,False,"Snapdragon",6.1,["IP68 rated","Compact size","3.5mm headphone jack"],["60Hz display","Slow charging","Expensive for specs"],"Slim compact phone with IP68 and headphone jack."),

    # ===== ASUS =====
    ph("Asus","ROG Phone 8 Pro",99999,5,"6.78-inch AMOLED 165Hz","Snapdragon 8 Gen 3","50MP+13MP+32MP","5500 mAh","65W Wired + 15W Wireless","IP54",24,"1TB",True,True,True,"Snapdragon",6.78,["Snapdragon 8 Gen 3","24GB RAM","Massive battery"],["Gaming aesthetic not for everyone","Expensive"],"Ultimate gaming smartphone with 24GB RAM."),
    ph("Asus","ROG Phone 7",69999,5,"6.78-inch AMOLED 165Hz","Snapdragon 8 Gen 2","50MP+13MP+5MP","6000 mAh","65W Wired","None",16,"512GB",True,True,False,"Snapdragon",6.78,["6000mAh battery","Snapdragon 8 Gen 2","165Hz display"],["Huge and heavy","Gaming looks"],"6000mAh gaming powerhouse with 165Hz display."),
    ph("Asus","Zenfone 10",59999,4,"5.92-inch AMOLED 144Hz","Snapdragon 8 Gen 2","50MP+13MP","4300 mAh","30W Wired","IP68",16,"512GB",True,True,False,"Snapdragon",5.92,["Ultra-compact flagship","IP68","Snapdragon 8 Gen 2"],["Small battery","Pricey"],"Smallest flagship Android phone in 2023."),
    ph("Asus","Zenfone 9",49999,4,"5.9-inch AMOLED 120Hz","Snapdragon 8+ Gen 1","50MP+12MP","4300 mAh","30W Wired","IP68",8,"256GB",True,True,False,"Snapdragon",5.9,["Compact design","IP68","Flagship chipset"],["Small battery","No wireless charging"],"Compact powerhouse with gimbal-style OIS camera."),

    # ===== HONOR =====
    ph("Honor","Magic 5 Pro",74999,5,"6.81-inch AMOLED 120Hz","Snapdragon 8 Gen 2","54MP+50MP+50MP","5100 mAh","66W Wired + 50W Wireless","IP68",12,"512GB",True,True,True,"Snapdragon",6.81,["IP68","50W wireless charging","Triple flagship cameras"],["Expensive","Limited availability"],"Flagship triple 50MP cameras with IP68 protection."),
    ph("Honor","Magic V2",99999,5,"7.92-inch inner OLED 120Hz","Snapdragon 8 Gen 2","50MP+50MP+20MP","5000 mAh","66W Wired","None",16,"512GB",True,True,False,"Snapdragon",7.92,["Thinnest foldable","Powerful chipset","Large inner screen"],["Very expensive","No IP rating"],"World's thinnest foldable phone at 9.9mm folded."),
    ph("Honor","90",32999,3,"6.7-inch AMOLED 120Hz","Snapdragon 7s Gen 2","200MP+12MP+2MP","5000 mAh","66W Wired","None",12,"512GB",True,True,False,"Snapdragon",6.7,["200MP main camera","5000mAh battery","66W fast charging"],["No IP rating","No wireless charging"],"200MP camera smartphone at mid-range pricing."),
    ph("Honor","X9b",24999,2,"6.78-inch AMOLED 120Hz","Snapdragon 6 Gen 1","108MP+5MP+2MP","5800 mAh","35W Wired","IP53",8,"256GB",True,False,False,"Snapdragon",6.78,["5800mAh massive battery","108MP camera","IP53"],["No fast wireless charging","Average main camera color"],"Massive 5800mAh battery with IP53 protection."),
    ph("Honor","X8b",18999,1,"6.7-inch AMOLED 90Hz","Snapdragon 685","108MP+5MP+2MP","4500 mAh","35W Wired","None",8,"256GB",False,False,False,"Snapdragon",6.7,["108MP camera","Slim design","AMOLED display"],["No 5G","Average battery"],"Slim and premium design with 108MP camera."),

    # ===== POCO =====
    ph("Poco","F6 Pro",49999,4,"6.67-inch AMOLED 144Hz","Snapdragon 8 Gen 2","50MP+8MP+2MP","5000 mAh","120W Wired","None",12,"256GB / 512GB",True,True,False,"Snapdragon",6.67,["Snapdragon 8 Gen 2","120W fast charging","144Hz AMOLED"],["No wireless charging","No IP rating"],"Flagship Snapdragon 8 Gen 2 at a mid-range price."),
    ph("Poco","F6",29999,3,"6.67-inch AMOLED 120Hz","Snapdragon 7s Gen 3","50MP+8MP+2MP","5000 mAh","90W Wired","None",12,"256GB",True,True,False,"Snapdragon",6.67,["Value flagship","90W charging","Snapdragon 7s Gen 3"],["No wireless charging","Camera could be better"],"Best performance per rupee in its segment."),
    ph("Poco","M6 Pro",18999,2,"6.67-inch AMOLED 120Hz","MediaTek Helio G99 Ultra","64MP+8MP+2MP","5000 mAh","67W Wired","None",8,"256GB",False,False,False,"MediaTek",6.67,["AMOLED display","67W fast charging","Large storage"],["No 5G","Average processor"],"Premium AMOLED with fast charging under 20K."),
    ph("Poco","X6 Pro",28999,3,"6.67-inch AMOLED 144Hz","MediaTek Dimensity 8300 Ultra","64MP+8MP+2MP","5000 mAh","67W Wired","None",12,"512GB",True,True,False,"MediaTek",6.67,["Dimensity 8300 Ultra","Fast 67W charging","144Hz AMOLED"],["No wireless charging","Camera disappoints"],"Dimensity 8300 Ultra flagship killer."),
    ph("Poco","X6",22999,2,"6.67-inch AMOLED 120Hz","Snapdragon 7s Gen 2","64MP+8MP+2MP","5000 mAh","67W Wired","None",8,"256GB",True,True,False,"Snapdragon",6.67,["Snapdragon 7s Gen 2","67W charging","Premium display"],["Camera mediocre","No wireless charging"],"Snapdragon mid-ranger with great display."),
    ph("Poco","C75",9999,1,"6.88-inch IPS LCD 120Hz","MediaTek Helio G91","50MP+2MP","5160 mAh","18W Wired","None",6,"128GB",False,False,False,"MediaTek",6.88,["Large 6.88-inch screen","5160mAh battery","Budget-friendly"],["Slow charging","No 5G","Basic camera"],"Largest screen in ultra-budget segment."),

    # ===== NOTHING =====
    ph("Nothing","Phone (2)",44999,4,"6.7-inch AMOLED 120Hz","Snapdragon 8+ Gen 1","50MP+50MP","4700 mAh","45W Wired + 15W Wireless","IP54",12,"256GB",True,True,True,"Snapdragon",6.7,["Unique Glyph interface","Wireless charging","Clean NothingOS"],["Glyph is a gimmick to some","Average cameras"],"Transparent design with advanced Glyph notification system."),
    ph("Nothing","Phone (2a)",23999,2,"6.7-inch AMOLED 120Hz","MediaTek Dimensity 7200 Pro","50MP+50MP","5000 mAh","45W Wired","IP54",12,"256GB",True,True,False,"MediaTek",6.7,["Large 5000mAh battery","Clean software","Glyph interface"],["No wireless charging","Average chipset"],"Iconic transparent design with 5000mAh battery."),
    ph("Nothing","Phone (2a) Plus",25999,2,"6.7-inch AMOLED 120Hz","MediaTek Dimensity 7350 Pro","50MP+50MP","5000 mAh","50W Wired","IP54",12,"256GB",True,True,False,"MediaTek",6.7,["Upgraded chipset","Clean NothingOS","Glyph"],["No wireless charging","Incremental upgrade"],"Slightly more powerful variant of Phone 2a."),
    ph("Nothing","CMF Phone 1",15999,1,"6.67-inch AMOLED 120Hz","MediaTek Dimensity 7300","50MP+2MP","5000 mAh","33W Wired","IP52",8,"128GB / 256GB",True,False,False,"MediaTek",6.67,["AMOLED at budget price","Unique case design","5G"],["No NFC","Average cameras","Basic design"],"Affordable AMOLED with swappable back covers."),

    # ===== REDMI =====
    ph("Redmi","Note 13 Pro Plus",30999,3,"6.67-inch AMOLED 120Hz","MediaTek Dimensity 7200 Ultra","200MP+8MP+2MP","5000 mAh","120W Wired","IP68",12,"256GB / 512GB",True,True,False,"MediaTek",6.67,["IP68 water resistance","200MP camera","120W charging"],["No wireless charging","Curved glass can crack"],"IP68 + 200MP camera + 120W charging in one phone."),
    ph("Redmi","Note 13 Pro",24999,2,"6.67-inch AMOLED 120Hz","Snapdragon 7s Gen 2","200MP+8MP+2MP","5100 mAh","67W Wired","IP54",8,"256GB",True,True,False,"Snapdragon",6.67,["200MP main camera","5100mAh battery","IP54"],["No wireless charging","Average zoom camera"],"Snapdragon with 200MP flagship-grade camera."),
    ph("Redmi","Note 13",15999,1,"6.67-inch AMOLED 120Hz","Snapdragon 685","108MP+8MP+2MP","5000 mAh","33W Wired","IP54",6,"128GB / 256GB",False,True,False,"Snapdragon",6.67,["108MP camera","AMOLED display","IP54 rating"],["No 5G","Slow charging"],"108MP AMOLED with IP54 at budget pricing."),
    ph("Redmi","K70 Pro",44999,4,"6.67-inch AMOLED 144Hz","Snapdragon 8 Gen 3","50MP+50MP+12MP","5000 mAh","120W Wired + 50W Wireless","IP64",16,"512GB",True,True,True,"Snapdragon",6.67,["Snapdragon 8 Gen 3","144Hz AMOLED","120W charging"],["No IP68 (only IP64)","Gaming-focused design"],"Snapdragon 8 Gen 3 flagship killer."),
    ph("Redmi","K60 Pro",39999,3,"6.67-inch AMOLED 144Hz","Snapdragon 8 Gen 2","50MP+8MP+2MP","5000 mAh","120W Wired","IP68",12,"256GB",True,True,False,"Snapdragon",6.67,["IP68","Snapdragon 8 Gen 2","120W fast charging"],["No wireless charging","Camera not best in class"],"Best value flagship with IP68 + Snapdragon 8 Gen 2."),
    ph("Redmi","A3",7999,1,"6.71-inch IPS LCD 90Hz","MediaTek Helio G36","8MP","5000 mAh","10W Wired","None",3,"64GB",False,False,False,"MediaTek",6.71,["Ultra-affordable","Large battery","Basic needs covered"],["Very weak chipset","Weak camera","Slow charging"],"Most affordable smartphone for basic users."),

    # ===== HUAWEI =====
    ph("Huawei","P60 Pro",89999,5,"6.67-inch OLED 120Hz","Kirin 9200+","48MP+13MP+48MP Periscope","4815 mAh","88W Wired + 50W Wireless","IP68",8,"256GB",False,True,True,"Kirin",6.67,["Amazing low-light camera","IP68","Wireless charging"],["No 5G","No Google services","Expensive"],"World-class Leica camera without Google services."),
    ph("Huawei","Mate 60 Pro",99999,5,"6.82-inch LTPO OLED 120Hz","Kirin 9000s","50MP+13MP+12MP","4600 mAh","66W Wired + 50W Wireless","IP68",12,"512GB",True,True,True,"Kirin",6.82,["Satellite communication","IP68","Kirin 9000s"],["No Google services","Limited availability","Expensive"],"Supports satellite calls — unprecedented on a smartphone."),

    # ===== LENOVO =====
    ph("Lenovo","Legion Phone Duel 3",64999,4,"6.67-inch AMOLED 144Hz","Snapdragon 8+ Gen 1","64MP+16MP","5500 mAh","68W Wired x2","None",18,"512GB",True,True,False,"Snapdragon",6.67,["18GB RAM","Dual-port charging","Pop-up camera"],["Gaming design only","Heavy","Unusual pop-up selfie camera"],"Dual charging ports for true gaming battery management."),
    ph("Lenovo","ThinkPhone",49999,4,"6.6-inch pOLED 144Hz","Snapdragon 8+ Gen 1","50MP+13MP+2MP","5000 mAh","68W Wired + 15W Wireless","IP68",12,"256GB",True,True,True,"Snapdragon",6.6,["Business-grade security","IP68","Wireless charging"],["Niche design appeal","Pricey"],"ThinkPad-inspired business phone with Moto connectivity."),

    # ===== TCL =====
    ph("TCL","50 Pro",19999,2,"6.78-inch AMOLED 120Hz","MediaTek Dimensity 6300","108MP+5MP+2MP","5010 mAh","33W Wired","None",8,"256GB",True,False,False,"MediaTek",6.78,["108MP camera","AMOLED display","5G ready"],["No fast wireless charging","Average chipset"],"Value AMOLED phone with 108MP camera."),
    ph("TCL","40 SE",8999,1,"6.75-inch IPS LCD 90Hz","Unisoc T606","13MP","5000 mAh","10W Wired","None",4,"64GB",False,False,False,"Unisoc",6.75,["Very affordable","Large screen","Big battery"],["Very weak processor","Slow charging","Basic cameras"],"Ultra-budget smartphone for first-time buyers."),
]

# ======================== LOAD AND MERGE ========================
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

match = re.search(r"(?:var|const) PHONES = (\[.*?\]);", content, re.DOTALL)
if not match:
    print("Cannot find PHONES array"); exit(1)

phones = json.loads(match.group(1))
existing_ids = {p["id"] for p in phones}

added = 0
for p in new_phones:
    if p["id"] not in existing_ids:
        phones.append(p)
        existing_ids.add(p["id"])
        added += 1

new_json = json.dumps(phones, indent=2)
new_content = content.replace(match.group(0), f"var PHONES = {new_json};")
with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Added {added} new phones. Total DB size: {len(phones)}")

import json

def get_price_category(price_int):
    if price_int < 20000: return 0
    elif price_int < 35000: return 1
    elif price_int < 50000: return 2
    elif price_int < 70000: return 3
    elif price_int < 100000: return 4
    else: return 5

# Data schema: 
# "Name", price, 
# (dur, cam, bat, char, disp, snd, ip, proc),
# (display_text, proc_text, ram_text, bat_text, char_text, cam_text, ip_text, weight_text)

phones_data = [
    # APPLE
    ("iPhone 16 Pro Max", 159900, "Apple", "🍎",
     (9.5, 9.8, 8.8, 7.5, 9.7, 9.2, 10.0, 9.9),
     ("6.9\" LTPO Super Retina XDR OLED, 120Hz", "A18 Pro (3 nm)", "8GB RAM", "4685 mAh", "30W Wired, 25W MagSafe", "48MP Main, 48MP UW, 12MP 5x Tele", "IP68 (6m for 30 min)", "227g, Titanium frame")),
    ("iPhone 16 Pro", 119900, "Apple", "🍎",
     (9.5, 9.5, 7.8, 7.5, 9.5, 9.0, 10.0, 9.9),
     ("6.3\" LTPO Super Retina XDR OLED, 120Hz", "A18 Pro (3 nm)", "8GB RAM", "3582 mAh", "30W Wired, 25W MagSafe", "48MP Main, 48MP UW, 12MP 5x Tele", "IP68 (6m for 30 min)", "199g, Titanium frame")),
    ("iPhone 16 Plus", 89900, "Apple", "🍎",
     (9.0, 8.8, 9.0, 7.3, 8.8, 8.8, 10.0, 9.6),
     ("6.7\" Super Retina XDR OLED, 60Hz", "A18 (3 nm)", "8GB RAM", "4674 mAh", "30W Wired, 25W MagSafe", "48MP Main, 12MP UW", "IP68 (6m for 30 min)", "199g, Aluminum frame")),
    ("iPhone 16", 79900, "Apple", "🍎",
     (9.0, 8.8, 8.0, 7.3, 8.8, 8.8, 10.0, 9.6),
     ("6.1\" Super Retina XDR OLED, 60Hz", "A18 (3 nm)", "8GB RAM", "3561 mAh", "30W Wired, 25W MagSafe", "48MP Main, 12MP UW", "IP68 (6m for 30 min)", "170g, Aluminum frame")),
    ("iPhone 15 Pro Max", 134900, "Apple", "🍎",
     (9.5, 9.4, 8.3, 7.0, 9.5, 9.0, 10.0, 9.5),
     ("6.7\" LTPO Super Retina XDR OLED, 120Hz", "A17 Pro (3 nm)", "8GB RAM", "4422 mAh", "27W Wired, 15W MagSafe", "48MP Main, 12MP UW, 12MP 5x Tele", "IP68 (6m for 30 min)", "221g, Titanium frame")),
    ("iPhone 15 Pro", 109900, "Apple", "🍎",
     (9.5, 9.2, 7.5, 7.0, 9.5, 8.8, 10.0, 9.5),
     ("6.1\" LTPO Super Retina XDR OLED, 120Hz", "A17 Pro (3 nm)", "8GB RAM", "3274 mAh", "27W Wired, 15W MagSafe", "48MP Main, 12MP UW, 12MP 3x Tele", "IP68 (6m for 30 min)", "187g, Titanium frame")),
    ("iPhone 15", 69900, "Apple", "🍎",
     (9.0, 8.5, 8.2, 6.8, 8.5, 8.5, 10.0, 9.0),
     ("6.1\" Super Retina XDR OLED, 60Hz", "A16 Bionic (4 nm)", "6GB RAM", "3349 mAh", "20W Wired, 15W MagSafe", "48MP Main, 12MP UW", "IP68 (6m for 30 min)", "171g, Aluminum frame")),
    ("iPhone 14 Pro", 109900, "Apple", "🍎",
     (9.3, 9.0, 7.5, 6.5, 9.2, 8.8, 10.0, 9.0),
     ("6.1\" LTPO Super Retina XDR OLED, 120Hz", "A16 Bionic (4 nm)", "6GB RAM", "3200 mAh", "20W Wired, 15W MagSafe", "48MP Main, 12MP UW, 12MP 3x Tele", "IP68 (6m for 30 min)", "206g, Stainless steel frame")),
    ("iPhone 14", 59900, "Apple", "🍎",
     (8.8, 8.2, 8.0, 6.5, 8.2, 8.2, 10.0, 8.5),
     ("6.1\" Super Retina XDR OLED, 60Hz", "A15 Bionic (5 nm)", "6GB RAM", "3279 mAh", "20W Wired, 15W MagSafe", "12MP Main, 12MP UW", "IP68 (6m for 30 min)", "172g, Aluminum frame")),
    ("iPhone 13", 49900, "Apple", "🍎",
     (8.5, 8.0, 8.5, 6.0, 8.0, 8.0, 10.0, 8.0),
     ("6.1\" Super Retina XDR OLED, 60Hz", "A15 Bionic (5 nm)", "4GB RAM", "3240 mAh", "20W Wired, 15W MagSafe", "12MP Main, 12MP UW", "IP68 (6m for 30 min)", "174g, Aluminum frame")),

    # SAMSUNG
    ("Galaxy S25 Ultra", 129999, "Samsung", "🌌",
     (9.5, 9.8, 8.9, 8.5, 9.8, 9.2, 10.0, 10.0),
     ("6.8\" Dynamic AMOLED 2X, 120Hz", "Snapdragon 8 Gen 4", "12GB/16GB RAM", "5000 mAh", "45W Wired, 15W Wireless", "200MP Main, 50MP UW, 50MP 5x, 10MP 3x", "IP68 Water Resistant", "232g, Titanium frame")),
    ("Galaxy S24 Ultra", 119999, "Samsung", "🌌",
     (9.5, 9.6, 8.7, 8.5, 9.7, 9.0, 10.0, 9.8),
     ("6.8\" Dynamic LTPO AMOLED 2X, 120Hz", "Snapdragon 8 Gen 3", "12GB RAM", "5000 mAh", "45W Wired, 15W Wireless", "200MP Main, 12MP UW, 50MP 5x, 10MP 3x", "IP68 Water Resistant", "232g, Titanium frame")),
    ("Galaxy S24+", 89999, "Samsung", "🌌",
     (9.0, 9.0, 8.5, 8.5, 9.5, 8.8, 10.0, 9.5),
     ("6.7\" Dynamic LTPO AMOLED 2X, 120Hz", "Exynos 2400 / SD8 Gen 3", "12GB RAM", "4900 mAh", "45W Wired, 15W Wireless", "50MP Main, 12MP UW, 10MP 3x Tele", "IP68 Water Resistant", "196g, Aluminum frame")),
    ("Galaxy S24", 69999, "Samsung", "🌌",
     (9.0, 8.8, 7.8, 7.0, 9.5, 8.8, 10.0, 9.5),
     ("6.2\" Dynamic LTPO AMOLED 2X, 120Hz", "Exynos 2400 / SD8 Gen 3", "8GB RAM", "4000 mAh", "25W Wired, 15W Wireless", "50MP Main, 12MP UW, 10MP 3x Tele", "IP68 Water Resistant", "167g, Aluminum frame")),
    ("Galaxy Z Fold 6", 164999, "Samsung", "🌌",
     (8.0, 9.0, 7.8, 7.0, 9.5, 9.0, 9.0, 9.8),
     ("7.6\" Foldable Dynamic AMOLED 2X, 120Hz", "Snapdragon 8 Gen 3", "12GB RAM", "4400 mAh", "25W Wired, 15W Wireless", "50MP Main, 12MP UW, 10MP 3x Tele", "IP48 Water Resistant", "239g, Armor Aluminum")),
    ("Galaxy Z Flip 6", 109999, "Samsung", "🌌",
     (8.0, 8.5, 7.5, 7.0, 9.0, 8.5, 9.0, 9.8),
     ("6.7\" Foldable Dynamic AMOLED 2X, 120Hz", "Snapdragon 8 Gen 3", "12GB RAM", "4000 mAh", "25W Wired, 15W Wireless", "50MP Main, 12MP UW", "IP48 Water Resistant", "187g, Armor Aluminum")),
    ("Galaxy S23 Ultra", 99999, "Samsung", "🌌",
     (9.2, 9.5, 8.5, 8.5, 9.5, 9.0, 10.0, 9.2),
     ("6.8\" Dynamic AMOLED 2X, 120Hz", "Snapdragon 8 Gen 2", "8GB/12GB RAM", "5000 mAh", "45W Wired, 15W Wireless", "200MP Main, 12MP UW, 10MP 10x, 10MP 3x", "IP68 Water Resistant", "234g, Aluminum frame")),
    ("Galaxy S23 FE", 49999, "Samsung", "🌌",
     (8.8, 8.2, 7.5, 7.0, 8.8, 8.2, 10.0, 8.0),
     ("6.4\" Dynamic AMOLED 2X, 120Hz", "Exynos 2200", "8GB RAM", "4500 mAh", "25W Wired, 15W Wireless", "50MP Main, 12MP UW, 8MP 3x Tele", "IP68 Water Resistant", "209g, Aluminum frame")),
    ("Galaxy A55", 39999, "Samsung", "🌌",
     (8.5, 8.0, 8.5, 7.0, 8.5, 8.0, 9.0, 7.5),
     ("6.6\" Super AMOLED, 120Hz", "Exynos 1480", "8GB/12GB RAM", "5000 mAh", "25W Wired", "50MP Main, 12MP UW, 5MP Macro", "IP67 Water Resistant", "213g, Aluminum frame")),
    ("Galaxy A35", 29999, "Samsung", "🌌",
     (8.0, 7.5, 8.5, 7.0, 8.2, 7.8, 9.0, 7.0),
     ("6.6\" Super AMOLED, 120Hz", "Exynos 1380", "8GB RAM", "5000 mAh", "25W Wired", "50MP Main, 8MP UW, 5MP Macro", "IP67 Water Resistant", "209g, Plastic frame")),
    ("Galaxy M55", 26999, "Samsung", "🌌",
     (7.5, 7.5, 8.5, 8.5, 8.5, 7.5, 2.0, 7.5),
     ("6.7\" Super AMOLED Plus, 120Hz", "Snapdragon 7 Gen 1", "8GB/12GB RAM", "5000 mAh", "45W Wired", "50MP Main, 8MP UW, 2MP Macro", "No IP Rating", "180g, Plastic frame")),
    ("Galaxy M34", 17999, "Samsung", "🌌",
     (7.5, 7.0, 9.5, 7.0, 7.8, 7.0, 2.0, 6.5),
     ("6.5\" Super AMOLED, 120Hz", "Exynos 1280", "6GB/8GB RAM", "6000 mAh", "25W Wired", "50MP Main, 8MP UW, 2MP Macro", "No IP Rating", "208g, Plastic body")),
    ("Galaxy M14", 12999, "Samsung", "🌌",
     (7.0, 6.0, 9.5, 5.0, 6.5, 6.0, 2.0, 6.0),
     ("6.6\" PLS LCD, 90Hz", "Exynos 1330", "4GB/6GB RAM", "6000 mAh", "15W Wired", "50MP Main, 2MP Macro, 2MP Depth", "No IP Rating", "206g, Plastic body")),

    # GOOGLE
    ("Pixel 9 Pro XL", 129999, "Google", "🔍",
     (9.2, 9.7, 8.5, 8.0, 9.6, 9.0, 10.0, 8.8),
     ("6.8\" LTPO OLED, 120Hz", "Google Tensor G4", "16GB RAM", "5060 mAh", "37W Wired, 23W Wireless", "50MP Main, 48MP UW, 48MP 5x Tele", "IP68 Water Resistant", "221g, Aluminum frame")),
    ("Pixel 9 Pro", 109999, "Google", "🔍",
     (9.2, 9.7, 8.0, 7.8, 9.5, 8.8, 10.0, 8.8),
     ("6.3\" LTPO OLED, 120Hz", "Google Tensor G4", "16GB RAM", "4700 mAh", "27W Wired, 21W Wireless", "50MP Main, 48MP UW, 48MP 5x Tele", "IP68 Water Resistant", "199g, Aluminum frame")),
    ("Pixel 9", 79999, "Google", "🔍",
     (9.0, 9.2, 8.0, 7.8, 9.2, 8.5, 10.0, 8.8),
     ("6.3\" OLED, 120Hz", "Google Tensor G4", "12GB RAM", "4700 mAh", "27W Wired, 15W Wireless", "50MP Main, 48MP UW", "IP68 Water Resistant", "198g, Aluminum frame")),
    ("Pixel 8 Pro", 99999, "Google", "🔍",
     (9.0, 9.5, 8.0, 7.5, 9.5, 8.5, 10.0, 8.5),
     ("6.7\" LTPO OLED, 120Hz", "Google Tensor G3", "12GB RAM", "5050 mAh", "30W Wired, 23W Wireless", "50MP Main, 48MP UW, 48MP 5x Tele", "IP68 Water Resistant", "213g, Aluminum frame")),
    ("Pixel 8", 69999, "Google", "🔍",
     (8.8, 9.0, 7.8, 7.5, 9.0, 8.2, 10.0, 8.5),
     ("6.2\" OLED, 120Hz", "Google Tensor G3", "8GB RAM", "4575 mAh", "27W Wired, 18W Wireless", "50MP Main, 12MP UW", "IP68 Water Resistant", "187g, Aluminum frame")),
    ("Pixel 8a", 49999, "Google", "🔍",
     (8.5, 8.5, 7.8, 6.0, 8.8, 8.0, 9.0, 8.2),
     ("6.1\" OLED, 120Hz", "Google Tensor G3", "8GB RAM", "4492 mAh", "18W Wired, 7.5W Wireless", "64MP Main, 13MP UW", "IP67 Water Resistant", "188g, Aluminum frame")),
    ("Pixel 7a", 39999, "Google", "🔍",
     (8.0, 8.2, 7.5, 6.0, 8.2, 7.8, 9.0, 7.8),
     ("6.1\" OLED, 90Hz", "Google Tensor G2", "8GB RAM", "4385 mAh", "18W Wired, 7.5W Wireless", "64MP Main, 13MP UW", "IP67 Water Resistant", "193g, Aluminum frame")),

    # XIAOMI & POCO
    ("Xiaomi 14 Ultra", 99999, "Xiaomi", "🟠",
     (9.2, 10.0, 8.5, 9.5, 9.6, 9.0, 10.0, 9.8),
     ("6.73\" LTPO AMOLED, 120Hz", "Snapdragon 8 Gen 3", "16GB RAM", "5000 mAh", "90W Wired, 80W Wireless", "50MP Main (1-inch), 50MP UW, 50MP 3.2x, 50MP 5x", "IP68 Water Resistant", "219g, Aluminum frame")),
    ("Xiaomi 14", 69999, "Xiaomi", "🟠",
     (9.0, 9.2, 8.0, 9.5, 9.4, 8.8, 10.0, 9.8),
     ("6.36\" LTPO OLED, 120Hz", "Snapdragon 8 Gen 3", "12GB RAM", "4610 mAh", "90W Wired, 50W Wireless", "50MP Main, 50MP UW, 50MP 3.2x Tele", "IP68 Water Resistant", "188g, Aluminum frame")),
    ("Redmi Note 13 Pro+", 29999, "Xiaomi", "🟠",
     (8.5, 8.2, 8.5, 9.8, 8.8, 8.0, 10.0, 7.5),
     ("6.67\" AMOLED, 120Hz", "Dimensity 7200 Ultra", "8GB/12GB RAM", "5000 mAh", "120W Wired", "200MP Main, 8MP UW, 2MP Macro", "IP68 Water Resistant", "204g, Aluminum frame")),
    ("Redmi Note 13 Pro", 24999, "Xiaomi", "🟠",
     (8.0, 8.0, 8.5, 8.5, 8.8, 7.8, 5.0, 7.2),
     ("6.67\" AMOLED, 120Hz", "Snapdragon 7s Gen 2", "8GB/12GB RAM", "5100 mAh", "67W Wired", "200MP Main, 8MP UW, 2MP Macro", "IP54 Splash Resistant", "187g, Plastic frame")),
    ("POCO F6", 29999, "Xiaomi", "🟠",
     (8.0, 7.5, 8.2, 9.0, 8.8, 8.0, 7.0, 9.0),
     ("6.67\" AMOLED, 120Hz", "Snapdragon 8s Gen 3", "8GB/12GB RAM", "5000 mAh", "90W Wired", "50MP Main, 8MP UW", "IP64 Splash Resistant", "179g, Plastic frame")),
    ("POCO X6 Pro", 24999, "Xiaomi", "🟠",
     (7.8, 7.0, 8.2, 8.5, 8.8, 7.8, 5.0, 8.8),
     ("6.67\" AMOLED, 120Hz", "Dimensity 8300 Ultra", "8GB/12GB RAM", "5000 mAh", "67W Wired", "64MP Main, 8MP UW, 2MP Macro", "IP54 Splash Resistant", "186g, Plastic frame")),
    ("POCO M6 Pro 5G", 10999, "Xiaomi", "🟠",
     (7.0, 5.5, 8.5, 6.0, 6.5, 6.0, 5.0, 6.5),
     ("6.79\" IPS LCD, 90Hz", "Snapdragon 4 Gen 2", "4GB/6GB RAM", "5000 mAh", "18W Wired", "50MP Main, 2MP Depth", "IP53 Splash Resistant", "199g, Plastic frame")),
    ("Redmi 13C 5G", 11999, "Xiaomi", "🟠",
     (7.0, 5.5, 8.5, 6.0, 6.5, 6.0, 2.0, 6.2),
     ("6.74\" IPS LCD, 90Hz", "Dimensity 6100+", "4GB/8GB RAM", "5000 mAh", "18W Wired", "50MP Main", "No IP Rating", "192g, Plastic frame")),

    # ONEPLUS
    ("OnePlus 12", 64999, "OnePlus", "🔴",
     (9.0, 9.2, 9.0, 10.0, 9.6, 9.0, 9.0, 9.8),
     ("6.82\" LTPO AMOLED, 120Hz", "Snapdragon 8 Gen 3", "12GB/16GB RAM", "5400 mAh", "100W Wired, 50W Wireless", "50MP Main, 48MP UW, 64MP 3x Tele", "IP65 Water/Dust Resistant", "220g, Aluminum frame")),
    ("OnePlus 12R", 39999, "OnePlus", "🔴",
     (8.8, 8.0, 9.0, 10.0, 9.2, 8.5, 9.0, 9.2),
     ("6.78\" LTPO4 AMOLED, 120Hz", "Snapdragon 8 Gen 2", "8GB/16GB RAM", "5500 mAh", "100W Wired", "50MP Main, 8MP UW, 2MP Macro", "IP64 Splash Resistant", "207g, Aluminum frame")),
    ("OnePlus 11", 54999, "OnePlus", "🔴",
     (8.8, 8.8, 8.5, 10.0, 9.4, 8.8, 9.0, 9.2),
     ("6.7\" LTPO3 AMOLED, 120Hz", "Snapdragon 8 Gen 2", "8GB/16GB RAM", "5000 mAh", "100W Wired", "50MP Main, 48MP UW, 32MP 2x Tele", "IP64 Splash Resistant", "205g, Aluminum frame")),
    ("Nord 4", 29999, "OnePlus", "🔴",
     (9.2, 7.8, 9.0, 10.0, 9.0, 8.2, 9.0, 8.5),
     ("6.74\" Fluid AMOLED, 120Hz", "Snapdragon 7+ Gen 3", "8GB/12GB RAM", "5500 mAh", "100W Wired", "50MP Main, 8MP UW", "IP65 Water/Dust Resistant", "199g, Full Metal Unibody")),
    ("Nord CE 4", 24999, "OnePlus", "🔴",
     (8.0, 7.5, 9.0, 10.0, 8.5, 8.0, 5.0, 7.8),
     ("6.7\" AMOLED, 120Hz", "Snapdragon 7 Gen 3", "8GB RAM", "5500 mAh", "100W Wired", "50MP Main, 8MP UW", "IP54 Splash Resistant", "186g, Plastic frame")),
    ("Nord CE 3 Lite", 17999, "OnePlus", "🔴",
     (7.5, 6.5, 8.5, 8.5, 7.0, 7.5, 2.0, 6.8),
     ("6.72\" IPS LCD, 120Hz", "Snapdragon 695", "8GB RAM", "5000 mAh", "67W Wired", "108MP Main, 2MP Macro, 2MP Depth", "No IP Rating", "195g, Plastic frame")),

    # VIVO & iQOO
    ("Vivo X100 Pro", 89999, "Vivo", "🔵",
     (9.0, 10.0, 9.0, 10.0, 9.5, 8.8, 10.0, 9.8),
     ("6.78\" LTPO AMOLED, 120Hz", "Dimensity 9300", "16GB RAM", "5400 mAh", "100W Wired, 50W Wireless", "50MP Main (1-inch), 50MP UW, 50MP 4.3x Tele", "IP68 Water Resistant", "221g, Aluminum frame")),
    ("Vivo X100", 63999, "Vivo", "🔵",
     (8.8, 9.5, 8.5, 10.0, 9.4, 8.5, 10.0, 9.8),
     ("6.78\" LTPO AMOLED, 120Hz", "Dimensity 9300", "12GB/16GB RAM", "5000 mAh", "120W Wired", "50MP Main, 50MP UW, 64MP 3x Tele", "IP68 Water Resistant", "206g, Aluminum frame")),
    ("Vivo V30 Pro", 41999, "Vivo", "🔵",
     (8.0, 9.2, 8.5, 9.0, 9.0, 8.0, 5.0, 8.0),
     ("6.78\" AMOLED, 120Hz", "Dimensity 8200", "8GB/12GB RAM", "5000 mAh", "80W Wired", "50MP Main, 50MP UW, 50MP 2x Tele (Zeiss)", "IP54 Splash Resistant", "188g, Plastic frame")),
    ("iQOO 12", 52999, "Vivo", "🔵",
     (8.8, 8.8, 8.5, 10.0, 9.4, 8.8, 9.0, 9.8),
     ("6.78\" LTPO AMOLED, 144Hz", "Snapdragon 8 Gen 3", "12GB/16GB RAM", "5000 mAh", "120W Wired", "50MP Main, 50MP UW, 64MP 3x Tele", "IP64 Splash Resistant", "203g, Aluminum frame")),
    ("iQOO Neo 9 Pro", 35999, "Vivo", "🔵",
     (8.2, 8.0, 8.8, 10.0, 9.0, 8.5, 5.0, 9.2),
     ("6.78\" LTPO AMOLED, 144Hz", "Snapdragon 8 Gen 2", "8GB/12GB RAM", "5160 mAh", "120W Wired", "50MP Main, 8MP UW", "IP54 Splash Resistant", "190g, Plastic frame")),
    ("iQOO Z9", 19999, "Vivo", "🔵",
     (7.5, 7.5, 8.5, 7.5, 8.5, 7.5, 5.0, 7.8),
     ("6.67\" AMOLED, 120Hz", "Dimensity 7200", "8GB RAM", "5000 mAh", "44W Wired", "50MP Main, 2MP Depth", "IP54 Splash Resistant", "188g, Plastic frame")),
    ("Vivo T2x", 12999, "Vivo", "🔵",
     (7.0, 5.5, 8.5, 6.0, 6.5, 6.0, 2.0, 6.2),
     ("6.58\" IPS LCD, 60Hz", "Dimensity 6020", "4GB/6GB RAM", "5000 mAh", "18W Wired", "50MP Main, 2MP Depth", "No IP Rating", "184g, Plastic frame")),

    # OPPO & MOTOROLA
    ("Oppo Find X7 Ultra", 99999, "Oppo", "🟢",
     (9.2, 10.0, 8.8, 10.0, 9.6, 9.0, 10.0, 9.8),
     ("6.82\" LTPO AMOLED, 120Hz", "Snapdragon 8 Gen 3", "12GB/16GB RAM", "5000 mAh", "100W Wired, 50W Wireless", "50MP Main (1-inch), 50MP UW, 50MP 3x, 50MP 6x", "IP68 Water Resistant", "221g, Aluminum frame")),
    ("Oppo Reno 11 Pro", 39999, "Oppo", "🟢",
     (8.0, 8.5, 8.0, 9.0, 8.8, 8.0, 2.0, 8.0),
     ("6.7\" AMOLED, 120Hz", "Dimensity 8200", "12GB RAM", "4600 mAh", "80W Wired", "50MP Main, 8MP UW, 32MP 2x Tele", "No IP Rating", "181g, Plastic frame")),
    ("Oppo F25 Pro", 23999, "Oppo", "🟢",
     (8.0, 7.5, 8.5, 8.5, 8.5, 7.0, 9.0, 7.2),
     ("6.7\" AMOLED, 120Hz", "Dimensity 7050", "8GB RAM", "5000 mAh", "67W Wired", "64MP Main, 8MP UW, 2MP Macro", "IP65 Water/Dust Resistant", "177g, Plastic frame")),
    ("Moto Edge 50 Pro", 29999, "Motorola", "🦇",
     (8.5, 8.2, 8.0, 10.0, 9.2, 8.5, 10.0, 7.8),
     ("6.7\" P-OLED, 144Hz", "Snapdragon 7 Gen 3", "8GB/12GB RAM", "4500 mAh", "125W Wired, 50W Wireless", "50MP Main, 13MP UW, 10MP 3x Tele", "IP68 Water Resistant", "186g, Aluminum frame")),
    ("Moto Edge 50 Fusion", 22999, "Motorola", "🦇",
     (8.5, 7.8, 8.5, 8.5, 9.0, 8.0, 10.0, 7.5),
     ("6.7\" P-OLED, 144Hz", "Snapdragon 7s Gen 2", "8GB/12GB RAM", "5000 mAh", "68W Wired", "50MP Main, 13MP UW", "IP68 Water Resistant", "175g, Plastic frame")),
    ("Moto G34", 10999, "Motorola", "🦇",
     (7.5, 5.5, 8.5, 6.0, 6.5, 7.5, 5.0, 6.5),
     ("6.5\" IPS LCD, 120Hz", "Snapdragon 695", "4GB/8GB RAM", "5000 mAh", "18W Wired", "50MP Main, 2MP Macro", "IP52 Splash Resistant", "179g, Plastic frame"))
]

phones_data.extend([
    # Samsung A-series & M-series & F-series & older S-series
    ("Galaxy S23+", 74999, "Samsung", "??", (9.0, 9.0, 8.5, 8.5, 9.5, 8.8, 10.0, 9.2), ("6.6\" Dynamic AMOLED 2X, 120Hz", "Snapdragon 8 Gen 2", "8GB RAM", "4700 mAh", "45W Wired, 15W Wireless", "50MP Main, 12MP UW, 10MP 3x", "IP68", "196g")),
    ("Galaxy S23", 59999, "Samsung", "??", (9.0, 8.8, 7.8, 7.0, 9.5, 8.8, 10.0, 9.2), ("6.1\" Dynamic AMOLED 2X, 120Hz", "Snapdragon 8 Gen 2", "8GB RAM", "3900 mAh", "25W Wired, 15W Wireless", "50MP Main, 12MP UW, 10MP 3x", "IP68", "168g")),
    ("Galaxy Z Fold 5", 154999, "Samsung", "??", (7.5, 9.0, 7.8, 7.0, 9.5, 9.0, 9.0, 9.2), ("7.6\" Foldable AMOLED, 120Hz", "Snapdragon 8 Gen 2", "12GB RAM", "4400 mAh", "25W Wired, 15W Wireless", "50MP Main, 12MP UW, 10MP 3x", "IPX8", "253g")),
    ("Galaxy Z Flip 5", 99999, "Samsung", "??", (7.5, 8.5, 7.5, 7.0, 9.0, 8.5, 9.0, 9.2), ("6.7\" Foldable AMOLED, 120Hz", "Snapdragon 8 Gen 2", "8GB RAM", "3700 mAh", "25W Wired, 15W Wireless", "12MP Main, 12MP UW", "IPX8", "187g")),
    ("Galaxy A54", 34999, "Samsung", "??", (8.5, 7.8, 8.5, 7.0, 8.5, 8.0, 9.0, 7.0), ("6.4\" Super AMOLED, 120Hz", "Exynos 1380", "8GB RAM", "5000 mAh", "25W Wired", "50MP Main, 12MP UW, 5MP Macro", "IP67", "202g")),
    ("Galaxy A34", 24999, "Samsung", "??", (8.0, 7.2, 8.5, 7.0, 8.2, 7.5, 9.0, 6.8), ("6.6\" Super AMOLED, 120Hz", "Dimensity 1080", "8GB RAM", "5000 mAh", "25W Wired", "48MP Main, 8MP UW, 5MP Macro", "IP67", "199g")),
    ("Galaxy F14", 11999, "Samsung", "??", (7.0, 5.5, 9.5, 5.0, 6.0, 6.0, 2.0, 6.0), ("6.6\" PLS LCD, 90Hz", "Exynos 1330", "4GB/6GB RAM", "6000 mAh", "25W Wired", "50MP Main, 2MP Macro", "No IP Rating", "206g")),
    ("Galaxy A14", 13999, "Samsung", "??", (7.0, 5.0, 8.5, 5.0, 6.0, 6.0, 2.0, 5.5), ("6.6\" PLS LCD, 60Hz", "Exynos 850", "4GB RAM", "5000 mAh", "15W Wired", "50MP Main, 5MP UW, 2MP Macro", "No IP Rating", "201g")),
    # Xiaomi/POCO
    ("Xiaomi 13 Pro", 79999, "Xiaomi", "??", (8.8, 9.5, 8.5, 10.0, 9.5, 8.8, 10.0, 9.2), ("6.73\" LTPO AMOLED, 120Hz", "Snapdragon 8 Gen 2", "12GB RAM", "4820 mAh", "120W Wired, 50W Wireless", "50MP Main (1-inch), 50MP UW, 50MP 3.2x", "IP68", "229g")),
    ("Xiaomi 13", 59999, "Xiaomi", "??", (8.8, 8.8, 8.0, 9.5, 9.2, 8.5, 10.0, 9.2), ("6.36\" AMOLED, 120Hz", "Snapdragon 8 Gen 2", "8GB/12GB RAM", "4500 mAh", "67W Wired, 50W Wireless", "50MP Main, 12MP UW, 10MP 3.2x", "IP68", "185g")),
    ("Redmi Note 13", 17999, "Xiaomi", "??", (7.5, 7.0, 8.5, 8.0, 8.2, 7.5, 5.0, 7.0), ("6.67\" AMOLED, 120Hz", "Dimensity 6080", "6GB/8GB RAM", "5000 mAh", "33W Wired", "108MP Main, 8MP UW", "IP54", "174g")),
    ("Redmi Note 12 Pro+", 27999, "Xiaomi", "??", (8.0, 8.0, 8.5, 10.0, 8.5, 7.8, 5.0, 7.2), ("6.67\" OLED, 120Hz", "Dimensity 1080", "8GB/12GB RAM", "4980 mAh", "120W Wired", "200MP Main, 8MP UW", "IP53", "208g")),
    ("POCO F6 Pro", 39999, "Xiaomi", "??", (8.5, 7.8, 8.5, 10.0, 9.2, 8.5, 5.0, 9.2), ("6.67\" AMOLED, 120Hz", "Snapdragon 8 Gen 2", "12GB/16GB RAM", "5000 mAh", "120W Wired", "50MP Main, 8MP UW, 2MP Macro", "IP54", "209g")),
    ("POCO F5", 27999, "Xiaomi", "??", (7.8, 7.0, 8.2, 8.5, 8.5, 7.8, 5.0, 8.5), ("6.67\" AMOLED, 120Hz", "Snapdragon 7+ Gen 2", "8GB/12GB RAM", "5000 mAh", "67W Wired", "64MP Main, 8MP UW, 2MP Macro", "IP53", "181g")),
    ("POCO X6", 19999, "Xiaomi", "??", (7.5, 6.8, 8.5, 8.5, 8.5, 7.5, 5.0, 7.8), ("6.67\" AMOLED, 120Hz", "Snapdragon 7s Gen 2", "8GB/12GB RAM", "5100 mAh", "67W Wired", "64MP Main, 8MP UW", "IP54", "181g")),
    # OnePlus
    ("OnePlus 11R", 34999, "OnePlus", "??", (8.5, 7.8, 8.8, 10.0, 9.0, 8.2, 2.0, 8.8), ("6.74\" Fluid AMOLED, 120Hz", "Snapdragon 8+ Gen 1", "8GB/16GB RAM", "5000 mAh", "100W Wired", "50MP Main, 8MP UW, 2MP Macro", "No IP Rating", "204g")),
    ("OnePlus Open", 139999, "OnePlus", "??", (8.0, 9.5, 8.0, 9.5, 9.6, 9.0, 5.0, 9.2), ("7.8\" Foldable LTPO3 OLED, 120Hz", "Snapdragon 8 Gen 2", "16GB RAM", "4805 mAh", "67W Wired", "48MP Main, 48MP UW, 64MP 3x", "IPX4", "239g")),
    ("Nord CE 3", 22999, "OnePlus", "??", (7.5, 7.0, 8.5, 9.0, 8.0, 7.5, 2.0, 7.5), ("6.7\" Fluid AMOLED, 120Hz", "Snapdragon 782G", "8GB RAM", "5000 mAh", "80W Wired", "50MP Main, 8MP UW", "No IP Rating", "184g")),
    # Vivo
    ("Vivo X90 Pro", 84999, "Vivo", "??", (8.8, 9.5, 8.5, 10.0, 9.4, 8.5, 10.0, 9.2), ("6.78\" AMOLED, 120Hz", "Dimensity 9200", "12GB RAM", "4870 mAh", "120W Wired, 50W Wireless", "50MP (1-inch), 12MP UW, 50MP 2x", "IP68", "214g")),
    ("Vivo X90", 59999, "Vivo", "??", (8.5, 9.0, 8.5, 10.0, 9.2, 8.2, 5.0, 9.2), ("6.78\" AMOLED, 120Hz", "Dimensity 9200", "8GB/12GB RAM", "4810 mAh", "120W Wired", "50MP Main, 12MP UW, 12MP 2x", "IP64", "200g")),
    ("Vivo V29 Pro", 39999, "Vivo", "??", (8.0, 8.8, 8.0, 9.0, 9.0, 7.5, 2.0, 8.2), ("6.78\" AMOLED, 120Hz", "Dimensity 8200", "8GB/12GB RAM", "4600 mAh", "80W Wired", "50MP Main, 8MP UW, 12MP 2x", "No IP Rating", "188g")),
    ("iQOO Neo 7 Pro", 31999, "Vivo", "??", (8.0, 7.5, 8.5, 10.0, 8.5, 8.0, 2.0, 8.8), ("6.78\" AMOLED, 120Hz", "Snapdragon 8+ Gen 1", "8GB/12GB RAM", "5000 mAh", "120W Wired", "50MP Main, 8MP UW, 2MP Macro", "No IP Rating", "197g")),
    # Oppo & Moto
    ("Oppo Reno 11", 29999, "Oppo", "??", (7.8, 8.0, 8.5, 8.5, 8.5, 7.8, 2.0, 7.5), ("6.7\" OLED, 120Hz", "Dimensity 7050", "8GB RAM", "5000 mAh", "67W Wired", "50MP Main, 8MP UW, 32MP 2x", "No IP Rating", "182g")),
    ("Moto Edge 50 Ultra", 59999, "Motorola", "??", (8.8, 9.0, 8.0, 10.0, 9.4, 8.8, 10.0, 9.0), ("6.7\" P-OLED, 144Hz", "Snapdragon 8s Gen 3", "12GB/16GB RAM", "4500 mAh", "125W Wired, 50W Wireless", "50MP Main, 50MP UW, 64MP 3x", "IP68", "197g")),
    ("Moto Edge 40 Neo", 22999, "Motorola", "??", (8.0, 7.5, 8.5, 8.5, 8.8, 8.0, 10.0, 7.5), ("6.55\" P-OLED, 144Hz", "Dimensity 7030", "8GB/12GB RAM", "5000 mAh", "68W Wired", "50MP Main, 13MP UW", "IP68", "170g"))
])
formatted_phones = []
for p in phones_data:
    name, price, brand, emoji, scores, spec_strings = p
    formatted_phones.append({
        "id": name.lower().replace(" ", "").replace("+", "plus").replace("-", ""),
        "name": name,
        "brand": brand,
        "emoji": emoji,
        "price": f"₹{price:,}",
        "priceCategory": get_price_category(price),
        "uniqueFeature": f"{brand} signature experience",
        "specs": {
            "display": spec_strings[0],
            "processor": spec_strings[1],
            "ram": spec_strings[2],
            "battery": spec_strings[3],
            "charging": spec_strings[4],
            "camera": spec_strings[5],
            "ip": spec_strings[6],
            "weight": spec_strings[7],
            "build": "Standard" # Condensed into weight string for most
        },
        "scores": {
            "durability": scores[0], "camera": scores[1], "battery": scores[2], 
            "charging": scores[3], "display": scores[4], "sound": scores[5], 
            "ipRating": scores[6], "processor": scores[7]
        }
    })

with open("phones.js", "w", encoding="utf-8") as f:
    f.write("const PHONES = " + json.dumps(formatted_phones, indent=2) + ";\n")
    f.write('''
const CRITERIA = [
  { key: 'durability', icon: '🛡️', label: 'Durability & Build', desc: 'Drop resistance & IP rating' },
  { key: 'camera', icon: '📸', label: 'Camera Quality', desc: 'Photos & video performance' },
  { key: 'battery', icon: '🔋', label: 'Battery Life', desc: 'Screen-on time & capacity' },
  { key: 'charging', icon: '⚡', label: 'Charging Speed', desc: 'Wired & wireless speeds' },
  { key: 'display', icon: '🖥️', label: 'Display Quality', desc: 'Brightness, colors, Hz' },
  { key: 'sound', icon: '🔊', label: 'Audio & Speakers', desc: 'Stereo quality & loudness' },
  { key: 'ipRating', icon: '💧', label: 'Water/Dust Resistance', desc: 'IP68 / IP67 / IP54' },
  { key: 'processor', icon: '🚀', label: 'Processor/Gaming', desc: 'CPU, GPU & Cooling' }
];

const PRESETS = {
  balanced: { durability: 7, camera: 7, battery: 7, charging: 7, display: 7, sound: 7, ipRating: 7, processor: 7 },
  camera: { durability: 4, camera: 10, battery: 6, charging: 5, display: 8, sound: 6, ipRating: 5, processor: 6 },
  battery: { durability: 6, camera: 5, battery: 10, charging: 9, display: 6, sound: 5, ipRating: 6, processor: 5 },
  rugged: { durability: 10, camera: 5, battery: 8, charging: 5, display: 6, sound: 5, ipRating: 10, processor: 5 },
  gaming: { durability: 7, camera: 5, battery: 8, charging: 8, display: 10, sound: 9, ipRating: 5, processor: 10 }
};

const BUDGET_LABELS = {
  0: "Under ₹20,000",
  1: "₹20K – ₹35K",
  2: "₹35K – ₹50K",
  3: "₹50K – ₹70K",
  4: "₹70K – ₹100K",
  5: "No Limit"
};
''')

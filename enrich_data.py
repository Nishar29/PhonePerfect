#!/usr/bin/env python3
"""
Enrich phones.js with additional filterable fields.
Reads the existing file, parses the PHONES array, adds new fields, writes back.
"""

import re
import json
import math
import os

PHONES_JS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phones.js")

# ─── Spec Database ───────────────────────────────────────────────────────────
# Accurate data for each phone model keyed by id
SPEC_DATA = {
    # ── Apple ──
    "iphone16promax": {
        "ram_gb": 8, "storage_options": "256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Apple",
        "screen_size": 6.9, "price_numeric": 159900, "tier": "flagship"
    },
    "iphone16pro": {
        "ram_gb": 8, "storage_options": "128GB / 256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Apple",
        "screen_size": 6.3, "price_numeric": 119900, "tier": "flagship"
    },
    "iphone16plus": {
        "ram_gb": 8, "storage_options": "128GB / 256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Apple",
        "screen_size": 6.7, "price_numeric": 89900, "tier": "flagship"
    },
    "iphone16": {
        "ram_gb": 8, "storage_options": "128GB / 256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Apple",
        "screen_size": 6.1, "price_numeric": 79900, "tier": "flagship"
    },
    "iphone15promax": {
        "ram_gb": 8, "storage_options": "256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Apple",
        "screen_size": 6.7, "price_numeric": 134900, "tier": "flagship"
    },
    "iphone15pro": {
        "ram_gb": 8, "storage_options": "128GB / 256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Apple",
        "screen_size": 6.1, "price_numeric": 109900, "tier": "flagship"
    },
    "iphone15": {
        "ram_gb": 6, "storage_options": "128GB / 256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Apple",
        "screen_size": 6.1, "price_numeric": 69900, "tier": "flagship"
    },
    "iphone14pro": {
        "ram_gb": 6, "storage_options": "128GB / 256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Apple",
        "screen_size": 6.1, "price_numeric": 109900, "tier": "flagship"
    },
    "iphone14": {
        "ram_gb": 6, "storage_options": "128GB / 256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Apple",
        "screen_size": 6.1, "price_numeric": 59900, "tier": "flagship"
    },
    "iphone13": {
        "ram_gb": 4, "storage_options": "128GB / 256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Apple",
        "screen_size": 6.1, "price_numeric": 49900, "tier": "midrange"
    },

    # ── Samsung Flagships ──
    "galaxys25ultra": {
        "ram_gb": 12, "storage_options": "256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.8, "price_numeric": 129999, "tier": "flagship"
    },
    "galaxys24ultra": {
        "ram_gb": 12, "storage_options": "256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.8, "price_numeric": 119999, "tier": "flagship"
    },
    "galaxys24plus": {
        "ram_gb": 12, "storage_options": "256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Exynos",
        "screen_size": 6.7, "price_numeric": 89999, "tier": "flagship"
    },
    "galaxys24": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Exynos",
        "screen_size": 6.2, "price_numeric": 69999, "tier": "flagship"
    },
    "galaxyzfold6": {
        "ram_gb": 12, "storage_options": "256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 7.6, "price_numeric": 164999, "tier": "flagship"
    },
    "galaxyzflip6": {
        "ram_gb": 12, "storage_options": "256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.7, "price_numeric": 109999, "tier": "flagship"
    },
    "galaxys23ultra": {
        "ram_gb": 12, "storage_options": "256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.8, "price_numeric": 99999, "tier": "flagship"
    },
    "galaxys23fe": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Exynos",
        "screen_size": 6.4, "price_numeric": 49999, "tier": "midrange"
    },

    # ── Samsung Mid-range / Budget ──
    "galaxya55": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Exynos",
        "screen_size": 6.6, "price_numeric": 39999, "tier": "midrange"
    },
    "galaxya35": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Exynos",
        "screen_size": 6.6, "price_numeric": 29999, "tier": "midrange"
    },
    "galaxym55": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.7, "price_numeric": 26999, "tier": "midrange"
    },
    "galaxym34": {
        "ram_gb": 6, "storage_options": "64GB / 128GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Exynos",
        "screen_size": 6.5, "price_numeric": 17999, "tier": "budget"
    },
    "galaxym14": {
        "ram_gb": 4, "storage_options": "64GB / 128GB", "has_5g": True,
        "has_nfc": False, "has_wireless_charging": False, "processor_brand": "Exynos",
        "screen_size": 6.6, "price_numeric": 12999, "tier": "budget"
    },

    # ── Google Pixel ──
    "pixel9proxl": {
        "ram_gb": 16, "storage_options": "128GB / 256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Tensor",
        "screen_size": 6.8, "price_numeric": 129999, "tier": "flagship"
    },
    "pixel9pro": {
        "ram_gb": 16, "storage_options": "128GB / 256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Tensor",
        "screen_size": 6.3, "price_numeric": 109999, "tier": "flagship"
    },
    "pixel9": {
        "ram_gb": 12, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Tensor",
        "screen_size": 6.3, "price_numeric": 79999, "tier": "flagship"
    },
    "pixel8pro": {
        "ram_gb": 12, "storage_options": "128GB / 256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Tensor",
        "screen_size": 6.7, "price_numeric": 99999, "tier": "flagship"
    },
    "pixel8": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Tensor",
        "screen_size": 6.2, "price_numeric": 69999, "tier": "flagship"
    },
    "pixel8a": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Tensor",
        "screen_size": 6.1, "price_numeric": 49999, "tier": "midrange"
    },
    "pixel7a": {
        "ram_gb": 8, "storage_options": "128GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Tensor",
        "screen_size": 6.1, "price_numeric": 39999, "tier": "midrange"
    },

    # ── Xiaomi Flagships ──
    "xiaomi14ultra": {
        "ram_gb": 16, "storage_options": "256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.73, "price_numeric": 99999, "tier": "flagship"
    },
    "xiaomi14": {
        "ram_gb": 12, "storage_options": "256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.36, "price_numeric": 69999, "tier": "flagship"
    },

    # ── Xiaomi / Redmi Mid-range ──
    "redminote13proplus": {
        "ram_gb": 8, "storage_options": "128GB / 256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.67, "price_numeric": 29999, "tier": "midrange"
    },
    "redminote13pro": {
        "ram_gb": 8, "storage_options": "128GB / 256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.67, "price_numeric": 24999, "tier": "midrange"
    },
    "pocof6": {
        "ram_gb": 8, "storage_options": "128GB / 256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.67, "price_numeric": 29999, "tier": "midrange"
    },
    "pocox6pro": {
        "ram_gb": 8, "storage_options": "128GB / 256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.67, "price_numeric": 24999, "tier": "midrange"
    },
    "pocom6pro5g": {
        "ram_gb": 4, "storage_options": "64GB / 128GB", "has_5g": True,
        "has_nfc": False, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.79, "price_numeric": 10999, "tier": "budget"
    },
    "redmi13c5g": {
        "ram_gb": 6, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": False, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.74, "price_numeric": 11999, "tier": "budget"
    },

    # ── OnePlus ──
    "oneplus12": {
        "ram_gb": 12, "storage_options": "128GB / 256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.82, "price_numeric": 64999, "tier": "flagship"
    },
    "oneplus12r": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.78, "price_numeric": 39999, "tier": "midrange"
    },
    "oneplus11": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.7, "price_numeric": 54999, "tier": "flagship"
    },
    "nord4": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.74, "price_numeric": 29999, "tier": "midrange"
    },
    "nordce4": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.7, "price_numeric": 24999, "tier": "midrange"
    },
    "nordce3lite": {
        "ram_gb": 8, "storage_options": "128GB", "has_5g": True,
        "has_nfc": False, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.72, "price_numeric": 17999, "tier": "budget"
    },

    # ── Vivo ──
    "vivox100pro": {
        "ram_gb": 16, "storage_options": "256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "MediaTek",
        "screen_size": 6.78, "price_numeric": 89999, "tier": "flagship"
    },
    "vivox100": {
        "ram_gb": 12, "storage_options": "256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.78, "price_numeric": 63999, "tier": "flagship"
    },
    "vivov30pro": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.78, "price_numeric": 41999, "tier": "midrange"
    },
    "iqoo12": {
        "ram_gb": 12, "storage_options": "256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.78, "price_numeric": 52999, "tier": "flagship"
    },
    "iqooneo9pro": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.78, "price_numeric": 35999, "tier": "midrange"
    },
    "iqooz9": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": False, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.67, "price_numeric": 19999, "tier": "budget"
    },
    "vivot2x": {
        "ram_gb": 4, "storage_options": "64GB / 128GB", "has_5g": True,
        "has_nfc": False, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.58, "price_numeric": 12999, "tier": "budget"
    },

    # ── Oppo ──
    "oppofindx7ultra": {
        "ram_gb": 16, "storage_options": "256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.82, "price_numeric": 99999, "tier": "flagship"
    },
    "opporeno11pro": {
        "ram_gb": 12, "storage_options": "256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.7, "price_numeric": 39999, "tier": "midrange"
    },
    "oppof25pro": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.7, "price_numeric": 23999, "tier": "midrange"
    },

    # ── Motorola ──
    "motoedge50pro": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.7, "price_numeric": 29999, "tier": "midrange"
    },
    "motoedge50fusion": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.7, "price_numeric": 22999, "tier": "midrange"
    },
    "motog34": {
        "ram_gb": 4, "storage_options": "64GB / 128GB", "has_5g": True,
        "has_nfc": False, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.5, "price_numeric": 10999, "tier": "budget"
    },

    # ── Batch 2 (added later phones) ──
    "galaxys23plus": {
        "ram_gb": 8, "storage_options": "256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.6, "price_numeric": 74999, "tier": "flagship"
    },
    "galaxys23": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.1, "price_numeric": 59999, "tier": "flagship"
    },
    "galaxyzfold5": {
        "ram_gb": 12, "storage_options": "256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 7.6, "price_numeric": 154999, "tier": "flagship"
    },
    "galaxyzflip5": {
        "ram_gb": 8, "storage_options": "256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.7, "price_numeric": 99999, "tier": "flagship"
    },
    "galaxya54": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Exynos",
        "screen_size": 6.4, "price_numeric": 34999, "tier": "midrange"
    },
    "galaxya34": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.6, "price_numeric": 24999, "tier": "midrange"
    },
    "galaxyf14": {
        "ram_gb": 4, "storage_options": "64GB / 128GB", "has_5g": True,
        "has_nfc": False, "has_wireless_charging": False, "processor_brand": "Exynos",
        "screen_size": 6.6, "price_numeric": 11999, "tier": "budget"
    },
    "galaxya14": {
        "ram_gb": 4, "storage_options": "64GB / 128GB", "has_5g": False,
        "has_nfc": False, "has_wireless_charging": False, "processor_brand": "Exynos",
        "screen_size": 6.6, "price_numeric": 13999, "tier": "budget"
    },
    "xiaomi13pro": {
        "ram_gb": 12, "storage_options": "256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.73, "price_numeric": 79999, "tier": "flagship"
    },
    "xiaomi13": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.36, "price_numeric": 59999, "tier": "flagship"
    },
    "redminote13": {
        "ram_gb": 6, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.67, "price_numeric": 17999, "tier": "budget"
    },
    "redminote12proplus": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.67, "price_numeric": 27999, "tier": "midrange"
    },
    "pocof6pro": {
        "ram_gb": 12, "storage_options": "256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.67, "price_numeric": 39999, "tier": "midrange"
    },
    "pocof5": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.67, "price_numeric": 27999, "tier": "midrange"
    },
    "pocox6": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.67, "price_numeric": 19999, "tier": "budget"
    },
    "oneplus11r": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.74, "price_numeric": 34999, "tier": "midrange"
    },
    "oneplusopen": {
        "ram_gb": 16, "storage_options": "256GB / 512GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 7.8, "price_numeric": 139999, "tier": "flagship"
    },
    "nordce3": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.7, "price_numeric": 22999, "tier": "midrange"
    },
    "vivox90pro": {
        "ram_gb": 12, "storage_options": "256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "MediaTek",
        "screen_size": 6.78, "price_numeric": 84999, "tier": "flagship"
    },
    "vivox90": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.78, "price_numeric": 59999, "tier": "flagship"
    },
    "vivov29pro": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.78, "price_numeric": 39999, "tier": "midrange"
    },
    "iqooneo7pro": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "Snapdragon",
        "screen_size": 6.78, "price_numeric": 31999, "tier": "midrange"
    },
    "opporeno11": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.7, "price_numeric": 29999, "tier": "midrange"
    },
    "motoedge50ultra": {
        "ram_gb": 12, "storage_options": "256GB / 512GB / 1TB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": True, "processor_brand": "Snapdragon",
        "screen_size": 6.7, "price_numeric": 59999, "tier": "flagship"
    },
    "motoedge40neo": {
        "ram_gb": 8, "storage_options": "128GB / 256GB", "has_5g": True,
        "has_nfc": True, "has_wireless_charging": False, "processor_brand": "MediaTek",
        "screen_size": 6.55, "price_numeric": 22999, "tier": "midrange"
    },
}


def compute_price_history(price_numeric, tier):
    """Generate 6-month price trend based on tier."""
    if tier == "flagship":
        decay = [0, -0.02, -0.05, -0.08, -0.12, -0.15]
    elif tier == "midrange":
        decay = [0, -0.03, -0.07, -0.12, -0.18, -0.22]
    else:  # budget
        decay = [0, -0.05, -0.10, -0.15, -0.20, -0.25]

    return [round(price_numeric * (1 + d)) for d in decay]


SCORE_LABELS = {
    "durability": "Durability & Build",
    "camera": "Camera Quality",
    "battery": "Battery Life",
    "charging": "Charging Speed",
    "display": "Display Quality",
    "sound": "Audio & Speakers",
    "ipRating": "Water/Dust Resistance",
    "processor": "Processor/Gaming",
}


def compute_pros_cons(phone, averages):
    """
    Compute top 3 pros and top 2 cons by comparing each score to the database average.
    """
    scores = phone.get("scores", {})
    deltas = {}
    for key, avg in averages.items():
        if key in scores:
            deltas[key] = scores[key] - avg

    # Sort by delta descending for pros, ascending for cons
    sorted_keys = sorted(deltas.keys(), key=lambda k: deltas[k], reverse=True)

    pro_phrases = {
        "durability": "Excellent build quality and durability",
        "camera": "Outstanding camera performance",
        "battery": "Impressive battery life",
        "charging": "Blazing fast charging speeds",
        "display": "Stunning display quality",
        "sound": "Superior audio and speaker quality",
        "ipRating": "Top-tier water and dust resistance",
        "processor": "Powerful processor for gaming and multitasking",
    }
    con_phrases = {
        "durability": "Build quality could be more robust",
        "camera": "Camera lags behind competitors",
        "battery": "Battery life is below average",
        "charging": "Charging speed is relatively slow",
        "display": "Display quality is average at best",
        "sound": "Speaker quality is underwhelming",
        "ipRating": "Limited water and dust protection",
        "processor": "Processor performance trails the competition",
    }

    pros = []
    for k in sorted_keys:
        if deltas[k] > 0 and len(pros) < 3:
            pros.append(pro_phrases.get(k, f"Strong {SCORE_LABELS.get(k, k)}"))
    # If we don't have 3, fill with the highest-scoring categories
    if len(pros) < 3:
        for k in sorted_keys:
            if len(pros) >= 3:
                break
            phrase = pro_phrases.get(k, f"Solid {SCORE_LABELS.get(k, k)}")
            if phrase not in pros:
                pros.append(phrase)

    cons = []
    for k in reversed(sorted_keys):
        if deltas[k] < 0 and len(cons) < 2:
            cons.append(con_phrases.get(k, f"Weak {SCORE_LABELS.get(k, k)}"))
    # If we don't have 2, fill with the lowest-scoring categories
    if len(cons) < 2:
        for k in reversed(sorted_keys):
            if len(cons) >= 2:
                break
            phrase = con_phrases.get(k, f"Average {SCORE_LABELS.get(k, k)}")
            if phrase not in cons:
                cons.append(phrase)

    return pros[:3], cons[:2]


def main():
    print(f"Reading {PHONES_JS_PATH}...")
    with open(PHONES_JS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse the PHONES array
    match = re.search(r"const PHONES = (\[.*?\]);", content, re.DOTALL)
    if not match:
        print("ERROR: Could not find PHONES array in phones.js")
        return

    phones_json_str = match.group(1)
    phones = json.loads(phones_json_str)
    print(f"Found {len(phones)} phones.")

    # Check which IDs we have data for
    phone_ids = [p["id"] for p in phones]
    missing = [pid for pid in phone_ids if pid not in SPEC_DATA]
    if missing:
        print(f"WARNING: No spec data for {len(missing)} phones: {missing}")

    # ── Compute averages across all phones ──
    score_keys = ["durability", "camera", "battery", "charging", "display", "sound", "ipRating", "processor"]
    averages = {}
    for key in score_keys:
        vals = [p["scores"][key] for p in phones if key in p.get("scores", {})]
        averages[key] = sum(vals) / len(vals) if vals else 5.0

    print("Score averages:")
    for k, v in averages.items():
        print(f"  {k}: {v:.2f}")

    # ── Enrich each phone ──
    enriched_count = 0
    for phone in phones:
        pid = phone["id"]
        spec = SPEC_DATA.get(pid)
        if not spec:
            print(f"  SKIP: {pid} (no spec data)")
            continue

        phone["ram_gb"] = spec["ram_gb"]
        phone["storage_options"] = spec["storage_options"]
        phone["has_5g"] = spec["has_5g"]
        phone["has_nfc"] = spec["has_nfc"]
        phone["has_wireless_charging"] = spec["has_wireless_charging"]
        phone["processor_brand"] = spec["processor_brand"]
        phone["screen_size"] = spec["screen_size"]
        phone["price_numeric"] = spec["price_numeric"]
        phone["price_history"] = compute_price_history(spec["price_numeric"], spec["tier"])

        pros, cons = compute_pros_cons(phone, averages)
        phone["pros"] = pros
        phone["cons"] = cons

        enriched_count += 1

    print(f"\nEnriched {enriched_count} / {len(phones)} phones.")

    # ── Serialize back ──
    phones_json_out = json.dumps(phones, indent=2, ensure_ascii=False)

    # Replace the PHONES array in the file
    new_content = content[:match.start()] + "const PHONES = " + phones_json_out + ";" + content[match.end():]

    with open(PHONES_JS_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[OK] Successfully wrote enriched data back to {PHONES_JS_PATH}")
    print(f"   File size: {len(new_content):,} bytes")

    # ── Quick validation ──
    verify_match = re.search(r"const PHONES = (\[.*?\]);", new_content, re.DOTALL)
    if verify_match:
        verify_phones = json.loads(verify_match.group(1))
        sample = verify_phones[0]
        new_fields = ["ram_gb", "storage_options", "has_5g", "has_nfc",
                       "has_wireless_charging", "processor_brand", "screen_size",
                       "price_numeric", "price_history", "pros", "cons"]
        present = [f for f in new_fields if f in sample]
        print(f"   Verification: {sample['name']} has {len(present)}/{len(new_fields)} new fields")
        for f in new_fields:
            print(f"     {f}: {sample.get(f, 'MISSING')}")
    else:
        print("   WARNING: Could not re-parse for verification")


if __name__ == "__main__":
    main()

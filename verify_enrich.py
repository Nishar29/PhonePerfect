import re, json

with open("phones.js", "r", encoding="utf-8") as f:
    c = f.read()

m = re.search(r"const PHONES = (\[.*?\]);", c, re.DOTALL)
phones = json.loads(m.group(1))

new_fields = ["ram_gb", "storage_options", "has_5g", "has_nfc",
              "has_wireless_charging", "processor_brand", "screen_size",
              "price_numeric", "price_history", "pros", "cons"]

p = phones[0]
print(f"Sample: {p['name']}")
for fld in new_fields:
    print(f"  {fld}: {p.get(fld, 'MISSING')}")

missing = [p2["name"] for p2 in phones if "ram_gb" not in p2]
print(f"\nTotal phones: {len(phones)}")
print(f"Enriched: {len(phones) - len(missing)}")
print(f"Missing: {len(missing)}")
if missing:
    for m2 in missing:
        print(f"  - {m2}")

import json

with open("phones.js", "r", encoding="utf-8") as f:
    js_content = f.read()

try:
    array_part = js_content.split("var PHONES = ")[1].split("];")[0] + "]"
    phones_data = json.loads(array_part)
    print("Parsed phones count:", len(phones_data))
    
    seen_names = {}
    for p in phones_data:
        name_key = f"{p.get('brand')} {p.get('name')}".strip()
        seen_names[name_key] = seen_names.get(name_key, []) + [p.get('id')]
        
    duplicates = {k: v for k, v in seen_names.items() if len(v) > 1}
    print(f"Unique names: {len(seen_names)}")
    print(f"Duplicate phone names: {len(duplicates)}")
    for name, ids in duplicates.items():
        print(f" - {name}: {ids}")
except Exception as e:
    print("Error:", e)

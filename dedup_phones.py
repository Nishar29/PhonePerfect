import json, re

with open("phones.js", "r", encoding="utf-8") as f:
    content = f.read()

# Split at "var PHONES = " and extract array
array_start = content.find("var PHONES = ") + len("var PHONES = ")
array_end = content.find("];", array_start) + 1  # include ']'
array_json = content[array_start:array_end]

phones = json.loads(array_json)
print(f"Total before dedup: {len(phones)}")

# Deduplicate: keep only first occurrence of each brand+name combo
seen = set()
unique_phones = []
removed = []
for p in phones:
    key = f"{p.get('brand', '').strip().lower()} {p.get('name', '').strip().lower()}"
    if key in seen:
        removed.append(f"{p.get('brand')} {p.get('name')} (id: {p.get('id')})")
    else:
        seen.add(key)
        unique_phones.append(p)

print(f"Total after dedup: {len(unique_phones)}")
print(f"Removed {len(removed)} duplicates:")
for r in removed:
    print(f"  - {r}")

# Write back
new_array_json = json.dumps(unique_phones, indent=2, ensure_ascii=False)
new_content = content[:array_start] + new_array_json + ";" + content[array_end + 1:]

with open("phones.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("\nDone! phones.js written successfully!")

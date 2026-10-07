import re

with open("phones.js", "r", encoding="utf-8") as f:
    content = f.read()

# Extract names and brands
matches = re.findall(r'"brand":\s*"([^"]+)",\s*"name":\s*"([^"]+)"', content)
print("Total phone matches parsed:", len(matches))

unique_full_names = set()
duplicates = []
for brand, name in matches:
    full = f"{brand} {name}"
    if full in unique_full_names:
        duplicates.append(full)
    else:
        unique_full_names.add(full)

print(f"Total unique phones: {len(unique_full_names)}")
print(f"Total duplicate entries found: {len(duplicates)}")
if duplicates:
    print("Some duplicates:")
    for d in duplicates[:10]:
        print(" -", d)
else:
    print("No duplicates found in dataset.")

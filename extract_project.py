import os
import re

input_file = r'c:\Users\nisha\OneDrive\Documents\project-all-code.txt'
output_dir = r'C:\Users\nisha\.gemini\antigravity\scratch\road-quality-monitor'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
    full_text = f.read()

# Pattern to match the header and capture the filename
pattern = r'================================================================\nFILE: \./(.*?)\n================================================================'

parts = re.split(pattern, full_text)

# parts[0] is garbage before first file
# parts[1] is filename 1
# parts[2] is content 1
# ...
for i in range(1, len(parts), 2):
    file_path = parts[i].strip()
    content = parts[i+1]
    
    # Normalize path
    full_path = os.path.join(output_dir, file_path.replace('/', os.sep))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    with open(full_path, 'w', encoding='utf-8') as out:
        out.write(content.strip() + '\n')

print(f"Successfully extracted {len(parts)//2} files to {output_dir}")

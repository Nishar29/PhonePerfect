import json
import re
import time
from duckduckgo_search import DDGS
from itertools import cycle

def run():
    print("Reading phones.js...")
    with open("phones.js", "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"const PHONES = (\[.*?\]);", content, re.DOTALL)
    if not match:
        print("Failed to find PHONES array.")
        return

    phones = json.loads(match.group(1))
    print(f"Found {len(phones)} phones to process.")
    
    ddgs = DDGS()
    
    missing_phones = [p for p in phones if len(p.get('images', [])) < 5]
    print(f"{len(missing_phones)} phones still need images.")
    
    for i, p in enumerate(missing_phones):
        query = f"{p['brand']} {p['name']} official render"
        print(f"[{i+1}/{len(missing_phones)}] Searching for: {query}")
        
        try:
            results = ddgs.images(
                keywords=query,
                region="wt-wt",
                safesearch="moderate",
                max_results=5
            )
            
            urls = []
            if results:
                for res in results:
                    url = res.get("image")
                    if url and url not in urls:
                        urls.append(url)
            
            p['images'] = urls[:5]
            print(f"  Found {len(p['images'])} images.")
            
        except Exception as e:
            print(f"  Error fetching images: {e}")
                
        # Sleep heavily to bypass DDG rate limit
        time.sleep(4)

    # Re-embed back into full phones array
    for p in phones:
        for m in missing_phones:
            if p['name'] == m['name']:
                p['images'] = m['images']

    new_content = content.replace(match.group(0), "const PHONES = " + json.dumps(phones, indent=2) + ";")
    with open("phones.js", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("\nSuccessfully updated phones.js!")

if __name__ == "__main__":
    run()

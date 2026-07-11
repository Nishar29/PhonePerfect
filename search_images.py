import json
import re
import time
from duckduckgo_search import DDGS

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
    
    for i, p in enumerate(phones):
        query = f"{p['brand']} {p['name']} smartphone high resolution"
        print(f"[{i+1}/{len(phones)}] Searching for: {query}")
        
        try:
            results = ddgs.images(
                keywords=query,
                region="wt-wt",
                safesearch="moderate",
                size="Large",
                max_results=5
            )
            
            urls = []
            if results:
                for res in results:
                    url = res.get("image")
                    if url and url not in urls:
                        urls.append(url)
            
            # If we didn't get exactly 5, maybe try a fallback query?
            # Or just use whatever we got up to 5.
            if len(urls) < 5:
                print(f"  Only found {len(urls)} images. Trying broader query...")
                fallback_results = ddgs.images(
                    keywords=f"{p['name']} phone",
                    region="wt-wt",
                    safesearch="moderate",
                    max_results=10
                )
                if fallback_results:
                    for res in fallback_results:
                        url = res.get("image")
                        if url and url not in urls:
                            urls.append(url)
                        if len(urls) >= 5:
                            break
            
            p['images'] = urls[:5]
            print(f"  Found {len(p['images'])} images.")
            
        except Exception as e:
            print(f"  Error fetching images: {e}")
            # Keep existing images if search completely fails to avoid crashing
            if 'images' not in p:
                p['images'] = []
                
        # Sleep to avoid rate limiting
        time.sleep(2)

    new_content = content.replace(match.group(0), "const PHONES = " + json.dumps(phones, indent=2) + ";")
    with open("phones.js", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("\nSuccessfully updated phones.js with exact images!")

if __name__ == "__main__":
    run()

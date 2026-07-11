import json
import random
import urllib.request
import urllib.parse
import time

def search_wikimedia_images(query, max_images=3):
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages|images&titles={urllib.parse.quote(query)}&pithumbsize=800"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PhoneAppBot/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            pages = data.get("query", {}).get("pages", {})
            urls = []
            for page_id, page_data in pages.items():
                if "thumbnail" in page_data:
                    urls.append(page_data["thumbnail"]["source"])
                if "images" in page_data:
                    for img in page_data["images"]:
                        title = img["title"]
                        if not any(x in title.lower() for x in ['.svg', 'icon', 'logo', '.ogg', '.ogv', 'commons-logo']):
                            img_url_req = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=imageinfo&titles={urllib.parse.quote(title)}&iiprop=url"
                            try:
                                img_req = urllib.request.Request(img_url_req, headers={'User-Agent': 'PhoneAppBot/1.0'})
                                with urllib.request.urlopen(img_req, timeout=2) as img_resp:
                                    img_data = json.loads(img_resp.read())
                                    img_pages = img_data.get("query", {}).get("pages", {})
                                    for _, i_data in img_pages.items():
                                        if "imageinfo" in i_data and len(i_data["imageinfo"]) > 0:
                                            url_i = i_data["imageinfo"][0]["url"]
                                            if url_i not in urls:
                                                urls.append(url_i)
                            except: pass
                        if len(urls) >= max_images: break
            return urls[:max_images]
    except:
        return []

brand_fallbacks = {
    "Apple": ["https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1605236453806-6ff36851218e?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=800&q=80"],
    "Samsung": ["https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1585060544812-6b45742d762f?auto=format&fit=crop&w=800&q=80"],
    "Google": ["https://images.unsplash.com/photo-1598327105666-5b89351cb315?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1662991080812-1d5ce100a7fa?auto=format&fit=crop&w=800&q=80"],
    "Xiaomi": ["https://images.unsplash.com/photo-1606775988583-0498b3f46f48?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=800&q=80"]
}
generic_fallback = ["https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=800&q=80", "https://images.unsplash.com/photo-1592890288564-76628a30a657?auto=format&fit=crop&w=800&q=80"]

with open("phones.js", "r", encoding="utf-8") as f:
    content = f.read()

# Instead of parsing json, let's just use python to extract the list of dictionaries if we can.
# Wait, phones.js is a valid JSON array assigned to const PHONES.
import re
match = re.search(r"const PHONES = (\[.*?\]);", content, re.DOTALL)
if match:
    phones = json.loads(match.group(1))
    print("Found", len(phones), "phones")
    for p in phones:
        if 'images' not in p or not p['images']:
            print("Fetching", p['name'])
            imgs = search_wikimedia_images(p['name'])
            if len(imgs) < 3:
                imgs.extend(brand_fallbacks.get(p['brand'], generic_fallback))
                imgs = list(dict.fromkeys(imgs))
            p['images'] = imgs[:4]
            time.sleep(0.1)
    
    new_content = content.replace(match.group(0), "const PHONES = " + json.dumps(phones, indent=2) + ";")
    with open("phones.js", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Success")
else:
    print("Failed to match")


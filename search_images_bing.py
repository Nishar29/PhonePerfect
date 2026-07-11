import json
import re
import time
import urllib.request
import urllib.parse
from html.parser import HTMLParser

class BingHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attrs_dict = dict(attrs)
            if 'class' in attrs_dict and 'iusc' in attrs_dict['class']:
                m_data = attrs_dict.get('m', '')
                if m_data:
                    try:
                        # Extract murl (Main URL) from the JSON-like string
                        m_json = json.loads(m_data)
                        if 'murl' in m_json:
                            self.urls.append(m_json['murl'])
                    except:
                        pass
        elif tag == 'img':
            attrs_dict = dict(attrs)
            if 'class' in attrs_dict and 'mimg' in attrs_dict['class']:
                src = attrs_dict.get('src') or attrs_dict.get('data-src')
                if src and src not in self.urls:
                    self.urls.append(src)

def scrape_bing_images(query, num_images=5):
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
            parser = BingHTMLParser()
            parser.feed(html)
            
            return list(dict.fromkeys(parser.urls))[:num_images]
    except Exception as e:
        print(f"Error scraping Bing: {e}")
        return []

def run():
    print("Reading phones.js...")
    with open("phones.js", "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"const PHONES = (\[.*?\]);", content, re.DOTALL)
    if not match:
        print("Failed to find PHONES array.")
        return

    phones = json.loads(match.group(1))
    
    # We will process phones that have less than 5 images
    missing_phones = [p for p in phones if len(p.get('images', [])) < 5]
    print(f"Found {len(missing_phones)} phones that still need images.")
    
    for i, p in enumerate(missing_phones):
        query = f"{p['brand']} {p['name']} official high resolution"
        print(f"[{i+1}/{len(missing_phones)}] Bing Search: {query}")
        
        urls = scrape_bing_images(query, 5)
        
        # If Bing failed, try alternative query
        if len(urls) < 5:
            urls += scrape_bing_images(f"{p['brand']} {p['name']} phone", 5 - len(urls))
            
        # Deduplicate
        urls = list(dict.fromkeys(urls))
        p['images'] = urls
        print(f"  Found {len(p['images'])} images.")
        
        time.sleep(1) # Be nice to Bing

    # Re-embed back into full phones array
    for p in phones:
        for m in missing_phones:
            if p['name'] == m['name']:
                p['images'] = m['images']

    new_content = content.replace(match.group(0), "const PHONES = " + json.dumps(phones, indent=2) + ";")
    with open("phones.js", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("\nSuccessfully updated phones.js using Bing Images!")

if __name__ == "__main__":
    run()

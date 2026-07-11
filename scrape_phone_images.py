#!/usr/bin/env python3
"""
Bing Image Scraper for phones.js
Fetches model-specific phone images via Bing HTML scraping.
"""

import urllib.request
import urllib.parse
import re
import json
import time
import sys
from html.parser import HTMLParser


class BingHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attrs_dict = dict(attrs)
            if 'class' in attrs_dict and 'mimg' in attrs_dict['class']:
                src = attrs_dict.get('src') or attrs_dict.get('data-src')
                if src and src.startswith('http') and src not in self.urls:
                    self.urls.append(src)


def scrape_bing_images(query, num_images=5):
    """Scrape image URLs from Bing Image Search HTML results."""
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            parser = BingHTMLParser()
            parser.feed(html)
            return list(dict.fromkeys(parser.urls))[:num_images]
    except Exception as e:
        print(f"  Error scraping '{query}': {e}")
        return []


def main():
    phones_path = r"c:\Users\nisha\.gemini\antigravity\scratch\phones.js"

    # Read phones.js
    with open(phones_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse the PHONES array
    match = re.search(r"(const|var|let) PHONES = (\s*\[.*?\]);", content, re.DOTALL)
    if not match:
        print("ERROR: Could not find PHONES array in phones.js")
        sys.exit(1)

    var_keyword = match.group(1)
    phones_json = match.group(2)
    phones = json.loads(phones_json)
    total = len(phones)
    print(f"Found {total} phones to process.")

    got5 = 0
    got_fewer = 0
    got_none = 0

    for i, phone in enumerate(phones):
        brand = phone.get('brand', '')
        name = phone.get('name', '')
        phone_id = phone.get('id', '')
        print(f"\n[{i+1}/{total}] {brand} {name} (id: {phone_id})")

        # Search 1: front/display images
        query1 = f"{brand} {name} front display screen"
        print(f"  Search 1: {query1}")
        urls1 = scrape_bing_images(query1, num_images=5)
        print(f"  Got {len(urls1)} from search 1")

        time.sleep(0.5)

        # Search 2: back/camera images
        query2 = f"{brand} {name} back camera design review"
        print(f"  Search 2: {query2}")
        urls2 = scrape_bing_images(query2, num_images=5)
        print(f"  Got {len(urls2)} from search 2")

        # Combine and deduplicate, take top 5
        combined = []
        seen = set()
        for url in urls1 + urls2:
            if url not in seen:
                seen.add(url)
                combined.append(url)

        final_images = combined[:5]
        count = len(final_images)
        print(f"  Final: {count} unique images")

        if count == 5:
            got5 += 1
        elif count > 0:
            got_fewer += 1
        else:
            got_none += 1

        phone['images'] = final_images

        # Rate limit: 1 second between phones
        if i < total - 1:
            time.sleep(1)

    # Write back to phones.js
    # Reconstruct the phones JS with proper formatting
    phones_json_new = json.dumps(phones, indent=2, ensure_ascii=False)
    new_content = content.replace(match.group(0), f"{var_keyword} PHONES = {phones_json_new};")

    with open(phones_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\n{'='*60}")
    print(f"DONE! Results:")
    print(f"  Total phones: {total}")
    print(f"  Got 5 images: {got5}")
    print(f"  Got fewer:    {got_fewer}")
    print(f"  Got none:     {got_none}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()

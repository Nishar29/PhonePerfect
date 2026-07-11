import urllib.request
import re

url = "https://corsproxy.io/?https://www.gsmarena.com/"
headers = {'User-Agent': 'Mozilla/5.0'}
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8')
        print("HTML length:", len(html))
        # Search for latest devices section
        # Often it is a list of links with "latest devices" or similar
        # Let's search for some recent phone names like "Galaxy" or "iPhone"
        matches = re.findall(r'href="([^"]+)"[^>]*>([^<]+)</a>', html)
        print("Found", len(matches), "links.")
        for href, text in matches[:50]:
            if '-' in href and '.php' in href:
                print(f"Link: {text.strip()} -> {href}")
except Exception as e:
    print("Error:", e)

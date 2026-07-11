import urllib.request
import json

url = "https://api-mobilespecs.azharimm.dev/latest"
headers = {'User-Agent': 'Mozilla/5.0'}
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
        print(json.dumps(data, indent=2)[:1000])
except Exception as e:
    print("Error:", e)

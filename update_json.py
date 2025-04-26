import requests
import json

url = "https://www.nseindia.com/api/holiday-master?type=trading"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

data = response.json()

with open("nse_holidays.json", "w") as f:
    json.dump(data, f, indent=2)

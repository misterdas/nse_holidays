import requests
import json

# Fetch the user-agent from the provided JSON file
user_agent = requests.get(
    "https://misterdas.github.io/risk_free_interest_rate/user_agents.json"
).json()[-2]

# Set headers with the dynamic user-agent
headers = {
    "user-agent": user_agent,
}

# Fetch the NSE holiday data
url = "https://www.nseindia.com/api/holiday-master?type=trading"
response = requests.get(url, headers=headers)
response.raise_for_status()

# Save the data to nse_holidays.json
data = response.json()

with open("nse_holidays.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

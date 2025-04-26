import requests
import json

# This function fetches the trading holidays data from NSE API
def fetch_nse_holidays(url: str = "https://www.nseindia.com/api/holiday-master?type=trading") -> None:
    # Set the user-agent for the request to mimic a real browser
    user_agent = requests.get(
        "https://misterdas.github.io/risk_free_interest_rate/user_agents.json"
    ).json()[-2]

    headers = {
        "user-agent": user_agent,
    }

    # Fetch the data from the NSE API
    response = requests.get(url, headers=headers)
    
    # Ensure the response is successful
    if response.status_code == 200:
        holidays_data = response.json()

        # Save the response JSON directly to the file
        with open("nse_holidays.json", "w") as jsonFile:
            json.dump(holidays_data, jsonFile, indent=4)
        
        print("NSE Holidays data has been updated successfully!")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_nse_holidays()

import requests
import json
import random

# This function fetches the trading holidays data from NSE API
def fetch_nse_holidays(url: str = "https://www.nseindia.com/api/holiday-master?type=trading"):
    try:
        # Fetch a random user agent from your JSON file
        user_agents_response = requests.get(
            "https://misterdas.github.io/risk_free_interest_rate/user_agents.json"
        )
        
        if user_agents_response.status_code != 200:
            print(f"Failed to fetch user agents: {user_agents_response.status_code}")
            # Fallback to a default user agent
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        else:
            # Get a random user agent from the list
            user_agents = user_agents_response.json()
            user_agent = random.choice(user_agents)
            
        print(f"Using user agent: {user_agent}")
        
        headers = {
            "user-agent": user_agent,
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br"
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
            return True
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    fetch_nse_holidays()

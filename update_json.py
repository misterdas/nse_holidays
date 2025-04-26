import requests
import json
import random
import time

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
        
        # Setup headers that mimic a real browser
        headers = {
            "user-agent": user_agent,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "sec-ch-ua": '"Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
        }

        # Create a session to maintain cookies
        session = requests.Session()
        
        # First visit the NSE homepage to get cookies
        print("Visiting NSE homepage to get cookies...")
        home_response = session.get("https://www.nseindia.com/", headers=headers, timeout=30)
        if home_response.status_code != 200:
            print(f"Failed to access NSE homepage: {home_response.status_code}")
            return False
            
        # Wait briefly to mimic human behavior
        time.sleep(2)
        
        # Add referer header for the API request (important)
        headers["referer"] = "https://www.nseindia.com/holidays/trading-holidays"
        
        # Then access the holidays page to get more cookies
        print("Visiting holidays page...")
        holidays_page = session.get("https://www.nseindia.com/holidays/trading-holidays", 
                                    headers=headers, timeout=30)
        if holidays_page.status_code != 200:
            print(f"Failed to access holidays page: {holidays_page.status_code}")
            return False
            
        # Wait briefly again
        time.sleep(2)
        
        # Now fetch the API data
        print(f"Fetching holiday data from API: {url}")
        response = session.get(url, headers=headers, timeout=30)
        
        # Debug information
        print(f"Response status code: {response.status_code}")
        
        # Ensure the response is successful and contains JSON
        if response.status_code == 200:
            try:
                holidays_data = response.json()
                
                # Save the response JSON directly to the file
                with open("nse_holidays.json", "w") as jsonFile:
                    json.dump(holidays_data, jsonFile, indent=4)
                
                print("NSE Holidays data has been updated successfully!")
                return True
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON response: {e}")
                # Save the raw response for debugging
                with open("nse_response.txt", "w") as file:
                    file.write(response.text)
                print("Raw response saved to nse_response.txt for debugging")
                return False
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            # Save the error response for debugging
            with open("nse_error.txt", "w") as file:
                file.write(response.text)
            print("Error response saved to nse_error.txt")
            return False
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

if __name__ == "__main__":
    fetch_nse_holidays()

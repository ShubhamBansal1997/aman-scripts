import time
import requests
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd


STATE_LIST = [
    {'State': 'Gujarat', 'Link': 'googlemap.php?state=Gujarat'},
    {'State': 'Goa', 'Link': 'googlemap.php?state=Goa'},
    {'State': 'Madhya Pradesh', 'Link': 'googlemap.php?state=Madhya Pradesh'},
    {'State': 'Maharashtra', 'Link': 'googlemap.php?state=Maharashtra'},
    {'State': 'Andhra Pradesh', 'Link': 'googlemap.php?state=Andhra Pradesh'},
    {'State': 'Karnataka', 'Link': 'googlemap.php?state=Karnataka'},
    {'State': 'kerala', 'Link': 'googlemap.php?state=kerala'},
    {'State': 'Tamilnadu', 'Link': 'googlemap.php?state=Tamilnadu'},
    {'State': 'Telangana', 'Link': 'googlemap.php?state=Telangana'},
]

def get_state_data(state):
    #state = urllib.parse.quote(state)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': '_gid=GA1.2.540648697.1719655067; PHPSESSID=v0al8574dl6qc3um67lmujdbb6; _ga=GA1.1.1244152040.1719655067; _ga_6ZWYPHEH1K=GS1.1.1719657075.2.0.1719657075.0.0.0',
        'Referer': 'https://www.mcdonaldsindia.com/convenience.html?v=5',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'state': state,
    }

    response = requests.get('https://www.mcdonaldsindia.com/googlemap.php', params=params, headers=headers)
    return response.text

def extract_location_data(html, state):
    soup = BeautifulSoup(html, 'html.parser')
    data = []

    # Find all locations
    for location in soup.find_all('li', class_='viewmap map_menu'):
        city = location.find_previous('h3').text.strip()
        contain = location['contain']
        lat = location['lat']
        long = location['long']

        # Parse the 'contain' attribute with BeautifulSoup
        contain_soup = BeautifulSoup(contain, 'html.parser')
        address_box = contain_soup.find('div', class_='addres_box')
        location_name = address_box.find('h1').text.strip()
        address = address_box.find('h2').text.strip()

        # Add the extracted data to the list
        data.append({
            'City': city,
            'Location': location_name,
            'Address': address,
            'Latitude': lat,
            'Longitude': long,
            'State': state,
        })

    return data

FINAL_DATA = []
def main():
    for state in STATE_LIST:
        html = get_state_data(state['State'])
        data = extract_location_data(html, state)
        print("Data in", state['State'], len(data), "locations")
        time.sleep(10)
        FINAL_DATA.extend(data)
    df = pd.DataFrame(FINAL_DATA)
    df['Address'] = df['Address'].str.replace('\n', ' ')
    df['Address'] = df['Address'].str.replace('\r', ' ')
    print(df)
    df.to_csv("/Users/shubham/Documents/aman-scripts/mcdonalds_locations.csv", index=False)

if __name__ == "__main__":
    main()
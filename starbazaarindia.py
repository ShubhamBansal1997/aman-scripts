# starbazaarindia.com/apps/s/storelocator
# This script will fetch all the store details of Star Bazaar India and save it in a CSV file.
import requests
from bs4 import BeautifulSoup
import pandas as pd

cities = [
    "Bangalore",
    "Hyderabad", 
    "Kolhapur",
    "Mumbai", 
    "Pune",  
    "Nashik",
]

def get_store_list(city):
    import requests

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://starbazaarindia.com',
        'priority': 'u=1, i',
        'referer': 'https://starbazaarindia.com/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    data = {
        'store_city': city,
    }

    response = requests.post(
        'https://shopifyapp.starbazaarindia.com/starbazaar/public/api/custom/getstore_name',
        headers=headers,
        data=data,
    )
    print("get_store_list: Response: ", response.status_code)
    data = response.json()
    site_ids = []
    print(data)
    return data['data']

def get_store_details(site_id):

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://starbazaarindia.com',
        'priority': 'u=1, i',
        'referer': 'https://starbazaarindia.com/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    data = {
        'store_name': site_id,
    }

    response = requests.post(
        'https://shopifyapp.starbazaarindia.com/starbazaar/public/api/custom/getstore_data',
        headers=headers,
        data=data,
    )
    print("get_store_details: Response: ", response.status_code)
    html_data = response.json()['data']
    return html_data

FINAL_DATA = []

def get_email(html_data):
    import re
    email = re.findall(r'[\w\.-]+@[\w\.-]+', html_data)
    return email[0] if len(email) > 0 else None

def get_phone(html_data):
    for a in html_data.find_all("a"):
        if "tel:" in a.get("href"):
            return a.get("href").replace("tel:", "")
    return None

def main():
    for city in cities:
        store_ids = get_store_list(city)
        for store_name, store_id in store_ids.items():
            print("store_id", store_id)
            store_details = get_store_details(store_id)
            root = BeautifulSoup(store_details, 'lxml')
            store_address = root.find_all("p", class_="address")[0].text
            store_email = get_email(root.find_all("a")[1].text)
            store_phone = get_phone(root)
            store_details = {
                "city": city,
                "store_address": store_address,
                "store_email": store_email,
                "store_phone": store_phone,
                "store_name": store_name
            }
            print(store_details)
            FINAL_DATA.append(store_details)
        df = pd.DataFrame(FINAL_DATA)
        df.to_csv("/Users/shubham/Documents/aman-scripts/star_bazaar_stores.csv", index=False)
    
if __name__ == "__main__":
    main()
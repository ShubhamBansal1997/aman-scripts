import requests

from bs4 import BeautifulSoup
import urllib.parse

STATES = {
    "Andhra Pradesh":"Andhra Pradesh",
    "Arunachal Pradesh":"Arunachal Pradesh",
    "Assam":"Assam",
    "Bihar":"Bihar",
    "Chandigarh":"Chandigarh",
    "Chhattisgarh":"Chhattisgarh",
    "Dadra And Nagar Haveli":"Dadra And Nagar Haveli",
    "Daman & Diu":"Daman & Diu",
    "Delhi":"Delhi",
    "Goa":"Goa",
    "Gujarat":"Gujarat",
    "Haryana":"Haryana",
    "Himachal Pradesh":"Himachal Pradesh",
    "Jammu And Kashmir":"Jammu And Kashmir",
    "Jharkhand":"Jharkhand",
    "Karnataka":"Karnataka",
    "Kerala":"Kerala",
    "Madhya Pradesh":"Madhya Pradesh",
    "Maharashtra":"Maharashtra",
    "Manipur":"Manipur",
    "Meghalaya":"Meghalaya",
    "Mizoram":"Mizoram",
    "Nagaland":"Nagaland",
    "Odisha":"Odisha",
    "Puducherry":"Puducherry",
    "Punjab":"Punjab",
    "Rajasthan":"Rajasthan",
    "Sikkim":"Sikkim",
    "Tamil Nadu":"Tamil Nadu",
    "Telangana":"Telangana",
    "Tripura":"Tripura",
    "Uttar Pradesh":"Uttar Pradesh",
    "Uttarakhand":"Uttarakhand",
    "West Bengal":"West Bengal",
}

def store_data(state, page):
    state = urllib.parse.quote(state)
    url = 'https://restaurants.pizzahut.co.in/{}'.format(state)
    print("Fetching data for ", url)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        # 'cookie': '_gcl_au=1.1.1352454967.1719647326; _fbp=fb.2.1719647326180.919826561259480831; _ga=GA1.1.344890649.1719647326; _d29=1719820127019; _ga_N6ZGSXEL7D=GS1.1.1719652038.2.1.1719652173.0.0.0',
        'priority': 'u=0, i',
        'referer': url,
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }
    if page != 1:
        params = {
            'page': '{}'.format(page),
        }
        response = requests.get(url, params=params, headers=headers)
    else:
        response = requests.get(url, headers=headers)
    return response.text

def extract_store_info(html_content, state_name):
    soup = BeautifulSoup(html_content, 'lxml')
    stores = soup.find_all('div', class_='store-info-box')
    stores_data = []
    for store in stores:
        latitude = store.find('input', class_='outlet-latitude')['value']
        longitude = store.find('input', class_='outlet-longitude')['value']
        phone_number = store.find('li', class_='outlet-phone').find('a')['href'].replace('tel:', '').strip()
        link = store.find('li', class_='outlet-name').find('a', {'title': 'Pizza Hut'})['href'].strip()
        address_parts = store.find('li', class_='outlet-address').find_all('span')
        address = ', '.join([part.text.strip() for part in address_parts if part.text.strip()])
        store_name = ""
        nearest_location = ""
        for li in store.find_all('li'):
            if li.find('span', class_='sprite-icon intro-icon icn-outlet'):
                store_name = li.find('div', class_='info-text').text
            if li.find('span', class_='sprite-icon intro-icon icn-landmark'):
                nearest_location = li.find('div', class_='info-text').text
        stores_data.append({
            'latitude': latitude,
            'longitude': longitude,
            'phone_number': phone_number,
            'link': link,
            'address': address,
            'store_name': store_name,
            'nearest_location': nearest_location,
            'state': state_name
        })
    return stores_data

FINAL_DATA = []

def main():
    for state_code, state_name in STATES.items():
        print("Fetching data for ", state_name)
        page = 1
        while True:
            print("Fetching data for ", state_name, page)
            response = store_data(state_code, page)
            if "Your search did not return any results. Please try advanced search." in response:
                print("No Results Found for ", state_name, page)
                break
            stores_data = extract_store_info(response, state_name)
            FINAL_DATA.extend(stores_data)
            page += 1
    print("Total Stores: ", len(FINAL_DATA))
    import pandas as pd
    df = pd.DataFrame(FINAL_DATA)
    df.to_csv("/Users/shubham/Documents/aman-scripts/pizza-hut.csv", index=False)
    
    
if __name__ == "__main__":
    main()
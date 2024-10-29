import requests
import pandas as pd

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Origin': 'https://www.westside.com',
    'Referer': 'https://www.westside.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

params = {
    'type': 'westside',
    'page': '2',
}
from bs4 import BeautifulSoup
FINAL_DATA = []
for page in range(1, 18):
    params['page'] = page
    response = requests.get('https://customapp.trent-tata.com/api/custom/getstore-all', params=params, headers=headers)
    data = response.json()
    soup = BeautifulSoup(data['data'], "lxml")
    store_details_divs = soup.find_all('div', class_='storedetails')
    for div in store_details_divs:
        store_name = div.find_all('h3')[0].text
        address = div.find_all('p')[0].text
        phone_no = div.find_all('p')[1].text
        store_link = div.find_all('a')[0].get('href')
        FINAL_DATA.append({
            'store_name': store_name,
            'address': address,
            'phone_no': phone_no,
            'store_link': store_link
        })
    print("Total records:", len(FINAL_DATA))

df = pd.Dataframe(FINAL_DATA)
df = df.drop_duplicates()
df.to_csv('/home/shubham/Downloads/westside.csv', index=False)

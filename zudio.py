import requests
import pandas as pd
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://www.zudio.com',
    'priority': 'u=1, i',
    'referer': 'https://www.zudio.com/',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

params = {
    'type': 'Zudio',
    'page': '3',
}
from bs4 import BeautifulSoup
FINAL_DATA = []
for page in range(1, 42):
    params['page'] = page
    response = requests.get('https://reports.trent-tata.com/api/custom/getstore-all', params=params, headers=headers)
    data = response.json()
    soup = BeautifulSoup(data['data'], "lxml")
    store_details_divs = soup.find_all('div', class_='storedetails')
    for div in store_details_divs:
        store_name = div.find_all('h3')[0].text
        address = div.find_all('p')[0].text
        store_link = div.find_all('a')[0].get('href')
        FINAL_DATA.append({
            'store_name': store_name,
            'address': address,
            'store_link': store_link
        })
    print("Total records:", len(FINAL_DATA))

df = pd.DataFrame(FINAL_DATA)
df['store_name'] = df['store_name'].apply(lambda x: x.replace('\n', ' '))
df['address'] = df['address'].apply(lambda x: x.replace('\n', ' '))
df['store_name'] = df['store_name'].apply(lambda x: x.strip())
df['address'] = df['address'].apply(lambda x: x.strip())
df['store_name'] = df['store_name'].apply(lambda x: " ".join(x.split()))
df['address'] = df['address'].apply(lambda x: " ".join(x.split()))
df.to_csv('/home/shubham/Downloads/zudio_complete.csv', index=False)
df = df.drop_duplicates()
df.to_csv('/home/shubham/Downloads/zudio.csv', index=False)

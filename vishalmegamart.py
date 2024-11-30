import requests
import pandas as pd

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': '_gcl_au=1.1.2085021004.1732958844; _fbp=fb.1.1732958843756.964562493160571009; _gid=GA1.2.315000050.1732958844; _clck=1mynvd8%7C2%7Cfrb%7C0%7C1795; __cq_uuid=abiaegaOicH4HvHb6uAhHMVCXq; __cq_seg=0~0.00!1~0.00!2~0.00!3~0.00!4~0.00!5~0.00!6~0.00!7~0.00!8~0.00!9~0.00; _clsk=ahu6u0%7C1732977976825%7C1%7C1%7Ci.clarity.ms%2Fcollect; _ga_KCFZ4D2YTF=GS1.1.1732977976.4.0.1732977986.50.0.0; _ga=GA1.2.1969795549.1732958844; _gat=1; XSRF-TOKEN=eyJpdiI6ImpCMDRwcTEyOE53TzJIRlFUM2kzSkE9PSIsInZhbHVlIjoieDF6STJ0QzBaREhFZjFEekJubGxKdHUxemZhWVBiVXo3QUdmUFB4eUY3NGFSWlErQ1hEdDJRU0FwRzQzSTNUYnA4bC9wa05rd3FWY2NFQ1VZaGVrdDRpb3RCMXVOWVJRTlRrWjNkMDFRdWtFNThQSkMyRHhmOUo0aytsUVdjR3MiLCJtYWMiOiI4OTNjZjc4ZGNmMmY0NjIwZTViMTU5YzVmNjdhN2RkODIzMmM0NjNiYTkzOGU4YThlOThhYTM5NmU0NmUwYzE2In0%3D; vishal_mega_mart_session=eyJpdiI6ImVPTFJyYmJ3T2RtSlJoNmg0MUcwSlE9PSIsInZhbHVlIjoiN01ZSE9nNFdJeVNHRGM5dTlSd3ZYRzB5SFNLSzViUzkyTGV5TXVBWGlJMzU5bW9wb1JZQ28rbDdybHNCaHIzQ0wyODJtcm94QXkwK2hMb3hDb0taK2xGRmlXNzJSeXhuTVhMT3Q5aXlacTVUREtKa2dBTlhqVWpDMWp1azdkWjkiLCJtYWMiOiI5ZTEwMmJmMzIzMzc3MmIwNzBlZWZiYjRmN2IxMTUxZjk2NDdjOTgzN2Y1NjVkNDg5YmM2N2I4YTA5ZjExY2RkIn0%3D; _ga_YCV8WTH1MC=GS1.2.1732977986.2.1.1732978036.10.0.1035291617',
    'priority': 'u=0, i',
    'referer': 'https://stores.vishalmegamart.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

params = {
    'page': '2',
}

from bs4 import BeautifulSoup
FINAL_DATA = []
for page in range(1, 26):
    params['page'] = page
    response = requests.get('https://stores.vishalmegamart.com/', params=params, headers=headers)
    data = response.text
    soup = BeautifulSoup(data, "lxml")
    store_details_divs = soup.find_all('div', class_='col-lg-4 col-md-6 p-0 my-3')
    for div in store_details_divs:
        card_header = div.find_all('div', class_='card-header idx-str-info-card-header d-flex justify-content-between mb-0 bg-color-3 rounded-0')[0]
        store_name = card_header.find_all('a', class_='col-store-name txt-color-3 txt-hover-1')[0].text
        store_linnk = card_header.find_all('a', class_='col-store-name txt-color-3 txt-hover-1')[0].get('href')
        store_locality = card_header.find_all('span', class_='mb-0 idx-str-locality')[0].text
        card_body = div.find_all('div', class_='card-body pt-3 px-3 pb-2')[0]
        store_phone_numbers = card_body.find_all('a', class_='txt-hover-1 txt-color-1')[0].text
        store_address = card_body.find_all('span', class_='store-address-info idx-info-card-str-add-info')[0].text
        print(store_name, store_linnk, store_locality, store_phone_numbers, store_address)
        FINAL_DATA.append({
            'store_name': store_name.strip(),
            'store_linnk': store_linnk.strip(),
            'store_locality': store_locality.strip(),
            'store_phone_numbers': store_phone_numbers.strip(),
            'store_address': store_address.strip()

        })
    print("Total records:", len(FINAL_DATA))

df = pd.DataFrame(FINAL_DATA)
df = df.drop_duplicates()
df.to_csv('/home/shubham/Documents/aman-scripts/vishalmegamart.csv', index=False)

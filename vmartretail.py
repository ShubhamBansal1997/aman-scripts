import requests
import pandas as pd

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': '_ga=GA1.2.852217642.1732959581; _gid=GA1.2.1567604116.1732959581; XSRF-TOKEN=eyJpdiI6IlBWRUFNSTRnS2JUNFJLVEU0RWlPQ1E9PSIsInZhbHVlIjoiSG5penR0VU41elhycDVQMGVtbGtNeGVKWTBoRmVWMXpFWmxqS2RSTnBNck81RVpURlJFckRPS1Z0Rjl5NE9WamFIRlNXOU1NQncydmgvRUNYT0hWWExpTy9OWU1odnJWck0zTE5xSVJZR1NJcERFRWRWbCtnNVJLbkZwSlI1aE4iLCJtYWMiOiI1YzBiNmIyMjAzYTdkYmMzMzdlYzkzZGRiN2U4NjhiZDdiODRkNzMxMmM0MmRmNDI3ZmMxZWYwZjQxNTA2MDRjIn0%3D; v_mart_retail_session=eyJpdiI6InlvbmFXalFxV0xkRkNkTU0vNDIyZGc9PSIsInZhbHVlIjoiQ1BkQjNoVS9NWG1RS2FQTEw1TGtuV1hGaU5aR1BrazR1UG1DK0FIQkNRWkszdUtRU0NlZ3pSUlNybkxuM0ZyTk15a1JvMW9DRkh1Q2dlTkg1Y1VKU2pybE5jN210NWtnM3FLNVFLNjZFN0xLWVhBREpOSlVUVGp5SXZSeW1HSmkiLCJtYWMiOiI5YjA3ZjNjZTY4ZDNiZTA4NjMxNTVkOWU0Y2Y0N2FjNTQ2NjczMzQ4NjFjNTQ1ODI1NmFmNjIzZDBiYzM2ZjczIn0%3D; _gat=1; _ga_G5DDHKY6QL=GS1.2.1732976143.3.0.1732976143.0.0.0',
    'priority': 'u=0, i',
    'referer': 'https://stores.vmartretail.com/?page=1',
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
    'page': '24',
}

from bs4 import BeautifulSoup
FINAL_DATA = []
for page in range(1, 24):
    params['page'] = page
    response = requests.get('https://stores.vmartretail.com/', params=params, headers=headers)
    data = response.text
    soup = BeautifulSoup(data, "lxml")
    store_details_divs = soup.find_all('div', class_='col-lg-4 col-md-6 col-12 p-0 my-3')
    for div in store_details_divs:
        card_header = div.find_all('div', class_='card-header idx-str-info-card-header mb-0 bg-color-3 rounded-0')[0]
        store_name = card_header.find_all('a', class_='col-store-name txt-color-3 txt-hover-1')[0].text
        store_linnk = card_header.find_all('a', class_='col-store-name txt-color-3 txt-hover-1')[0].get('href')
        store_locality = card_header.find_all('div', class_='mt-1 pl-2 idx-str-locality ml-n1')[0].text
        card_footer = div.find_all('div', class_='card-footer bg-color-4 info-card-footer p-0 border-0')[0]
        store_phone_numbers = card_footer.find_all('a', class_='redirect_website_click w-100 bdr-color-5 idx-info-card-str-web-btn text-uppercase')[0].text
        card_body = div.find_all('div', class_='card-body pt-3 px-3 pb-2')[0]
        store_address = card_body.find_all('span', class_='store-address-info idx-info-card-str-add-info')[0].text
        try:
            store_landmark = card_body.find_all('div', class_='nearby d-flex align-items-center mb-2')[0].text
        except Exception as e:
            store_landmark = ''
        print(store_name, store_linnk, store_locality, store_phone_numbers, store_address, store_landmark)
        FINAL_DATA.append({
            'store_name': store_name.strip(),
            'store_linnk': store_linnk.strip(),
            'store_locality': store_locality.strip(),
            'store_phone_numbers': store_phone_numbers.strip(),
            'store_address': store_address.strip(),
            'store_landmark': store_landmark.strip()

        })
    print("Total records:", len(FINAL_DATA))

df = pd.DataFrame(FINAL_DATA)
df = df.drop_duplicates()
df.to_csv('/home/shubham/Documents/aman-scripts/vmartretail.csv', index=False)

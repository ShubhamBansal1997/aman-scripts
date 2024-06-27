# stores.pantaloons.com
# This script will fetch all the store details of pantaloons and save it in a CSV file.
import requests
from bs4 import BeautifulSoup
import pandas as pd

OFFSET = 0
JUMP = 25

def get_store_list(offset):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'origin': 'https://stores.pantaloons.com',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    params = {
        'limit': '25',
        'offset': offset,
    }

    response = requests.get(
        'https://weblocationapi.dashloc.com/v1/branches-by-company/3694fdb9-e628-44a8-8a5a-6096303ae9c9/',
        params=params,
        headers=headers,
    )
    print("get_store_list: Response: ", response.status_code)
    data = response.json()
    return data["data"]["data"]


FINAL_DATA = []


def main():
    for i in range(0, 401, 25):
        store_details = get_store_list(i)
        FINAL_DATA.extend(store_details)
        print(len(store_details))
    df = pd.DataFrame(FINAL_DATA)
    df.to_csv("/Users/shubham/Documents/aman-scripts/pantaloons.csv", index=False)
    
if __name__ == "__main__":
    main()
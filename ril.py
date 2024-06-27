import pandas as pd
import requests
import urllib.parse


def get_store_data(lat, long, keys_to_extract=['datatype', 'id', 'kind', 'type', 'sections', 'latitude', 'longitude', 'isPickupAllowed', 'addressLines', 'city', 'stateCode', 'countryCode', 'zipCode', 'phones', 'stockThreshold', 'highProbabilityStockThreshold', 'country', 'state', 'isDonationAllow', 'isBeautyRecycling', 'isOnlyForEmployees', 'messages', 'radius', 'timezone', 'status', 'isShowable']):

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        # 'Cookie': '_gid=GA1.2.1381803042.1719420918; ASP.NET_SessionId=zfmv3ifhdo2s2qwxtbxqzllg; /=; /firsttimeload=0; /Retail.aspx=; /Retail.aspxfirsttimeload=0; TS01bc4783=0186a6c0de46dab3be614c034ed29f8e7e3ffd933596d2c92347bfc04e888a5020eb8f02631bfed4d7ba23264f684261a74cb7ef86; _gat_gtag_UA_58583947_1=1; _ga_1YWZ7P8MZ0=GS1.1.1719492142.5.0.1719492142.0.0.0; _ga=GA1.1.1115682037.1719420918',
        'Referer': 'https://storelocator.ril.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'flag': 'false',
        'Searchformat': 'All',
        'distance': '500',
        'latitude': lat,
        'longitude': long,
    }

    response = requests.get('https://storelocator.ril.com/getAllStores.aspx', params=params, headers=headers)
    print("Response: ", response.status_code)
    return response.text, response.status_code

def get_row_data(data, city, state):
    if data.strip() == "":
        return []
    storeInfo = data.split('$')
    data = []
    for store in storeInfo:
        if store.strip() == "":
            continue
        mstore = store.split('^')
        data.append({
            'title': urllib.parse.unquote(mstore[0]),
            'lat': urllib.parse.unquote(mstore[1]),
            'long': urllib.parse.unquote(mstore[2]),
            'icon': urllib.parse.unquote(mstore[3]),
            'storename': urllib.parse.unquote(mstore[4]),
            'address': urllib.parse.unquote(mstore[5]),
            'eid': urllib.parse.unquote(mstore[6]),
            'contactno': urllib.parse.unquote(mstore[7]),
            'storetime': urllib.parse.unquote(mstore[8]),
            'howtoreach': urllib.parse.unquote(mstore[9]),
            'shopfor': urllib.parse.unquote(mstore[10]),
            'random_field': urllib.parse.unquote(mstore[11]),
            'inourstore': urllib.parse.unquote(mstore[12]),
            'managername': urllib.parse.unquote(mstore[13]),
            'managerid': urllib.parse.unquote(mstore[14]),
            'storeimages': urllib.parse.unquote(mstore[15]),
            'state': state,
            'city': city
        })
    return data
        
        

FINAL_STORE_DATA = []
NUMBER = 94
def main():
    pincode_df = pd.read_csv("/Users/shubham/Downloads/IN/IN.txt", sep='\t', header=None)
    # clean duplicate entries with same lat long
    pincode_df = pincode_df.drop_duplicates(subset=[9, 10])
    for i, row in pincode_df.iterrows():
        if i > NUMBER:
            lat, long = row[9], row[10]
            print(lat, long)
            store_data, code = get_store_data(lat, long)
            if code == 404:
                print("Response not found")
                continue
            store_data = get_row_data(store_data, row[5], row[3])
            print("State", row[3], " City:", row[5], " i:", i, " Data", len(store_data))
            FINAL_STORE_DATA.extend(store_data)
    final_df = pd.DataFrame(FINAL_STORE_DATA)
    df_new = final_df.drop_duplicates()
    df_new.to_csv("/Users/shubham/Documents/aman-scripts/ril.csv", index=False)

import pandas as pd
import requests



def get_store_data(lat, long, keys_to_extract=['datatype', 'id', 'kind', 'type', 'sections', 'latitude', 'longitude', 'isPickupAllowed', 'addressLines', 'city', 'stateCode', 'countryCode', 'zipCode', 'phones', 'stockThreshold', 'highProbabilityStockThreshold', 'country', 'state', 'isDonationAllow', 'isBeautyRecycling', 'isOnlyForEmployees', 'messages', 'radius', 'timezone', 'status', 'isShowable']):

    headers = {
        'accept': 'application/json',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'device': 'desktop',
        'deviceid': '5786814-577-2f6-3f02-10c7ad76516',
        'devicetoken': 'a26786d145cc818fe52f6a0b9b23a289.1719424277',
        'devicetype': 'desktop',
        'env': 'PROD',
        'hash': 'e87dec47eca6d9072073db0229acf3a5',
        'origin': 'https://peterengland.abfrl.in',
        'priority': 'u=1, i',
        'referer': 'https://peterengland.abfrl.in/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sessionid': 'a26786d145cc818fe52f6a0b9b23a289',
        'shopid': '5',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    json_data = {
        'brand': 'pe',
        'customerId': 0,
        'cartId': 0,
        'fcmToken': '111',
        'version': '1.2',
        'validateHash': False,
        'geoLocation': {
            'latitude': 343,
            'longitude': 343,
        },
        'latitude': lat,
        'longitude': long,
        'deviceid': '5786814-577-2f6-3f02-10c7ad76516',
        'devicetoken': 'a26786d145cc818fe52f6a0b9b23a289.1719424277',
        'hash': '08af384545cf446dbcb17f4747653aec.131ad470493cb8731cf5b090cf5a4521',
        'sessionId': 'a26786d145cc818fe52f6a0b9b23a289',
        'utmSource': '',
        'searchWord': 'Delhi, India',
        'isStoreMode': 0,
        'pincode': '',
        'storeId': 0,
        'deviceId': '5786814-577-2f6-3f02-10c7ad76516',
        'deviceToken': 'a26786d145cc818fe52f6a0b9b23a289.1719424277',
    }

    response = requests.post('https://apigate.abfrl.in/location/store', headers=headers, json=json_data)
    print("Response: ", response.status_code)
    return response.json()['results']

FINAL_STORE_DATA = []

def main():
    pincode_df = pd.read_csv("/Users/shubham/Downloads/IN/IN.txt", sep='\t', header=None)
    # clean duplicate entries with same lat long
    pincode_df = pincode_df.drop_duplicates(subset=[9, 10])
    for i, row in pincode_df.iterrows():
        lat, long = row[9], row[10]
        store_data = get_store_data(lat, long)
        print("State", row[3], " City:", row[5], " i:", i, " Data", len(store_data))
        FINAL_STORE_DATA.extend(store_data)
    final_df = pd.DataFrame(FINAL_STORE_DATA)
    df_new = final_df.drop_duplicates(['id_store_locator', 'storeId'])
    df_new.to_csv("/Users/shubham/Documents/aman-scripts/peter-england.csv", index=False)

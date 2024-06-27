import pandas as pd
import requests
import sys
import time
import os

BRANDS = {
    "american-eagle": "aeo",
    "allensolly": "as",
    "forever-21": "f21",
    "louis-philippe": "lp",
    "reebok": "rbk",
    "simon-carter": "sc",
    "van-heusen": "vh"
}

BRANDS_WEBSITE = {
    "allensolly": "https://allensolly.abfrl.in",
    "american-eagle": "https://aeo.abfrl.in",
    "forever-21": "https://forever21.abfrl.in",
    "louis-philippe": "https://louisphilippe.abfrl.in",
    "reebok": "https://reebok.abfrl.in",
    "simon-carter": "https://simoncarter.abfrl.in",
    "van-heusen": "https://vanheusenindia.abfrl.in"
}

BRANDS_HASH = {
    "allensolly": "1097c3892595d74d9e3fc879a448025e",
    "american-eagle": "3e96fb10b298cadfa71aa09ae9f4411d",
    "forever-21": "f4d70fbdce804d4d693b4b6fa6539bc5",
    "louis-philippe": "12f0ca45acb1646d2fb9d0df87be8784",
    "reebok": "64e24cf2a05282a27302582f7552f838",
    "simon-carter": "a26786d145cc818fe52f6a0b9b23a289",
    "van-heusen": "a4c5688075b32c8f63e26ec876857070"
}

BRANDS_SHOPID = {
    "allensolly": "2",
    "american-eagle": "15",
    "forever-21": "16",
    "louis-philippe": "3",
    "reebok": "32",
    "simon-carter": "12",
    "van-heusen": "6"
}

STATES = [
    'Andaman & Nicobar Islands',
    'Andhra Pradesh',
    'Arunachal Pradesh',
    'Assam',
    'Bihar',
    'Chandigarh',
    'Chattisgarh',
    'Dadra and Nagar Haveli and Daman and Diu',
    'Delhi',
    'Goa',
    'Gujarat',
    'Haryana',
    'Himachal Pradesh',
    'Jammu & Kashmir',
    'Jharkhand',
    'Karnataka',
    'Kerala',
    'Lakshadweep',
    'Madhya Pradesh',
    'Maharashtra',
    'Manipur',
    'Meghalaya',
    'Mizoram',
    'Nagaland',
    'Odisha',
    'Pondicherry',
    'Punjab',
    'Rajasthan',
    'Sikkim',
    'Tamil Nadu',
    'Telangana',
    'Tripura',
    'Uttar Pradesh',
    'Uttarakhand',
    'West Bengal'
]

def get_store_data(lat, long, brand, brand_website, brand_hash, shop_id):

    headers = {
        'accept': 'application/json',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'device': 'desktop',
        'deviceid': '5786814-577-2f6-3f02-10c7ad76516',
        'devicetoken': 'a26786d145cc818fe52f6a0b9b23a289.1719424277',
        'devicetype': 'desktop',
        'env': 'PROD',
        'hash': brand_hash,
        'origin': brand_website,
        'priority': 'u=1, i',
        'referer': f'{brand_website}/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sessionid': 'a26786d145cc818fe52f6a0b9b23a289',
        'shopid': shop_id,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    json_data = {
        'brand': brand,
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

def main(state, brand):
    file_path = f"/Users/shubham/Documents/aman-scripts/{state}-{brand}.csv"
    if os.path.exists(file_path):
        print(f"File {file_path} already exists. Skipping")
        return
    brand_name = BRANDS[brand]
    brand_website = BRANDS_WEBSITE[brand]
    brand_hash = BRANDS_HASH[brand]
    shop_id = BRANDS_SHOPID[brand]
    print("Brand name:", brand_name, "Brand website:", brand_website, "Brand hash:", brand_hash, "Shop id:", shop_id)
    pincode_df = pd.read_csv("/Users/shubham/Downloads/IN/IN.txt", sep='\t', header=None)
    pincode_df = pincode_df[pincode_df[3] == state]
    # clean duplicate entries with same lat long
    pincode_df = pincode_df.drop_duplicates(subset=[9, 10])
    for i, row in pincode_df.iterrows():
        lat, long = row[9], row[10]
        store_data = get_store_data(lat, long, brand_name, brand_website, brand_hash, shop_id)
        if store_data is None:
            print("Sleeping for 1 sec as no data found in API")
            time.sleep(3)
            store_data = get_store_data(lat, long, brand_name, brand_website, brand_hash, shop_id)
        print("State", row[3], " City:", row[5], " i:", i, " Data", len(store_data), "Brand name:", brand_name, "Brand website:", brand_website)
        FINAL_STORE_DATA.extend(store_data)
    final_df = pd.DataFrame(FINAL_STORE_DATA)
    df_new = final_df.drop_duplicates(['id_store_locator', 'storeId', 'address'])
    df_new.to_csv(f"/Users/shubham/Documents/aman-scripts/{state}-{brand}.csv", index=False)

for k, v in BRANDS.items():
    FINAL_STORE_DATA = []
    main(STATES[35], k)


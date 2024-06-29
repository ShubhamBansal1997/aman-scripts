import json
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

STATE_LIST = {
    '1': 'Andaman And Nicobar Islands',
    '2': 'Andhra Pradesh',
    '3': 'Arunachal Pradesh',
    '4': 'Assam',
    '5': 'Bihar',
    '7': 'Chandigarh',
    '8': 'Daman And Diu',
    '9': 'Delhi',
    '10': 'Dadra And Nagar Haveli',
    '11': 'Goa',
    '13': 'Himachal Pradesh',
    '14': 'Haryana',
    '15': 'Jammu And Kashmir',
    '16': 'Jharkhand',
    '17': 'Kerala',
    '18': 'Karnataka',
    '19': 'Lakshadweep',
    '20': 'Meghalaya',
    '21': 'Maharashtra',
    '22': 'Manipur',
    '23': 'Madhya Pradesh',
    '24': 'Mizoram',
    '25': 'Nagaland',
    '26': 'Orissa',
    '27': 'Punjab',
    '28': 'Pondicherry',
    '29': 'Rajasthan',
    '30': 'Sikkim',
    '31': 'Tamil Nadu',
    '32': 'Tripura',
    '33': 'Uttarakhand',
    '34': 'Uttar Pradesh',
    '35': 'West Bengal',
    '36': 'Telangana',
    '37': 'Gujarat',
    '41': 'Chhattisgarh'
}

CITY_LIST = [{'city_id': 11, 'state_id': 2, 'city_name': 'Hyderabad', 'state': 'Andhra Pradesh'}, {'city_id': 53, 'state_id': 2, 'city_name': 'Vijayawada', 'state': 'Andhra Pradesh'}, {'city_id': 80, 'state_id': 2, 'city_name': 'Visakhapatnam', 'state': 'Andhra Pradesh'}, {'city_id': 59, 'state_id': 7, 'city_name': 'Chandigarh', 'state': 'Chandigarh'}, {'city_id': 9, 'state_id': 9, 'city_name': 'Delhi', 'state': 'Delhi'}, {'city_id': 61, 'state_id': 11, 'city_name': 'Goa', 'state': 'Goa'}, {'city_id': 55, 'state_id': 14, 'city_name': 'Ambala', 'state': 'Haryana'}, {'city_id': 20, 'state_id': 14, 'city_name': 'Karnal', 'state': 'Haryana'}, {'city_id': 15, 'state_id': 14, 'city_name': 'Panchkula', 'state': 'Haryana'}, {'city_id': 21, 'state_id': 14, 'city_name': 'Sonipat', 'state': 'Haryana'}, {'city_id': 12, 'state_id': 17, 'city_name': 'Cochin', 'state': 'Kerala'}, {'city_id': 37, 'state_id': 17, 'city_name': 'Kannur', 'state': 'Kerala'}, {'city_id': 3, 'state_id': 17, 'city_name': 'Kochin', 'state': 'Kerala'}, {'city_id': 78, 'state_id': 17, 'city_name': 'Trissur', 'state': 'Kerala'}, {'city_id': 42, 'state_id': 17, 'city_name': 'Trivandrum', 'state': 'Kerala'}, {'city_id': 13, 'state_id': 18, 'city_name': 'Bangalore', 'state': 'Karnataka'}, {'city_id': 39, 'state_id': 18, 'city_name': 'Mangalore', 'state': 'Karnataka'}, {'city_id': 68, 'state_id': 18, 'city_name': 'Manipal', 'state': 'Karnataka'}, {'city_id': 70, 'state_id': 18, 'city_name': 'Mysore', 'state': 'Karnataka'}, {'city_id': 56, 'state_id': 21, 'city_name': 'Aurangabad', 'state': 'Maharashtra'}, {'city_id': 34, 'state_id': 21, 'city_name': 'Kalyan', 'state': 'Maharashtra'}, {'city_id': 1, 'state_id': 21, 'city_name': 'Mumbai', 'state': 'Maharashtra'}, {'city_id': 27, 'state_id': 21, 'city_name': 'Nagpur', 'state': 'Maharashtra'}, {'city_id': 33, 'state_id': 21, 'city_name': 'Nasik', 'state': 'Maharashtra'}, {'city_id': 2, 'state_id': 21, 'city_name': 'Pune', 'state': 'Maharashtra'}, {'city_id': 48, 'state_id': 21, 'city_name': 'Raigad', 'state': 'Maharashtra'}, {'city_id': 46, 'state_id': 21, 'city_name': 'Thane', 'state': 'Maharashtra'}, {'city_id': 50, 'state_id': 23, 'city_name': 'Bhopal', 'state': 'Madhya Pradesh'}, {'city_id': 58, 'state_id': 23, 'city_name': 'Bilaspur', 'state': 'Madhya Pradesh'}, {'city_id': 63, 'state_id': 23, 'city_name': 'Gwalior', 'state': 'Madhya Pradesh'}, {'city_id': 49, 'state_id': 23, 'city_name': 'Indore', 'state': 'Madhya Pradesh'}, {'city_id': 18, 'state_id': 27, 'city_name': 'Amritsar', 'state': 'Punjab'}, {'city_id': 19, 'state_id': 27, 'city_name': 'Bhatinda', 'state': 'Punjab'}, {'city_id': 65, 'state_id': 27, 'city_name': 'Hoshiarpur', 'state': 'Punjab'}, {'city_id': 16, 'state_id': 27, 'city_name': 'Jalandhar', 'state': 'Punjab'}, {'city_id': 17, 'state_id': 27, 'city_name': 'Ludhiana', 'state': 'Punjab'}, {'city_id': 69, 'state_id': 27, 'city_name': 'Mohali', 'state': 'Punjab'}, {'city_id': 32, 'state_id': 27, 'city_name': 'Patiala', 'state': 'Punjab'}, {'city_id': 72, 'state_id': 27, 'city_name': 'Rajpura', 'state': 'Punjab'}, {'city_id': 73, 'state_id': 27, 'city_name': 'Rupnagar', 'state': 'Punjab'}, {'city_id': 40, 'state_id': 28, 'city_name': 'Puducherry', 'state': 'Pondicherry'}, {'city_id': 4, 'state_id': 31, 'city_name': 'Chennai', 'state': 'Tamil Nadu'}, {'city_id': 60, 'state_id': 31, 'city_name': 'Coimbatore', 'state': 'Tamil Nadu'}, {'city_id': 67, 'state_id': 31, 'city_name': 'Madurai', 'state': 'Tamil Nadu'}, {'city_id': 82, 'state_id': 31, 'city_name': 'Nagarcoil', 'state': 'Tamil Nadu'}, {'city_id': 83, 'state_id': 31, 'city_name': 'Pondicherry', 'state': 'Tamil Nadu'}, {'city_id': 5, 'state_id': 31, 'city_name': 'Tanjore', 'state': 'Tamil Nadu'}, {'city_id': 74, 'state_id': 31, 'city_name': 'Thanjavur', 'state': 'Tamil Nadu'}, {'city_id': 81, 'state_id': 31, 'city_name': 'Tiruchirapalli', 'state': 'Tamil Nadu'}, {'city_id': 76, 'state_id': 31, 'city_name': 'Tirunelveli', 'state': 'Tamil Nadu'}, {'city_id': 6, 'state_id': 31, 'city_name': 'Trichy', 'state': 'Tamil Nadu'}, {'city_id': 77, 'state_id': 31, 'city_name': 'Trichy', 'state': 'Tamil Nadu'}, {'city_id': 29, 'state_id': 31, 'city_name': 'Vellore', 'state': 'Tamil Nadu'}, {'city_id': 35, 'state_id': 33, 'city_name': 'Dehradun', 'state': 'Uttarakhand'}, {'city_id': 22, 'state_id': 33, 'city_name': 'Haldwani', 'state': 'Uttarakhand'}, {'city_id': 64, 'state_id': 33, 'city_name': 'Haridwar', 'state': 'Uttarakhand'}, {'city_id': 23, 'state_id': 33, 'city_name': 'Rudrapur', 'state': 'Uttarakhand'}, {'city_id': 24, 'state_id': 34, 'city_name': 'Across UP', 'state': 'Uttar Pradesh'}, {'city_id': 25, 'state_id': 34, 'city_name': 'Allahabad', 'state': 'Uttar Pradesh'}, {'city_id': 57, 'state_id': 34, 'city_name': 'Bareilly', 'state': 'Uttar Pradesh'}, {'city_id': 62, 'state_id': 34, 'city_name': 'Gorakhpur', 'state': 'Uttar Pradesh'}, {'city_id': 28, 'state_id': 34, 'city_name': 'Kanpur', 'state': 'Uttar Pradesh'}, {'city_id': 36, 'state_id': 34, 'city_name': 'Khatauli', 'state': 'Uttar Pradesh'}, {'city_id': 66, 'state_id': 34, 'city_name': 'Khautali', 'state': 'Uttar Pradesh'}, {'city_id': 31, 'state_id': 34, 'city_name': 'Moradabad', 'state': 'Uttar Pradesh'}, {'city_id': 54, 'state_id': 36, 'city_name': 'Secunderabad', 'state': 'Telangana'}, {'city_id': 10, 'state_id': 37, 'city_name': 'Ahmedabad', 'state': 'Gujarat'}, {'city_id': 43, 'state_id': 37, 'city_name': 'Anand', 'state': 'Gujarat'}, {'city_id': 51, 'state_id': 37, 'city_name': 'Bhavnagar', 'state': 'Gujarat'}, {'city_id': 41, 'state_id': 37, 'city_name': 'Gandhinagar', 'state': 'Gujarat'}, {'city_id': 44, 'state_id': 37, 'city_name': 'Rajkot', 'state': 'Gujarat'}, {'city_id': 26, 'state_id': 37, 'city_name': 'Surat', 'state': 'Gujarat'}, {'city_id': 30, 'state_id': 37, 'city_name': 'Vadodara', 'state': 'Gujarat'}, {'city_id': 45, 'state_id': 37, 'city_name': 'Vapi', 'state': 'Gujarat'}, {'city_id': 14, 'state_id': 41, 'city_name': 'Bhillai', 'state': 'Chhattisgarh'}, {'city_id': 71, 'state_id': 41, 'city_name': 'Raipur', 'state': 'Chhattisgarh'}]

def get_city_data(city_id):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_gid=GA1.2.1045076704.1719647653; _fbp=fb.1.1719647653342.730442521827278557; _I_=8a3373a4c29a120ffc0f78eee509a040fec901903bb566b1dfb2512100ee422e-1719658339; october_session=eyJpdiI6IkFaV3J5WHdDM3l5bWR6T3UwMHEzc0E9PSIsInZhbHVlIjoiQzVNSlZiaWRhSkIzdGRJbmxlWjVpZjlPMEJkdFFkZ2N2dVVSNncwb0RENzNsbFdzdEw3RnROK01sWEtmc3gzbUlQdDJQYU1tc0VNR1F5RlRjeDJEc3c9PSIsIm1hYyI6IjA0NDAzNzQ0N2Y3M2YyMGIzMmM2ZjYyMzk0ODA4MGNlMzMyNWRlNDg1ZDc0ZjVkZjg3ZTE4ZjQ1ZTI5MDY1ODEifQ%3D%3D; _ga_M8T7VKK5S6=GS1.1.1719663275.3.1.1719663278.0.0.0; _ga=GA1.1.1136351101.1719647653',
        'origin': 'https://www.sapphirefoods.in',
        'priority': 'u=1, i',
        'referer': 'https://www.sapphirefoods.in/store-locator/pizza-hut',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'x-october-request-handler': 'onFilterRole',
        'x-october-request-partials': 'storelist',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'city_id': f'{city_id}',
        'brand': 'pizza-hut',
    }
    try:
        response = requests.post('https://www.sapphirefoods.in/store-locator/kfc', headers=headers, data=data, verify=False, timeout=10)
    except:
        print("Request timeout")
        return get_city_data(city_id)
    return response.json()['storelist']

FINAL_DATA = []

def main():
    for city in CITY_LIST:
        time.sleep(3)
        print("Sleeping for 10 seconds")
        print("Fetching data for ", city['city_name'], city['state'], city['city_id'])
        city_data = get_city_data(city['city_id'])
        soup = BeautifulSoup(city_data, "lxml")
        city_data_all = json.loads(soup.find(id='lat_lang')['value'])
        print("Data fetched for ", len(city_data_all))
        for store in city_data_all:
            store['city'] = city['city_name']
            store['state'] = city['state']
        FINAL_DATA.extend(city_data_all)
    df = pd.DataFrame(FINAL_DATA)
    df.to_csv('/Users/shubham/Documents/aman-scripts/sapphire-pizza-hut.csv', index=False)

if __name__ == '__main__':
    main()
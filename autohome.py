from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
from dateutil.parser import parse
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import json
import sys
from datetime import datetime
import os
import pandas as pd

from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service as ChromeService



def open_page_with_retries(url, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            driver.get(url)
            # Wait for a specific element to be present to ensure the page is loaded
            print(f"Page loaded successfully on attempt {attempt + 1}")
            return True
        except (TimeoutException, WebDriverException) as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            attempt += 1
            time.sleep(10)
    print(f"Failed to load the page after {retries} attempts")
    return False


def brand_page_links():
    brand_links = []
    cartree = driver.find_element(By.ID, 'cartree')
    ul_elements = cartree.find_elements(By.TAG_NAME, 'ul')
    for ul in ul_elements:
        li_elements = ul.find_elements(By.TAG_NAME, 'li')
        for li in li_elements:
            a_link = li.find_element(By.TAG_NAME, 'a')
            brand_name = a_link.text
            brand_link = a_link.get_attribute('href')
            brand_links.append({'brand_name': brand_name, 'brand_link': brand_link})
    print("brand_links: ", len(brand_links))
    return brand_links

# ALLOWED_BRAND_LINKS = [
#     "阿斯顿·马丁","阿维塔","埃安","奥迪","宝马","保时捷","北京","北京汽车","北汽新能源","奔驰","本田","比亚迪","标致","别克","长安","长安凯程","长安跨越","长安欧尚","长安启源","长城","大众","东风风度","东风风光","东风风神","东风风行","东风富康","东风纳米","东风小康","东风奕派","东风御风","东南","法拉利","方程豹","飞凡汽车","菲亚特","丰田","福特","广汽传祺","广汽集团","哈弗","昊铂","合创汽车","红旗","鸿蒙智行","iCAR","ARCFOX极狐","Jeep","Polestar极星","吉利几何","吉利汽车","吉利银河","吉祥汽车","极氪","极石","极越","江淮汽车","江淮瑞风","凯迪拉克","凯翼","兰博基尼","岚图汽车","蓝电","乐道","雷克萨斯","理想汽车","力帆汽车","零跑汽车","领克","路虎","MINI","马自达","玛莎拉蒂","迈巴赫","名爵","哪吒汽车","讴歌","欧拉","奇瑞","奇瑞新能源","启辰","起亚","日产","荣威","瑞驰新能源","SERES赛力斯","smart","上汽大通MAXUS","深蓝汽车","思皓","斯巴鲁","斯柯达","坦克","特斯拉","腾势","蔚来","魏牌","沃尔沃","五菱汽车","现代","小米汽车","小鹏","雪佛兰","雪铁龙","仰望","烨","一汽","英菲尼迪"
# ]

ALLOWED_BRAND_LINKS = [
    "阿斯顿·马丁",
    "阿维塔"
]

def generate_brand_tab_link(brand_page_links):
    in_stock = '在售' # /price/brand-70.html
    coming_soon = '即将销售' # /price/brand-70-0-2-1.html
    discontinued = '停售' # /price/brand-70-0-3-1.html
    brand_tab_links = []
    for brand in brand_page_links:
        brand_link = brand['brand_link']
        brand_name = brand['brand_name']
        base_link = brand_link.split('.html')[0]
        in_stock_link = f"{base_link}.html"
        coming_soon_link = f"{base_link}-0-2-1.html"
        discontinued_link = f"{base_link}-0-3-1.html"
        brand_links = [{
            'brand_name': brand_name,
            'status': in_stock,
            'link': in_stock_link
        }, {
            'brand_name': brand_name,
            'status': coming_soon,
            'link': coming_soon_link
        }, {
            'brand_name': brand_name,
            'status': discontinued,
            'link': discontinued_link
        }]
        brand_tab_links.extend(brand_links)
    print("Brand Tab Links: ", len(brand_tab_links))
    return brand_tab_links


def get_individual_car_page_links(status, brand_name, brand_link):
    main_div_element = driver.find_element(By.CSS_SELECTOR, '.tab-content.fn-visible')
    list_elements = main_div_element.find_elements(By.CLASS_NAME, 'list-cont')
    car_links = []
    for list_element in list_elements:
        main_title = list_element.find_element(By.CLASS_NAME, 'main-title')
        a_element = main_title.find_elements(By.TAG_NAME, 'a')
        car_name = a_element[0].text
        car_link = a_element[0].get_attribute('href')
        car_links.append({'car_name': car_name, 'car_link': car_link, 'brand_name': brand_name, 'status': status, 'brand_link': brand_link})
    print(f"Brand Name: {brand_name}, Status: {status}, Total Cars: {len(car_links)}, Car Links: {car_links}")
    return car_links

def extra_page_links(base_link):
    extra_links = []
    try:
        base_link = base_link.split('.html')[0]
        pagination = driver.find_element(By.CLASS_NAME, 'price-page')
        a_elements = pagination.find_elements(By.TAG_NAME, 'a')
        for a in a_elements:
            link = a.get_attribute('href')
            if link and link.startswith(base_link):
                extra_links.append(link)
        print(f"Total Extra Links: {len(extra_links)}")
    except NoSuchElementException:
        pass
    return extra_links

def process_brand_tab_links(brand_tab_links):
    car_links = []
    for brand_tab in brand_tab_links:
        driver.get(brand_tab['link'])
        car_links.extend(get_individual_car_page_links(brand_tab['status'], brand_tab['brand_name'], brand_tab['link']))
        extra_links = extra_page_links(brand_tab['link'])
        for extra_link in extra_links:
            driver.get(extra_link)
            car_links.extend(get_individual_car_page_links(brand_tab['status'], brand_tab['brand_name'], brand_tab['link']))
    print("Total Car Links: ", len(car_links))
    return car_links


def check_if_a_valid_brand_name(brand_name):
    for brand in ALLOWED_BRAND_LINKS:
        if brand in brand_name:
            return True
    return False


def get_car_links():
    brand_links = brand_page_links()
    print("Total Brand Links: ", len(brand_links))
    filtered_brand_links = []
    for brand_link in brand_links:
        if not check_if_a_valid_brand_name(brand_link['brand_name']):
            continue
        filtered_brand_links.append(brand_link)
    print("Filtered Brand Links: ", len(filtered_brand_links))
    brand_tab_links = generate_brand_tab_link(filtered_brand_links)
    car_links = process_brand_tab_links(brand_tab_links)
    print("Total Car Links: ", len(car_links))
    print("Car Links: ", car_links)
    unique_car_links = list({v['car_link']:v for v in car_links}.values())
    print("Unique Car Links: ", len(unique_car_links))
    return unique_car_links

def get_car_info(car_link, car_name):
    car_info = {}
    car_info['car_detail_name'] = 'N/A'
    car_info['tag_price'] = 'N/A'
    car_info['transaction_price'] = 'N/A'
    car_info['oem_name'] = 'N/A'
    link = car_link.split('#')[0]
    print("Fetching Link: ", link)
    if not open_page_with_retries(link, retries=5):
        raise Exception("Failed to open the page")
    car_names = driver.find_elements(By.CLASS_NAME, 'athm-sub-nav__car__name')
    if len(car_names) > 0:
        oem_car_name = car_names[0].find_element(By.TAG_NAME, 'a').text
        entries = oem_car_name.split('-')
        if len(entries) != 2:
            raise Exception(f"Invalid Car Name: {oem_car_name}")
        brand_name = ''
        if oem_car_name.endswith(car_name):
            brand_name = oem_car_name[:len(oem_car_name)-len(car_name)-1].strip()
        car_info['car_detail_name'] = car_name.strip()
        car_info['oem_name'] = brand_name.strip()
    price = driver.find_elements(By.CLASS_NAME, 'emphasis')
    if len(price) > 0:
        car_info['tag_price'] = price[0].text
    sale_price = driver.find_elements(By.CLASS_NAME, 'price-sale')
    if len(sale_price) > 0:
        for s in sale_price:
            if link in s.get_attribute('href'):
                car_info['transaction_price'] = s.text
    print("Car Info: ", car_info)
    return car_info


def process_car_links():
    car_links = get_car_links()
    print("Total Car Links: ", len(car_links))
    for car_link in car_links:
        car_info = get_car_info(car_link['car_link'], car_link['car_name'])
        car_link.update(car_info)
    return car_links



if __name__ == '__main__':
    oem_names = input("Enter OEM names (comma separated): ").split(",")
    filtered_data = [oem_name.strip() for oem_name in oem_names]
    print("OEM names: ", filtered_data)
    ALLOWED_BRAND_LINKS = filtered_data
    driver = webdriver.Chrome()
    try:
        #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get("https://car.autohome.com.cn/price/brand-3-0-3-1.html")
        FINAL_DATA = process_car_links()
        df = pd.DataFrame(FINAL_DATA)
        df.to_csv("/Users/shubham/Documents/aman-scripts/autohome_filtered.csv", index=False)
        print("df", df)
    except Exception as e:
        print("Error: ", e)
    finally:
        driver.close()
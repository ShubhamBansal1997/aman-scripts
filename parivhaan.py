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

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service as ChromeService

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml")



STATE_IDS = {
    "Andaman & Nicobar Island(8)": "j_idt38_1",
    "Andhra Pradesh(80)": "j_idt38_2",
    "Arunachal Pradesh(27)": "j_idt38_3",
    "Assam(36)": "j_idt38_4",
    "Bihar(49)": "j_idt38_5",
    "Chhattisgarh(30)": "j_idt38_6",
    "Chandigarh(1)": "j_idt38_7",
    "UT of DNH and DD(3)": "j_idt38_8",
    "Delhi(23)": "j_idt38_9",
    "Goa(13)": "j_idt38_10",
    "Gujarat(37)": "j_idt38_11",
    "Himachal Pradesh(113)": "j_idt38_12",
    "Haryana(178)": "j_idt38_13",
    "Jharkhand(31)": "j_idt38_14",
    "Jammu and Kashmir(21)": "j_idt38_15",
    "Karnataka(68)": "j_idt38_16",
    "Kerala(87)": "j_idt38_17",
    "Ladakh(3)": "j_idt38_18",
    "Maharashtra(56)": "j_idt38_19",
    "Meghalaya(13)": "j_idt38_20",
    "Manipur(12)": "j_idt38_21",
    "Madhya Pradesh(53)": "j_idt38_22",
    "Mizoram(10)": "j_idt38_23",
    "Nagaland(9)": "j_idt38_24",
    "Odisha(39)": "j_idt38_25",
    "Punjab(95)": "j_idt38_26",
    "Puducherry(8)": "j_idt38_27",
    "Rajasthan(142)": "j_idt38_28",
    "Sikkim(9)": "j_idt38_29",
    "Tamil Nadu(148)": "j_idt38_30",
    "Tripura(9)": "j_idt38_31",
    "Uttarakhand(21)": "j_idt38_32",
    "Uttar Pradesh(78)": "j_idt38_33",
    "West Bengal(56)": "j_idt38_34"
}

VECHICLE_IDS = {
    "TWO WHEELER": "vchgroupTable:selectCatgGrp_0",
    "THREE WHEELER": "vchgroupTable:selectCatgGrp_1",
    "FOUR WHEELER": "vchgroupTable:selectCatgGrp_2",
    "AMBULANCE/HEARSES": "vchgroupTable:selectCatgGrp_3",
    "CONSTRUCTION EQUIPMENT VEHICLE": "vchgroupTable:selectCatgGrp_4",
    "GOODS VEHICLES": "vchgroupTable:selectCatgGrp_5",
    "PUBLIC SERVICE VEHICLE": "vchgroupTable:selectCatgGrp_6",
    "SPECIAL CATEGORY VEHICLES": "vchgroupTable:selectCatgGrp_7",
    "TRAILER": "vchgroupTable:selectCatgGrp_8",
    "TRACTOR": "vchgroupTable:selectCatgGrp_9"
}

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.get("https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml")


def changing_state(state):
    # opening state drop down
    drop_down = driver.find_element(By.ID, 'j_idt38')
    state_id = STATE_IDS[state]
    drop_down.click()
    print("State ID: ", state_id)
    time.sleep(5)
    drop_down = driver.find_element(By.ID, state_id)
    drop_down.click()


def changing_category(category):
    # opening category drop down
    drop_down = driver.find_element(By.ID, 'vchgroupTable:selectCatgGrp')
    category_id = VECHICLE_IDS[category]
    drop_down.click()
    print("Category ID: ", category_id)
    time.sleep(5)
    drop_down = driver.find_element(By.ID, category_id)
    drop_down.click()

def get_body_data():
     table_data = []
     tbody = driver.find_element(By.ID, 'vchgroupTable_data')
     tr_elements = tbody.find_elements(By.TAG_NAME, 'tr')
     for tr in tr_elements:
          td_elements = tr.find_elements(By.TAG_NAME, 'td')
          row_data = [td.text for td in td_elements]
          table_data.append(row_data)
     return table_data

def get_table_headers():
     table_headers = []
     thead = driver.find_element(By.ID, 'vchgroupTable_head')
     tr_elements = thead.find_elements(By.TAG_NAME, 'tr')[-1]
     th_elements = tr_elements.find_elements(By.TAG_NAME, 'th')
     for th in th_elements:
          if not th.text.strip():
               continue
          table_headers.append(th.text.strip())
     table_headers = ['S.No.', 'Vehicle Class'] + table_headers
     return table_headers

for state in STATE_IDS:
     print("State: ", state)
     changing_state(state)
     for category in VECHICLE_IDS:
          if os.path.exists(f"/Users/shubham/Documents/aman-scripts/parivhaan/{STATE_IDS[state]}--{VECHICLE_IDS[category]}.csv"):
               continue
          print("Category: ", category)
          changing_category(category)
          time.sleep(10)
          table_data = get_body_data()
          table_headers = get_table_headers()
          print(table_headers)
          print(table_data)
          if len(table_data[0]) == 1 and table_data[0][0] == "No records found.":
               continue
          df = pd.DataFrame(table_data, columns=table_headers)
          df.to_csv(f"/Users/shubham/Documents/aman-scripts/parivhaan/{STATE_IDS[state]}--{VECHICLE_IDS[category]}.csv", index=False)


driver.close()

FINAL_DATA = []
for state, state_id in STATE_IDS.items():
     print("State: ", state)
     for category, category_id in VECHICLE_IDS.items():
          if os.path.exists(f"/Users/shubham/Documents/aman-scripts/parivhaan/{state_id}--{category_id}.csv"):
               df = pd.read_csv(f"/Users/shubham/Documents/aman-scripts/parivhaan/{state_id}--{category_id}.csv")
               columns = list(df.columns)
               melted_df = df.melt(id_vars=columns[1], value_vars=columns[2:], var_name="Vehicle Category Group", value_name="Count")
               melted_df = melted_df.sort_values(by=["Vehicle Class"])
               melted_df["State"] = state
               melted_df["Vehicle Category"] = category
               FINAL_DATA.extend(melted_df.to_dict("records"))
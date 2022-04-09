from tqdm import tqdm
from tkinter import N
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from os import rename
import pandas as pd

dz = pd.read_excel("assets/DataZone/HBW-BirdLife_List_of_Birds_v6.xlsx")
# dz.head(5)
list_of_birds = list(dz.loc[:,'Common name'])
options = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "C:\\Users\\LEGION\\Documents\\birds\\assets\\AviBase"}
options.add_experimental_option("prefs",prefs);
path = './chromedriver'
driver = webdriver.Chrome(path,options=options);
fail = []
csvList = pd.DataFrame(columns=['Bird Name','Data set name'])
try:
    for birdname in list_of_birds[5000:7500]:
        try:
            driver.get('https://avibase.bsc-eoc.org/search.jsp?lang=EN&isadv=yes')
            input_avibase = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[placeholder='Enter a species name']")))
            input_avibase.send_keys(birdname)
            input_avibase.send_keys(Keys.ENTER)
            sleep(0.5)
            driver.find_elements(by=By.XPATH, value='//*[@id="avbform"]/table/tbody/tr[2]/td[3]/a')[0].click()
            sleep(0.5)
            link = driver.find_elements(by=By.XPATH, value='/html/body/div[1]/div[4]/div/div/div[1]/ul/li[5]/a')[0].click()
            driver.find_element(by=By.LINK_TEXT, value="CSV").click()
            sleep(1)
            birddatafilename = f"{'-'.join(birdname.split(' '))}-lifehistory.csv"
            rename("C:\\Users\\LEGION\\Documents\\birds\\assets\\AviBase\\lifehistory.csv",f"C:\\Users\\LEGION\\Documents\\birds\\assets\\AviBase\\{birddatafilename}")
            # bird_data_csvs[birdname] = [birddatafilename]
            d = {'Bird Name':[birdname],'Data set name':[birddatafilename]}
            csvList = pd.concat([csvList,pd.DataFrame(d)])
            # print('+',list_of_birds.index(birdname),birdname)
        except Exception:
            fail.append(birdname)
            # print(fail)
except Exception:
    print('UN Ex')
finally:
    driver.close()
    pd.DataFrame(fail).to_pickle('C:\\Users\\LEGION\\Documents\\birds\\assets\\AviBase\\AviBase-Scrape-Report-2500-end-fail.pkl')
    # pd.read_pickle('C:\\Users\\LEGION\\Documents\\birds\\assets\\AviBase\\AviBase-Scrape-Report-fail.pkl')
    pd.DataFrame.from_dict(csvList).to_pickle('C:\\Users\\LEGION\\Documents\\birds\\assets\\AviBase\\AviBase-Scrape-Report-2500-end.pkl')
    list_of_csvs = pd.read_pickle('C:\\Users\\LEGION\\Documents\\birds\\assets\\AviBase\\AviBase-Scrape-Report-2500-end.pkl')
    list_of_csvs.tail(5)
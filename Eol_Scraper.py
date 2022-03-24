from bs4 import BeautifulSoup
from selenium import webdriver
import scrapy
import pandas as pd
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_page_of_bird(bird_name):
    driver.get('https://eol.org/')
    input_eol = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='q']")))
    input_eol.send_keys(bird_name)
    input_eol.send_keys(u'\ue007')
    try:
        ps = driver.find_element(by=By.CLASS_NAME, value="uk-link-reset")
        return ps.get_attribute('href')
    except Exception:
        return None

def scrape_v_2(URL):
    if URL :
        d = {}
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        keys = soup.find_all("div",class_="sample-trait-key")
        values = soup.find_all("div",class_="sample-trait-val")
        
        for i,j in zip(keys,values):
            key = i.get_text()
            value = j.get_text()
            if key in d:
                d[key] = str(d[key]) + "," + str(value)
            else:
                d[key] = value
        return d
    return 'NODATA'


def eol(fro,to,csv_file):
    types_of_birds_df = pd.read_csv('assets/birds.csv',index_col='ID')
    list_of_bird_names = [ types_of_birds_df.loc[ _ ,'Common Bird Names'] for _ in range(1,types_of_birds_df.shape[0]) ]
    data_from_eol = {}
    re_search_on = [] 
    writer = csv.writer(open('assets/'+ csv_file +'.csv',"a",newline=''))
    for bird_name in list_of_bird_names[fro:to]:
        try:
            data_from_eol[bird_name] = scrape_v_2(get_page_of_bird(bird_name))
            try:
                writer.writerow([bird_name,data_from_eol[bird_name]])
            except UnicodeEncodeError:
                writer.writerow([list_of_bird_names.index(bird_name),data_from_eol[bird_name]])
            if (not data_from_eol) or (data_from_eol[bird_name]=='NODATA') :
                re_search_on.append(bird_name)
                print('[-] ',bird_name)
            else:
                print('[+] ',bird_name)
        except Exception:
            writer.writerow([bird_name,'NODATA'])
            print('----------> Unknown Exceptions for Bird ',bird_name)
    print(re_search_on)
    # return (data_from_eol,re_search_on)



if __name__ == '__main__':
    startTime = datetime.now()
    driver = webdriver.Chrome('./chromedriver.exe')
    f = int(input('from :'))
    t = int(input('to :'))
    ds = input('ds_name Nospace FileWhichAlreadyExists :')
    eol(f,t,ds)
    print('\n\nTime taken : ',datetime.now() - startTime)
    
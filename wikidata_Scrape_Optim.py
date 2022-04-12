from tkinter import N
from typing import final
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import csv
import requests
import time
from datetime import datetime
import logging
from timeit import default_timer as timer
import numpy as np
import pandas as pd
from time import sleep

fail = []

def scrape_a_bird(birdname,driver):
    try:
        d = {}
        # driver = webdriver.Chrome(executable_path='./chromedriver');
        driver.get('https://www.wikidata.org/wiki/Wikidata:Main_Page')
        input_wd = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[placeholder='Search Wikidata']")))
        input_wd.send_keys(birdname)
        input_wd.send_keys(Keys.ENTER)
        confirm = '//*[@id="mw-content-text"]/div[4]/ul/li[1]/div[2]/span'
        sea = driver.find_elements(by=By.XPATH, value=confirm)[0].text.strip()
        if sea == 'species of bird':
            first_res ='//*[@id="mw-content-text"]/div[4]/ul/li[1]/div[1]/a'
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, first_res)))
            driver.find_elements(by=By.XPATH, value=first_res)[0].click()
            d={'Name':[birdname],'Wikidata_link':[driver.current_url]}
            return pd.DataFrame(d)
        else:
            fail.append(birdname)
            d={'Name':[birdname],'Wikidata_link':[np.nan]}
            return pd.DataFrame(d)
    except Exception:
            fail.append(birdname)
            d={'Name':[birdname],'Wikidata_link':[np.nan]}
            return pd.DataFrame(d)

def wikidata(fro,to,driver,data_df,list_of_birds):
    for bird_name in list_of_birds[fro:to]:
        try:
            data_df = pd.concat([data_df,scrape_a_bird(bird_name,driver)] )
            logging.debug('[+] '+ bird_name)
            print('[+] '+ bird_name)
        except Exception:
            logging.error('Unknown Exceptions for Bird-' + bird_name)
            print("[-] :'(\t"+ bird_name)
    return data_df

if __name__ == '__main__':
    startTime = datetime.now()
    birds = pd.DataFrame(columns=['Name','Wikidata_link'])
    driver = webdriver.Chrome(executable_path='./chromedriver');
    dz = pd.read_pickle("data/Birds.pkl")
    list_of_birds = list(dz.loc[:,'Bird Original Name'])
    ds = 'None-error'
    try:
        f = int(input('from :'))
        t = int(input('to :'))
        ds = 'wikidata_'+str(f)+'_'+str(t)
        logging.basicConfig(filename="assets/Wikidata_Ultimate_Source/Log_"+ds+".log",format='%(asctime)s - %(levelname)s - %(message)s',filemode='a')
        birds = wikidata(f,t,driver,birds,list_of_birds)
    finally:
        birds.to_pickle("assets/Wikidata_Ultimate_Source/Pick_"+ds+".pkl")
        birds.to_csv("assets/Wikidata_Ultimate_Source/csv_"+ds+".csv")
        try:
            logging.info('\n\nTime taken : ',datetime.now() - startTime)
        finally:
            if len(fail) != 0 :
                print('falied birds : ',fail)
            print('\n\nTime taken : ',datetime.now() - startTime) 
            driver.quit() 

'''
conda activate indicwiki & cd Documents\birds & python wikidata_Scrape_Optim.py
'''
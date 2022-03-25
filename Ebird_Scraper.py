from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import scrapy
import pandas as pd
import csv
import os
import requests
import time
import random 
from datetime import datetime
import logging
from numba import jit, cuda
import numpy as np
from timeit import default_timer as timer  
# import code
# code.interact(local=locals)
# Create and configure logger
# logging.basicConfig(filename="Log_"+log+".log",format='%(asctime)s %(message)s',filemode='a')
# placeholder="Enter species name" 
def get_page_of_bird_ebird(bird_name,driver):
    driver.get('https://ebird.org/explore')
    input_ebird = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[placeholder='Enter species name']")))
    input_ebird.send_keys(bird_name)
    input_ebird.send_keys(Keys.ENTER)
    time.sleep(2)
    input_ebird.send_keys(Keys.ENTER)
    return driver.current_url

# URL = "https://ebird.org/species/grswoo"
def scrape(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("div",class_="Breadcrumbs")
    names_main = soup.find_all("span",class_="Heading-main")
    names_sub = soup.find_all("span",class_="Heading-sub")
    udescription=soup.find_all("p",class_="u-stack-sm")
    for i,j,k,l in zip(results,names_main,names_sub,udescription):
        print('fam , order :',i.get_text())
        print('Main :',j.get_text())
        print('Sci name :',k.get_text())
        print('des : ',l.get_text())

# scrape(URL)
def scrape_v_2_ebird(URL):
    if URL :
        d = {}
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div",class_="Breadcrumbs")
        names_main = soup.find_all("span",class_="Heading-main")
        names_sub = soup.find_all("span",class_="Heading-sub")
        udescription=soup.find_all("p",class_="u-stack-sm")
        
        for i,j,k,l in zip(results,names_main,names_sub,udescription):
            a = i.get_text().strip().split('\n')
            b = j.get_text().strip()
            c = k.get_text().strip()
            e = l.get_text()
            d[b] = {'Order':a[0],'Family':a[1],'Scientific Name':c,'Description':e}
        return d
    return 'NODATA'

# @jit
def ebird_gpu(fro,to,csv_file,driver):
    types_of_birds_df = pd.read_csv('assets/birds.csv',index_col='ID')
    list_of_bird_names = [ types_of_birds_df.loc[ _ ,'Common Bird Names'] for _ in range(1,types_of_birds_df.shape[0]) ]
    data_from_ebird = {}
    re_search_on = [] 
    writer = csv.writer(open('assets/'+ csv_file +'.csv',"a",newline='',encoding='utf-8'))
    for bird_name in list_of_bird_names[fro:to]:
        try:
            data_from_ebird[bird_name] = scrape_v_2_ebird(get_page_of_bird_ebird(bird_name,driver))
            try:
                writer.writerow([bird_name,data_from_ebird[bird_name]])
            except UnicodeEncodeError:
                writer.writerow([list_of_bird_names.index(bird_name),data_from_ebird[bird_name]])
            if (not data_from_ebird) or (data_from_ebird[bird_name]=='NODATA') :
                re_search_on.append(bird_name)
                print('[-] ',bird_name)
            else:
                print('[+] ',bird_name)
        except Exception:
            writer.writerow([bird_name,'NODATA'])
            print('----------> Unknown Exceptions for Bird ',bird_name)
    print(re_search_on)


def ebird(fro,to,csv_file,driver):
    types_of_birds_df = pd.read_csv('assets/birds.csv',index_col='ID')
    list_of_bird_names = [ types_of_birds_df.loc[ _ ,'Common Bird Names'] for _ in range(1,types_of_birds_df.shape[0]) ]
    data_from_ebird = {}
    re_search_on = [] 
    writer = csv.writer(open('assets/'+ csv_file +'.csv',"a",newline='',encoding='utf-8'))
    for bird_name in list_of_bird_names[fro:to]:
        try:
            data_from_ebird[bird_name] = scrape_v_2_ebird(get_page_of_bird_ebird(bird_name,driver))
            try:
                writer.writerow([bird_name,data_from_ebird[bird_name]])
            except UnicodeEncodeError:
                writer.writerow([list_of_bird_names.index(bird_name),data_from_ebird[bird_name]])
            if (not data_from_ebird) or (data_from_ebird[bird_name]=='NODATA') :
                re_search_on.append(bird_name)
                print('[-] ',bird_name)
            else:
                print('[+] ',bird_name)
        except Exception:
            writer.writerow([bird_name,'NODATA'])
            print('----------> Unknown Exceptions for Bird ',bird_name)
    print(re_search_on)


if __name__ == '__main__':
    startTime = datetime.now()
    driver = webdriver.Chrome('./chromedriver.exe')
    f = int(input('from :'))
    t = int(input('to :'))
    ds = input('ds_name Nospace FileWhichAlreadyExists :')
    ebird_gpu(f,t,'ebird/'+ ds , driver)
    print('\n\nTime taken : ',datetime.now() - startTime)
    driver.quit()
    
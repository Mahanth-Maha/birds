import requests
from bs4 import BeautifulSoup
from tkinter import N
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


def scrape_animalia(URL,bird_name):
    if URL :
        d = {}
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        table1 = soup.find("table",class_="table table-bordered")
        key = []
        for i in table1.find_all('td',class_="col-lg-5"):
            title = i.text
            key.append(title)
        values = []
        for j in table1.find_all('td',class_="col-lg-7"):
            info = j.text
            values.append(info)
        for i,j in zip(key,values):
            d[i] = j
        d2 = {}
        for i in d:
            d2[i] = [d[i]]
        d2['Link'] = [URL]
        d2['Common Name'] = [bird_name]
        return pd.DataFrame(d2)
    emp_d = {} 
    return pd.DataFrame(emp_d)

if __name__ == '__main__':
    startTime = datetime.now()
    types_of_birds_df = pd.read_csv('assets/final_names_unq.csv',index_col='ID')
    list_of_bird_names = [ types_of_birds_df.loc[ _ ,'Common Name'] for _ in range(1,types_of_birds_df.shape[0]) ]
    animalia = pd.DataFrame(columns=['Common Name','Conservation status','Synonyms','Old latin name for bird','Order','Family', 'Genus','Breeding region','Breeding subregion','Link'])
    f = int(input('from :'))
    t = int(input('to :'))
    ds = 'animalia_'+str(f)+'_'+str(t)
    logging.basicConfig(filename="assets/rescrape_animalia/Log_"+ds+".log",format='%(asctime)s - %(levelname)s - %(message)s',filemode='a')
    failed =[]
    for bird_name in list_of_bird_names[f:t]:
        try:
            bird_name = '-'.join(bird_name.lower().split(' '))
            URL_d = f"https://animalia.com/{bird_name}/"
            temp_df = scrape_animalia(URL_d,bird_name,animalia)
            animalia = pd.concat([animalia,temp_df])
            print('[+] '+bird_name)
        except Exception:
            failed.append(bird_name)
            print('[+] '+bird_name)
    animalia.to_pickle("assets/rescrape_animalia/Pick_"+ds+".pkl")
    animalia.to_csv("assets/rescrape_animalia/csv_"+ds+".csv")
    pd.DataFrame(failed).to_csv("assets/rescrape_animalia/Failed_"+ds+".csv")
    logging.info('\n\nTime taken : ',datetime.now() - startTime)
    print('\n\nTime taken : ',datetime.now() - startTime) 

'''conda activate indicwiki & cd Documents\birds & python animalia_Scrape_Optim.py'''
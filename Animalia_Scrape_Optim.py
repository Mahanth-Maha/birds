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
        # key = []
        # values = []
        section_main = soup.find("section",class_="s-char")
        if section_main:
            for i,j in zip(section_main.find_all('div',class_="s-char-kinds__attr"),section_main.find_all(('a','div'),class_="s-char-kinds__name")):
                title = i.text
                # key.append(title.strip())
                info = j.text
                # values.append(info.strip())
                d[title.strip()] = info.strip()
        section_dist = soup.find("section",class_="s-distr")
        if section_dist:
            for i,j in zip(section_dist.find_all('div',class_="s-distr-geography__slug"),section_dist.find_all(('a','div'),class_="s-distr-geography__link")):
                title = i.text
                # key.append(title.strip())
                info = j.text
                # values.append(info.strip())
                d[title.strip()] = info.strip()
        section_dist_zone = soup.find("div",class_="s-distr-zone")
        # print(section_dist_zone)
        if section_dist_zone:
            title = ''
            for i in section_dist_zone.find_all('span'):
                title = title + ',' + i.text.strip()
            # key.append('Biome')
            # values.append(title.strip())
            d['Biome'] = title.strip()[1:]
            
        # HABITAT ON HOLD ?
        section_hbt = soup.find("section",class_="s-habbit")
        # 
        # print(section_hbt)
        if section_hbt:
            for i,j in zip(section_hbt.find_all('div',class_="s-habbit-group__slug"),section_hbt.find_all(('a','div'),class_="col-sm-9")):
                title = i.text
                # key.append(title.strip())
            # values = []
            # for j in section_pop.find_all(('a','div'),class_="s-population__link"):
                info = j.text
                # values.append(info.strip())
                if title.strip().lower() != "BIRD'S CALL".lower():
                    d[title.strip()] = ','.join(info.strip().split('\n'))

        section_pop = soup.find("section",class_="s-population-block")
        if section_pop:
            for i,j in zip(section_pop.find_all('div',class_="s-population-slug"),section_pop.find_all(('a','div'),class_="s-population__link")):
                title = i.text
                # key.append(title.strip())
            # values = []
            # for j in section_pop.find_all(('a','div'),class_="s-population__link"):
                info = j.text
                # values.append(info.strip())
                d[title.strip()] = info.strip()

        section_ref = soup.find("section",class_="s-ref")
        # print(section_ref)
        if section_ref:
            # key.append('References')
            # values = []
            info = ''
            for j in section_ref.find_all('a'):
                k = j.get('href')
                if k:
                    info = info + ',' + str(k)
                # print(j.get('href'))
            # values.append(info.strip())
            d['Ref'] = info.strip()[1:]
            

        # for i,j in zip(key,values):
        #     d[i] = j
        d2 = {}
        for i in d:
            d2[i] = [d[i]]
        d2['Animalia_Link'] = [URL]
        d2['Common Name'] = [bird_name]
        return pd.DataFrame(d2)
        # pd.DataFrame(d2)
    emp_d = {} 
    return pd.DataFrame(emp_d)

if __name__ == '__main__':
    startTime = datetime.now()
    types_of_birds_df = pd.read_csv('assets/final_names_unq.csv',index_col='ID')
    list_of_bird_names = [ types_of_birds_df.loc[ _ ,'Common Name'] for _ in range(1,types_of_birds_df.shape[0]) ]
    animalia = pd.DataFrame(columns=['Common Name'])
    f = int(input('from :'))
    t = int(input('to :'))
    ds = 'animalia_'+str(f)+'_'+str(t)
    logging.basicConfig(filename="assets/rescrape_animalia/Log_"+ds+".log",format='%(asctime)s - %(levelname)s - %(message)s',filemode='a')
    failed =[]
    for bird_name in list_of_bird_names[f:t]:
        try:
            bird_name = '-'.join(bird_name.lower().split(' '))
            URL_d = f"https://animalia.bio/{bird_name}/"
            temp_df = scrape_animalia(URL_d,bird_name)
            animalia = pd.concat([animalia,temp_df])
            print('[+] '+ bird_name)
        except Exception:
            failed.append(bird_name)
            print('[-] '+ URL_d)
    animalia.to_pickle("assets/rescrape_animalia/Pick_"+ds+".pkl")
    animalia.to_csv("assets/rescrape_animalia/csv_"+ds+".csv")
    pd.DataFrame(failed).to_csv("assets/rescrape_animalia/Failed_"+ds+".csv")
    logging.info('\n\nTime taken : ',datetime.now() - startTime)
    print('\n\nTime taken : ',datetime.now() - startTime) 

'''conda activate indicwiki & cd Documents\birds & python Animalia_Scrape_Optim.py'''
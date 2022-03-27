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


def get_page_of_bird(bird_name,driver):
    driver.get('https://eol.org/')
    input_eol = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='q']")))
    input_eol.send_keys(bird_name)
    input_eol.send_keys(Keys.ENTER)
    try:
        ps = driver.find_element(by=By.CLASS_NAME, value="uk-link-reset")
        # print('Eol Link ok')
        return ps.get_attribute('href')
    except Exception:
        print('[-] Eol Link Fail -__- ',bird_name)
        return None
    # return driver.current_url

def scrape_v_3_ebird(URL,bird_name):
    if URL :
        d = {}
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        keys = soup.find_all("div",class_="sample-trait-key")
        values = soup.find_all(["div","a"],class_="sample-trait-val")
        des = soup.find("div",class_="desc")
        children = des.findChildren("p" , recursive=False)
        # s = ''
        # print(type(children[0]))
        # for child in children:
        #     # s += child
        #     print(child)
        #     print("---------------?")
        description = children[0].get_text()
        for i,j in zip(keys,values):
            key = i.get_text()
            value = j.get_text()
            if key in d:
                d[key] = str(d[key]) + "," + str(value)
            else:
                d[key] = value
        d2 = {}
        for i in d:
            d2[i] = [d[i]]
        # return d
            # d = {'Common Name':[b],'Kingdom':['Animalia'],'Phylum':['Chordata'],'Class':['Aves'],'Order':[a[0]],'Family':[a[1]],'Binomial Name':[c],'Description':[e],'Link':[URL]}
        d2['Link'] = [URL]
        d2['Description'] = [description]
        d2['Common Name'] = [bird_name]
        d2['Kingdom'] = ['Animalia']
        d2['Phylum']=['Chordata']
        d2['Class']=['Aves']
        # print('d2 = ',d2)
        return pd.DataFrame(d2) 
    emp_d = {} 
    # print('Eol Fail')
    return pd.DataFrame(emp_d)
    
def eol(fro,to,driver,birds):
    types_of_birds_df = pd.read_csv('assets/final_names_unq.csv',index_col='ID')
    list_of_bird_names = [ types_of_birds_df.loc[ _ ,'Common Name'] for _ in range(1,types_of_birds_df.shape[0]) ]
    for bird_name in list_of_bird_names[fro:to]:
        try:
            birds = pd.concat([birds,scrape_v_3_ebird(get_page_of_bird(bird_name,driver),bird_name)] )
            logging.debug('[+] '+ bird_name)
            print('[+] '+ bird_name)
        except Exception:
            logging.error('Unknown Exceptions for Bird-' + bird_name)
    return birds

if __name__ == '__main__':
    startTime = datetime.now()
    birds = pd.DataFrame(columns=['Common Name','Kingdom','Phylum','Class','Link','Description'])
    driver = webdriver.Chrome('./chromedriver.exe')
    f = int(input('from :'))
    t = int(input('to :'))
    ds = 'eol_'+str(f)+'_'+str(t)
    logging.basicConfig(filename="assets/rescrape_eol/Log_"+ds+".log",format='%(asctime)s - %(levelname)s - %(message)s',filemode='a')
    birds = eol(f,t,driver,birds)
    birds.to_pickle("assets/rescrape_eol/Pick_"+ds+".pkl")
    birds.to_csv("assets/rescrape_eol/csv_"+ds+".csv")
    logging.info('\n\nTime taken : ',datetime.now() - startTime)
    print('\n\nTime taken : ',datetime.now() - startTime) 
    driver.quit()    
'''
conda activate indicwiki & cd Documents\birds & python Eol_Scraper_Optim.py
<f>
<t>
'''
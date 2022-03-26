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


def get_page_of_bird_ebird(bird_name,driver):
    driver.get('https://ebird.org/explore')
    input_ebird = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[placeholder='Enter species name']")))
    input_ebird.send_keys(bird_name)
    input_ebird.send_keys(Keys.ENTER)
    time.sleep(2)
    input_ebird.send_keys(Keys.ENTER)
    return driver.current_url


# URL = "https://ebird.org/species/grswoo"

def scrape_v_3_ebird(URL):
    if URL != None :
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find_all("div",class_="Breadcrumbs")
        names_main = soup.find_all("span",class_="Heading-main")
        names_sub = soup.find_all("span",class_="Heading-sub")
        udescription=soup.find_all("p",class_="u-stack-sm")
        # print(birds)
        for i,j,k,l in zip(results,names_main,names_sub,udescription):
            a = i.get_text().strip().split('\n')
            b = j.get_text().strip()
            c = k.get_text().strip()
            e = l.get_text()
            d = {'Common Name':[b],'Kingdom':['Animalia'],'Phylum':['Chordata'],'Class':['Aves'],'Order':[a[0]],'Family':[a[1]],'Binomial Name':[c],'Description':[e],'Link':[URL]}
            return pd.DataFrame(d) 
    emp_d = {'Common Name':[b],'Kingdom':pd.notna,'Phylum':pd.notna,'Class':pd.notna,'Order':pd.notna,'Family':pd.notna,'Binomial Name':pd.notna,'Description':pd.notna,'Link':[URL]} 
    
    return pd.DataFrame(emp_d)
    
def ebird(fro,to,c,driver,birds):
    types_of_birds_df = pd.read_csv('assets/final_names.csv',index_col='ID')
    list_of_bird_names = [ types_of_birds_df.loc[ _ ,'Common Name'] for _ in range(1,types_of_birds_df.shape[0]) ]
    for bird_name in list_of_bird_names[fro:to]:
        try:
            birds = pd.concat([birds,scrape_v_3_ebird(get_page_of_bird_ebird(bird_name,driver))] )
            logging.debug('[+] '+ bird_name)
            print('[+] '+ bird_name)
        except Exception:
            logging.error('[-] Unknown Exceptions for Bird ' + bird_name)
    return birds

if __name__ == '__main__':
    startTime = datetime.now()
    birds = pd.DataFrame(columns=['Common Name','Kingdom','Phylum','Class','Order','Family', 'Binomial Name', 'Link','Description'])
    driver = webdriver.Chrome('./chromedriver.exe')
    f = int(input('from :'))
    t = int(input('to :'))
    ds = 'ebird_'+str(f)+'_'+str(t)
    logging.basicConfig(filename="assets/rescrape/Log_"+ds+".log",format='%(asctime)s - %(levelname)s - %(message)s',filemode='a')
    birds = ebird(f,t,'ebird/'+ ds , driver,birds)
    birds.to_pickle("assets/rescrape/Pick_"+ds+".pkl")
    birds.to_csv("assets/rescrape/csv_"+ds+".csv")
    logging.info('\n\nTime taken : ',datetime.now() - startTime)
    print('\n\nTime taken : ',datetime.now() - startTime) 
    driver.quit()
    
'''
conda activate indicwiki ; cd Documents\birds ; python Ebird_Scraper_Optim.py
<f>
<t>
'''
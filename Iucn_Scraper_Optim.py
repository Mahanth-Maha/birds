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
# driver = webdriver.Chrome(executable_path='./chromedriver');
def scrape_a_bird(birdname,driver):
    try:
        driver.get('https://www.iucnredlist.org/')
        input_avibase = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[placeholder='Names - common, scientific, regions etc...']")))
        input_avibase.send_keys(birdname)
        input_avibase.send_keys(Keys.ENTER)
        sleep(1)
        xp = '//*[@id="redlist-js"]/div/div/div[2]/section/div[2]/article/a'
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp)))
            driver.find_elements(by=By.XPATH, value=xp)[0].click()
        except Exception:
            sleep(1)
            new_xp = '//*[@id="redlist-js"]/div/div/div[2]/section/div[2]/article/a'
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, new_xp)))
                driver.find_elements(by=By.XPATH, value=new_xp)[0].click()
            except Exception:
                fail.append(birdname)
        finally:        
            # sleep(3)
            xp_expand = '//*[@id="details__toggle-all"]'
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xp_expand)))
                expand = driver.find_elements(by=By.XPATH, value=xp_expand)
                expand[0].click()
            except Exception:
                fail.append(birdname+':Expandfail')
            finally:
                sleep(1)
                try:
                    xp_year = '//*[@id="habitat-ecology"]/div[2]/div[1]/p[1]'
                    # xp_year = '//*[@id="habitat-ecology"]/div[2]/div[1]/p'
                    new_xp_year = '//*[@id="habitat-ecology"]/div[2]/div[1]/div/p'
                    xp_alt ='//*[@id="geographic-range"]/div[2]/div[2]/div/p[1]'
                    # xp_alt ='//*[@id="geographic-range"]/div[2]/div[2]/div/p'
                    new_xp_alt ='//*[@id="geographic-range"]/div[2]/div[2]/div/p'
                    xp_populate = '//*[@id="redlist-js"]/div/div[3]/div/div[1]/div[1]/p[2]'
                    # xp_populate = '//*[@id="redlist-js"]/div/div[3]/div/div[1]/div[1]/p'
                    new_xp_populate = '//*[@id="redlist-js"]/div/div[3]/div/div[1]/div[1]/p'
                    xp_habitat ='//*[@id="redlist-js"]/div/div[3]/div/div[1]/div[3]/p[2]'
                    # xp_habitat ='//*[@id="redlist-js"]/div/div[3]/div/div[1]/div[3]/p'
                    new_xp_habitat ='//*[@id="redlist-js"]/div/div[3]/div/div[1]/div[3]/p'
                    xp_sci_n_year = '//*[@id="taxonomy-details"]/div[1]/div[2]/p'
                    xp_conserv = '//*[@id="assessment-information"]/div[2]/div/p[1]/a/strong'
                    xp_sci_name = '//*[@id="taxonomy-details"]/div[1]/div[1]/p/span/em[1]'
                    # xp_sci_name = '//*[@id="taxonomy-details"]/div[1]/div[1]/p/span/em'
                    new_xp_sci_name = '//*[@id="taxonomy-details"]/div[1]/div[1]/p/span/em'
                    xp_order = '//*[@id="taxonomy"]/div[2]/div[1]/p/a/strong'
                    xp_family = '//*[@id="taxonomy"]/div[2]/div[2]/p/a/strong'
                    xp_genus = '//*[@id="taxonomy"]/div[2]/div[3]/p/a/strong'
                    xp_other_c_names = '//*[@id="taxonomy-details"]/div[2]/div[2]/div/p'
                    sci_name = driver.find_elements(by=By.XPATH, value=xp_sci_name)
                    d={'Name':[birdname],'IUCN_link':[driver.current_url]}
                    try:
                        d['sci_name'] = [sci_name[0].text]
                    except Exception:
                        new_xp_sci = '//*[@id="taxonomy-details"]/div[1]/div[2]/p'
                        try:
                            d['sci_name'] = [driver.find_elements(by=By.XPATH, value=new_xp_sci)[0].text]
                        except Exception:
                            d['sci_name'] = np.nan
                    order = driver.find_elements(by=By.XPATH, value=xp_order)
                    try:
                        d['order'] = [order[0].text]
                    except Exception:
                        d['order']= np.nan
                    family = driver.find_elements(by=By.XPATH, value=xp_family)
                    try:
                        d['family'] = [family[0].text]
                    except Exception:
                        d['family']= np.nan
                    genus = driver.find_elements(by=By.XPATH, value=xp_genus)
                    try:
                        d['genus'] = [genus[0].text]
                    except Exception:
                        d['genus']= np.nan
                    sci_n_year = driver.find_elements(by=By.XPATH, value=xp_sci_n_year)
                    try:
                        d['sci_n_year'] = [sci_n_year[0].text]
                    except Exception:
                        d['sci_n_year']= np.nan
                    year = driver.find_elements(by=By.XPATH, value=xp_year)
                    try:
                        d['year'] = [year[0].text]
                    except Exception:
                        d['year']= np.nan
                    altitude = driver.find_elements(by=By.XPATH, value=xp_alt)
                    try:
                        d['altitude'] = [altitude[0].text]
                    except Exception:
                        d['altitude']= np.nan
                    populate = driver.find_elements(by=By.XPATH, value=xp_populate)
                    try:
                        d['populate'] = [populate[0].text]
                    except Exception:
                        d['populate']= np.nan
                    habitat = driver.find_elements(by=By.XPATH, value=xp_habitat)
                    try:
                        d['habitat'] =[habitat[0].text]
                    except Exception:
                        d['habitat']= np.nan
                    conservation =  driver.find_elements(by=By.XPATH, value=xp_conserv)
                    try:
                        d['conservation'] = [conservation[0].text]
                    except Exception:
                        d['conservation']= np.nan
                    other_names = driver.find_elements(by=By.XPATH, value=xp_other_c_names)
                    try:
                        d['other_names'] = [other_names[0].text]
                    except Exception:
                        d['other_names'] = np.nan
                    # print(d)
                    idf = pd.DataFrame(d)
                    return idf
                except Exception:
                    fail.append(birdname)
                    return pd.DataFrame(d)
    except Exception:
        fail.append(birdname)
                
def iucn(fro,to,driver,data_df,list_of_birds):
    for bird_name in list_of_birds[fro:to]:
        try:
            data_df = pd.concat([data_df,scrape_a_bird(bird_name,driver)] )
            logging.debug('[+] '+ bird_name)
            print('[+] '+ bird_name)
        except Exception:
            logging.error('Unknown Exceptions for Bird-' + bird_name)
    return data_df

# # if __name__ == '__main__':
# startTime = datetime.now()
# birds = pd.DataFrame(columns=['Name','sci_name','order','family','genus','sci_n_year','year','altitude','populate','habitat','conservation','other_names','IUCN_link'])
# # driver = webdriver.Chrome('./chromedriver.exe')
# dz = pd.read_excel("assets/DataZone/HBW-BirdLife_List_of_Birds_v6.xlsx")
# list_of_birds = list(dz.loc[:,'Common name'])
# # f = int(input('from :'))
# # t = int(input('to :'))
# f = 8888
# t = 8891
# ds = 'iucn_'+str(f)+'_'+str(t)
# logging.basicConfig(filename="assets/rescrape_iucn/Log_"+ds+".log",format='%(asctime)s - %(levelname)s - %(message)s',filemode='a')
# birds = iucn(f,t,driver,birds,list_of_birds)
# birds.to_pickle("assets/rescrape_iucn/Pick_"+ds+".pkl")
# birds.to_csv("assets/rescrape_iucn/csv_"+ds+".csv")
# logging.info('\n\nTime taken : ',datetime.now() - startTime)
# print('falied birds : ',fail)
# print('\n\nTime taken : ',datetime.now() - startTime) 

# driver.quit()    
'''
conda activate indicwiki & cd Documents\birds & python Eol_Scraper_Optim.py
<f>
<t>
'''
if __name__ == '__main__':
    startTime = datetime.now()
    birds = pd.DataFrame(columns=['Name','sci_name','order','family','genus','sci_n_year','year','altitude','populate','habitat','conservation','other_names','IUCN_link'])
    driver = webdriver.Chrome(executable_path='./chromedriver');
    dz = pd.read_excel("assets/DataZone/HBW-BirdLife_List_of_Birds_v6.xlsx")
    list_of_birds = list(dz.loc[:,'Common name'])
    ds = 'None-error'
    try:
        f = int(input('from :'))
        t = int(input('to :'))
        ds = 'iucn_'+str(f)+'_'+str(t)
        logging.basicConfig(filename="assets/rescrape_iucn/Log_"+ds+".log",format='%(asctime)s - %(levelname)s - %(message)s',filemode='a')
        birds = iucn(f,t,driver,birds,list_of_birds)
    finally:
        birds.to_pickle("assets/rescrape_iucn/Pick_"+ds+".pkl")
        birds.to_csv("assets/rescrape_iucn/csv_"+ds+".csv")
        try:
            logging.info('\n\nTime taken : ',datetime.now() - startTime)
        finally:
            if len(fail) != 0 :
                print('falied birds : ',fail)
            print('\n\nTime taken : ',datetime.now() - startTime) 
            driver.quit()    
'''
conda activate indicwiki & cd Documents\birds & python Iucn_Scraper_Optim.py
<f>
<t>
'''


'''
1 
2 
3 
4 
5 ['Pangani Longclaw', 'Pangani Longclaw:Expandfail', 'Five-striped Sparrow', 'Five-striped Sparrow:Expandfail', 'Stripe-capped Sparrow', 'Stripe-capped Sparrow:Expandfail', 'Chestnut-capped Brush-finch', 'Chestnut-capped Brush-finch:Expandfail', 'Amazonian Oropendola', 'Amazonian Oropendola:Expandfail', 'Greater Antillean Grackle', 'Greater Antillean Grackle:Expandfail', 'Hermit Warbler', 'Hermit Warbler:Expandfail', 'Scarlet-and-white Tanager', 'Scarlet-and-white Tanager:Expandfail', 'Slate-colored Seedeater', 'Slate-colored Seedeater:Expandfail', 'Buff-bellied Tanager', 'Buff-bellied Tanager:Expandfail', 'Rusty-browed Warbling-finch', 'Rusty-browed Warbling-finch:Expandfail', 'Three-striped Hemispingus', 'Three-striped Hemispingus:Expandfail', 'Ochraceous Conebill', 'Ochraceous Conebill:Expandfail', 'Rusty Flowerpiercer', 'Rusty Flowerpiercer:Expandfail', 'Scaled Flowerpiercer', 'Scaled Flowerpiercer:Expandfail', 'Black-throated Flowerpiercer', 'Black-throated Flowerpiercer:Expandfail', 'Merida Flowerpiercer', 'Merida Flowerpiercer:Expandfail', 'Grass-green Tanager', 'Grass-green Tanager:Expandfail', 'Black-capped Tanager', 'Black-capped Tanager:Expandfail']
'''
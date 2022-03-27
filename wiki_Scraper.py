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
import pandas as pd
import wikipedia
import numpy as np
import pycountry

birds = pd.DataFrame(columns=['Name','Conservation status','Kingdom','Phylum','Class','Order','Family', 'Genus', 'Species', 'Binomial Name', 'Synonyms', 'Summary', 'Categories', 'References', 'Wiki URL', 'Image'])


def get_conservation_status(df1):
    for i in range(0,len(list(df1.index))):
        if list(df1.index)[i] == 'Conservation status':
            return (list(df1.index)[i+1])
    if 'Conservation status' not in list(df1.index):
        return np.NaN
def get_kingdom(df1):
    if 'Kingdom:' in list(df1.index):
        return (df1.loc['Kingdom:'][0])
    else:
        return np.NaN
def get_phylum(df1):
    if 'Phylum:' in list(df1.index):
        return (df1.loc['Phylum:'][0])
    else:
        return np.NaN
def get_class(df1):
    if 'Class:' in list(df1.index):
        return (df1.loc['Class:'][0])
    else:
        return np.NaN
def get_order(df1):
    if 'Order:' in list(df1.index):
        return (df1.loc['Order:'][0])
    else:
        return np.NaN
def get_family(df1):
    if 'Family:' in list(df1.index):
        return (df1.loc['Family:'][0])
    else:
        return np.NaN
def get_genus(df1):
    if 'Genus:' in list(df1.index):
        return (df1.loc['Genus:'][0])
    else:
        return np.NaN
def get_species(df1):
    if 'Species:' in list(df1.index):
        return (df1.loc['Species:'][0])
    else:
        return np.NaN
def get_binomial_name(df1):
    for i in range(0,len(list(df1.index))):
        if list(df1.index)[i] == 'Binomial name':
            return(list(df1.index)[i+1])
    if 'Binomial name' not in list(df1.index):
        return np.NaN
def get_synonyms(df1):
    for i in range(0,len(list(df1.index))):
        if list(df1.index)[i] == 'Synonyms':
            return(list(df1.index)[i+1])
    if 'Synonyms' not in list(df1.index):
        return np.NaN
def get_summary(name):
    return(wikipedia.summary(name, sentences=2))
def get_categories(name):
    categories = wikipedia.page(name)
    return(categories.categories[0:3])
def get_references(name):
    refs = wikipedia.page(name)
    return(refs.references[0:3])
def get_url(name):
    url = wikipedia.page(name)
    return(url.url)
def get_image(name):
    image = wikipedia.page(name)
    return(image.images[0])
def findCountry(data):
    countries = sorted([country.name for country in pycountry.countries] , key=lambda x: -len(x))
    for country in countries:
        if country.lower() in data.lower():
            return country
    return None
def findHabitat(data):
    habitats_list = ['forest', 'forests', 'woods', 'woods', 'woodland', 'woodlands', 'bog', 'bogs', 'fen', 'fens', 'marsh', 'marshes', 'swamp', 'swamps', 'wetland', 'grasslands', 'prairie', 'scrubs','shrubs', 'backyards']
    for habitat in habitats_list:
        if habitat in data.lower():
            return habitat
    return None
def extract_data(infobox):
    df = pd.DataFrame(infobox)
    df = df.dropna()
    row = [list(df.columns)[0]]
    
    df = df.set_index(list(df.columns)[0])
    
    row.append(get_conservation_status(df))
    row.append(get_kingdom(df))
    row.append(get_phylum(df))
    row.append(get_class(df))
    row.append(get_order(df))
    row.append(get_family(df))
    row.append(get_genus(df))
    row.append(get_species(df))
    row.append(get_binomial_name(df))
    row.append(get_synonyms(df))
    row.append(get_summary(row[0]))
    row.append(get_categories(row[0]))
    row.append(get_references(row[0]))
    row.append(get_url(row[0]))
    row.append(get_image(row[0]))
    
    birds_length = len(birds)
    birds.loc[birds_length] = row

def get_page_of_bird(bird_name,driver):
    wiki = 'https://wikipedia.org/'
    driver.get(wiki)
    input_wiki = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='search']")))
    input_wiki.send_keys(bird_name)
    input_wiki.send_keys(Keys.ENTER)
    bird_url = driver.current_url
    l = bird_url.lower()
    if bird_url != wiki and 'search' not in l :
        return bird_url
    return None

def scrape(URL,f,t):
    if URL != None :
        types_of_birds_df = pd.read_csv('assets/wiki_list_to.csv')
        pages = [ types_of_birds_df.loc[ _ ,'Common Name'] for _ in range(1,types_of_birds_df.shape[0]) ]
        for i in pages:
            infoboxes = pd.read_html(i, attrs={"class":"infobox biota"})
        if len(infoboxes)==1:
            extract_data(infoboxes[0])
    # birds
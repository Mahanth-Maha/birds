import requests
from bs4 import BeautifulSoup
URL = "https://www.iucnredlist.org/species/22690302/93269030"
def scrape(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    heading = soup.find("h3",class_="heading")
    age = soup.find_all("p",class_="card__data card__data--std card__data--accent")
    print("yughj")
    for i,j in zip(heading,age):
        print(i)
        print(j)
scrape(URL)
#done

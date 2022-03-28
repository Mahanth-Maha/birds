import requests
from bs4 import BeautifulSoup
URL = "https://www.audubon.org/field-guide/bird/american-woodcock"
def scrape(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    table1 = soup.find_all("table",class_="collapse")
    headers = []
    for i in table1.find_all('th'):
        title = i.text
        headers.append(title)
    values = []
    for j in table1.find_all('td'):
        info = j.text
        values.append(info)
    for i,j in zip(headers, values):
        print(i.get_text(),"-",end=" ")
        print(j.get_text)
        print()
scrape(URL)

#https://dibird.com/species/greyandbuff-woodpecker/
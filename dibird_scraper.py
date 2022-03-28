import requests
from bs4 import BeautifulSoup
URL = "https://dibird.com/species/greyandbuff-woodpecker/"
def scrape(URL,bird_name):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    table1 = soup.find("table",class_="table table-bordered")
    headers = []
    for i in table1.find_all('td',class_="col-lg-5"):
        title = i.text
        headers.append(title)
    values = []
    for j in table1.find_all('td',class_="col-lg-7"):
        info = j.text
        values.append(info)
    for i,j in zip(headers, values):
        print(i,"-",end=" ")
        print(j)
        print()
scrape(URL)


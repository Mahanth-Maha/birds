import requests
from bs4 import BeautifulSoup
URL = "https://a-z-animals.com/animals/woodpecker/#"
def scrape(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    table1 = soup.find("div",class_="col-lg-8")
    for i in table1:
   
        print(i,"-",end=" ")

scrape(URL)
#done

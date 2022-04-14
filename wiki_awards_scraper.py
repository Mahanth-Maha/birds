import requests
from bs4 import BeautifulSoup
URL = "https://en.wikipedia.org/wiki/Kewal_Singh"
def scrape(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    info = soup.find("p",class_=False, id=False)
    for i in info:
        print(i)
scrape(URL)
#done

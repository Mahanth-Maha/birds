import requests
from bs4 import BeautifulSoup

def get_infobox(url):
    page = requests.get(url)
    bs = BeautifulSoup(page.content, "html.parser")

    table = bs.find('table', class_ ='infobox biota')
    result = {}
    row_count = 0
    if table is None:
        pass
    else:
        for tr in table.find_all('tr'):
            if tr.find('th'):
                row_count += 1
        if row_count > 1:
            if tr is not None:
                result[tr.find('td').text.strip()] = tr.find('td').text
    return result

print(get_infobox("https://en.wikipedia.org/wiki/Little_crow_(bird)"))
    

import requests
from bs4 import BeautifulSoup

def foxParser(url):
    request = requests.get(url)
    coverpage = request.content
    soup1 = BeautifulSoup(coverpage, 'html.parser')
    titleData = soup1.find_all("h1", attrs={
            'class':'headline'})
    subtitleData = soup1.find_all("h2", attrs={
            'class':'sub-headline speakable'})
    bodyData = soup1.find_all('p')
    pageData = {}
    pageData["title"] = titleData[0].get_text()
    pageData["subtitle"] = subtitleData[0].get_text()
    pageData["text"] = ""
    for p in bodyData:
        if "class" in p.attrs:
            if p.attrs["class"] == ["speakable"]:
                pageData["text"] += p.get_text()
        else:
            if p.attrs == {}:
                pageData["text"] += p.get_text()
    return pageData

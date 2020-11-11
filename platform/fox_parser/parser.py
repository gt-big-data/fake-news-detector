#Fox Parser
import requests
from bs4 import BeautifulSoup

def parse(url):
    #Check if link has leading https://
    try:
        url.index('https://')
    except ValueError:
        url = 'https://' + url

    #Check if link has been passed to the correct parser
    try:
        url.index('https://www.fox')
    except ValueError:
        print('Incorrect parser used with this URL.')
        exit()

    #Get the HTML from the URL and format using Beautiful Soup
    try:
        request = requests.get(url)
        if not request:
            raise Exception()
        coverpage = request.content
        soup1 = BeautifulSoup(coverpage, 'html.parser')
    except Exception:
        print('Not a valid article.')
        exit()

    try:
        titleData = soup1.find_all("h1", attrs={'class':'headline'})
        subtitleData = soup1.find_all("h2", attrs={'class':'sub-headline'})

        articleBody = soup1.find('div', attrs={'class':'article-body'})
        bodyData = articleBody.find_all('p')
        if not titleData or not subtitleData or not articleBody or not bodyData:
            raise Exception()
    except:
        print('Page text has unrecognized attributes and/or formatting.')
        exit()

    try:
        pageData = {}
        pageData["title"] = titleData[0].get_text()
        pageData["subtitle"] = subtitleData[0].get_text()
        pageData["text"] = ''

        #Parses text out of the HTML elements in content and updates the body
        for p in bodyData:
            #This looks for Fox's links to other irrelevant articles within the page text
            ad = p.find("strong", recursive=False)
            #This looks for tab characters hidden in span tags in image sources
            tab = p.find('span', recursive=False)
            #This eliminates random non-breaking space characters
            text = p.text.replace(u'\xa0', ' ')
            if ad or tab:
                continue
            else:
                pageData['text'] += text

                #Adds a space after a section if there is no terminating space
                if pageData['text'][-1:] != ' ':
                    pageData['text'] += ' '
    except:
        print('Unexpected error occurred while parsing through the body text.')
    finally:
        #Removes line break characters and terminating space
        pageData["text"] = pageData["text"].replace(u'\n', '')
        pageData['text'] = pageData['text'][:-1:]

    return pageData
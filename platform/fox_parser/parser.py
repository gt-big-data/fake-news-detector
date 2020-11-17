#Fox Parser
import requests
from bs4 import BeautifulSoup

def parse(url):
    #Check if link has leading https://
    try:
        url.find('http')
    except ValueError:
        url = 'https://' + url

    #Check if link has been passed to the correct parser
    try:
        url.find('//www.fox')
    except ValueError:
        print('Incorrect parser used with' + '\'' + url + '\'')
        return None

    #Get the HTML from the URL and format using Beautiful Soup
    try:
        request = requests.get(url)
        if not request:
            raise Exception()
        coverpage = request.content
        soup1 = BeautifulSoup(coverpage, 'html.parser')
    except Exception:
        print('\'' + url + '\'' + ' page info could not be requested.')
        return None

    try:
        titleData = soup1.find_all("h1", attrs={'class':'headline'})

        articleBody = soup1.find('div', attrs={'class':'article-body'})
        bodyData = articleBody.find_all('p')
        if not titleData or not articleBody or not bodyData:
            raise Exception()
    except:
        print('\'' + url + '\' has unrecognized attributes and/or formatting.')
        return None

    try:
        pageData = {}
        pageData["title"] = titleData[0].get_text()
        pageData['body'] = ''

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
                pageData['body'] += text

                #Adds a space after a section if there is no terminating space
                if pageData['body'][-1:] != ' ':
                    pageData['body'] += ' '
    except:
        print('Unexpected error occurred while parsing through' + '\'' + url + '\'')
        return None
    finally:
        #Removes line break characters and terminating space
        pageData['body'] = pageData['body'].replace(u'\n', '')
        pageData['body'] = pageData['body'][:-1:]

    return pageData
#CNN Parser
import requests
from bs4 import BeautifulSoup

def parse(url):
    output = {}

    #Check if link has leading https://
    try:
        url.index('http')
    except ValueError:
        url = 'https://' + url

    #Check if link has been passed to the correct parser
    try:
        url.index('//www.cnn')
    except ValueError:
        print('Incorrect parser used with ' + '\'' + url + '\'')
        return None

    #Get the HTML from the URL and format using Beautiful Soup
    try:
        page = requests.get(url)
        if not page:
            raise Exception()
        soup = BeautifulSoup(page.content, 'html.parser')
    except Exception:
        print('\'' + url + '\'' + ' page info could not be requested.')
        return None

    #If page text can be parsed based on pre-determined CSS classes, this updates the title and gets the body text
    output['title'] = ''
    try:
        output['title'] = soup.find('h1', attrs={"class": ["pg-headline", "headline__text", "sc-jTzLTM"]}).text
        content = soup.find_all(attrs={"class": ["zn-body__paragraph", "paragraph", "list-items", "sc-gxMtzJ", "sc-dfVpRl", "sc-gZMcBi"]})
        if not content:
            raise Exception()
    except Exception:
        print('\'' + url + '\'' + ' has unrecognized attributes and/or formatting.')
        return None

    #Parses text out of the HTML elements in content and updates the body
    try:
        output['body'] = ''
        for paragraph in content:
            text = paragraph.text.replace(u'\xa0', ' ')
            output['body'] += text

            #Adds a space after a section if there is no terminating space
            try:
                output['body'][-1]
            except:
                continue
            if output['body'][-1] != ' ':
                output['body'] += ' '
    except:
        print('Unexpected error occurred while parsing through ' + '\'' + url + '\'')
        return None
    finally:
        #Removes terminating space
        output['body'] = output['body'][:-1:]

    return output
#CNBC Parser
import requests
from bs4 import BeautifulSoup

def parse(url):
    output = {}

    #Check if link has leading https://
    try:
        url.index('https://')
    except ValueError:
        url = 'https://' + url

    #Check if link has been passed to the correct parser
    try:
        url.index('https://www.cnbc')
    except ValueError:
        print('Incorrect parser used with this URL.')
        return None

    #Get the HTML from the URL and format using Beautiful Soup
    try:
        page = requests.get(url)
        if not page:
            raise Exception()
        soup = BeautifulSoup(page.content, 'html.parser')
    except Exception:
        print('Not a valid article')
        return None

    #If page text can be parsed based on pre-determined CSS classes, this updates the title and gets the body text
    output['title'] = ''
    try:
        output['title'] = soup.find('h1', attrs={"class": ["LiveBlogHeader-headline", "ArticleHeader-headline"]}).text

        articleBody = soup.find('div', attrs={'class':['ArticleBody-articleBody', 'FeaturedContent-articleBody']})
        content = articleBody.find_all(['p', 'li'])
        proCheck = articleBody.find('div', attrs={'class': 'ArticleBody-proGate'})
        if not content:
            raise Exception('Page text has unrecognized attributes and/or formatting.')
        if proCheck:
            raise Exception('Page locked to Pro users.')
    except Exception as e:
        print(e)
        return None

    #Parses text out of the HTML elements in content and updates the body
    try:
        output['body'] = ''
        for paragraph in content:
            text = paragraph.text.replace(u'\xa0', ' ')
            output['body'] += text

            #Adds a space after a section if there is no terminating space
            if output['body'][-1] != ' ':
                output['body'] += ' '
    except:
        print('Unexpected error occurred while parsing through body text.')
    finally:
        #Removes terminating space
        output['body'] = output['body'][:-1:]

    return output
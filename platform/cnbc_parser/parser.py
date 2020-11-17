#CNBC Parser
import requests
from bs4 import BeautifulSoup
import datetime

def parse(url):
    output = {}

    #Check if link has leading https://
    try:
        url.index('http')
    except ValueError:
        url = 'https://' + url

    #Check if link has been passed to the correct parser
    try:
        url.index('//www.cnbc')
    except ValueError:
        print('Incorrect parser used with ' + '\'' + url + '\'')
        return None

    #Check if link is an article or not
    foundChar = True
    for char in url:
        if char == '?':
            foundChar = True
            break
        if char.isdigit():
            foundChar = False
    if foundChar == True:
        print('\'' + url + '\'' + ' is not an article.')
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

    #If page is restricted to pro users, don't parse for title or body
    try:
        proCheck1 = soup.find('div', attrs={'class': 'ArticleBody-proGate'})
        proCheck2 = soup.find('div', attrs={'id':['checkout-container', 'articlePayload']})
        if proCheck1 or proCheck2:
            raise Exception('\'' + url + '\'' + ' is locked to Pro users.')
    except Exception as e:
        print(e)
        return None

    #If page text can be parsed based on pre-determined CSS classes, this updates the title
    output['title'] = ''
    try:
        output['title'] = soup.find('h1', attrs={"class": ["LiveBlogHeader-headline", "ArticleHeader-headline"]}).text
    except:
        print('\'' + url + '\'' + ' has unrecognized title attributes and/or formatting.')
        return None

    # Find body text as above
    try:
        articleBody = soup.find('div', attrs={'class':['ArticleBody-articleBody', 'FeaturedContent-articleBody']})

        if articleBody is None:
            raise Exception('\'' + url + '\'' + ' has unrecognized article body attributes and/or formatting.')

        content = articleBody.find_all(['p', 'li'])

        if not content:
            raise Exception('\'' + url + '\'' + ' has unrecognized page attributes and/or formatting.')
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
        print('Unexpected error occurred while parsing through ' + '\'' + url + '\'')
        return None
    finally:
        #Removes terminating space
        output['body'] = output['body'][:-1:]

    return output
# NPR Parser
import requests
import urllib.request
import time
import bs4
from bs4 import BeautifulSoup

def find_text(tag):
    paragraph = ""
    for element in tag.children:
        # The find_all method return an image caption twice. One of the repeats contains <b>hide caption<b> tag
        # Ignore that tag if we see it.
        if str(element).strip() == "hide caption":
            return " "
        # for all other child elements, extract the text and append it to paragraph
        paragraph += str(element).strip() + " "
    return paragraph

def parse(url):
    #Check if link has leading https://
    try:
        url.index('https://')
    except ValueError:
        url = 'https://' + url

    #Check if link has been passed to the correct parser
    try:
        url.index('https://www.npr')
    except ValueError:
        print('Incorrect parser used with this URL.')
        exit()

    output = {}
    try:
        response = requests.get(url)
        if not response:
            raise Exception()
        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.find("article", class_="story")
    except:
        print('Not a valid article.')
        exit()

    try:
        # the article title is wrapped within the h1 tag inside a div with class="storytitle"
        h1_tag = article.find("div", class_="storytitle").h1
        output["title"] = h1_tag.string

        # the article body is wrapped within <p> tags
        output["body"] = ""
        content_tags = article.find('div', class_='storytext').find_all("p")
        if not content_tags:
            raise Exception()
    except:
        print('Page text has unrecognized attributes and/or formatting.')
        exit()

    try:
        #Parses text out of the p tags in content_tags and updates the body
        showNext = True
        for tag in content_tags:
            #Find the text so that all subtags are ignored and eliminate leading and trailing spaces
            text = tag.text
            #A caption is defined if there is a <b> subtag
            caption = tag.find('b', recursive=False)

            #Image captions are repeated twice consecutively. Therefore, if an image caption was the last tag,
            #skip the next one.
            if showNext == False:
                showNext = True
                continue
            #If a caption is found, eliminate leading and trailing spaces.
            if caption:
                output['body'] += tag.find(text=True, recursive=False).strip()
                showNext = False
            elif text:
                output["body"] += text

            if output['body'][-1] != ' ':
                output['body'] += ' '
    except:
        print('Unexpected error occurred while parsing through the body text.')
    finally:
        #Removes line break characters and terminating space
        output['body'] = output['body'][:-1:]
        output["body"] = output["body"].replace(u'\n', '')

    return output

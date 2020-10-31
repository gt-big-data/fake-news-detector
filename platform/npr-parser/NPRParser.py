# NPR Parser
import requests
import urllib.request
import time
import bs4
from bs4 import BeautifulSoup

def NPR_article_parser(url):
    output = {}

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    article = soup.find("article", class_="story")

    # the article title is wrapped within the h1 tag inside a div with class="storytitle"
    h1_tag = article.find("div", class_="storytitle").h1
    output["title"] = h1_tag.string

    # the article body is wrapped within <p> tags
    output["body"] = ""
    content_tags = article.find_all("p")
    for tag in content_tags:
        output["body"] += find_text(tag)

    return output

def find_text(tag):
    paragraph = ""
    for element in tag.children:
        # The find_all method return an image caption twice. One of the repeats contains <b>hide caption<b> tag
        # Ignore that tag if we see it.
        if element.string.strip() == "hide caption":
            return " "
        # for all other child elements, extract the text and append it to paragraph
        paragraph += element.string.strip() + " "
    return paragraph

if __name__ == "__main__":
    url = input().strip()
    result = NPR_article_parser(url)
    print(result)

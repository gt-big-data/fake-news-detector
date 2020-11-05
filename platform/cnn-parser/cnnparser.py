import requests;
import urllib.request;
import time;
import bs4;
from bs4 import BeautifulSoup;

def CNN_article_parser(url):
    output = {};
    # Do a get request to obain the article
    response = requests.get(url);
    soup = BeautifulSoup(response.text, "html.parser");
    # article title is in the <h1> tag, which is the only one in the entire article
    h1_tag = soup.find("h1");
    output["title"] = h1_tag.string;
    # article body is the string wrapped inside the <div> element with class="zn-body__paragraph"
    output["body"] = ""
    paragraph_tags = soup.find_all(class_="zn-body__paragraph");
    for tag in paragraph_tags:
        for child in tag.children:
            if child.name == None:
                output["body"] += child;

    return output

if __name__ == "__main__":
    url = input("Please enter a CNN article url: ").strip();
    # url = "https://www.cnn.com/2020/10/12/health/johnson-coronavirus-vaccine-pause-bn/index.html";
    # url = "https://www.cnn.com/2020/10/12/politics/iowa-senate-race-joni-ernst/index.html";
    print(CNN_article_parser(url));

    
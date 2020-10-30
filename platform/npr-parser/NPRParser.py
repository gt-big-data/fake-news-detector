# NPR Parser
import requests;
import urllib.request;
import time;
import bs4;
from bs4 import BeautifulSoup;

def NPR_article_parser(url):
    output = {};

    response = requests.get(url);
    soup = BeautifulSoup(response.text, "html.parser");

    # the article title is wrapped within the h1 tag inside a div with class="storytitle"
    title_div = soup.find("div", class_="storytitle");
    h1_tag = title_div.find("h1");
    output["title"] = h1_tag.string;

    # the article body is wrapped within <p> tags and <em> tags
    output["body"] = "";
    content_tags = soup.find_all("p");
    for tag in content_tags:
        print([x for x in tag.children]);
        output["body"] += find_text(tag);

    return output;

def find_text(tag):
    if tag.name == None:
        return tag.strip() + " ";
    else:
        text = "";
        for child in tag.children:
            text += find_text(child);
        return text;

if __name__ == "__main__":
    url = input().strip();
    result = NPR_article_parser(url);
    print(result);

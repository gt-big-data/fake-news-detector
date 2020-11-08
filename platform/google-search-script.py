# Required dependencies:
# pip install google

from googlesearch import search

# to search
def searchGoogle():
    query = input("Enter a google search query: ")

    website_dictionary = {}
    for j in search(query, tld="com", num=30, stop=30, pause=4):
        if j.find("www.cnn")>0:
            website_dictionary["cnn"] = j
        if j.find("www.fox")>0:
            website_dictionary["fox"] = j
        if j.find("www.npr")>0:
            website_dictionary["npr"] = j
        if j.find("www.cnbc")>0:
            website_dictionary["cnbc"] = j

searchGoogle()


#return dict: {which site name, URL}
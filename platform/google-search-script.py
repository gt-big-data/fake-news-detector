# Required dependencies:
# pip install google

from googlesearch import search

# to search

def searchGoogle():
    query = input("Enter a google search query: ")

    for j in search(query, tld="com", num=100, stop=100, pause=4):
        if(j.find("cnn.com")>0 or j.find("foxnews.com")>0):
            print(j)

searchGoogle()
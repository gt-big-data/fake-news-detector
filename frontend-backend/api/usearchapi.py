import requests
import json

url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"
headers = {
    'x-rapidapi-key': "4d52858044msh2b4bbc2652d4b66p133682jsn315965608529",
    'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com"}

def call_usearch_news_api(query):
    querystring = {"q":query,
               "pageNumber":"10",
               "pageSize":"10",
               "autoCorrect":"true",
               "fromPublishedDate":"null",
               "toPublishedDate":"null"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = json.loads(response.text)

    output = []
    for article in res['value']:
        print(article)
        output.append([article['title'], article['body'], article['url']])
    return output
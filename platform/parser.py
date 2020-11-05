import pandas as pd

import cnn_parser
import fox_parser
import npr_parser
import query_articles

def get_articles(query):
    out_data = list()
    article_results = query_articles.search_google(query)
    for news_source in article_results:
        for article_url in article_results[news_source]:
            parsed_data = None
            if(news_source == 'cnn'):
                parsed_data = cnn_parser.parse(article_url)
            elif(news_source == 'fox'):
                parsed_data = fox_parser.parse(article_url)
            elif(news_source == 'npr'):
                parsed_data = npr_parser.parse(article_url)
            if(parsed_data):
                out_data.append({
                    "title": parsed_data["title"],
                    "body": parsed_data["body"],
                    "source": news_source
                })
    article_df = pd.DataFrame(data=out_data)
    return article_df
print(get_articles("trump visits prime minister"))



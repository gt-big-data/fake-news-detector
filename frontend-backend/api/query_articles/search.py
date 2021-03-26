from googlesearch import search

def search_google(query):
    websiteDict = {}
    for result in search(query, tld="com", num=30, stop=30, pause=2):
        if "www.foxnews.com" in result or "www.foxbusiness.com" in result or "www.cnn.com" in result or "www.cnbc.com" in result or "www.npr.org" in result:
            if "foxnews.com" in result or "foxbusiness.com" in result:
                if "fox" in websiteDict:
                    websiteDict["fox"].append(result)
                else:
                    websiteDict["fox"] = [result]
            if "cnn.com" in result:
                if "cnn" in websiteDict:
                    websiteDict["cnn"].append(result)
                else:
                    websiteDict["cnn"] = [result]
            if "cnbc.com" in result:
                if "cnbc" in websiteDict:
                    websiteDict["cnbc"].append(result)
                else:
                    websiteDict["cnbc"] = [result]
            if "npr.org" in result:
                if "npr" in websiteDict:
                    websiteDict["npr"].append(result)
                else:
                    websiteDict["npr"] = [result]
    return websiteDict

from googlesearch import search

def searchGoogle(query):
    websiteDict = {}
    for result in search(query, tld="com", num=30, stop=30, pause=2): 
        if "foxnews.com" in result or "cnn.com" in result or "cnbc.com" in result or "npr.org" in result:
            if "foxnews.com" in result:
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
                if "fox" in websiteDict:
                    websiteDict["cnbc"].append(result)
                else:
                    websiteDict["cnbc"] = [result]
            if "npr.org" in result:
                if "npr" in websiteDict:
                    websiteDict["npr"].append(result)
                else:
                    websiteDict["npr"] = [result]
    return websiteDict

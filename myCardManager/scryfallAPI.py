# https://github.com/NandaScott/Scrython
# we can use this (scrython) or we can write our own code

""""
We kindly ask that you insert 50 – 100 milliseconds of delay between the requests you send to the server at api.scryfall.com. (i.e., 10 requests per second on average).
Submitting excessive requests to the server may result in a HTTP 429 Too Many Requests status code. Overloading the API after this point may result in a temporary or permanent ban of your IP address. Applications that continuously receive rate limit warnings over a longer period may also be blocked.
The file origins used by the API, located at *.scryfall.io do not have these rate limits.
We encourage you to cache the data you download from Scryfall or process it locally in your own database, at least for 24 hours. Scryfall provides our entire database compressed for download in daily bulk data files.
"""


import requests
import json

headers = {
    'User-Agent': 'MyMTGApp/1.2.0',
    'Accept': '*/*'
}

def search_card(search_query):
    results = requests.get(f"https://api.scryfall.com/cards/search?q={search_query}", headers=headers).text
    results = json.loads(results) # make it a dict
    try:
        print(results) # debug
        if results["total_cards"] == 1:
            return results["data"][0]#["name"]
        elif results["total_cards"] > 1:
            myRet = ""
            for i in range(results["total_cards"]): 
                if (results["data"][i]["name"] == search_query):
                    myRet = results["data"][i]#["name"] # should only be one
            return myRet
        else:
            return "unable to find card"
    except Exception as e:
        return f"Unable to find card {e}"

def remove_formating(txt):
    # remove commas, spaces, hyphens, case etc
    return txt.lower().replace(",", "").replace("-","").replace(" ", "")
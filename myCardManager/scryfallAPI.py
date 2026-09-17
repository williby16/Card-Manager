# https://github.com/NandaScott/Scrython
# we can use this (scrython) or we can write our own code

""""
We kindly ask that you insert 50 – 100 milliseconds of delay between the requests you send to the server at api.scryfall.com. (i.e., 10 requests per second on average).
Submitting excessive requests to the server may result in a HTTP 429 Too Many Requests status code. Overloading the API after this point may result in a temporary or permanent ban of your IP address. Applications that continuously receive rate limit warnings over a longer period may also be blocked.
The file origins used by the API, located at *.scryfall.io do not have these rate limits.
We encourage you to cache the data you download from Scryfall or process it locally in your own database, at least for 24 hours. Scryfall provides our entire database compressed for download in daily bulk data files.
"""

import time
import requests
import json
from tqdm import tqdm
import os
import gzip
import shutil
import gc

headers = {
    'User-Agent': 'MyMTGApp/1.2.0',
    'Accept': '*/*'
}

class ScryBulkUtils:
    scryBulk = {}
    isOpen = False

    @staticmethod
    def openBulk():
        ScryBulkUtils.isOpen = True
        with open("myCardmanager/bulk/default-cards.json", "r") as f:
            ScryBulkUtils.scryBulk = json.load(f)
    @staticmethod
    def closeBulk():
        ScryBulkUtils.isOpen = False
        ScryBulkUtils.scryBulk = {}
        gc.collect()


def search_card(key):
    if (not ScryBulkUtils.isOpen):
        print("Fatal error, unable to open dict!")
        return "Fatal Error - dict not open?"
    try:
        return ScryBulkUtils.scryBulk[key]
    except:
        return f"Fatal Error - key: {key} not found in bulk"


def query_card(search_query):
    time.sleep(0.5) # ensure give time before last query
    #results = requests.get(f"https://api.scryfall.com/cards/search?q={search_query}", headers=headers).text # THIS IS TERRIBLE
    # IF we're searching card names, we should strip the name! but thats not up to this to do...
    results = requests.get(
    "https://api.scryfall.com/cards/search",
    params={"q": search_query},
    headers=headers
).text
    results = json.loads(results) # make it a dict
    try:
        #print(results) # debug
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
        print(results) # debug
        return f"Unable to find card {e}"

def download_bulk():
    if os.path.isfile('myCardmanager/bulk/default-cards.jsonl'):
        os.remove('myCardmanager/bulk/default-cards.jsonl')

    metadata = requests.get(
        "https://api.scryfall.com/bulk-data",
        timeout=30,
        headers=headers
    ).json()

    default_cards = None

    for i in metadata["data"]:
        if i["type"] == "default_cards":
            default_cards=i
            break

    if default_cards == None:
        print("error, returning!")
        return

    download_url = default_cards["jsonl_download_uri"]

    with requests.get(download_url, stream=True, timeout=120) as r:
        r.raise_for_status()

        total_size = int(r.headers.get("Content-Length", 0))

        with open("myCardmanager/bulk/default-cards.jsonl.gz", "wb") as f:
            with tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc="Downloading",
            ) as pbar:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

    # UNZIP THE FILE
    # Define your file paths
    input_file = 'myCardmanager/bulk/default-cards.jsonl.gz'
    output_file = 'myCardmanager/bulk/default-cards.jsonl'

    # Open the .gz file in binary read mode ('rb') and the destination in binary write mode ('wb')
    with gzip.open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    # delete zipped file once done.
    os.remove(input_file)

    # create new with updated text!
    newDict = {}
    with open("myCardmanager/bulk/default-cards.json", "w", encoding='utf-8') as f_out:
        with open(output_file, "r", encoding="utf-8") as f_in:
            for line in tqdm(f_in, desc="Processing"):
                obj = json.loads(line)
                newDict.update({f'{obj["set"]}-{obj["collector_number"]}-': obj})
            json.dump(newDict, f_out)
    os.remove(output_file)

def remove_formating(txt):
    # remove commas, spaces, hyphens, case etc
    return txt.lower().replace(",", "").replace("-","").replace(" ", "")
from scryfallAPI import *
from datetime import datetime
import json
import csv
from tqdm import tqdm
import gc

# needed to make the class serializable
from json import JSONEncoder

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default
JSONEncoder.default = _default

class Card:
    def __init__(self, cardData, cardMeta):
        self.cardMeta = cardMeta
        self.cardData = cardData
    
    def print_name(self):
        print(self.cardData["set"])
    
    # custom implementation to make it serializable
    def to_json(self):
        return [self.cardMeta, self.cardData]

# import the card from a csv
class csvCard(Card):
    def __init__(self, card):
        thisSearch = f'{card["Edition"]}-{card["Collector Number"]}-'
        self.cardMeta = card
        self.cardData = search_card(thisSearch)

# add a card from scryfall, need to create csv metadata for it 
class scryCard(Card):
    def __init__(self, cardName, foil=""): # cardname should include additional filters for specfic printing! (Implemented in collection class)
        self.cardData = query_card(cardName)
        self.generateMetaData(foil)
    
    def generateMetaData(self, foil=""):
        now = datetime.now()
        # "1","1","NAME","SET_CODE","Near Mint","English","","","TIME","COLLECTOR_NUMBER","False","False",""
        # "Count","Tradelist Count","Name","Edition","Condition","Language","Foil","Tags","Last Modified","Collector Number","Alter","Proxy","Purchase Price"
        self.cardMeta = {"Count": "1",
                         "Tradelist Count": "1",
                         "Name": self.cardData["name"],
                         "Edition": self.cardData["set"],
                         "Condition": "Near Mint",
                         "Language": "English",
                         "Foil": foil,
                         "Tags": "",
                         "Last Modified": str(now),
                         "Collector Number": self.cardData["collector_number"]
                         }


class Collection:
    def __init__(self, cards=None):
        if (cards == None):
            self.cards = {} # []
        else:
            self.cards = cards
    
    def save_to_json(self, target_path):
        with open(target_path, 'w') as file:
            json.dump(self.cards, file)

    def save_to_csv(self, target_path): # save only card meta to a csv so it can be uploaded to moxfield!
        # generate list of metadata
        metas = []
        # for i in self.cards:
        for i in self.cards.values():
            metas.append(i.cardMeta)
        keys = metas[0].keys()

        with open(target_path, 'w', newline='') as file:
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(metas)
            

    def load_from_json(self, path): # use pathlib later!
        with open(path, 'r') as file:
            self.cards = json.load(file)
            #data = json.load(file)
            #for card in data:
             #   self.cards.append(Card(card[1], card[0]))
    
    def load_from_csv(self, path): # load from metadata and use scryfall bulk collection!!
        ScryBulkUtils.openBulk() # open in close book so we don't have to keep it loaded in memory! idk if its necassary but 
        with open(path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            numRows = len(rows)

            #for row in reader:
            #    self.add_card_meta(row)
            for row in tqdm(range(numRows)):
                self.add_card_meta(rows[row])
        ScryBulkUtils.closeBulk()

    def update_collection(self, path): # read collection.csv and compare it to the currently loaded collection and add the cards!
        # there is probably a better way to do this, but this way will utilize functions already written completely.
        tempPath = "myCardManager/binder/collecton.csv.temp"
        # redownload latest bulk data
        download_bulk()
        # temp save collection to a csv.
        self.save_to_csv(tempPath)
        # reload card and scrycard data
        self.load_from_csv(tempPath)
        # remove the temp
        os.remove(tempPath)
        # NOTE will have to manually save the updated information to the .json file

    def refresh_scryfall_data(self): # data like price can change, but this will take a while to run...
        download_bulk()

    # when adding a card, check if its already in the collection, then if so, just increase its number!
    def add_card(self, toAdd):
        thisKey = f'{toAdd.cardMeta["Edition"]}-{toAdd.cardMeta["Collector Number"]}-{toAdd.cardMeta["Foil"]}'
        #existing_card = self.is_card_in_collection(toAdd.cardMeta)
        if (thisKey in self.cards):
            self.cards[thisKey].cardMeta["Count"] = str(int(self.cards[thisKey].cardMeta["Count"]) + int(toAdd.cardMeta["Count"]))
        else:
            #self.cards.append(toAdd)
            self.cards.update({thisKey: toAdd})

    # I don't remember what this does. It adds a card by name, with set and cn as optional
    def add_card_name(self, name, foil="", s=None, cn=None): # set id and collector number
        if (s):
            name += f" set={s}"
        if (cn):
            name += f" cn={cn}"
        toAdd = scryCard(name, foil)
        self.add_card(toAdd)
    
    def add_card_meta(self, toAddMeta):
        toAdd = csvCard(toAddMeta)
        self.add_card(toAdd)

    # Scryfall functions
    def search_collection(self, query, retCard=False): # search entire collection with scryfall syntax # retCard for if we return card objects
        query = query + " unique:prints" # enforce unique prints!
        targets = query_card(query)
        if targets["object"] == 'error':
            return
        for thisCard in targets["data"]:
            thisKey = f'{thisCard["set"]}-{thisCard["collector_number"]}-'
            if (thisKey in self.cards.keys()):
                print("found card: " + thisKey)
            thisKey = thisKey + "foil"
            if (thisKey in self.cards.keys()):
                print("found card: " + thisKey)
            

    # legacy code
    """
    # there must be an error in here... Its fine for now tho, just need to look into it later
    def is_card_in_collection(self, cardMeta):
        name, setNum, collector, foil = cardMeta["Name"], cardMeta["Edition"], cardMeta["Collector Number"], cardMeta["Foil"]
        
        #for card in range(len(self.cards)):
            #thisCard = self.cards[card]
        for thisCard in self.cards.values():
            cName, cSetNum, cCollector, cFoil = thisCard.cardMeta["Name"], thisCard.cardMeta["Edition"], thisCard.cardMeta["Collector Number"], thisCard.cardMeta["Foil"]
            # are they the same? # currently ignoring purchase price and condition bc I dont use those # really should check most of the metadata....
            if (name == cName and setNum == cSetNum and collector == cCollector and foil == cFoil):
                return thisCard
        return False
    """


    
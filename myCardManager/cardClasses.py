from scryfallAPI import search_card
from datetime import datetime
import json
import csv

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
        self.cardMeta = card
        self.cardData = search_card(card["Name"])

# add a card from scryfall, need to create csv metadata for it 
class scryCard(Card):
    def __init__(self, cardName):
        self.cardData = search_card(cardName)
        self.generateMetaData()
    
    def generateMetaData(self):
        now = datetime.now()
        # "1","1","NAME","SET_CODE","Near Mint","English","","","TIME","COLLECTOR_NUMBER","False","False",""
        # "Count","Tradelist Count","Name","Edition","Condition","Language","Foil","Tags","Last Modified","Collector Number","Alter","Proxy","Purchase Price"
        self.cardMeta = {"Count": 1,
                         "Tradelist Count": 1,
                         "Name": self.cardData["name"],
                         "Edition": self.cardData["set"],
                         "Condition": "Near Mint",
                         "Language": "English",
                         "Foil": "",
                         "Tags": "",
                         "Last Modified": str(now),
                         "Collector Number": self.cardData["collector_number"]
                         }


class Collection:
    def __init__(self, cards=None):
        if (cards == None):
            self.cards = []
        else:
            self.cards = cards
    
    def save_to_json(self, target_path):
        with open(target_path, 'w') as file:
            json.dump(self.cards, file)

    def save_to_csv(self, target_path): # save only card meta to a csv so it can be uploaded to moxfield!
        # generate list of metadata
        metas = []
        for i in self.cards:
            metas.append(i.cardMeta)
        keys = metas[0].keys()

        with open(target_path, 'w', newline='') as file:
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(metas)
            

    def load_from_json(self, path): # use pathlib later!
        with open(path, 'r') as file:
            data = json.load(file)
            for card in data:
                self.cards.append(Card(card[1], card[0]))
    
    def load_from_csv(self, path): # load from metadata and use scryfall!
        with open(path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                self.add_card_meta(row)
                

    def update_collection(self, path): # read collection.csv and compare it to the currently loaded collection and add the cards!
        pass

    def refresh_scryfall_data(self): # data like price can change, but this will take a while to run...
        pass

    # when adding a card, check if its already in the collection, then if so, just increase its number!
    def add_card(self, toAdd):
        if (not self.is_card_in_collection(toAdd.cardMeta)):
            self.cards.append(toAdd)
    
    def add_card_name(self, name):
        toAdd = scryCard(name)
        if (not self.is_card_in_collection(toAdd.cardMeta)):
            self.cards.append(toAdd)
    
    def add_card_meta(self, toAddMeta):
        toAdd = csvCard(toAddMeta)
        if (not self.is_card_in_collection(toAddMeta)):
            self.cards.append(toAdd)

    # there must be an error in here... Its fine for now tho, just need to look into it later
    def is_card_in_collection(self, cardMeta):
        name, setNum, collector, foil = cardMeta["Name"], cardMeta["Edition"], cardMeta["Collector Number"], cardMeta["Foil"]
        
        for card in range(len(self.cards)):
            thisCard = self.cards[card]
            cName, cSetNum, cCollector, cFoil = thisCard.cardMeta["Name"], thisCard.cardMeta["Edition"], thisCard.cardMeta["Collector Number"], thisCard.cardMeta["Foil"]
            # are they the same? # currently ignoring purchase price and condition bc I dont use those # really should check most of the metadata....
            if (name == cName and setNum == cSetNum and collector == cCollector and foil == cFoil):
                self.cards[card].cardMeta["Count"] = str(int(thisCard.cardMeta["Count"])+1) # increase our count by 1
                return True
        return False

    
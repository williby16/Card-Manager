from scryfallAPI import search_card

class baseCard:
    def __init__(self, card):
        # metadata
        self.count = card["Count"]
        self.TradelistCount = card["Tradelist Count"]
        self.name = card["Name"]
        self.edition = card["Edition"]
        self.condition  = card["Condition"]
        self.language = card["Language"]
        self.foil = card["Foil"]
        self.tags = card["Tags"]
        self.lastModified = card["Last Modified"]
        self.collectorNumber = card["Collector Number"]
        self.alter = card["Alter"]
        self.proxy = card["Proxy"]
        self.purchasePrice = card["Purchase Price"]
        self.generateCardData()

    def generateCardData(self):
        self.cardInfo = search_card(self.name)

class collection:
    def __init__(self):
        self.cards = {}
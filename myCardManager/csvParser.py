# holy pandas # make this into a class/function
import pandas as pd
from pathlib import Path
from scryfallAPI import search_card
import csv
from cardClasses import *
"""
myCards = []

# need to implement  windows / mac path solution (pathlib)
with open('myCardManager/binder/collection.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        myCards.append(row)
"""

collectionPath = Path('myCardManager/binder/collection.csv')
storedCollectionPath = Path('myCardmanager/binder/scriptCollection.json')


# initial collection build
if True:
    myCollection = Collection()

    myCollection.load_from_csv(collectionPath)

    myCollection.save_to_json(storedCollectionPath)

collection = Collection()
collection.load_from_json(storedCollectionPath) # yes this is like instant!

cards = collection.cards

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
# initial collection build
if False:
    load_from_csv('myCardManager/binder/collection.csv')

    myCollection.save_to_json("myCardmanager/binder/scriptCollection.json")

newCollection = Collection()
newCollection.load_from_json("myCardmanager/binder/scriptCollection.json") # yes this is like instant!


    


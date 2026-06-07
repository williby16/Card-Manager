# holy pandas # make this into a class/function
import pandas as pd
from pathlib import Path
from scryfallAPI import search_card
import csv
import cardClasses

myCards = []

with open('myCardManager\\binder\\collection.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        myCards.append(row)

thisCard = cardClasses.baseCard(myCards[0])
print(thisCard.cardInfo)

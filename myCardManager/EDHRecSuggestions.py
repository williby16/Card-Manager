from pyedhrec import EDHRec
import pandas as pd

edhrec = EDHRec()

suggestedCollectionSynergy = ""

def format_to_mox(df, tag=""):
    myRet = ""
    if tag != "":
        tag = "#" + tag
    for i, row in df.iterrows():
        foil = ""
        if row["Foil"] == "foil":
            foil = "*F*"
        myRet += f'{row["Count"]} {row["Name"]} ({row["Edition"]}) {row["Collector Number"]} {foil} {tag}\n'
    return myRet

def get_owned_synergetic(edhTypes):
    suggestedCards = pd.DataFrame()
    for cardType in edhTypes:
        thisType = list(cardType.keys())
        if len(thisType) > 0:
            thisType = thisType[0] # if not top card of a type, it will return an empty dict.
            #print(f"-----  {thisType} -----")
            for suggestion in cardType[thisType]:
                suggestion = suggestion["name"]
                if (suggestion not in cardsInDeck) and (suggestion in ownedCards):
                    #print(suggestion)
                    suggestedCards = pd.concat([suggestedCards, collection.loc[collection['Name'] == suggestion]], ignore_index=True)
    return suggestedCards

collection = pd.read_csv("binders/entire.csv")
deck = pd.read_csv("binders/eshki.csv")
commander = "Eshki, Temur's Roar"

#test 2
deck = pd.read_csv("binders/venom.csv")
commander = "Eddie Brock"

cardsInDeck = deck["Name"].to_list()
ownedCards = collection["Name"].to_list()

# Get combos for a card
combos = edhrec.get_card_combos(commander)

# Get commander data 
#commander_data = edhrec.get_commander_data(commander)

# Get cards commonly associated with a commander
commander_cards = edhrec.get_commander_cards(commander)

# Get the average decklist for a commander
avg_deck = edhrec.get_commanders_average_deck(commander)

# Get known deck lists for a commander
commander_decks = edhrec.get_commander_decks(commander)

# This library provides several methods to get specific types of recommended cards
new_cards = edhrec.get_new_cards(commander)
high_synergy_cards = edhrec.get_high_synergy_cards(commander)

# Get all top cards
top_cards = edhrec.get_top_cards(commander)

# Get specific top cards by type
top_creatures = edhrec.get_top_creatures(commander)
top_instants = edhrec.get_top_instants(commander)
top_sorceries = edhrec.get_top_sorceries(commander)
top_enchantments = edhrec.get_top_enchantments(commander)
top_artifacts = edhrec.get_top_artifacts(commander)
top_mana_artifacts = edhrec.get_top_mana_artifacts(commander)
top_battles = edhrec.get_top_battles(commander)
top_planeswalkers = edhrec.get_top_planeswalkers(commander)
top_utility_lands = edhrec.get_top_utility_lands(commander)
top_lands = edhrec.get_top_lands(commander)


# get top synergy cards in collection
top_of_type = [top_creatures, top_instants, top_sorceries, top_enchantments, top_artifacts, top_mana_artifacts, top_battles, top_planeswalkers, top_utility_lands, top_lands]

suggestedCards = get_owned_synergetic(top_of_type)
suggestedCollectionSynergy += format_to_mox(suggestedCards)

suggestedCards = get_owned_synergetic([high_synergy_cards])
suggestedCollectionSynergy += format_to_mox(suggestedCards)

# implemnt combos

with open(f"output/suggestions_{commander}.csv", "w") as f:
    f.write(suggestedCollectionSynergy)
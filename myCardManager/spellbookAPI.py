import requests
import json

class Combo: # parse out the json of a combo into a single object! # write this out more later lol
    # TODO implement me </3
    def __init__(self, comboJson):
        self.usesNames = []
        for i in comboJson["uses"]:
            self.usesNames.append(i["card"]["name"])

headers = {
    'User-Agent': 'MyMTGApp/0.1 (contact: the.williby@gmail.com)',
    'Accept': '*/*'
}

# Right now, just doing card names, to just display the combo, rather than explain it, which can be added later
# needs error handling!
def get_combos(query):
    # returns a list of combos
    params = {
        "q": query
    }
    response = requests.get("https://backend.commanderspellbook.com/variants/", params=params, headers=headers)
    response.raise_for_status()

    data = response.json()

    # produces a list with JUST THE CARD NAMES used in the combo
    combos = []
    while (1):
        for combo in data["results"]:
            """
            thisCombo = []
            for card in combo["uses"]:
                thisCombo.append(card["card"]["name"]) # maybe can cut this and return all combo info later?
            combos.append(thisCombo)
            """
            combos.append(Combo(combo))
    
        nextData = data["next"]
        if nextData: # the way commanderspellbook does it for a lot of returns, they break it into multiple pages
            data = requests.get(nextData, headers=headers).json()
        else:
            break

    return combos

# find-my-combos # https://backend.commanderspellbook.com/find-my-combos # needs a list of card names (hint: a deck will be a collection!)

def find_my_combos(decklistPayload): # show combos that are already in the deck and potential combos!
    # returns a dict of combos
    """format payload as a dict like:
        "commanders": [
        {
            "card": "Atraxa, Praetors' Voice",
            "quantity": 1
        }
    ],
    "main": [
        {
            "card": "Sol Ring",
            "quantity": 1
        },
    ]}
    """
    response = requests.post(
        "https://backend.commanderspellbook.com/find-my-combos",
        json=decklistPayload,
        headers=headers
    )
    response.raise_for_status()

    data = response.json()

    # need to parse out all of these
    combos = {
    "included": [],
    "includedByChangingCommanders": [],
    "almostIncluded": [],
    "almostIncludedByAddingColors": [],
    "almostIncludedByChangingCommanders": [],
    "almostIncludedByAddingColorsAndChangingCommanders": []
    }

    print(data["results"].keys())

    while (1):
        for types in list(data["results"].keys()):
            if types == "identity":
                continue
            for combo in data["results"][types]:
                combos[types].append(Combo(combo))
    
        nextData = data["next"]
        if nextData: # the way commanderspellbook does it for a lot of returns, they break it into multiple pages
            data = requests.get(nextData, headers=headers).json()
        else:
            break
    return combos

#example input
find_my_combos(
{
    "commanders": [
        {
            "card": "Atraxa, Praetors' Voice",
            "quantity": 1
        }
    ],
    "main": [
        {
            "card": "Sol Ring",
            "quantity": 1
        },
        {
            "card": "Doubling Season",
            "quantity": 1
        },
        {
            "card": "Hullbreaker Horror",
            "quantity": 1
        }
    ]
}
    )


# estimate-bracket # https://backend.commanderspellbook.com/estimate-bracket  # maybe

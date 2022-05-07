import json

def __load_file(path : str):
    with open(path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

def __parse_entry(entry):
    x = {}
    x["id"] = entry["id"]
    x["productName"] = entry["productName"]
    x["brand"] = entry["brand"]["name"]
    x["currentRetailPrice"] = entry["_embedded"]["articles"][0]["_embedded"]["listing"]["pricing"]["currentRetailPrice"] / 100
    x["currency"] = entry["_embedded"]["articles"][0]["_embedded"]["listing"]["pricing"]["currency"]
    
    if "grammage" in entry["_embedded"]["articles"][0]["_embedded"]["listing"]["pricing"]:
        x["grammage"] = entry["_embedded"]["articles"][0]["_embedded"]["listing"]["pricing"]["grammage"]

    if "basePrice" in entry["_embedded"]["articles"][0]["_embedded"]["listing"]["pricing"]:
        x["basePrice"] = entry["_embedded"]["articles"][0]["_embedded"]["listing"]["pricing"]["basePrice"] / 100

        for k in entry["_embedded"]["articles"][0]["_embedded"]["listing"]["pricing"]["baseUnit"]:
            x["baseUnit"] = str(k)

    return x
    
def get_base_units():
    return [
        {"baseUnit" : "G", "amount" : 100},
        {"baseUnit" : "KG", "amount" : 1},
        {"baseUnit" : "L", "amount" : 1},
        {"baseUnit" : "ML", "amount" : 100}
    ]

def __get_sql_tuple(entry):
    x = __parse_entry(entry)
    t = (
        x["id"],
        x["productName"],
        x["brand"],
        x["currentRetailPrice"],
        x["currency"],
        x["grammage"] if "grammage" in x else None,
        x["basePrice"] if "basePrice" in x else None,
        x["baseUnit"] if "baseUnit" in x else None
    )
    return t

def get_all_sql_tuples(filepath):
    data = __load_file(filepath)

    return map(__get_sql_tuple, data)
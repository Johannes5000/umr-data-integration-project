import json
import re

def __load_file(path : str):
    with open(path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

# Rewe products
def __parse_entry(entry):
    x = {}
    x["id"] = entry["id"]
    x["product_name"] = entry["productName"]
    x["brand"] = entry["brand"]["name"]
    x["current_retail_price"] = entry["_embedded"]["articles"][0]["_embedded"]["listing"]["pricing"]["currentRetailPrice"] / 100
    x["currency"] = entry["_embedded"]["articles"][0]["_embedded"]["listing"]["pricing"]["currency"]

    if "grammage" in entry["_embedded"]["articles"][0]["_embedded"]["listing"]["pricing"]:
        grammage = entry["_embedded"]["articles"][0]["_embedded"]["listing"]["pricing"]["grammage"]
        grammage = re.sub(r"\s\(.+\)", '', grammage) # remove base price infos

        # extract and delete number_of_items if present
        r = re.search(r"\d+(?=x)", grammage) # Schreibweise 1
        if r: 
            x["number_of_items"] = int(r.group(0))
            grammage = re.sub(r"\d+x", '', grammage)
        r = re.search(r"\d+(?=\sStück\sca.\s)", grammage) # Schreibweise 2
        if r:
            x["number_of_items"] = int(r.group(0))
            grammage = re.sub(r"\d+\sStück\sca.\s", '', grammage)
            x["unit"] = "Stück"

        # extract and delete unit if present
        u = re.search(r"((?<=\d)(ml|l|g|kg|m(?!l)|Stück))|((?<=\d\s)(ml|l|g|kg|m(?!l)|Stück))", grammage)
        if u:
            x["unit"] = u.group(0)
            grammage = re.sub(r"(?<=\d)\s?(ml|l|g|kg|m(?!l)|Stück)", '', grammage)
        
        x["amount"] = float(grammage.replace(',', '.')) if ',' in grammage else int(grammage)
    
    if "basePrice" in entry["_embedded"]["articles"][0]["_embedded"]["listing"]["pricing"]:
        x["base_price"] = entry["_embedded"]["articles"][0]["_embedded"]["listing"]["pricing"]["basePrice"] / 100
        for k in entry["_embedded"]["articles"][0]["_embedded"]["listing"]["pricing"]["baseUnit"]: # json array, therefore for
            x["base_unit"] = str(k)

    return x

def __get_sql_tuple(entry):
    x = __parse_entry(entry)
    t = (
        x["id"],
        x["product_name"],
        x["brand"],
        x["current_retail_price"],
        x["currency"],
        x["number_of_items"] if "number_of_items" in x else 1,
        x["amount"] if "amount" in x else None,
        x["unit"] if "unit" in x else None,
        x["base_price"] if "base_price" in x else None,
        x["base_unit"] if "base_unit" in x else None
    )
    return t

def get_all_sql_tuples(filepath):
    data = __load_file(filepath)
    return map(__get_sql_tuple, data)

# Base units of Rewe products
def get_base_units():
    return [
        {"base_unit" : "G", "amount" : 100},
        {"base_unit" : "KG", "amount" : 1},
        {"base_unit" : "L", "amount" : 1},
        {"base_unit" : "ML", "amount" : 100},
        {"base_unit" : "M", "amount" : 1} # meter
    ]

def __unit_to_tuple(entry):
    return (entry["base_unit"], entry["amount"])

def get_base_units_as_tuples():
    return map(__unit_to_tuple, get_base_units())
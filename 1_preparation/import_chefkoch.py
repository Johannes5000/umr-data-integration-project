import json
#import re

def __load_file(path : str):
    with open(path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

# chefkoch recipes
def __parse_entry(entry):
    x = {}
    x["recipe_name"] = entry["name"]
    # x["recipe_id"] = entry["id"]
    x["category"] = entry["category"]["title"]
    for k in entry["ingredients"][0]:
        x["ingredient_name"] = entry["ingredients"][0]["name"] #TODO Wie bekomme ich mehrere Einträge für ingredient_name und amount
        x["amount"] = entry["ingredients"][0]["amount"]

    return x

def __get_sql_tuple(entry):
    x = __parse_entry(entry)
    t = (
        x["recipe_name"],
        # x["recipe_id"],
        x["category"],
        x["ingredient_name"],
        x["amount"]
    )
    return t

def get_all_sql_tuples(filepath):
    data = __load_file(filepath)
    return map(__get_sql_tuple, data)

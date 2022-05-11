import json
import re

# flatens the given array t
def __flatten_array(t):
    return [item for sublist in t for item in sublist]

def __load_file(path : str):
    with open(path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

# chefkoch recipes
def __parse_entry_to_ingredients(entry):
    arr = []
    for i in entry["ingredients"]:
        x = {}
        x["recipe_id"] = entry["id"]
        x["ingredient_name"] = i["name"]

        amount = i["amount"]
        # extract and delete additional remarks / comments
        r = re.search(r"(?<=,\s).*", amount) 
        if r: 
            x["comment"] = r.group(0)
            amount = re.sub(r",\s.*", '', amount)
        # extract and delete unit
        r = re.search(r"(?<=(\d\s)|([¼¾½⅛]\s))[^¼½⅛¾]+", amount) 
        if r: 
            x["unit"] = r.group(0)
            amount = re.sub(r"(?<=(\d)|([¼½⅛¾]))\s[^¼½¾⅛]+", '', amount)
        # replace ¼ and ½ and ¾ and ⅛
        r = re.search(r"[½¼⅛¾]", amount) 
        if r: 
            amount = re.sub(r"\s?½+", '.5', amount)
            amount = re.sub(r"\s?¼+", '.25', amount)
            amount = re.sub(r"\s?¾+", '.75', amount)
            amount = re.sub(r"\s?⅛+", '.125', amount)
        # extract and delete n. B.
        r = re.search(r"n\.\sB\.|etwas|evtl\.|einige|viel|wenig|mehr|ml|Scheibe/n|Msp\.|Paar|extra|Stiel\/e", amount) # Ja, Scheibe/n kommt bei Salz Pfeffer als Menge vor ... :/
        if r: 
            x["comment"] = r.group(0)
            amount = ""
        # delete only unit with no number
        r = re.search(r"Prise\(n\)|EL|Pck\.|TL|kl\.\sBund|Schuss|Bund|Liter|Spritzer|Handvoll|Prise(?=n)|Glas", amount)
        if r:
            amount = "1"
            x["unit"] = r.group(0)
        # delete Stück equivilent units
        r = re.search(r"dünne|Zweig\/e|halbe|Blätter|Würfel|g|Zehe\/n", amount)
        if r:
            amount = "1"
            x["unit"] = "Stück"
        # replace , with .
        amount = re.sub(r"(?<=\d),(?=\d)", '.', amount)

        try:
            x["amount"] = float(amount) if len(amount) > 0 else None
        except:
            print('Error parsing amount "' + amount + '"!')
            amount = ""

        arr.append(x)
    return arr

def __parse_entry_to_recipe(entry):
    x = {}
    x["recipe_id"] = entry["id"]
    x["recipe_name"] = entry["name"]
    x["category"] = entry["category"]["title"]
    return x

def __get_recipe_sql_tuple(entry):
    x = __parse_entry_to_recipe(entry)
    t = (
        x["recipe_id"],
        x["recipe_name"],
        x["category"],
        x["recipe_id"], # doppelt für die Überprüfung beim Einfügen
    )
    return t

def __get_ingredient_sql_tuple(entry):
    arr = []
    x = __parse_entry_to_ingredients(entry)
    for i in x:
        arr.append((
            i["recipe_id"],
            i["ingredient_name"],
            i["amount"] if "amount" in i else None,
            i["unit"] if 'unit' in i else None,
            i["comment"] if 'comment' in i else None,
            i["recipe_id"], # doppelt für die Überprüfung beim Einfügen
            i["ingredient_name"], # doppelt für die Überprüfung beim Einfügen
        ))
    return arr

def get_all_ingredients_sql_tuples(filepath):
    data = __load_file(filepath)
    return __flatten_array(map(__get_ingredient_sql_tuple, data))

def get_all_recipes_sql_tuples(filepath):
    data = __load_file(filepath)
    return map(__get_recipe_sql_tuple, data)
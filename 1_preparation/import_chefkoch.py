import json

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
        x["amount"] = i["amount"]
        x["unit"] = "TODO" ########################### TODO ##################################
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
    )
    return t

def __get_ingredient_sql_tuple(entry):
    arr = []
    x = __parse_entry_to_ingredients(entry)
    for i in x:
        arr.append((
            i["recipe_id"],
            i["ingredient_name"],
            i["amount"],
            i["unit"],
        ))
    return arr

def get_all_ingredients_sql_tuples(filepath):
    data = __load_file(filepath)
    return __flatten_array(map(__get_ingredient_sql_tuple, data))

def get_all_recipes_sql_tuples(filepath):
    data = __load_file(filepath)
    return map(__get_recipe_sql_tuple, data)
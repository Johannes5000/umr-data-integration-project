import re
import json
import psycopg2
from config import *
import py_stringmatching as sm
from queue import PriorityQueue
import time
from postgres_to_json import *

# Setzte diesen Wert auf True, falls keine Postgres Anbindung besteht, 
# dann werden die angegebenen JSON Dateien aus postgres_to_json.py benutzt
USE_JSON_FILES_INSTEAD_OF_POSTGRES = True

def connect():
    return psycopg2.connect(**config())

def __get_file_content_as_string(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read().replace('\n', ' ')

def __write_data_to_file(data : str):
    with open(INGREDIENTS_PRODUCTS_MAPPING_FILEPATH, "w", encoding='utf-8') as outfile:
        outfile.write(data)
    
def __append_data_to_file(data : str):
    with open(INGREDIENTS_PRODUCTS_MAPPING_FILEPATH, "a", encoding='utf-8') as outfile:
        outfile.write(data)

def __append_json_to_file(data : json):
    with open(INGREDIENTS_PRODUCTS_MAPPING_FILEPATH, "a", encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

# Tabellen erstellen
def create_tables(cur):
    print('Creating Tables ...', end = ' ', flush=True)
    cur.execute(__get_file_content_as_string(SQL_CREATE_TABLES_FILEPATH))
    print('FINISHED')

# Liest aus der Datenbank alle Ingredients aus
def get_ingredients_array_from_postgres(cur):
    cur.execute("select distinct ingredient_name, unit from ingredients limit 10;")
    ingredients = cur.fetchall()
    # print(ingredients)
    return ingredients

# Liest aus der Datenbank alle Produkte aus
def get_products_array_from_postgres(cur):
    cur.execute("select distinct product_name, unit from products order by product_name;")
    products = cur.fetchall()
    # print(products)
    return products

def write_ingredient_with_product_in_database(cur, tuple):
    cur.execute(""" INSERT INTO ingredients_with_rewe_products (ingredient_name, product_name)
                    values (%s, %s);
                """, tuple)

# Gibt ein Array von Produkten zurück, die dem ersten Token der Zutat am ähnlichsten sind.
# Unter diesen Produkten kann man dann nochmal mit allen Tokens nach dem besten suchen.
# Die erhaltenen Produkte sind also Kandidaten für eine genauere Suche.
def get_best_matching_products_with_first_token(ingredient, products, monge_elkan, max_size, delta):
    best_sim_value = 0
    best_products = []

    q = PriorityQueue(max_size + 1) 
    # +1 weil wir ja immer eins hinzufügen und dann ein Platz nicht aussagekräftig ist

    ingredient_tokens = re.split(r'[\s\(\)\!\-\_\.\,]', ingredient[0])
    ingredient_first_token = ingredient_tokens[0]

    for p in products:
        product_tokens = re.split(r'[\s\(\)\!\-\_\.\,]', p[0])
        res = monge_elkan.get_raw_score([ingredient_first_token], product_tokens)

        if q.full():
            q.get() # entferne das Produkt mit der niedrigsten Ähnlichkeit
        q.put((res, p))

        if (res >= best_sim_value):
            best_sim_value = res
    
    q.get() # niedrigstes Entfernen, da immer hinzugefügt wurde --> nicht repräsentativ
    required_similarity = best_sim_value * (1 - delta)
    while not q.empty():
        next_item = q.get()
        if next_item[0] > required_similarity: 
            best_products.insert(0, next_item[1])

    return best_products


def get_best_matching_product(ingredient, products, monge_elkan):
    best_sim = 0
    best_product = None
    ingredient_tokens = re.split(r'[\s\(\)\!\-\_\.\,]', ingredient[0])

    for p in products:
        product_tokens = re.split(r'[\s\(\)\!\-\_\.\,]', p[0])
        res = monge_elkan.get_raw_score(ingredient_tokens, product_tokens)
        if (res >= best_sim):
            best_sim = res
            best_product = p
    return best_product

def __match_ingredient(ingredient, products, me):
    print("Mapping ingredient " + ingredient[0] + " ...", end = ' ', flush=True)

    x = {}
    product_candidates = get_best_matching_products_with_first_token(ingredient, products, me, 10, 0.05)
    matching_product = get_best_matching_product(ingredient, product_candidates, me)

    x["ingredient_name"] = ingredient[0]
    x["product_name"] = matching_product[0]

    return x

def write_matched_ingredients_to_file(ingredients, products):
    me = sm.MongeElkan()

    length = len(ingredients)
    current = 1

    __write_data_to_file("[")
    for i in ingredients:
        print("Mapping ingredient " + i[0] + " ...", end = ' ', flush=True)

        x = __match_ingredient(i, products, me)

        if current != 1:
            __append_data_to_file(",")
        __append_json_to_file(x)

        print("FINISHED " + str(round(100 * (current / length), 2)) + "%")
        current += 1
    __append_data_to_file("]")

def write_matched_ingredients_to_postgres(ingredients, products, cur):
    me = sm.MongeElkan()

    length = len(ingredients)
    current = 1

    for i in ingredients:
        print("Mapping ingredient " + i[0] + " ...", end = ' ', flush=True)

        x = __match_ingredient(i, products, me)

        write_ingredient_with_product_in_database(cur, (
            x["ingredient_name"],
            x["product_name"]
        ))

        print("FINISHED " + str(round(100 * (current / length), 2)) + "%")
        current += 1


if __name__ == '__main__':
    ingredients = None
    products = None
    conn = None
    cur = None

    if USE_JSON_FILES_INSTEAD_OF_POSTGRES:
        ingredients = read_ingredient_names_from_json_file()
        products = read_product_names_from_json_file()

        start = time.time()
        write_matched_ingredients_to_file(ingredients, products)
        end = time.time()
        total_time = end - start
        print("\n"+ str(round(total_time,2)))
    else:
        try:
            conn =  connect()
            cur = conn.cursor()

            create_tables(cur)

            ingredients = get_ingredients_array_from_postgres(cur)
            products = get_products_array_from_postgres(cur)

            start = time.time()
            write_matched_ingredients_to_postgres(ingredients, products, cur)
            end = time.time()
            total_time = end - start
            print("\n"+ str(round(total_time,2)))
        except (psycopg2.DatabaseError) as error:
            print('Database Exception: ' + str(error))
        except (Exception) as error:
            print(error)
        finally:
            if conn is not None:
                if cur is not None:
                    cur.close()
                    conn.commit()
                conn.close()
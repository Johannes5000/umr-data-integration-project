
# Diese Funktionen sind ausschließlich dazu gedacht, 
# die Funktion des Programms ohne aktive PostgreSQL anbindung zu gewährleisten.


import json
import psycopg2
from config import *


def __connect():
    return psycopg2.connect(**config())

def __write_data_to_file(data : str, filepath):
    with open(filepath, "w", encoding='utf-8') as outfile:
        outfile.write(data)
    
def __append_data_to_file(data : str, filepath):
    with open(filepath, "a", encoding='utf-8') as outfile:
        outfile.write(data)

def __append_json_to_file(data : json, filepath):
    with open(filepath, "a", encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

def write_product_names_to_json_file(cur):
    cur.execute("select distinct product_name, unit from products order by product_name;")
    products = cur.fetchall()
    print("Writing " + str(len(products)) + " products of postgres to file ...", end = ' ', flush=True)
    products = map(lambda product: {"product_name" : product[0], "product_unit" : product[1]}, products)

    __write_data_to_file("[", PRODUCT_NAMES_FILEPATH)
    first = True
    for p in products:
        if first:
            first = False
        else:
            __append_data_to_file(", ", PRODUCT_NAMES_FILEPATH)
        __append_json_to_file(p, PRODUCT_NAMES_FILEPATH)
    __append_data_to_file("]", PRODUCT_NAMES_FILEPATH)
    print("FINISHED")

def write_ingredient_names_to_json_file(cur):
    cur.execute("select distinct ingredient_name, unit from ingredients limit 3;")
    ingredients = cur.fetchall()
    print("Writing " + str(len(ingredients)) + " ingredients of postgres to file ...", end = ' ', flush=True)
    ingredients = map(lambda ingredient: {"ingredient_name" : ingredient[0], "ingredient_unit" : ingredient[1]}, ingredients)

    __write_data_to_file("[", INGREDIENT_NAMES_FILEPATH)
    first = True
    for i in ingredients:
        if first:
            first = False
        else:
            __append_data_to_file(", ", INGREDIENT_NAMES_FILEPATH)
        __append_json_to_file(i, INGREDIENT_NAMES_FILEPATH)
    __append_data_to_file("]", INGREDIENT_NAMES_FILEPATH)
    print("FINISHED")

def __load_file(path : str):
    with open(path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

def read_ingredient_names_from_json_file():
    return __load_file(INGREDIENT_NAMES_FILEPATH)

def read_product_names_from_json_file():
    return __load_file(PRODUCT_NAMES_FILEPATH)

if __name__ == '__main__':
    conn = None
    cur = None
    try:
        conn =  __connect()
        cur = conn.cursor()

        write_product_names_to_json_file(cur)
        write_ingredient_names_to_json_file(cur)

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
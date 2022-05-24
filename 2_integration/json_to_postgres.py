
# Diese Funktionen sind ausschließlich dazu gedacht, 
# die Funktion des Programms ohne aktive PostgreSQL anbindung zu gewährleisten.


import json
import psycopg2
from config import *

def __connect():
    return psycopg2.connect(**config())

def __get_file_content_as_string(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read().replace('\n', ' ')

# Tabellen erstellen
def create_tables(cur):
    print('Creating Tables ...', end = ' ', flush=True)
    cur.execute(__get_file_content_as_string(SQL_CREATE_TABLES_FILEPATH))
    print('FINISHED')

def __load_file(path : str):
    with open(path, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

def read_ingredient_mappings_from_file_and_insert_to_postgres(cur):
    json_array = __load_file(INGREDIENTS_PRODUCTS_MAPPING_FILEPATH)

    print('Inserting ' + str(len(json_array)) + ' mappings into PostgreSQL ...', end = ' ', flush=True)
    cur.executemany(""" INSERT INTO ingredients_with_rewe_products 
                        (ingredient_name, ingredient_unit, product_name, product_unit, similarity, first_token_similarity) values 
                        (%(ingredient_name)s, %(ingredient_unit)s, %(product_name)s, %(product_unit)s, %(similarity)s, %(first_token_similarity)s);
                    """, json_array)
    print('FINISHED')


if __name__ == '__main__':
    conn = None
    cur = None
    try:
        conn =  __connect()
        cur = conn.cursor()

        create_tables(cur)
        read_ingredient_mappings_from_file_and_insert_to_postgres(cur)

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
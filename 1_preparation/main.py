import psycopg2
from config import config
import import_rewe as rewe
import import_chefkoch as chefkoch

REWE_JSON_FILEPATH = "0_datasets\\rewe.json"
CHEFKOCH_JSON_FILEPATH = "0_datasets\\Hauptspeise\\Dessert.json"

SQL_CREATE_TABLES_FILEPATH = '1_preparation\\sql\\01_create_tables.sql'


def get_file_content_as_string(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read().replace('\n', ' ')

def connect():
    conn = None
    try:
        conn = psycopg2.connect(**config())
        cur = conn.cursor()

        # Tabellen erstellen
        cur.execute(get_file_content_as_string(SQL_CREATE_TABLES_FILEPATH))

        # Rewe Produkte hinzufügen
        cur.executemany("""
                INSERT INTO products (id, product_name, brand, current_retail_price, currency, number_of_items, amount, unit, base_price, base_unit) 
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, rewe.get_all_sql_tuples(REWE_JSON_FILEPATH))

        # add chefkoch recipes
        cur.executemany("""
                INSERT INTO recipes (recipe_id, recipe_name, category)
                values (%s, %s, %s)
            """, chefkoch.get_all_recipes_sql_tuples(CHEFKOCH_JSON_FILEPATH))

        # add chefkoch ingredients
        cur.executemany("""
                INSERT INTO ingredients (recipe_id, ingredient_name, amount, unit)
                values (%s, %s, %s, %s)
            """, chefkoch.get_all_ingredients_sql_tuples(CHEFKOCH_JSON_FILEPATH))

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    connect()

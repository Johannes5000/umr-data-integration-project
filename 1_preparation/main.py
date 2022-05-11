from glob import glob
import psycopg2
from config import config
import import_rewe as rewe
import import_chefkoch as chefkoch

REWE_JSON_FILEPATH = "0_datasets\\rewe.json"
CHEFKOCH_PARENT_FILEPATH = "0_datasets\\Hauptspeise\\"

SQL_CREATE_TABLES_FILEPATH = '1_preparation\\sql\\01_create_tables.sql'


def get_file_content_as_string(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read().replace('\n', ' ')

def get_all_json_filepaths():
    return [f for f in glob(CHEFKOCH_PARENT_FILEPATH + "**/*.json", recursive=True)]

def connect():
    conn = None
    try:
        conn = psycopg2.connect(**config())
        cur = conn.cursor()

        # Tabellen erstellen
        print('Creating Tables ...', end = ' ', flush=True)
        cur.execute(get_file_content_as_string(SQL_CREATE_TABLES_FILEPATH))
        print('FINISHED')

        # Rewe Produkte hinzufügen
        print('Inserting Rewe products ...', end = ' ', flush=True)
        cur.executemany("""
                INSERT INTO products (id, product_name, brand, current_retail_price, currency, number_of_items, amount, unit, base_price, base_unit) 
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, rewe.get_all_sql_tuples(REWE_JSON_FILEPATH))
        print('FINISHED')

        for file in get_all_json_filepaths():
            print('Inserting chefkoch recipes from ' + file + ' ...', end = ' ', flush=True)

            # add chefkoch recipes
            cur.executemany("""
                    INSERT INTO recipes (recipe_id, recipe_name, category)
                    (select %s, %s, %s where not exists (select recipe_id from recipes where recipe_id = %s))
                """, chefkoch.get_all_recipes_sql_tuples(file))

            # add chefkoch ingredients
            cur.executemany("""
                    INSERT INTO ingredients (recipe_id, ingredient_name, amount, unit, comment)
                    (select %s, %s, %s, %s, %s where not exists (select recipe_id from ingredients where recipe_id = %s and ingredient_name = %s))
                """, chefkoch.get_all_ingredients_sql_tuples(file))
            print('FINISHED')

        print('Finished inserting!')

        cur.close()
        conn.commit()
    except (psycopg2.DatabaseError) as error:
        print('Database Exception: ' + error)
    except (Exception) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    connect()

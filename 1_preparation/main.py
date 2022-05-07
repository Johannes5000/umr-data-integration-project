import psycopg2
from config import config
import import_rewe as rewe

REWE_JSON_FILEPATH = "0_datasets\\rewe.json"

def connect():
    conn = None
    try:
        conn = psycopg2.connect(**config())
        cur = conn.cursor()

        # Rewe Produkte hinzufügen   
        cur.executemany("""
                INSERT INTO products (id, productName, brand, currentRetailPrice, currency, grammage, basePrice, baseUnit) 
                values (%s, %s, %s, %s, %s, %s, %s, %s)
            """, rewe.get_all_sql_tuples(REWE_JSON_FILEPATH))

        # Rewe Basiseinheiten hinzufügen
        cur.executemany("""
                INSERT INTO base_units (baseUnit, amount) 
                values (%s, %s)
            """, rewe.get_base_units_as_tuples())

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    connect()

import psycopg2
from config import config
import import_rewe as rewe

def connect():
    conn = None
    try:
        conn = psycopg2.connect(**config())
        cur = conn.cursor()

        cur.executemany("""
                INSERT INTO products (id, productName, brand, currentRetailPrice, currency, grammage, basePrice, baseUnit) 
                values (%s, %s, %s, %s, %s, %s, %s, %s)
            """, rewe.get_all_sql_tuples("0_datasets\\rewe.json"))

        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    connect()

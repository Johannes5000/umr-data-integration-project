import psycopg2
from config import config

SQL_CREATE_TABLES_FILEPATH = '3_cleaning\\sql\\01_create_tables.sql'

def get_file_content_as_string(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read().replace('\n', ' ')

def connect():
    conn = None
    try:
        conn = psycopg2.connect(**config())
        cur = conn.cursor()

        # Tabellen erstellen
        print('Creating Tables ...', end = ' ', flush=True)
        cur.execute(get_file_content_as_string(SQL_CREATE_TABLES_FILEPATH))
        print('FINISHED')

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

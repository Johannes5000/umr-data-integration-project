import psycopg2
from config import config
from os import listdir
from os.path import isfile, join

SQL_FOLDER_PATH = '3_showcase/sql'

def get_file_content_as_string(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read().replace('\n', ' ')

def execute_sql_files(path, cur):
    paths = [path + "/" + f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".sql")]
    for p in paths:
        print('Executing ' + p + ' ...', end = ' ', flush=True)
        # print(get_file_content_as_string(p))
        cur.execute(get_file_content_as_string(p))
        print('FINISHED')

def connect():
    conn = None
    try:
        conn = psycopg2.connect(**config())
        cur = conn.cursor()

        # SQL Dateien ausführen
        execute_sql_files(SQL_FOLDER_PATH, cur)

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

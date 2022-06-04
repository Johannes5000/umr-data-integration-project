# 2_integration

## Abhängigkeiten
- [psycopg2](https://pypi.org/project/psycopg2/)
- [py_stringmatching](https://pypi.org/project/py-stringmatching/)
- [eine PostgreSQL Datenbank (z.B. lokal)](https://www.postgresql.org/download/)

## Installation

### Mit aktiver PostgreSQL Datenbank
1.  Erstelle auf oberster Ebene eine Datei `database.ini`. Diese soll entsprechend der Vorlage die Hostadresse (und Port, falls dieser vom Standart 5432 abweicht), die Datenbank, Nutzer und Passwort beinhalten.
2.  Füge gemäß [Schritt 1](../1_preparation/README.md) alle Daten in die Datenbank ein.
3.  Setze `USE_JSON_FILES_INSTEAD_OF_POSTGRES` in der Datei `main.py` auf `False`.
4.  Führe `main.py` aus.


### Ohne aktiver PostgreSQL Datenbank (Mit json Dateien)
1.  Lade die beiden Startdateien von der Hessenbox herunter und füge sie unter folgenden Pfaden ein.
    - `2_integration\ingredient_names.json`
    - `2_integration\product_names.json`
2.  Setze `USE_JSON_FILES_INSTEAD_OF_POSTGRES` in der Datei `main.py` auf `True`. Somit wird keine aktive Datenbank benötigt und die Werte werden aus den beiden Dateien eingelesen und am Ende unter dem Pfad `2_integration\ingredients_products_mapping.json` gespeichert.
3.  Führe `main.py` aus.


## Extraktion der Startwerte aus der Datenbank
1.  Erstelle auf oberster Ebene eine Datei `database.ini`, falls diese noch nicht existiert. Diese soll entsprechend der Vorlage die Hostadresse (und Port, falls dieser vom Standart 5432 abweicht), die Datenbank, Nutzer und Passwort beinhalten.
2.  Füge gemäß [Schritt 1](../1_preparation/README.md) alle Daten in die Datenbank ein, falls diese noch nicht enthalten sind.
3.  Führe die Datei `2_integration\postgres_to_json.py` aus.

Die Ergebnisse werden in den folgenden Pfaden abgespeichert.
- `2_integration\ingredient_names.json`
- `2_integration\product_names.json`


## Integration der Ergebnisse in die Datenbank
1.  Speichere die Ergebnisdatei unter dem Pfad `2_integration\ingredients_products_mapping.json` ab. 
2.  Erstelle auf oberster Ebene eine Datei `database.ini`, falls diese noch nicht existiert. Diese soll entsprechend der Vorlage die Hostadresse (und Port, falls dieser vom Standart 5432 abweicht), die Datenbank, Nutzer und Passwort beinhalten.
3.  Führe die Datei `2_integration\json_to_postgres.py` aus.

## Ergebnisse in PostgreSQL anzeigen lassen
Das gefundene Mapping kann mit dem SQL Befehl 
```sql
select * from view_integrated_data;
```
angezeigt werden.
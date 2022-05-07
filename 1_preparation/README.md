# 1_preparation

## Abhängigkeiten (Python)
- [psycopg2](https://pypi.org/project/psycopg2/)
- [eine PostgreSQL Datenbank (z.B. lokal)](https://www.postgresql.org/download/)

## Installation
-  Erstelle auf oberster Ebene eine Datei `database.ini`. Diese soll entsprechend der Vorlage die Hostadresse (und Port, falls dieser vom Standart 5432 abweicht), die Datenbank, Nutzer und Passwort beinhalten.
-  Erzeuge gemäß der Datei `1_preparation\sql\01_create_tables.sql` die entsprechenden Tabellen.
-  Füge die Datensätze aus der Hessenbox in den Ordner `0_datasets` ein. Gehe dabei sicher, dass die in der `main.py` angegebenen Dateipfade zu den Datensätzen passen.
-  Führe `main.py` aus.
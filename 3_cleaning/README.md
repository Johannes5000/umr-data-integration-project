# 3_cleaning

## Abhängigkeiten
- [psycopg2](https://pypi.org/project/psycopg2/)
- [eine PostgreSQL Datenbank (z.B. lokal)](https://www.postgresql.org/download/)

## Datenreinigung
1.  Integriere gemäß [Schritt 2](../2_integration/README.md) alle Daten.
2.  Führe `main.py` aus, um die Daten reinigen zu lassen. Dabei werden zusätzliche Views erstellt.

## Ergebnisse in PostgreSQL anzeigen lassen
Das gefundene Mapping kann mit dem SQL Befehl 
```sql
select * from view_integrated_data;
```
angezeigt werden.
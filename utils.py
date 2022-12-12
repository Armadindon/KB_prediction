from os.path import exists
import sqlite3

database_exist = exists("database/data.db")
conn = sqlite3.connect("database/data.db")

# If the database wasn't existing before, we create it and supply it some data to start
if not database_exist:
    # On ajoute la structure de base
    with open("database/init.sql") as init_script:
        conn.executescript(init_script.read())

    # On ajoute les données de bases
    with open("database/initial_values.txt") as initial_values:
        names = initial_values.read().splitlines()
        for name in names:
            conn.execute(f"INSERT INTO knowledge_base(name, trust_level) VALUES ('{name.upper()}', 0.5)")
        
        conn.commit()

conn.close()

def get_connection():
    return sqlite3.connect("database/data.db")

def search(search_string):
    cur = get_connection().cursor()
    cur.execute(f"SELECT name FROM knowledge_base WHERE name LIKE '%{search_string.upper()}%' ORDER BY trust_level DESC;")

    return cur.fetchall()



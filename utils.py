from os.path import exists
import sqlite3

# GLOBAL VARIABLE
pk_threshold = 0.5
pk_min = 0.2
pk_new_increasing = 0.1
pk_new_decreasing = 0.2

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
            conn.execute(f"INSERT INTO knowledge_base(name, trust_level) VALUES ('{name.upper()}', {pk_threshold})")
        
        conn.commit()

conn.close()

def get_connection():
    return sqlite3.connect("database/data.db")

def search(search_string):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT name FROM knowledge_base WHERE name LIKE '%{search_string.upper()}%' ORDER BY trust_level DESC;")
    results = cur.fetchall()
    conn.close()
    return results


def add_name(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO knowledge_base(name, trust_level) VALUES ('{name.upper()}', {pk_threshold});")
    conn.commit()
    conn.close()

"""
Utility function, will do several things:
  - Add the name if it doesnt exist
  - Update is Pk otherwise
  - Update all others pk
  - Do a database cleaning (deleting all the entries with a Pk < 0.2)
"""
def update_database(chosen, names_to_update):
    conn = get_connection()
    cursor = conn.cursor()
    
    # We check if the entry is in the database
    cursor.execute(f"SELECT * FROM knowledge_base WHERE name = '{chosen.upper()}';")
    result = cursor.fetchall()

    # Add the name
    if len(result) == 0:
        add_name(chosen)
    # Update the name
    else:
        names_to_update.remove(chosen)
        # If i understood well, pk_new is the same as pk_old in the formula since we have chosen this entry
        pk_bis = result[0][2] + (1-result[0][2]) * pk_new_increasing
        cursor.execute(f"UPDATE knowledge_base SET trust_level = {pk_bis} WHERE id = {result[0][0]};")
    
    
    # Update all names
    names_to_update = [f"'{name}'".upper() for name in names_to_update]
    cursor.execute(f"UPDATE knowledge_base SET trust_level = trust_level - (1 - trust_level) * {pk_new_decreasing} WHERE name in ({','.join(names_to_update)});")
    
    # clean database
    cursor.execute(f"DELETE FROM knowledge_base WHERE trust_level < {pk_min};")
    
    # Commit all changes to the database
    conn.commit()





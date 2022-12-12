from os.path import exists
import sqlite3

database_exist = exists("database/data.db")
con = sqlite3.connect("database/data.db")

# If the database wasn't existing before, we create it and supply it some data to start
if not database_exist:
    # On ajoute la structure de base
    with open("database/init.sql") as init_script:
        con.executescript(init_script.read())

    # On ajoute les données de bases
    with open("database/initial_values.txt") as initial_values:
        names = initial_values.readlines()
        for name in names:
            con.execute(f"INSERT INTO knowledge_base(name, trust_level) VALUES ('{name.capitalize()}', 0.5)")
        
        con.commit()



import sqlite3

conn = sqlite3.connect('dati.db')
c = conn.cursor()


c.execute("""
CREATE TABLE IF NOT EXISTS rezultati (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vards TEXT,
    meginajumi INTEGER,
    laiks REAL,
    limenis INTEGER
)
""")

conn.commit()
conn.close()

print("Izveidots!")

import sqlite3

conn = sqlite3.connect('dati.db')
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS rezultati (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vards TEXT,
    kliksk iINTEGER,
    laiks REAL,
    datums TEXT
)
""")

conn.commit()
conn.close()

print("Tabelle erstellt!")
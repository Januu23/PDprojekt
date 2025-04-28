import sqlite3

# Verbindet sich mit dati.db (wird erstellt, falls nicht vorhanden)
conn = sqlite3.connect('dati.db')
c = conn.cursor()

# Erstellt Tabelle rezultati mit richtigen Feldern
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
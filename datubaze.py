import sqlite3

def get_top_results():
    conn = sqlite3.connect('dati.db')
    c = conn.cursor()
    # Holt alle gespeicherten Ergebnisse aus der Datenbank
    c.execute("SELECT * FROM rezultati")
    rezultati = c.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "vards": r[1],
            "meginajumi": r[2],
            "laiks": r[3],
            "limenis": r[4]
        }
        for r in rezultati
    ]

def pievienot(dati):
    conn = sqlite3.connect('dati.db')
    c = conn.cursor()
    # Fügt ein neues Ergebnis in die Datenbank ein
    c.execute("""
        INSERT INTO rezultati(vards, meginajumi, laiks, limenis)
        VALUES(?, ?, ?, ?)
    """, (dati['vards'], dati['meginajumi'], dati['laiks'], dati['limenis']))
    conn.commit()
    conn.close()
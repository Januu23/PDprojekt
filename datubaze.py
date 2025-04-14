import sqlite3

def get_top_results():
    conn = sqlite3.connect('dati.db')
    c = conn.cursor()
    c.execute("SELECT * FROM rezultati")
    rezultati = c.fetchall()
    conn.close()
    return [
        {"id": r[0], "vards": r[1], "klikski": r[2], "laiks": r[3], "datums": r[4]}
        for r in rezultati
    ]

def pievienot(dati):
    conn = sqlite3.connect('dati.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO rezultati(vards, klikski, laiks, datums)
        VALUES(?, ?, ?, ?)
    """, (dati['vards'], dati['klikski'], dati['laiks'], dati['datums']))
    conn.commit()
    conn.close()
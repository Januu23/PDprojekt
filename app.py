import random
import time
from flask import Flask, render_template, request, jsonify, session
import json
from datubaze import get_top_results, pievienot

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/game')
def game():
    return render_template("game.html")

@app.route('/top')
def top():
    return render_template("top.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/topData', methods=['GET'])
def top_data():
    try:
        top_rezultati = get_top_results()
        top_5 = sorted(top_rezultati, key=lambda x: (x['klikski'], x['laiks']))[:5]
        return jsonify(top_5), 200
    except Exception:
        return jsonify({'status': 'error'}), 500
    
@app.route('/pievienot-rezultatu', methods=['POST'])
def pievienot_rezultatu():
    dati = request.json
    try:
        pievienot(dati)
        top_5 = sorted(get_top_results(), key=lambda x: (x['klikski'], x['laiks']))[:5]
        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(top_5, f, ensure_ascii=False, indent=4)
        return jsonify({'status': 'success'}), 200
    except Exception:
        return jsonify({'status': 'error'}), 500


app.secret_key = "supersecretkey"  # Für die Sitzungsverwaltung

# 🟢 Starten des Spiels und Festlegen des Levels
@app.route('/start_game', methods=['POST'])
def start_game():
    """Setzt das Level und startet das Spiel."""
    dati = request.json
    limenis = dati.get("level", 1)

    if limenis == 1:
        maksimalais_skaitlis = 100
    elif limenis == 2:
        maksimalais_skaitlis = 500
    elif limenis == 3:
        maksimalais_skaitlis = 1000
    else:
        return jsonify({'status': 'error', 'message': 'Nederīgs līmenis'}), 400

    session['maksimalais_skaitlis'] = maksimalais_skaitlis  # Speichert den Zahlenbereich
    session['slepenais_skaitlis'] = random.randint(1, maksimalais_skaitlis)  # Generiert eine Zufallszahl
    session['meginajumi'] = 0  # Setzt die Versuche auf 0
    session['start_time'] = time.time()  # Startzeit des Spiels

    return jsonify({'status': 'success', 'message': f'Spēle sākta! Skaitļu diapazons: 1–{maksimalais_skaitlis}'}), 200

# 🟢 Überprüfung des Rateversuchs
@app.route('/guess', methods=['POST'])
def guess():
    """Nimmt den Benutzerraten und gibt Feedback zurück."""
    dati = request.json
    minejums = int(dati.get("guess"))  # Der Benutzerraten
    session['meginajumi'] += 1  # Erhöht die Versuche
    slepenais_skaitlis = session.get('slepenais_skaitlis', None)
    maksimalais_skaitlis = session.get('maksimalais_skaitlis', 100)

    if minejums < slepenais_skaitlis:
        return jsonify({'result': 'zemāk', 'message': f'Par mazu! Mēģini starp {minejums} un {maksimalais_skaitlis}.'}), 200
    elif minejums > slepenais_skaitlis:
        return jsonify({'result': 'augstāk', 'message': f'Par lielu! Mēģini starp 1 un {minejums}.'}), 200
    else:
        # Spiel beendet, speichere das Ergebnis
        end_time = time.time()
        time_taken = round(end_time - session['start_time'], 2)  # Berechnet die Zeit in Sekunden

        # Ergebnisse speichern
        results = {
            "name": session.get("player_name", "Anonīms"),  # Standardname, wenn keiner eingegeben wurde
            "meginajumi": session['meginajumi'],
            "laiks": time_taken,
            "level": session['maksimalais_skaitlis']
        }

        # Speichert das Ergebnis in der Datei oder einer Datenbank
        try:
            pievienot(results)  # Füge das Ergebnis in die Datenbank oder Datei ein
            return jsonify({'result': 'pareizi', 'message': f'Pareizi! Tu minēji ar {session["meginajumi"]} mēģinājumiem. Laiks: {time_taken} sek.'}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

# 🟢 Ergänzung für die Eingabe des Namens (falls du das im Frontend noch nicht machst)
@app.route('/set_name', methods=['POST'])
def set_name():
    """Setzt den Spielernamen in der Sitzung."""
    dati = request.json
    name = dati.get("name", "Anonīms")
    session['player_name'] = name
    return jsonify({'status': 'success', 'message': f'Vārds ir iestatīts uz {name}'}), 200

if __name__ == '__main__':
    app.run(debug=True)
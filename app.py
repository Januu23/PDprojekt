import random
import time
import json
from flask import Flask, render_template, request, jsonify, session
from datubaze import get_top_results, pievienot

app = Flask(__name__)
app.secret_key = "your-secure-random-key"  # Ersetze dies durch einen sicheren, zufällig generierten Schlüssel

# Sākumlapa
@app.route('/')
def index():
    return render_template("index.html")

# Spēles lapa
@app.route('/game')
def game():
    return render_template("game.html")

# Top rezultāti
@app.route('/top')
def top():
    return render_template("top.html")

# ℹ️ Par spēli
@app.route('/about')
def about():
    return render_template("about.html")

# API: Top dati (atgriež 5 labākos pēc klikšķiem un laika)
@app.route('/topData', methods=['GET'])
def top_data():
    try:
        top_rezultati = get_top_results()
        top_5 = sorted(top_rezultati, key=lambda x: (x['klikski'], x['laiks']))[:5]
        return jsonify(top_5), 200
    except Exception as e:
        print(f"Fehler beim Laden der Top-Daten: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Fehler beim Laden der Top-Daten!'}), 500

# Saglabā rezultātu pēc pareizas minēšanas
@app.route('/pievienot-rezultatu', methods=['POST'])
def pievienot_rezultatu():
    try:
        dati = request.json
        pievienot(dati)
        top_5 = sorted(get_top_results(), key=lambda x: (x['klikski'], x['laiks']))[:5]
        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(top_5, f, ensure_ascii=False, indent=4)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Fehler beim Hinzufügen des Ergebnisses: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Fehler beim Hinzufügen des Ergebnisses!'}), 500

# Spēles sākšana – iestata līmeni, slepeno skaitli un sākuma laiku
@app.route('/start_game', methods=['POST'])
def start_game():
    """Saņem līmeni un vārdu, iestata sesiju un sāk spēli."""
    try:
        dati = request.json
        limenis = dati.get("level", 1)
        vards = dati.get("vards", "Anonīms")  # Spēlētāja vārds

        # Noteikt maksimālo skaitli pēc līmeņa
        if limenis == 1:
            maksimalais_skaitlis = 100
        elif limenis == 2:
            maksimalais_skaitlis = 500
        elif limenis == 3:
            maksimalais_skaitlis = 1000
        else:
            return jsonify({'status': 'error', 'message': 'Nederīgs līmenis'}), 400

        # Saglabāt sesijā
        session['maksimalais_skaitlis'] = maksimalais_skaitlis
        session['slepenais_skaitlis'] = random.randint(1, maksimalais_skaitlis)
        session['meginajumi'] = 0
        session['start_time'] = time.time()
        session['player_name'] = vards

        return jsonify({'status': 'success', 'message': f'Spēle sākta! Skaitļu diapazons: 1–{maksimalais_skaitlis}'}), 200
    except Exception as e:
        print(f"Fehler beim Starten des Spiels: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Fehler beim Starten des Spiels!'}), 500

# Spēlētāja minējuma apstrāde
@app.route('/guess', methods=['POST'])
def guess():
    """Apstrādā spēlētāja minējumu un sniedz atgriezenisko saiti."""
    try:
        dati = request.json
        minejums = int(dati.get("guess"))
        session['meginajumi'] += 1

        slepenais_skaitlis = session.get('slepenais_skaitlis')
        maksimalais_skaitlis = session.get('maksimalais_skaitlis', 100)

        if minejums < slepenais_skaitlis:
            return jsonify({'result': 'zemāk', 'message': f'Par mazu! Mēģini starp {minejums} un {maksimalais_skaitlis}.'}), 200
        elif minejums > slepenais_skaitlis:
            return jsonify({'result': 'augstāk', 'message': f'Par lielu! Mēģini starp 1 un {minejums}.'}), 200
        else:
            # Ja minēts pareizi – aprēķina laiku un saglabā rezultātu
            end_time = time.time()
            time_taken = round(end_time - session['start_time'], 2)

            results = {
                "vards": session.get("player_name", "Anonīms"),
                "klikski": session['meginajumi'],
                "laiks": time_taken,
                "limenis": session['maksimalais_skaitlis']
            }

            pievienot(results)  # Hier wird der Fehler abgefangen
            return jsonify({
                'result': 'pareizi',
                'message': f'Pareizi! Tu minēji ar {session["meginajumi"]} mēģinājumiem. Laiks: {time_taken} sek.'
            }), 200
    except KeyError as e:
        return jsonify({'status': 'error', 'message': f"Fehler: {str(e)}"}), 400
    except Exception as e:
        print(f"Fehler beim Verarbeiten des Minens: {str(e)}")
        return jsonify({'status': 'error', 'message': f"Unbekannter Fehler: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

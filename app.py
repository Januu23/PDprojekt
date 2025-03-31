import random
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
    try :
        top_rezultati = get_top_results()
        top_5 = sorted(top_rezultati, key=lambda x: (x['klikski'], x['laiks'] ))[:5]
        return jsonify(top_5), 200
    except Exception:
        return jsonify({'status': 'error'}), 500
    
@app.route('/pievienot-rezultatu', methods=['POST'])
def pievienot_rezultatu():
    dati= request.json
    try:
        pievienot(dati)
        top_5 = sorted(get_top_results(), key=lambda x: (x['klikski'], x['laiks'] ))[:5]
        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(top_5, f, ensure_ascii=False, indent=4)
        return jsonify({'status': 'success'}), 200
    except Exception:
        return jsonify({'status': 'error'}), 500
    

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Für Sessions    

    # 🟢 Route zum Setzen des Levels und Starten eines neuen Spiels
@app.route('/start_game', methods=['POST'])
def start_game():
    """Setzt das Level und startet ein neues Spiel."""
    data = request.json
    level = data.get("level", 1)

    if level == 1:
        max_number = 100
    elif level == 2:
        max_number = 500
    elif level == 3:
        max_number = 1000
    else:
        return jsonify({'status': 'error', 'message': 'Ungültiges Level'}), 400

    session['max_number'] = max_number  # Speichert den Zahlenbereich
    session['random_number'] = random.randint(1, max_number)  # Generiert eine Zufallszahl innerhalb des Levels
    session['attempts'] = 0  # Setzt die Versuche auf 0

    return jsonify({'status': 'success', 'message': f'Spiel gestartet! Zahlenbereich: 1-{max_number}'}), 200

# 🟢 Route zum Raten einer Zahl
@app.route('/guess', methods=['POST'])
def guess():
    """Nimmt die Nutzereingabe entgegen und gibt Rückmeldung."""
    data = request.json
    user_guess = int(data.get("guess"))  # Eingabe des Spielers
    session['attempts'] += 1  # Zählt die Versuche
    random_number = session.get('random_number', None)
    max_number = session.get('max_number', 100)

    if user_guess < random_number:
        return jsonify({'result': 'low', 'message': f'Zu niedrig! Versuche es zwischen {user_guess} und {max_number}.'}), 200
    elif user_guess > random_number:
        return jsonify({'result': 'high', 'message': f'Zu hoch! Versuche es zwischen 1 und {user_guess}.'}), 200
    else:
        return jsonify({'result': 'correct', 'message': f'Richtig! Du hast {session["attempts"]} Versuche gebraucht.'}), 200

if __name__ == '__main__':
  app.run(debug=True)


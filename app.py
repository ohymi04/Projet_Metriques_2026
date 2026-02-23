import requests
from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT,
            email TEXT,
            objet TEXT,
            message TEXT,
            date_envoi TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Déposez votre code à partir d'ici :

# @app.route("/contact")
# def contact():
#   return render_template("contact.html")

@app.get("/paris")
def api_paris():
    
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])

    n = min(len(times), len(temps))
    result = [
        {"datetime": times[i], "temperature_c": temps[i]}
        for i in range(n)
    ]

    return jsonify(result)

@app.route("/rapport")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme")
def histogramme():
    return render_template("histogramme.html")

@app.get("/versailles")
def api_versailles():
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8048&longitude=2.1203&hourly=relativehumidity_2m"
    response = requests.get(url)
    data = response.json()
    times    = data.get("hourly", {}).get("time", [])
    humidity = data.get("hourly", {}).get("relativehumidity_2m", [])
    n = min(len(times), len(humidity))
    result = [{"datetime": times[i], "humidity_pct": humidity[i]} for i in range(n)]
    return jsonify(result)

@app.route("/atelier")
def atelier():
    return render_template("atelier.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.get_json()
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO messages (nom, prenom, email, objet, message, date_envoi)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get('nom'), data.get('prenom'), data.get('email'),
            data.get('objet'), data.get('message'),
            datetime.now().strftime('%d/%m/%Y à %H:%M')
        ))
        conn.commit()
        conn.close()
        return jsonify({"status": "ok"})
    return render_template("contact.html")

@app.route("/admin")
def admin():
    conn = sqlite3.connect('contacts.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM messages ORDER BY id DESC')
    messages = [dict(row) for row in c.fetchall()]
    conn.close()
    return render_template("admin.html", messages=messages)

# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)

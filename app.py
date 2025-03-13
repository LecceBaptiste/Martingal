from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)



from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Connexion et création de la base de données
conn = sqlite3.connect('participants.db', check_same_thread=False)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS participants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        agence TEXT NOT NULL
    )
""")
conn.commit()

@app.route('/')
def index():
    c.execute("SELECT COUNT(*) FROM participants")
    count = c.fetchone()[0]
    return render_template('index.html', count=count)

@app.route('/inscription', methods=['POST'])
def inscription():
    nom = request.form['nom']
    prenom = request.form['prenom']
    email = request.form['email']
    agence = request.form['agence']

    try:
        c.execute("INSERT INTO participants (nom, prenom, email, agence) VALUES (?, ?, ?, ?)", (nom, prenom, email, agence))
        conn.commit()
        c.execute("SELECT COUNT(*) FROM participants")
        count = c.fetchone()[0]
        return f"<p class='text-green-600'>Inscription réussie ! Nombre total d'inscrits : {count}</p>"
    except sqlite3.IntegrityError:
        return "<p class='text-red-600'>Cet email est déjà inscrit.</p>"

if __name__ == '__main__':
    app.run(debug=True)

# Frontend (index.html)

index_html = """
<!DOCTYPE html>
<html lang='fr'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Martingal - Inscription</title>
    <script src='https://cdn.tailwindcss.com'></script>
    <script src='https://unpkg.com/htmx.org@1.7.0'></script>
</head>
<body class='bg-gray-100 flex items-center justify-center h-screen'>
    <div class='bg-white p-8 rounded-lg shadow-lg max-w-md w-full'>
        <h1 class='text-2xl font-bold text-gray-800 text-center'>Inscription Martingal</h1>
        <p class='text-gray-600 text-center mt-2'>Participants inscrits : <span id='count' class='font-bold'>{{ count }}</span></p>
        <form id='form' class='mt-6' hx-post='/inscription' hx-target='#message' hx-swap='innerHTML'>
            <input type='text' name='nom' placeholder='Nom' required class='w-full p-2 border rounded mb-3'>
            <input type='text' name='prenom' placeholder='Prénom' required class='w-full p-2 border rounded mb-3'>
            <input type='email' name='email' placeholder='Email' required class='w-full p-2 border rounded mb-3'>
            <input type='text' name='agence' placeholder='Agence' required class='w-full p-2 border rounded mb-3'>
            <button type='submit' class='w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600'>S'inscrire</button>
        </form>
        <div id='message' class='mt-4 text-center'></div>
    </div>
</body>
</html>
"""


    
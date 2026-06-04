from flask import Flask, jsonify, request, send_from_directory, session, redirect
import pyodbc
import os
app = Flask(__name__)
app.secret_key = 'eksamen2026'
def get_db():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=192.168.10.30\\SQLEXPRESS,1433;'
        'DATABASE=EksamenDB;'
        'Trusted_Connection=yes;'
    )
    return conn
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)
@app.route('/api/logginn', methods=['POST'])
def logg_inn():
    data = request.json
    brukernavn = data.get('brukernavn')
    passord = data.get('passord')
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Rolle FROM Bruker WHERE Brukernavn=? AND Passord=?", brukernavn, passord)
        bruker = cursor.fetchone()
        if bruker:
            cursor.execute("INSERT INTO Logg (BrukerId, Handling) VALUES (?, ?)", bruker.Id, f'Innlogging: {brukernavn}')
            conn.commit()
            return jsonify({'status': 'ok', 'rolle': bruker.Rolle})
        else:
            return jsonify({'status': 'feil', 'melding': 'Feil brukernavn eller passord'})
    except Exception as e:
        return jsonify({'status': 'feil', 'melding': str(e)})
@app.route('/api/saker')
def get_saker():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sak ORDER BY Opprettet DESC")
        saker = []
        for row in cursor.fetchall():
            saker.append({'id': row.Id, 'tittel': row.Tittel, 'kategori': row.Kategori, 'status': row.Status, 'opprettet': str(row.Opprettet)})
        return jsonify(saker)
    except Exception as e:
        return jsonify({'feil': str(e)})
@app.route('/api/nysak', methods=['POST'])
def ny_sak():
    data = request.json
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Sak (ElevId, Tittel, Beskrivelse, Kategori, Status) VALUES (?, ?, ?, ?, 'aapen')",
            data.get('elevId'), data.get('tittel'), data.get('beskrivelse'), data.get('kategori')
        )
        conn.commit()
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'feil', 'melding': str(e)})
@app.route('/api/endrestatus', methods=['POST'])
def endre_status():
    data = request.json
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE Sak SET Status=? WHERE Id=?", data.get('status'), data.get('id'))
        conn.commit()
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'feil', 'melding': str(e)})
@app.route('/api/sendsvar', methods=['POST'])
def send_svar():
    data = request.json
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Svar (SakId, LaererId, Innhold) VALUES (?, ?, ?)",
            data.get('sakId'), 2, data.get('innhold'))
        conn.commit()
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'feil', 'melding': str(e)})
@app.route('/api/kritiske')
def get_kritiske():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sak WHERE Kategori='kritisk' ORDER BY Opprettet DESC")
        saker = []
        for row in cursor.fetchall():
            saker.append({'id': row.Id, 'tittel': row.Tittel, 'status': row.Status})
        return jsonify(saker)
    except Exception as e:
        return jsonify({'feil': str(e)})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
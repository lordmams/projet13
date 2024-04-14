from flask import Flask, render_template, request, redirect, url_for,jsonify
import requests
import psycopg2
import json

app = Flask(__name__)

MODULE3_URL = 'http://module3:5001/delete'
MODULE4_URL = 'http://module4:5002/add'


def get_db_connection():
    return psycopg2.connect(host="postgres-master1",
                            database="master1",
                            user="admin",
                            password="admin")

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM etudiant;')
    etudiants = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', etudiants=etudiants)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    response = requests.post(f'{MODULE3_URL}/{id}')
    return jsonify(response.json()), response.status_code

@app.route('/add', methods=['POST'])
def add_student():
    student_data = {
        'nom': request.form['nom'],
        'specialite': request.form['specialite'],
        'annee_academique': request.form['annee_academique']
    }
    response = requests.post(MODULE4_URL, json=student_data)
    return jsonify(response.json()), response.status_code

@app.route('/alumni', methods=['GET'])
def alumni():
    alumni_file_path = '/data/alumni.json'
    try:
        with open(alumni_file_path, 'r') as alumni_file:
            alumni_data = [json.loads(line) for line in alumni_file]
    except FileNotFoundError:
        alumni_data = []

    return render_template('alumni.html', alumni=alumni_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

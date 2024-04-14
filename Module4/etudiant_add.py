from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
import psycopg2
import json

app = Flask(__name__)
CORS(app)  

def get_db_connection():
    try:
        conn = psycopg2.connect(host='postgres-master1',
                                database='master1',
                                user='admin',
                                password='admin')
        return conn
    except psycopg2.Error as e:
        print("Unable to connect to the database:", e)
        return None

@app.route('/add', methods=['POST'])
def add_student():
    if request.is_json:
        data = request.get_json()
        nom = data.get('nom')
        specialite = data.get('specialite')
        annee_academique = data.get('annee_academique')
    else:
        nom = request.form.get('nom')
        specialite = request.form.get('specialite')
        annee_academique = request.form.get('annee_academique')
    
    if not all([nom, specialite, annee_academique]):
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500
    
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO etudiant (nom, specialite, annee_academique) VALUES (%s, %s, %s)",
                        (nom, specialite, annee_academique))
            conn.commit()
            student_data = {
                'nom': nom,
                'specialite': specialite,
                'annee_academique': annee_academique
            }
            with open('/data/alumni.json', 'a') as f:
                json.dump(student_data, f)
                f.write('\n')
            return jsonify({'status': 'success', 'message': 'Student added'}), 201
        
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': 'Database error', 'details': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

from flask import Flask,jsonify
import psycopg2
import json
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(host='postgres-master1',
                            database='master1',
                            user='admin',
                            password='admin')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM etudiant WHERE id = %s;', (id,))
    student_data = cur.fetchone()
    
    if student_data:
        cur.execute('DELETE FROM etudiant WHERE id = %s;', (id,))
        conn.commit()

        cur.execute('SELECT * FROM etudiant;')
        remaining_students = cur.fetchall()
        with open('/data/alumni.json', 'w') as f:
            for student in remaining_students:
                json.dump({
                    'nom': student[1],
                    'specialite': student[2],
                    'annee_academique': student[3]
                }, f)
                f.write('\n')

        cur.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Student deleted and file updated','remaining_students':remaining_students}), 200
    else:
        cur.close()
        conn.close()
        return jsonify({'status': 'error', 'message': 'Student not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

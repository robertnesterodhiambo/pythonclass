from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL connection settings (root user, no password)
MYSQL_DATABASE_HOST = 'localhost'
MYSQL_DATABASE_USER = 'root'
MYSQL_DATABASE_PASSWORD = ''
MYSQL_DATABASE_DB = 'dojos_and_ninjas_schema'

# Establish a MySQL connection using MySQL Connector
def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_DATABASE_HOST,
        user=MYSQL_DATABASE_USER,
        password=MYSQL_DATABASE_PASSWORD,
        database=MYSQL_DATABASE_DB
    )

# Route to create a dojo and display all dojos
@app.route('/dojos', methods=['GET', 'POST'])
def dojos():
    db = get_db_connection()
    cursor = db.cursor()
    if request.method == 'POST':
        dojo_name = request.form['name']
        cursor.execute("INSERT INTO dojos (name) VALUES (%s)", (dojo_name,))
        db.commit()
        return redirect(url_for('dojos'))
    
    cursor.execute("SELECT * FROM dojos")
    dojos = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('dojos.html', dojos=dojos)

# Route to add a ninja to a dojo
@app.route('/ninjas', methods=['GET', 'POST'])
def ninjas():
    db = get_db_connection()
    cursor = db.cursor()
    if request.method == 'POST':
        dojo_id = request.form['dojo']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        cursor.execute("INSERT INTO ninjas (dojo_id, first_name, last_name, age) VALUES (%s, %s, %s, %s)", 
                       (dojo_id, first_name, last_name, age))
        db.commit()
        return redirect(url_for('dojo_show', dojo_id=dojo_id))
    
    cursor.execute("SELECT * FROM dojos")
    dojos = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('ninjas.html', dojos=dojos)

# Route to display a dojo's ninjas
@app.route('/dojos/<int:dojo_id>')
def dojo_show(dojo_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM dojos WHERE id = %s", (dojo_id,))
    dojo = cursor.fetchone()
    
    cursor.execute("SELECT * FROM ninjas WHERE dojo_id = %s", (dojo_id,))
    ninjas = cursor.fetchall()
    cursor.close()
    db.close()
    
    return render_template('dojo_show.html', dojo=dojo, ninjas=ninjas)

# Home route redirects to the dojo page
@app.route('/')
def home():
    return redirect(url_for('dojos'))

if __name__ == '__main__':
    app.run(debug=True)

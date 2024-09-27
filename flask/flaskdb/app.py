from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import datetime

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_mysql_username'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'your_database_name'

mysql = MySQL(app)

# Route to display all users
@app.route('/users')
def read_all_users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    return render_template('read.html', users=users)

# Route to render the form for creating a new user
@app.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Get the form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        
        # Insert the new user into the database
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s)
        ''', (first_name, last_name, email, datetime.datetime.now(), datetime.datetime.now()))
        
        mysql.connection.commit()
        cursor.close()
        
        # Redirect to the read page
        return redirect('/users')
    
    # If GET request, render the form
    return render_template('create.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port= 5002)

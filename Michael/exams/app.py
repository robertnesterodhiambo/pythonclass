from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'recipe_share'

mysql = MySQL(app)

# Helper function to check login status
def is_logged_in():
    return 'user_id' in session

@app.route('/')
def index():
    if not is_logged_in():
        return redirect(url_for('login'))
    user_id = session['user_id']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM recipes WHERE user_id=%s", [user_id])
    recipes = cursor.fetchall()
    cursor.close()
    return render_template('dashboard.html', recipes=recipes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_pw = request.form['confirm_pw']

        if password != confirm_pw:
            flash("Passwords do not match!", 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                       (first_name, last_name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        flash("Registration successful! Please log in.", 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", [email])
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user[4], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash("Login successful!", 'success')
            return redirect(url_for('index'))
        flash("Invalid credentials!", 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have logged out.", 'success')
    return redirect(url_for('login'))

@app.route('/recipes/new', methods=['GET', 'POST'])
def create():
    if not is_logged_in():
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        instructions = request.form['instructions']
        date_cooked = request.form['date_cooked']
        under_30_minutes = 'under_30_minutes' in request.form

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO recipes (user_id, name, description, instructions, date_cooked, under_30_minutes) VALUES (%s, %s, %s, %s, %s, %s)",
                       (session['user_id'], name, description, instructions, date_cooked, under_30_minutes))
        mysql.connection.commit()
        cursor.close()
        flash("Recipe added successfully!", 'success')
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/recipes/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not is_logged_in():
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        instructions = request.form['instructions']
        date_cooked = request.form['date_cooked']
        under_30_minutes = 'under_30_minutes' in request.form

        cursor.execute("UPDATE recipes SET name=%s, description=%s, instructions=%s, date_cooked=%s, under_30_minutes=%s WHERE id=%s AND user_id=%s",
                       (name, description, instructions, date_cooked, under_30_minutes, id, session['user_id']))
        mysql.connection.commit()
        cursor.close()
        flash("Recipe updated successfully!", 'success')
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM recipes WHERE id=%s AND user_id=%s", (id, session['user_id']))
    recipe = cursor.fetchone()
    cursor.close()
    return render_template('edit.html', recipe=recipe)

@app.route('/recipes/delete/<int:id>', methods=['POST'])
def delete(id):
    if not is_logged_in():
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM recipes WHERE id=%s AND user_id=%s", (id, session['user_id']))
    mysql.connection.commit()
    cursor.close()
    flash("Recipe deleted successfully!", 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

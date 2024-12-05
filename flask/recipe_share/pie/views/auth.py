from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.user import User, bcrypt, mysql

# Initialize Flask-Login's LoginManager
auth = Blueprint('auth', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    """
    Load a user by their ID (required by Flask-Login).
    """
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id, first_name, last_name, email, password FROM users WHERE id=%s", (user_id,)
    )
    user_data = cursor.fetchone()
    if user_data:
        return User(*user_data)
    return None

# Root route to redirect to signup page
@auth.route('/')
def index():
    """
    Redirects to the signup page when visiting the root URL.
    """
    return redirect(url_for('auth.signup'))  # Redirect to the signup page

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Route for user signup.
    """
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('auth.signup'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%s, %s, %s, %s)
            """, (first_name, last_name, email, hashed_password))
            mysql.connection.commit()
            # After successful signup, log the user in and redirect to the dashboard
            user = User.find_by_email(email)  # Get the newly created user from the database
            login_user(user)
            flash(f"Welcome, {first_name}! You have successfully signed up.", 'success')
            return redirect(url_for('auth.dashboard'))  # Redirect to the dashboard or another welcome page
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('auth.signup'))

    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login.
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.find_by_email(email)

        if not user:
            flash('No user found with this email.', 'danger')
            return redirect(url_for('auth.login'))

        if User.validate_password(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid email or password!', 'danger')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    """
    Route for user logout.
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/dashboard')
@login_required
def dashboard():
    """
    Route for the user dashboard (protected).
    """
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id, name, description, date_cooked, under_30_minutes FROM recipes WHERE user_id = %s",
        (current_user.id,)
    )
    recipes = cursor.fetchall()  # Fetch all recipes for the logged-in user
    return render_template('dashboard.html', user=current_user, recipes=recipes)

@auth.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    """
    Route for adding a new recipe.
    """
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        instructions = request.form['instructions']
        date_cooked = request.form['date_cooked']
        under_30_minutes = 'under_30_minutes' in request.form

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                INSERT INTO recipes (user_id, name, description, instructions, date_cooked, under_30_minutes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (current_user.id, name, description, instructions, date_cooked, under_30_minutes))
            mysql.connection.commit()
            flash('Recipe added successfully!', 'success')
            return redirect(url_for('auth.dashboard'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('auth.add_recipe'))
    return render_template('add_recipe.html')

@auth.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        instructions = request.form['instructions']
        date_cooked = request.form['date_cooked']
        under_30_minutes = 'under_30_minutes' in request.form

        try:
            cursor.execute("""
                UPDATE recipes SET name=%s, description=%s, instructions=%s, date_cooked=%s, under_30_minutes=%s
                WHERE id=%s AND user_id=%s
            """, (name, description, instructions, date_cooked, under_30_minutes, recipe_id, current_user.id))
            mysql.connection.commit()
            flash('Recipe updated successfully!', 'success')
            return redirect(url_for('auth.dashboard'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('auth.edit_recipe', recipe_id=recipe_id))

    # Get the current recipe data to pre-fill the form
    cursor.execute("SELECT id, name, description, instructions, date_cooked, under_30_minutes FROM recipes WHERE id=%s AND user_id=%s", (recipe_id, current_user.id))
    recipe = cursor.fetchone()
    if recipe:
        return render_template('edit_recipe.html', recipe=recipe)
    else:
        flash('Recipe not found or not authorized to edit', 'danger')
        return redirect(url_for('auth.dashboard'))

from flask import render_template, request, redirect, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/recipes')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id(session['user_id'])
    recipes = Recipe.get_all()
    return render_template('index.html', user=user, recipes=recipes)

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('create_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under_30_minutes': request.form['under_30_minutes'] == 'yes',
        'date_cooked': request.form['date_cooked'],
        'user_id': session['user_id']
    }
    Recipe.save(data)
    return redirect('/recipes')

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    recipe = Recipe.get_by_id(recipe_id)
    if recipe.user_id != session['user_id']:
        return redirect('/recipes')
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/recipes/update/<int:recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{recipe_id}')
    data = {
        'id': recipe_id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under_30_minutes': request.form['under_30_minutes'] == 'yes',
        'date_cooked': request.form['date_cooked']
    }
    Recipe.update(data)
    return redirect('/recipes')

@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    Recipe.delete(recipe_id)
    return redirect('/recipes')

@app.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    recipe = Recipe.get_by_id(recipe_id)
    return render_template('details_page.html', recipe=recipe)

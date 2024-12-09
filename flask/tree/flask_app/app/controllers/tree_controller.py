from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.tree_model import create_tree, get_all_trees
from flask_login import login_required, current_user

tree_bp = Blueprint('tree', __name__, url_prefix='/trees')

@tree_bp.route('/')
@login_required
def dashboard():
    # Fetch all trees to display
    trees = get_all_trees()
    return render_template('tree/dashboard.html', trees=trees)

@tree_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_tree():
    if request.method == 'POST':
        species = request.form['species']
        location = request.form['location']
        date_found = request.form['date_found']
        zipcode = request.form['zipcode']
        notes = request.form['notes']
        
        # Add tree to database
        create_tree(species, location, date_found, zipcode, notes, current_user.id)
        flash("Tree added successfully!", 'success')
        return redirect(url_for('tree.dashboard'))
    
    return render_template('tree/add_tree.html')

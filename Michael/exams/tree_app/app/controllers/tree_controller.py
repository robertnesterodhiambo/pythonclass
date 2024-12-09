from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..config.database import get_db_connection
from ..models.tree import Tree

tree_bp = Blueprint('tree', __name__)

@tree_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()

    if request.method == 'POST':
        Tree.add_tree(
            conn, 
            request.form['name'], 
            request.form['species'], 
            request.form['date_found'], 
            request.form['note'], 
            request.form['location_found'], 
            session['user_id']
        )

    trees = Tree.get_all_trees(conn)
    conn.close()

    return render_template('dashboard.html', trees=trees)

@tree_bp.route('/edit/<int:tree_id>', methods=['GET', 'POST'])
def edit_tree(tree_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()

    if request.method == 'POST':
        Tree.update_tree(
            conn, tree_id, 
            request.form['name'], 
            request.form['species'], 
            request.form['date_found'], 
            request.form['note'], 
            request.form['location_found'], 
            session['user_id']
        )
        conn.close()
        flash('Tree details updated!', 'success')
        return redirect(url_for('tree.dashboard'))

    tree = Tree.get_tree_by_id(conn, tree_id, session['user_id'])
    conn.close()

    if not tree:
        flash('Tree not found or access denied!', 'danger')
        return redirect(url_for('tree.dashboard'))

    return render_template('edit_tree.html', tree=tree)

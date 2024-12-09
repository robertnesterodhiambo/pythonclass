from flask_app import app
from flask import request, redirect, render_template, session, flash
from flask_app.models.sighting import Sighting


@app.route('/dashboard')
def dashboard():
    sightings = Sighting.get_all_sightings()
    return render_template('dashboard.html', sightings=sightings)

@app.route('/sightings/new', methods=['GET', 'POST'])
def new_sighting():
    if request.method == 'POST':
        location = request.form['location']
        date_of_sighting = request.form['date_of_sighting']
        number_of_sasquatches = request.form['number_of_sasquatches']
        description = request.form['description']
        
        Sighting.create_sighting(location, date_of_sighting, number_of_sasquatches, description, session['user_id'])
        
        flash("Sighting reported successfully!", "success")
        return redirect('/dashboard')

    return render_template('new_sighting.html')

@app.route('/sightings/edit/<int:id>', methods=['GET', 'POST'])
def edit_sighting(id):
    sighting = Sighting.get_sighting_by_id(id)
    if request.method == 'POST':
        sighting['location'] = request.form['location']
        sighting['date_of_sighting'] = request.form['date_of_sighting']
        sighting['number_of_sasquatches'] = request.form['number_of_sasquatches']
        sighting['description'] = request.form['description']
        
        Sighting.update_sighting(id, sighting['location'], sighting['date_of_sighting'], sighting['number_of_sasquatches'], sighting['description'])
        
        flash('Sighting updated successfully!', 'success')
        return redirect('/dashboard')
    
    return render_template('edit_sighting.html', sighting=sighting)

@app.route('/sightings/delete/<int:id>', methods=['POST'])
def delete_sighting(id):
    Sighting.delete_sighting(id)
    flash('Sighting deleted successfully!', 'success')
    return redirect('/dashboard')

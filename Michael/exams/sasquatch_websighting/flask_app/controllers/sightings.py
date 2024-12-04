from flask import request, redirect, render_template, session, flash
from flask_app import app, db
from flask_app.models.sighting import Sighting

@app.route('/dashboard')
def dashboard():
    sightings = Sighting.query.all()
    return render_template('dashboard.html', sightings=sightings)

@app.route('/sightings/new', methods=['GET', 'POST'])
def new_sighting():
    if request.method == 'POST':
        location = request.form['location']
        date_of_sighting = request.form['date_of_sighting']
        number_of_sasquatches = request.form['number_of_sasquatches']
        description = request.form['description']
        
        new_sighting = Sighting(
            location=location,
            date_of_sighting=date_of_sighting,
            number_of_sasquatches=number_of_sasquatches,
            description=description,
            user_id=session['user_id']
        )
        db.session.add(new_sighting)
        db.session.commit()

        flash("Sighting reported successfully!", "success")
        return redirect('/dashboard')

    return render_template('new_sighting.html')

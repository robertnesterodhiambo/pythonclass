from flask_app import db

class Sighting(db.Model):
    __tablename__ = 'sightings'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    date_of_sighting = db.Column(db.Date, nullable=False)
    number_of_sasquatches = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('User', backref='sightings')

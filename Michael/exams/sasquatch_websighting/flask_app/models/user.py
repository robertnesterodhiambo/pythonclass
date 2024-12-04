from flask_app import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    @classmethod
    def hash_password(cls, password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    @classmethod
    def verify_password(cls, hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)

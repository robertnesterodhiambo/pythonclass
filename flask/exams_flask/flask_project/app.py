from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and login manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'  # Redirect to login if not logged in

# Import views after initializing app to avoid circular imports
from views.auth import auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# User model import
from models.user import User

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize the app context and create all tables
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)

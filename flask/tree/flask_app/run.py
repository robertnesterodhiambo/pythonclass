from flask import Flask
from flask_login import LoginManager
from app.controllers.user_controller import user_bp  # This is correct

app = Flask(__name__)

# Set up secret key for session management
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Define the login view (where users are redirected if they are not logged in)
login_manager.login_view = 'user.login'  # Update with your actual login route name

# Register your Blueprint
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from flask_login import LoginManager
from app.controllers.user_controller import user_bp
from app.controllers.tree_controller import tree_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    
    # Register Blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(tree_bp)
    
    return app

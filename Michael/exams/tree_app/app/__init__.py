from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret_key'

    # Register Blueprints
    from .controllers.auth_controller import auth_bp
    from .controllers.tree_controller import tree_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tree_bp)

    return app

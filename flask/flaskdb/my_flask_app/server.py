# server.py

from flask import Flask
from controllers.user_controller import user_controller
from models.user_model import init_db

app = Flask(__name__)

# Register blueprints
app.register_blueprint(user_controller)

# Initialize the database
init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5003)

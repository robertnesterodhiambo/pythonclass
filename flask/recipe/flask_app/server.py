from flask import Flask

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Import controllers after app initialization
from flask_app.controllers import users

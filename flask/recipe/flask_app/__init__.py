from flask import Flask

app = Flask(__name__)
app.secret_key = "shh"  

# Import controllers after app initialization
from flask_app.controllers import users

from flask import Flask
from flask_bcrypt import Bcrypt
import pymysql.cursors

# Initialize the app here
app = Flask(__name__)
app.secret_key = "super_secret_key"

# Raw SQL connection function
def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        database='sasquatch_websighting',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

bcrypt = Bcrypt(app)

# Now, only import controllers here, AFTER app is initialized
from flask_app.controllers import users, sightings

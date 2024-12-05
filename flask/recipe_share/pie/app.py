from flask import Flask
from config import Config
from models.user import mysql, bcrypt
from views.auth import auth, login_manager

app = Flask(__name__)
app.config.from_object(Config)

mysql.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

app.register_blueprint(auth, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)

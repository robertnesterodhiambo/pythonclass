from flask import Flask, render_template
from controllers.user_controller import user_blueprint

app = Flask(__name__)
app.secret_key = "baki"

# Register Blueprints
app.register_blueprint(user_blueprint, url_prefix="/user")

if __name__ == "__main__":
    app.run(debug=True)

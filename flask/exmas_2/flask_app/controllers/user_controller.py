from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import create_user, get_user_by_email

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Validation
        if not all([first_name, last_name, email, password, confirm_password]):
            flash("All fields are required.", "error")
        elif password != confirm_password:
            flash("Passwords do not match.", "error")
        elif get_user_by_email(email):
            flash("Email is already registered.", "error")
        else:
            password_hash = generate_password_hash(password)
            try:
                create_user(first_name, last_name, email, password_hash)
                flash("User created successfully!", "success")
                return redirect("/user/register")
            except Exception as e:
                flash(f"Error creating user: {e}", "error")

    return render_template("register.html")
    
from flask import Blueprint, render_template, request, session, redirect, url_for
from infrastructure.db import db
from models.user import User
from middleware.auth import auth

user_controller = Blueprint("user_bp", __name__)


@user_controller.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")

    return render_template("signup.html")


@user_controller.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session["user_id"] = user.id  # Store the user id in session
            return redirect(url_for("crew_bp.index"))
        else:
            return render_template("login.html", error="Invalid user")

    return render_template("login.html")


@user_controller.route("/logout")
def logout():
    session.pop("user_id", None)  # Clear the session to log the user out
    return redirect(url_for("user_bp.login"))  # Redirect to the login page

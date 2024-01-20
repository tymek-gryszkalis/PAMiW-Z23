from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username != "" and password != "":
            user = User.query.filter_by(username = username).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for("views.home"))
        flash("Login failed", category = "error")
    return render_template("login.html")

@auth.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User.query.filter_by(username = username).first()
        if user:
            flash("Username taken", category = "error")
        elif password1 != password2:
            flash("Passwords don't match", category = "error")
        else:
            newUser = User(username = username, password = generate_password_hash(password1, method='sha256'))
            db.session.add(newUser)
            db.session.commit()
            flash("Account created", category = "success")
            return redirect(url_for("auth.login"))
    return render_template("signup.html")

@auth.route("logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
from app import app
from flask import render_template, request, redirect, session
import users
import players
import draftInit


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    else:
        return render_template("error.html", message="Wrong username or password")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registerSend", methods=["POST"])
def registerSend():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("error.html", message="Passwords do not match")
    if users.registerSend(username, password1):
        return redirect("/")
    else:
        return render_template("error.html", message="Registering failed. Try another username")
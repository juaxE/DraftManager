from app import app
from flask import render_template, request, redirect
import users
import players
import draftConfig


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
    
    
@app.route("/usersList")
def usersList():
    list=users.listUsers()
    return render_template("usersList.html", userslisted=list)

@app.route("/delete", methods=["POST"])
def delete():    
    id = request.form["id"]
    users.deleteUser(id)
    return redirect("/usersList")

@app.route("/config")
def config():
    configs=draftConfig.loadConfig()
    list=configs[0]
    return render_template("config.html", configuration=list)

@app.route("/updateConfig", methods=["POST"])
def updateConfig():
    id = request.form["id"]
    name = request.form["name"]
    participants = request.form["participants"]
    rounds = request.form["rounds"]
    snake = request.form["snake"]
    if draftConfig.updateConfig(id, name, participants, rounds, snake):
        return redirect("config")
    else:
        render_template("error.html", message="Settings update failed")
    
from app import app
from flask import render_template, request, redirect
import users
import players
import draftConfig
import teams


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
    usersListed=users.listUsers()
    return render_template("usersList.html", usersListed=usersListed)

@app.route("/delete", methods=["POST"])
def delete():    
    id = request.form["id"]
    users.deleteUser(id)
    return redirect("/usersList")

@app.route("/config")
def config():
    configuration=draftConfig.loadConfig()
    teamsList=teams.loadTeams()
    return render_template("config.html", configuration=configuration, teamsList = teamsList)

@app.route("/toggleConfirmConfig", methods=["POST"])
def toggleConfirmConfig():
    id = request.form["id"]
    confirmed = request.form["confirmed"]
    print(confirmed)
    if draftConfig.toggleLockConfig(id, confirmed):
        config=draftConfig.loadConfig()
        teams.initTeams(config[2])
        print("jee")
        return redirect("config")
    else:
        teams.deleteTeams()
        return redirect("config")

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
        
@app.route("/updateTeams", methods=["POST"])
def updateTeams():
    ids = request.form.getlist("id")
    names = request.form.getlist("name")
    teams.updateTeams(ids,names)
    return redirect("config")
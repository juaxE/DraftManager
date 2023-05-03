from app import app
from flask import render_template, request, redirect, session
import users, players, draftConfig, teams, draft

@app.route("/")
def index():
    if "username" in session:
        teamList = teams.loadFreeTeams()
        userTeam = teams.checkTeam(session["username"])
        nextPick = draft.nextPick()
        return render_template("index.html", teamList=teamList, userTeam=userTeam, nextPick=nextPick)
    else:
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
    

    
@app.route("/users")
def usersList():
    usersListed=users.listUsers()
    return render_template("users.html", usersListed=usersListed)

@app.route("/deleteUser", methods=["POST"])
def delete():    
    id = request.form["id"]
    users.deleteUser(id)
    return redirect("/users")



@app.route("/config")
def config():
    configuration=draftConfig.loadConfig()
    teamsList=teams.loadTeams()
    return render_template("config.html", configuration=configuration, teamsList = teamsList)

@app.route("/toggleConfirmConfig", methods=["POST"])
def toggleConfirmConfig():
    id = request.form["id"]
    confirmed = request.form["confirmed"]
    if draftConfig.toggleLockConfig(id, confirmed):
        config=draftConfig.loadConfig()
        teams.initTeams(config[2])
        teamsInfo =  teams.loadTeams()
        draft.initPicks(config, teamsInfo)
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
    if teams.updateTeams(ids,names):
        return redirect("config")
    else:
        return render_template("error.html", message="Teamnames must be unique")

@app.route("/selectTeam", methods=["POST"])    
def selectTeam():
    teamId = request.form["teamId"]
    username = request.form["username"]
    if teams.selectTeam(teamId, username):
        return redirect("/")
    else:
        return render_template("error.html", message="Team is already taken.")
    





@app.route("/players")
def playersGet():
    playerList=players.loadPlayers()
    playerList.reverse()
    return render_template("players.html", playerList=playerList)
    
@app.route("/addPlayer", methods=["POST"])
def addPlayer():
    iss = request.form["iss"]
    name = request.form["name"]
    role = request.form["role"]
    
    if players.addPlayer(iss, name, role):
        return redirect("players")
    else:
        return render_template("error.html", message="ISS number must be unique")
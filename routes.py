from app import app
from flask import render_template, request, redirect, session
import users, players, draft_config, teams, draft, user_players

@app.route("/")
def index():
    if "username" in session:
        team_list = teams.load_free_teams()
        user_team = teams.check_team(session["username"])
        next_pick = draft.next_pick()
        return render_template("index.html", team_list=team_list, user_team=user_team, next_pick=next_pick)
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
def register_send():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("error.html", message="Passwords do not match")
    if users.register_send(username, password1):
        return redirect("/")
    else:
        return render_template("error.html", message="Registering failed. Try another username")
    

    
@app.route("/users")
def users_list():
    users_listed=users.list_users()
    return render_template("users.html", users_listed=users_listed)

@app.route("/deleteUser", methods=["POST"])
def delete():    
    id = request.form["id"]
    users.delete_user(id)
    return redirect("/users")



@app.route("/config")
def config():
    configuration=draft_config.load_config()
    teams_list=teams.load_teams()
    return render_template("config.html", configuration=configuration, teams_list = teams_list)

@app.route("/toggleConfirmConfig", methods=["POST"])
def toggle_confirm_config():
    id = request.form["id"]
    confirmed = request.form["confirmed"]
    if draft_config.toggle_lock_config(id, confirmed):
        config=draft_config.load_config()
        teams.init_teams(config[2])
        teams_info =  teams.load_teams()
        draft.init_picks(config, teams_info)
        return redirect("config")
    else:
        teams.delete_teams()
        return redirect("config")

@app.route("/updateConfig", methods=["POST"])
def update_config():
    id = request.form["id"]
    name = request.form["name"]
    participants = request.form["participants"]
    rounds = request.form["rounds"]
    snake = request.form["snake"]
    if draft_config.update_config(id, name, participants, rounds, snake):
        return redirect("config")
    else:
        render_template("error.html", message="Settings update failed")


        
@app.route("/updateTeams", methods=["POST"])
def update_teams():
    ids = request.form.getlist("id")
    names = request.form.getlist("name")
    if teams.update_teams(ids,names):
        return redirect("config")
    else:
        return render_template("error.html", message="Teamnames must be unique")

@app.route("/selectTeam", methods=["POST"])    
def select_team():
    teamId = request.form["teamId"]
    username = request.form["username"]
    if teams.select_team(teamId, username):
        return redirect("/")
    else:
        return render_template("error.html", message="Team is already taken.")
    





@app.route("/players")
def get_players():
    players_list=players.load_players()
    players_list.reverse()
    return render_template("players.html", players_list=players_list)
    
@app.route("/addPlayer", methods=["POST"])
def add_player():
    iss = request.form["iss"]
    name = request.form["name"]
    role = request.form["role"]
    
    if players.add_player(iss, name, role):
        return redirect("players")
    else:
        return render_template("error.html", message="ISS number must be unique")
    
    
@app.route("/list/<int:user_id>")
def draftList(user_id):
    if user_id != session["user_id"]:
        return render_template("error.html", message="Unauthorized")
    else:
        max_items = 10
        current_list=user_players.load_list(user_id)
        players_list=players.load_available_players(user_id)
        return render_template("list.html", current_list=current_list, players_list=players_list, max_items=max_items)
    
@app.route("/addItem", methods=["POST"])
def add_item_to_list():
    user_id = session["user_id"]
    player_id = request.form["player_id"]
    list_order = request.form["order"]
    
    if (user_players.add_item(user_id, player_id, list_order)):
        return redirect(request.referrer)
    else:
        return render_template("error.html", message="Index not unique.")
    
@app.route("/editItem", methods=["POST"])
def edit_item_in_list():
    user_id = session["user_id"]
    player_id = request.form["player_id"]
    item_id = request.form["item_id"]
    if (user_players.edit_item(item_id,user_id,player_id)):
        return redirect(request.referrer)
    else:
        return render_template("error.html", message="Index not unique")
    
@app.route("/deleteItem", methods=["POST"])
def delete_item_in_list():
    user_id = session["user_id"]
    item_id = request.form["item_id"]
    order = request.form["order"]
    user_players.delete_item(item_id, user_id, order)
    return redirect(request.referrer)

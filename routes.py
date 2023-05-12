from flask import render_template, request, redirect, session
from app import app
import users, players, draft_config, teams, draft, user_players

@app.route("/")
def index():
    if "username" in session:
        team_list = teams.load_free_teams()
        user_team = teams.check_team(session["username"])
        user_team_id = None
        if (user_team):
            user_team_id=user_team[0]
        user_picks = draft.team_picks_list(user_team_id)            
        next_pick = draft.next_pick()
        return render_template("index.html", team_list=team_list, 
                               user_team=user_team, next_pick=next_pick, user_picks=user_picks)
    else:
        return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
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

@app.route("/deleteOwnUser", methods=["POST"])
def delete_own():
    if session["admin"]:
        return render_template("error.html", message="Admins can not delete their account")
    else:    
        id = session["user_id"]
        users.delete_user(id)
        users.logout()
        return redirect("/")

@app.route("/profile")
def profile():
    user_team = teams.check_team(session["username"])
    return render_template("profile.html", user_team=user_team)



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
        return render_template("error.html", message="Settings update failed")


        
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
    team_id = request.form["team_id"]
    username = request.form["username"]
    if teams.select_team(team_id, username):
        return redirect("/")
    else:
        return render_template("error.html", message="Team is already taken.")

@app.route("/unselectTeam", methods=["POST"])    
def unselect_team():
    user_id = session["user_id"]
    teams.unselect_team(user_id)    
    return redirect("/")



@app.route("/players")
def get_players():
    players_list=players.load_players()
    players_list.reverse()
    return render_template("players.html", players_list=players_list)
    
@app.route("/addPlayer", methods=["POST"])
def add_player():
    if not "admin" in session:
        return render_template("error.html", message="Not Authorized")
    iss = request.form["iss"]
    name = request.form["name"]
    role = request.form["role"]   
    if players.add_player(iss, name, role):
        return redirect("players")
    return render_template("error.html", message="ISS number must be unique")
    
@app.route("/deletePlayer", methods=["POST"])
def del_player():
    if not "admin" in session:
        return render_template("error.html", message="Not Authorized")
    player_id = request.form["id"]
    players.delete_player(player_id)
    return redirect(request.referrer)
    
@app.route("/list")
def draft_list():
    user_id=session["user_id"]
    max_items = 100
    current_list=user_players.load_list(user_id)
    players_list=players.load_available_players_for_user(user_id)
    return render_template("list.html", current_list=current_list, 
                           players_list=players_list, max_items=max_items)

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


@app.route("/draft")
def draft_page():
    next_pick = draft.next_pick()
    picks = draft.picks_list()
    players_available = players.check_available()
    picks_left = draft.picks_left()
    return render_template("draft.html", next_pick=next_pick, picks=picks,
                           players_available=players_available, picks_left=picks_left) 

@app.route("/makeNextPick", methods=["POST"])
def admin_make_pick():
    if "admin" in session:
        draft.make_next_pick()
        return redirect(request.referrer)
    return render_template("error.html", message="Not Authorized")

@app.route("/revertLastPick", methods=["POST"])
def revert_pick():
    if "admin" in session:
        draft.revert_last_pick()
        return redirect(request.referrer)
    return render_template("error.html", message="Not Authorized")

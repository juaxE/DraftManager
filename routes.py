from flask import render_template, request, redirect, session
from app import app
import users
import players
import draft_config
import teams
import draft
import user_players

@app.route("/")
def index():
    if users.require_user():
        team_list = teams.load_free_teams()
        user_team = teams.check_team(session["username"])
        user_team_id = None
        if user_team:
            user_team_id = user_team[0]
        user_picks = draft.team_picks_list(user_team_id)
        next_pick = draft.next_pick()
        return render_template("index.html", team_list=team_list,
                               user_team=user_team, next_pick=next_pick, user_picks=user_picks)
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
    if not 2 < len(username) < 21:
        return render_template("error.html",
                               message="Username needs to be between 3 and 20 characters long")
    password1 = request.form["password1"]
    if not 4 < len(password1) < 31:
        return render_template("error.html",
                               message="Your password needs to be between 5 and 30 characters long")
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("error.html", message="Passwords do not match")
    if users.register_send(username, password1):
        return redirect("/")
    return render_template("error.html", message="Username already taken")



@app.route("/users")
def users_list():
    if not users.require_admin():
        return render_template("error.html", message="Not Authorized")
    users_listed = users.list_users()
    return render_template("users.html", users_listed=users_listed)

@app.route("/deleteUser", methods=["POST"])
def deleting_user():
    if not users.require_admin():
        return render_template("error.html", message="Not Authorized")
    user_id = request.form["id"]
    users.delete_user(user_id)
    return redirect("/users")



@app.route("/profile")
def profile():
    if not users.require_user():
        return render_template("error.html", message="Please log in")
    user_team = teams.check_team(session["username"])
    return render_template("profile.html", user_team=user_team)

@app.route("/deleteOwnUser", methods=["POST"])
def delete_own():
    if users.require_admin():
        return render_template("error.html", message="Admins can not delete their account")
    user_id = session["user_id"]
    users.delete_user(user_id)
    users.logout()
    return redirect("/")



@app.route("/config")
def load_draft_config():
    if not users.require_admin():
        return render_template("error.html", message="Not Authorized")
    configuration = draft_config.load_config()
    teams_list = teams.load_teams()
    return render_template("config.html", configuration=configuration, teams_list=teams_list)

@app.route("/toggleConfirmConfig", methods=["POST"])
def toggle_confirm_config():
    if not users.require_admin():
        return render_template("error.html", message="Not Authorized")
    config_id = request.form["id"]
    confirmed = request.form["confirmed"]
    if draft_config.toggle_lock_config(config_id, confirmed):
        current_config = draft_config.load_config()
        teams.init_teams(current_config[2])
        teams_info = teams.load_teams()
        draft.init_picks(current_config, teams_info)
        return redirect("config")
    teams.delete_teams()
    return redirect("config")

@app.route("/updateConfig", methods=["POST"])
def update_config():
    if not users.require_admin():
        return render_template("error.html", message="Not Authorized")
    config_id = request.form["id"]
    name = request.form["name"]
    if not 0 < len(name) < 41:
        return render_template("error.html",
                               message="Name must be non-empty and maximum of 40 characters")
    participants = request.form["participants"]
    if not 0 < int(participants) < 51:
        return render_template("error.html",
                               message="Amount of participants must be between 1 and 50")
    rounds = request.form["rounds"]
    if not 0 < int(rounds) < 41:
        return render_template("error.html",
                               message="Amount of rounds must be between 1 and 40")
    snake = request.form["snake"]
    if draft_config.update_config(config_id, name, participants, rounds, snake):
        return redirect("config")
    return render_template("error.html", message="Config update failed")

@app.route("/updateTeams", methods=["POST"])
def update_teams():
    if not users.require_admin():
        return render_template("error.html", message="Not Authorized")
    team_ids = request.form.getlist("id")
    names = request.form.getlist("name")
    for name in names:
        if not 0 < len(name) < 61:
            return render_template("error.html",
                                   message="Teamnames must be non-empty and maximum 60 characters")
    if teams.update_teams(team_ids, names):
        return redirect("config")
    return render_template("error.html", message="Teamnames must be unique")


@app.route("/selectTeam", methods=["POST"])
def select_team():
    if not users.require_user():
        return render_template("error.html", message="Please log in")
    team_id = request.form["team_id"]
    username = session["username"]
    if teams.select_team(team_id, username):
        return redirect("/")
    return render_template("error.html", message="Team is already taken.")

@app.route("/unselectTeam", methods=["POST"])
def unselect_team():
    user_id = session["user_id"]
    teams.unselect_team(user_id)
    return redirect("/")



@app.route("/players")
def get_players():
    if not users.require_user():
        return render_template("error.html", message="Please log in")
    players_list = players.load_players()
    players_list.reverse()
    return render_template("players.html", players_list=players_list)

@app.route("/addPlayer", methods=["POST"])
def add_player():
    if not users.require_admin():
        return render_template("error.html", message="Not Authorized")
    iss = request.form["iss"]
    if not 0 < int(iss) < 32768:
        return render_template("error.html", message="Iss number must be between 1 and 32767")
    name = request.form["name"]
    if not 0 < len(name) < 101:
        return render_template("error.html",
                               message="Name must be non-empty and maximum 100 characters long")
    role = request.form["role"]
    if players.add_player(iss, name, role):
        return redirect("players")
    return render_template("error.html", message="ISS number must be unique")

@app.route("/deletePlayer", methods=["POST"])
def del_player():
    if not users.require_admin():
        return render_template("error.html", message="Not Authorized")
    player_id = request.form["id"]
    players.delete_player(player_id)
    return redirect(request.referrer)




@app.route("/list")
def draft_list():
    if not users.require_user():
        return render_template("error.html", message="Please log in")
    user_id = session["user_id"]
    max_items = 100
    current_list = user_players.load_list(user_id)
    players_list = players.load_available_players_for_user(user_id)
    return render_template("list.html", current_list=current_list,
                           players_list=players_list, max_items=max_items)

@app.route("/addItem", methods=["POST"])
def add_item_to_list():
    user_id = session["user_id"]
    player_id = request.form["player_id"]
    list_order = request.form["order"]
    if user_players.add_item(user_id, player_id, list_order):
        return redirect(request.referrer)
    return render_template("error.html", message="Index not unique.")

@app.route("/editItem", methods=["POST"])
def edit_item_in_list():
    user_id = session["user_id"]
    player_id = request.form["player_id"]
    item_id = request.form["item_id"]
    if user_players.edit_item(item_id, user_id, player_id):
        return redirect(request.referrer)
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
    if not users.require_user():
        return render_template("error.html", message="Please log in")
    next_pick = draft.next_pick()
    picks = draft.picks_list()
    players_available = players.check_available()
    picks_left = draft.picks_left()
    return render_template("draft.html", next_pick=next_pick, picks=picks,
                           players_available=players_available, picks_left=picks_left)

@app.route("/makeNextPick", methods=["POST"])
def admin_make_pick():
    if not users.require_admin():
        return render_template("error.html", message="Not Authorized")
    draft.make_next_pick()
    return redirect(request.referrer)

@app.route("/revertLastPick", methods=["POST"])
def revert_pick():
    if not users.require_admin():
        return render_template("error.html", message="Not Authorized")
    draft.revert_last_pick()
    return redirect(request.referrer)

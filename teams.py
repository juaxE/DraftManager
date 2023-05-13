from sqlalchemy import text
from db import db
import users

def init_teams(amount):
    for i in range(amount):
        index = i+1
        sql = text("INSERT INTO teams (name, position, created_at) "\
                   "VALUES (:name, :position, NOW())")
        db.session.execute(sql, {"name":index, "position":index})
        db.session.commit()

def load_teams():
    sql = text("SELECT id, name, position FROM teams ORDER BY position ASC")
    result = db.session.execute(sql)
    return result.fetchall()

def delete_teams():
    users.reset_team_ids()
    sql = text("DELETE FROM teams")
    db.session.execute(sql)
    db.session.commit()

def update_teams(team_ids, names):
    try:
        for (team_id, name) in zip(team_ids, names):
            sql = text("UPDATE teams SET name=:name WHERE id=:id")
            db.session.execute(sql, {"name":name, "id":team_id})
            db.session.commit()
    except Exception:
        return False
    return True

def load_free_teams():
    sql = text("SELECT teams.id, teams.name FROM teams "\
               "LEFT JOIN users ON teams.id = users.team_id WHERE users.team_id IS NULL")
    result = db.session.execute(sql)
    return result.fetchall()

def check_team(username):
    sql = text("SELECT teams.id, teams.name FROM teams "\
               "LEFT JOIN users ON teams.id = users.team_id WHERE users.username=:username")
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()

def select_team(team_id, username):
    try:
        sql = text("UPDATE users SET team_id=:team_id WHERE username=:username")
        db.session.execute(sql, {"team_id":team_id, "username":username})
        db.session.commit()
        return True
    except Exception:
        return False

def unselect_team(user_id):
    sql = text("UPDATE users SET team_id=NULL WHERE id=:user_id")
    db.session.execute(sql, {"user_id":user_id})
    db.session.commit()

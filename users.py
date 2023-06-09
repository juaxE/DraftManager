from flask import session
from werkzeug.security import check_password_hash, generate_password_hash, secrets
from sqlalchemy import text
from db import db

def check(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    hash_value = user.password
    if check_password_hash(hash_value, password):
        check_admin(username)
        return True
    return False

def check_admin(username):
    sql = text('SELECT admin FROM users WHERE username=:username')
    result = db.session.execute(sql, {"username":username})
    admin_status = result.fetchone()
    if admin_status[0]:
        session["admin"] = True

def login(username, password):
    if check(username, password):
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        set_id(username)
        return True
    return False

def set_id(username):
    sql = text("SELECT users.id FROM users WHERE users.username=:username")
    result = db.session.execute(sql, {"username":username})
    session["user_id"] = result.scalar()

def register_send(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password, created_at) "\
                   "VALUES (:username, :password, NOW())")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except Exception:
        return False
    session["username"] = username
    set_id(username)
    session["csrf_token"] = secrets.token_hex(16)
    return True

def get_team_owner(team_id):
    try:
        sql = text("SELECT u.id FROM users u JOIN teams t ON u.team_id = t.id WHERE t.id=:team_id")
        result = db.session.execute(sql, {"team_id":team_id})
        return result.scalar()
    except Exception:
        return None

def logout():
    session.clear()

def list_users():
    sql = text("SELECT users.id, users.username, teams.name FROM users "\
               "LEFT JOIN teams ON users.team_id = teams.id WHERE admin IS NULL")
    result = db.session.execute(sql)
    return result.fetchall()

def delete_user(user_id):
    sql = text("DELETE FROM users WHERE id=:id")
    db.session.execute(sql, {"id":user_id})
    db.session.commit()

def reset_team_ids():
    sql = text("UPDATE users SET team_id=NULL")
    db.session.execute(sql)
    db.session.commit()

def require_admin():
    if "admin" in session:
        return True
    return False

def require_user():
    if "username" in session:
        return True
    return False

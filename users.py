from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
from db import db

def check(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user.password
    if check_password_hash(hash_value, password):
        check_admin(username)
        return True
    else:
        return False
    
def check_admin(username):
    sql = text('SELECT admin FROM users WHERE username=:username')
    result = db.session.execute(sql, {"username":username})
    admin_status = result.fetchone()
    if admin_status[0]==True:
        session["admin"] = True
    else:
        session["admin"] = False
    return
    
def login(username, password):
    if(check(username,password)==True):
        session["username"] = username
        set_id(username)
        
        return True
    else:
        return False
    
def set_id(username):
    sql = text("SELECT users.id FROM users WHERE users.username=:username")
    result = db.session.execute(sql, {"username":username})
    session["user_id"] = result.scalar()    

def register_send(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password, created_at) VALUES (:username, :password, NOW())")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    session["username"] = username
    set_id(username)
    return True

def logout():    
    try:
        del session["username"]
        del session["user_id"]
        del session["admin"]
    except:
        pass

def list_users():
    sql = text("SELECT users.id, users.username, teams.name FROM users LEFT JOIN teams ON users.team_id = teams.id WHERE admin IS NULL")
    result = db.session.execute(sql)
    return result.fetchall()

def delete_user(id):
    sql = text("DELETE FROM users WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    
def reset_team_ids():
    sql = text("UPDATE users SET team_id=NULL")
    db.session.execute(sql)
    db.session.commit()
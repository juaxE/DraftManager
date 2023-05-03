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
        checkAdmin(username)
        return True
    else:
        return False
    
def checkAdmin(username):
    sql = text('SELECT admin FROM users WHERE username=:username')
    result = db.session.execute(sql, {"username":username})
    adminStatus = result.fetchone()
    if adminStatus[0]==True:
        session["admin"] = True
    else:
        session["admin"] = False
    return
    
def login(username, password):
    if(check(username,password)==True):
        session["username"] = username
        setId(username)
        
        return True
    else:
        return False
    
def setId(username):
    sql = text("SELECT users.id FROM users WHERE users.username=:username")
    result = db.session.execute(sql, {"username":username})
    session["userId"] = result.scalar()
    return 
    

def registerSend(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password, created_at) VALUES (:username, :password, NOW())")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    session["username"] = username
    setId(username)
    return True

def logout():    
    try:
        del session["username"]
        del session["userId"]
        del session["admin"]
    except:
        pass

def listUsers():
    sql = text("SELECT users.id, users.username, teams.name FROM users LEFT JOIN teams ON users.team_id = teams.id WHERE admin IS NULL")
    result = db.session.execute(sql)
    return result.fetchall()

def deleteUser(id):
    sql = text("DELETE FROM users WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    
def resetTeamIds():
    sql = text("UPDATE users SET team_id=NULL")
    db.session.execute(sql)
    db.session.commit()
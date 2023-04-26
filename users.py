from db import db
from app import app
from os import getenv
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
from flask import redirect, render_template, request, session

app.secret_key = getenv("SECRET_KEY")


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
    return
    
def login(username, password):
    if(check(username,password)==True):
        session["username"] = username
        return True
    else:
        return False
    
def register():
    return render_template("register.html")

def registerSend(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return True

def logout():    
    del session["username"]
    try:
        del session["admin"]
    except:
        pass
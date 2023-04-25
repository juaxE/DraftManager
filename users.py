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
        return True
    else:
        return False
    
def login():
    username = request.form["username"]
    password = request.form["password"]
    if(check(username,password)==True):
        session["username"] = username
        return redirect("/")
    else:
        return redirect("/")
    
def register():
    return render_template("register.html")

def registerSend():
    username = request.form["username"]
    hash_value = generate_password_hash(request.form["password"])
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    return redirect("/")

def logout():
    del session["username"]
    return redirect("/")
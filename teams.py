from flask import session
from sqlalchemy import text
from db import db

def initTeams(amount):
    for i in range(amount):
        index = i+1
        sql = text("INSERT INTO teams (name, position) VALUES (:name, :position)")
        db.session.execute(sql, {"name":index, "position":index})
        db.session.commit()

def loadTeams():
    sql = text("SELECT id, name, position FROM teams")
    result = db.session.execute(sql)
    return result.fetchall()

def deleteTeams():
    sql = text("DELETE FROM teams")
    db.session.execute(sql)
    db.session.commit()
    
def updateTeams(ids, names):
    
    for i in range(len(ids)):
        id=ids[i]
        name=names[i]        
        sql = text("UPDATE teams SET name=:name WHERE id=:id")
        db.session.execute(sql, {"name":name, "id":id})
        db.session.commit()
from flask import session
from sqlalchemy import text
from db import db

def initTeams(amount):
    for i in range(amount):
        index = i+1
        sql = text("INSERT INTO teams (name, position, created_at) VALUES (:name, :position, NOW())")
        db.session.execute(sql, {"name":index, "position":index})
        db.session.commit()

def loadTeams():
    sql = text("SELECT id, name, position FROM teams ORDER BY position ASC")
    result = db.session.execute(sql)
    return result.fetchall()

def deleteTeams():
    sql = text("DELETE FROM teams")
    db.session.execute(sql)
    db.session.commit()
    
def updateTeams(ids, names):
    
    try:
        for i in range(len(ids)):
            id=ids[i]
            name=names[i]        
            sql = text("UPDATE teams SET name=:name WHERE id=:id")
            db.session.execute(sql, {"name":name, "id":id})
            db.session.commit()
            sql = text("UPDATE users SET team_id=NULL WHERE team_id=:id")
            db.session.execute(sql, {"id":id})
            db.session.commit()            
    except:
        return False
    else:
        return True
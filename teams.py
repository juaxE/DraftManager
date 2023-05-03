from sqlalchemy import text
from db import db
import users

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
    users.resetTeamIds() 
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
    except:
        return False
    else:
        return True
    
def loadFreeTeams():
    sql = text("SELECT teams.id, teams.name FROM teams LEFT JOIN users ON teams.id = users.team_id WHERE users.team_id IS NULL")
    result = db.session.execute(sql)
    return result.fetchall()

def checkTeam(username):
    sql = text("SELECT teams.id, teams.name FROM teams LEFT JOIN users ON teams.id = users.team_id WHERE users.username=:username")
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()

def selectTeam(team_id, username):
    try:
        sql = text("UPDATE users SET team_id=:team_id WHERE username=:username")
        db.session.execute(sql, {"team_id":team_id, "username":username})
        db.session.commit()
        return True
    except:
        return False
from db import db
from sqlalchemy import text

def addPlayer(iss, name, role):
    
    try: 
        sql = text("INSERT INTO players (iss, name, role, created_at) VALUES (:iss, :name, :role, NOW())")
        db.session.execute(sql, {"iss":iss, "name":name, "role":role})
        db.session.commit()
    except:
        return False
    return True

def loadPlayers():
    sql = text("SELECT id, iss, name, role, drafted FROM players ORDER BY iss ASC")
    result = db.session.execute(sql)
    return result.fetchall()

def loadAvailablePlayers(user_id):
    sql = text("SELECT p.id, p.iss, p.name, p.role FROM players p WHERE p.drafted=FALSE " \
               "AND NOT EXISTS( SELECT 1 FROM user_players up WHERE up.user_id=:user_id AND up.player_id=p.id) ORDER BY iss ASC")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def deletePlayer(id):
    sql = text("DELETE FROM players WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    
def updatePlayer(id, iss, name, role):    
    try:
        sql = text("UPDATE players SET iss=:iss, name=:name, role=:role WHERE id=:id")
        db.session.execute(sql, {"id":id, "iss":iss, "name":name, "role":role})
        db.session.commit()
    except:
        return False
    return True
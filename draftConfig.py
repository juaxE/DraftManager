from db import db
from sqlalchemy import text


def loadConfig():
    sql = text("SELECT id, name, participants, rounds, snake FROM draft_configuration")
    result = db.session.execute(sql)
    config = result.fetchall()
    if not config:
        return newConfig()    
    return config
    
def newConfig():
    sql = text("INSERT INTO draft_configuration (name, participants, rounds, snake) VALUES (Default, 30, 7, False)")
    db.session.execute(sql)
    db.session.commit()
    return loadConfig()

def updateConfig(id, name, participants, rounds, snake):
    sql = text("UPDATE draft_configuration SET name=:name, participants=:participants, rounds=:rounds, snake=:snake WHERE id=:id")
    try:
        db.session.execute(sql, {"id":id, "name":name, "participants":participants, "rounds":rounds, "snake":snake})
        db.session.commit()
    except:
        return False
    return True
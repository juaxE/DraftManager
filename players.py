from db import db
from sqlalchemy import text

def add_player(iss, name, role):
    
    try: 
        sql = text("INSERT INTO players (iss, name, role, created_at) VALUES (:iss, :name, :role, NOW())")
        db.session.execute(sql, {"iss":iss, "name":name, "role":role})
        db.session.commit()
    except:
        return False
    return True

def load_players():
    sql = text("SELECT id, iss, name, role, drafted FROM players ORDER BY iss ASC")
    result = db.session.execute(sql)
    return result.fetchall()

def load_available_players_for_user(user_id):
    sql = text("SELECT p.id, p.iss, p.name, p.role FROM players p WHERE p.drafted=FALSE " \
               "AND NOT EXISTS( SELECT 1 FROM user_players up WHERE up.user_id=:user_id AND up.player_id=p.id) ORDER BY iss ASC")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def load_available_players():
    sql = text("SELECT p.id, p.iss, p.name, p.role FROM players p WHERE p.drafted=FALSE " \
               "ORDER BY iss ASC")
    result = db.session.execute(sql,)
    return result.fetchall()

def set_drafted(player_id):
    sql = text("UPDATE players SET drafted=True WHERE id=:player_id")
    db.session.execute(sql, {"player_id":player_id})
    db.session.commit()

def delete_player(id):
    sql = text("DELETE FROM players WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    
def update_player(id, iss, name, role):    
    try:
        sql = text("UPDATE players SET iss=:iss, name=:name, role=:role WHERE id=:id")
        db.session.execute(sql, {"id":id, "iss":iss, "name":name, "role":role})
        db.session.commit()
    except:
        return False
    return True
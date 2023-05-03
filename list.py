from sqlalchemy import text
from db import db


def loadList(user_id):
    sql = text("SELECT user_players.id, user_players.list_order, players.id, players.iss, players.name, players.role FROM user_players INNER JOIN players ON user_players.player_id=players.id WHERE user_players.user_id=:user_id ORDER BY user_players.list_order ASC")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def addItem(user_id,  player_id, list_order):    
    try:
        sql = text("INSERT INTO user_players (user_id, player_id, list_order, created_at) VALUES (:user_id, :player_id, :list_order, NOW())")
        db.session.execute(sql, {"user_id":user_id, "player_id":player_id, "list_order":list_order})
        db.session.commit()
    except:
        return False
    return True

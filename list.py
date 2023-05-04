from sqlalchemy import text
from db import db


def loadList(user_id):
    sql = text("SELECT user_players.id, user_players.list_order, players.id, players.iss, players.name, players.role, players.drafted FROM user_players INNER JOIN players ON user_players.player_id=players.id WHERE user_players.user_id=:user_id ORDER BY user_players.list_order ASC")
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

def editItem(id, user_id, player_id):
    try:
        sql = text("UPDATE user_players SET player_id=:player_id WHERE id=:id AND user_id=:user_id")
        db.session.execute(sql, {"id":id, "player_id":player_id, "user_id":user_id})
        db.session.commit()
    except:
        return False
    return True

def deleteItem(id, user_id, order):
    sql = text("DELETE from user_players WHERE id=:id AND user_id=:user_id")
    db.session.execute(sql,{"id":id, "user_id":user_id})
    db.session.commit()
    fix_order(order, user_id)

def fix_order(list_order, user_id):
    sql = text("UPDATE user_players up SET list_order = CASE WHEN up.list_order > :list_order THEN up.list_order - 1 ELSE up.list_order END " \
                "WHERE up.user_id=:user_id")
    db.session.execute(sql, {"list_order":list_order, "user_id":user_id})
    db.session.commit()

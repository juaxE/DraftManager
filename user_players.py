from sqlalchemy import text
from db import db
import players

def load_list(user_id):
    sql = text("SELECT user_players.id, user_players.list_order, players.id, players.iss, players.name, players.role, players.drafted FROM user_players INNER JOIN players ON user_players.player_id=players.id WHERE user_players.user_id=:user_id ORDER BY user_players.list_order ASC")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def first_in_list(user_id):
    sql = text("SELECT up.player_id FROM user_players up JOIN players p ON up.player_id = p.id" \
               " WHERE up.user_id =:user_id AND p.drafted IS FALSE ORDER BY up.list_order ASC limit 1")
    result = db.session.execute(sql, {"user_id":user_id})
    player_id = result.scalar()
    if player_id:
        return player_id
    player_id = players.load_next_available_player()  
    return player_id

def add_item(user_id,  player_id, list_order):    
    try:
        sql = text("INSERT INTO user_players (user_id, player_id, list_order, created_at) VALUES (:user_id, :player_id, :list_order, NOW())")
        db.session.execute(sql, {"user_id":user_id, "player_id":player_id, "list_order":list_order})
        db.session.commit()
    except:
        return False
    return True

def edit_item(id, user_id, player_id):
    try:
        sql = text("UPDATE user_players SET player_id=:player_id WHERE id=:id AND user_id=:user_id")
        db.session.execute(sql, {"id":id, "player_id":player_id, "user_id":user_id})
        db.session.commit()
    except:
        return False
    return True

def delete_item(id, user_id, order):
    sql = text("DELETE from user_players WHERE id=:id AND user_id=:user_id")
    db.session.execute(sql,{"id":id, "user_id":user_id})
    db.session.commit()
    fix_order(order, user_id)

def fix_order(list_order, user_id):
    sql = text("UPDATE user_players up SET list_order = CASE WHEN up.list_order > :list_order THEN up.list_order - 1 ELSE up.list_order END " \
                "WHERE up.user_id=:user_id")
    db.session.execute(sql, {"list_order":list_order, "user_id":user_id})
    db.session.commit()

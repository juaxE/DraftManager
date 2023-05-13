from sqlalchemy import text
from db import db


def load_config():
    sql = text("SELECT id, name, participants, rounds, snake, confirmed FROM draft_configuration")
    result = db.session.execute(sql)
    config = result.fetchone()
    if not config:
        return new_config()
    return config

def new_config():
    sql = text("INSERT INTO draft_configuration "\
               "(name, participants, rounds, snake, confirmed) "\
                "VALUES (Default, 30, 7, False, False)")
    db.session.execute(sql)
    db.session.commit()
    return load_config()

def toggle_lock_config(config_id, confirmed):
    if confirmed == "False":
        confirmed = "True"
    elif confirmed == "True":
        confirmed = "False"
    sql = text("UPDATE draft_configuration SET confirmed=:confirmed WHERE id=:id")
    db.session.execute(sql, {"id":config_id, "confirmed":confirmed})
    db.session.commit()
    if confirmed == "False":
        return False
    return True

def update_config(config_id, name, participants, rounds, snake):
    sql = text("UPDATE draft_configuration SET name=:name, participants=:participants, "\
            "rounds=:rounds, snake=:snake WHERE id=:id")
    try:
        db.session.execute(sql, {"id":config_id, "name":name,
                                 "participants":participants, "rounds":rounds, "snake":snake})
        db.session.commit()
    except Exception:
        return False
    return True

def delete_config(config_id):
    sql = text("DELETE FROM draft_configuration WHERE id=:id")
    db.session.execute(sql, {"id":config_id})
    db.session.commit()

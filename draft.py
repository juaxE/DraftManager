from sqlalchemy import text
from db import db
import users
import user_players
import players

def init_picks(config, teamsInfo):
    participants = config[2]
    rounds = config[3]
    team_ids = [item[0] for item in teamsInfo]
    total_picks = participants*rounds
    
    for i in range(total_picks):
        pickorder=i+1
        team_index = i%participants
        team_id = team_ids[team_index]
        
        sql = text("INSERT INTO draft_picks (pickorder, team_id, created_at) VALUES (:pickorder, :team_id, NOW())")
        db.session.execute(sql, {"pickorder":pickorder, "team_id":team_id})
        db.session.commit()

def picks_list():
    sql = text("SELECT dp.id, dp.pickorder, t.name, p.name, p.iss t FROM draft_picks dp LEFT JOIN teams t ON dp.team_id = t.id" \
                " LEFT JOIN players p ON dp.player_id = p.id ORDER BY pickorder ASC")
    result = db.session.execute(sql)
    return result.fetchall()
        
def next_pick():
    sql = text("SELECT id, pickorder, team_id FROM draft_picks WHERE player_id IS NULL ORDER BY pickorder ASC")
    result = db.session.execute(sql)
    return result.fetchone()

def make_next_pick():
    pick = next_pick()
    pick_id = pick[0]
    team_picking = pick[2]
    user_id = users.get_team_owner(team_picking)
    if user_id:
        player_id = user_players.first_in_list(user_id)[0]
    else:
        player_id = players.load_available_players()[0][0]
    sql = text("UPDATE draft_picks SET player_id=:player_id WHERE id =:pick_id")
    db.session.execute(sql, {"player_id":player_id, "pick_id":pick_id})
    db.session.commit() 
    players.set_drafted(player_id)
    
    
from sqlalchemy import text
from db import db

def init_picks(config, teamsInfo):
    participants = config[2]
    rounds = config[3]
    teamIds = [item[0] for item in teamsInfo]
    totalPicks = participants*rounds
    
    for i in range(totalPicks):
        pickorder=i+1
        teamIndex = i%participants
        team_id = teamIds[teamIndex]
        
        sql = text("INSERT INTO draft_picks (pickorder, team_id, created_at) VALUES (:pickorder, :team_id, NOW())")
        db.session.execute(sql, {"pickorder":pickorder, "team_id":team_id})
        db.session.commit()
        
def next_pick():
    sql = text("SELECT pickorder, team_id FROM draft_picks WHERE player_id IS NULL ORDER BY pickorder ASC")
    result = db.session.execute(sql)
    return result.fetchone()
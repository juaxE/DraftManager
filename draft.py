from sqlalchemy import text
from db import db

def initPicks(config, teamsInfo):
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
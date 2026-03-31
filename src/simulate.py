import csv 
import numpy as np 
from config import PROCESSED_DIR, DEF_SEASON, TEAM, POINTS_DRAW, POINTS_LOSS, POINTS_WIN


#Reads CSV and splits into played and remaining matches
def load_matches(season: int = DEF_SEASON):
    played = []
    remaining = []
    path = PROCESSED_DIR / f"matches_{season}.csv"

    with path.open(encoding = "utf-8") as f:

        for row in csv.DictReader(f):
            if row["home-goals"] and row["away_goals"]:
                row["home_goals]"] = int(row["home_goals"])
                row["away_goals"] = int(row["away_goals"])
                played.append(row)

            else:
                remaining.append(row)

    return played, remaining

def build_team_stats(played):

    stats = {}

    for m in played:
        home = m["home"]
        away = m["away"]
        hg = m["home_goals"]
        ag = m["away_goals"]

        if home not in stats:
            stats[home] = {"scored": 0, "conceded": 0, "games": 0}
        if away not in stats:
            stats[away] = {"scored": 0, "conceded": 0, "games": 0}

        stats[home]["scored"] +=hg
        stats[home]["conceded"] += ag
        stats[home]["games"] += 1

        stats[away]["scored"] +=hg
        stats[away]["conceded"] += ag
        stats[away]["games"] += 1
    
    for team in stats:
        g = stats[team]["games"]
        stats[team]["avg_scored"] = stats[team]["scored"] /g
        stats[team]["avg_conceded"] = stats[team]["conceded"] /g

    return stats

def simulate_match(home_team, away_team, stats):

    home_attack = stats[home_team]["avg_scored"]
    away_attack = stats[away_team]["avg_scored"]

    home_defense = stats[home_team]["avg_conceded"]
    away_defense = stats[away_team]["avg_conceded"]

#Creates an everage of one team's attack and anothers weaknesses
    home_expected = (home_attack + away_defense) / 2
    away_expected = (away_attack + home_defense) / 2

    home_goals = np.random.poisson(home_expected)
    away_goals = np.random.poisson(away_expected)

    return home_goals, away_goals

def build_table(played, sim_remaining):

    points = {}

    all_matches = played + sim_remaining

    for m in all_matches:
        home = m["home"]
        away = m["away"]

        hg = m["home_goals"]
        ag = m["away_goals"]

        if home not in points:
            points[home] = 0
            if away not in points:
                points[away] = 0
        #Points Distribution based on results
                if hg > ag:
                    points[home] += POINTS_WIN
                    points[away] += POINTS_LOSS
                elif ag > hg:
                    points[home] += POINTS_LOSS
                    points[away] += POINTS_WIN
                else:
                    points[home] += POINTS_DRAW
                    points[away] += POINTS_DRAW

        #This sorts teams in descending orders based on points        
        table = sorted(points.items(), key = lambda x: x[1], reverse = True)
        return table   

    def run_once(season: int = DEF_SEASON):
        played, remaining = load_matches(season)
        stats = build_team_stats(played)

        sim = []

        for m in remaining:
            hg, ag = simulate_match(m["home"], m["away"], stats)
            sim.append({
                "home": m["home"],
                "away": m["away"],
                "home_goals": hg,
                "away_goals": ag
            })  

            return build_table(played, sim)        



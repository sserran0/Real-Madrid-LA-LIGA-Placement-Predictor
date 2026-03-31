from config import NUM_SIMS, TEAM, DEF_SEASON
from simulate import run_once

def predict(season: int = DEF_SEASON, n_sims: int = NUM_SIMS):

    final_positions = []
    point_total = []
    title_wins = 0

    for i in range(n_sims):
        table = run_once(season)
        teams = [entry[0] for entry in table]
        points = dict(table)
        if TEAM not in points:
            raise RuntimeError(f"'{TEAM}' not found in results. Make sure team name matches API.")
        
        pos = teams.index(TEAM) + 1
        pts = points[TEAM]

        final_positions.append(pos)
        point_total.append(pts)

        if pos == 1:
            title_wins += 1

        if (i + 1) % 1000 == 0:
            print(f"{i + 1}/{n_sims} season simulations complete!")

    results = {
        "team": TEAM,
        "simulations": n_sims,
        "avg_points": sum(point_total) / n_sims,
        "min_points": min(point_total),
        "max_points": max(point_total),
        "avg_position": sum(final_positions) / n_sims,
        "title_prob": title_wins / n_sims * 100,
        "top_4_prob": sum(1 for p in final_positions if p <= 4) / n_sims * 100,
        "relegation_prob": sum(1 for p in final_positions if p >= 18) / n_sims * 100,
    }

    return results
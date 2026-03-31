import json 
import csv 
from pathlib import Path
from config import RAW_DIR, PROCESSED_DIR, DEF_SEASON

def main(season: int = DEF_SEASON):
    inPath = RAW_DIR / f"matches_{season}.json"
    outPath = PROCESSED_DIR / f"matches_{season}.csv"
    PROCESSED_DIR.mkdir(parents = True, exist_ok = True)
    data = json.loads(inPath.read_text(encoding = "utf-8"))
   
    with outPath.open("w", newline = "", encoding = "utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "home", "away", "home_goals", "away_goals"])

        for m in data.get("matches", []):
            full_time = (m.get("score") or {}).get("fullTime") or {}
            writer.writerow([
                m["utcDate"],
                m["homeTeam"]["name"], 
                m["awayTeam"]["name"],
                full_time.get("home"),
                full_time.get("away"),])
        

    print(f"Wrote CSV to {outPath}")

if __name__ == "__main__":
    main()





import json 
import csv 
from pathlib import Path
rawData = Path("data/raw")
processedData = Path("data/processed")

def main(season: int = 2025):
    inPath = rawData / f"matches_{season}.json"
    outPath = processedData / f"matches_{season}.csv"
    processedData.mkdir(parents = True, exist_ok = True)
    data = json.loads(inPath.read_text(encoding = "utf-8"))
   
    with outPath.open("w", newline = "", encoding = "utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "home", "away", "home_goals", "away_goals"])

        for m in data.get("matches", []):
            full_time = (m.get("score") or {}).get("fullTime") or {}
            writer.writerow([m["utcDate"], m["homeTeam"]["name"], m["awayTeam"]["name"],m["score"]["fullTime"]["home"],m["score"]["fullTime"]["away"],])

    print(f"Wrote CSV to {outPath}")

if __name__ == "__main__":
    main()





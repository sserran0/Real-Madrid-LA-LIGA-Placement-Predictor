import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
from config import API_URL, COMPETITION, RAW_DIR, DEF_SEASON

load_dotenv()

api_url = 'https://api.football-data.org/v4'
competition = "PD"
rawData = Path("data/raw")


def cache_raw_json(data: dict, filename: str) -> Path:
    rawData.mkdir(parents = True, exist_ok = True)
    path = rawData / filename
    path.write_text(json.dumps(data, indent = 2),encoding = "utf-8")
    return path
#function to cache raw json data fetched from api

def match_fetch(season: int) -> dict:
    url = f"{api_url}/competitions/{competition}/matches"
    apiKey = os.getenv("footballAPI")
    if not apiKey:
        raise RuntimeError()
    headers = {"X-Auth-Token": apiKey}
    params = {"season": season} 
    response = requests.get(url, headers=headers, params=params, timeout=30)
    print("Status:", response.status_code)
    response.raise_for_status()
    return response.json()

#function that fetches matches from api
def main():
    data = match_fetch(DEF_SEASON)
    cache_raw_json(data, f"matches_{DEF_SEASON}.json")
    



if __name__ == "__main__":
    main()
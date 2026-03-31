import argparse
from config import DEF_SEASON, NUM_SIMS, TEAM
from fetch import match_fetch, cache_raw_json
from normalize import main as normalize
from predict import predict

def parse_args():
    parser = argparse.ArgumentParser(
        description = "Predict Real Madrid's final position in LALiga EASports using Monte Carlos simulation."
    )
    parser.add_argument(
        "--season", type = int, default = DEF_SEASON,
        help = f"Season start year (default: {DEF_SEASON})"
    )
    parser.add_argument(
        "--sims", type = int, default = NUM_SIMS,
        help = f"Number of simulations to run (default: {NUM_SIMS})"
    )
    parser.add_argument(
        "--skip-fetch", action="store_true",
        help = "Skip API fetch and use cached data"
    )

    return parser.parse_args()


def display_results(results):
    print("\n" + "=" * 50)
    print(f" {results['team']} Season Prediction")
    print("=" * 50)
    print(f" Simulations Ran: {results['simulations']:,}")
    print(f" Avg Finishing Points: {results['avg_points']:.1f}")
    print(f" Points range:: {results['min_points']} - {results['max_points']}")
    print(f" Avg Finishing Position: {results['avg_position']:,}")
    print(f" Title Probability:       {results['title_prob']:.1f}%")
    print(f" Top 4 Probability:       {results['top_4_prob']:.1f}%")
    print(f" Relegation Probability: {results['relegation_prob']:.1f}%")
    print("=" * 50)

def main():
    args = parse_args()

    if not args.skip_fetch:
        print(f"Fetching match data for {args.season} season ...")
        data = match_fetch(args.season)
        cache_raw_json(data, f"matches_{args.season}.json")

    else:
        print ("Skipping fetch, using cached data...")

    print("Normalizing data...")
    normalize(args.season)
    print(f"Running {args.sims:,} simulations...")
    results = predict(season = args.season, n_sims=args.sims)

    display_results(results)

if __name__ == "__main__":
    main()



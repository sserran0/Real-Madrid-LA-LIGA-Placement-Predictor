## Real Madrid Season Predictor
A command-line tool that predicts Real Madrid's final La Liga standings using Monte Carlo simulation. Built with Python, it pulls live match data from the football-data.org API, analyzes completed results, and simulates the remainder of the season thousands of times to produce probabilistic predictions.
### Sample Output:

```
==================================================
 Real Madrid CF — Season Prediction
==================================================
 Simulations Ran:        10,000
 Avg Finishing Points:   85.7
 Points Range:           72 – 96
 Avg Finishing Position: 1.8
 Title Probability:      20.0%
 Top 4 Probability:      100.0%
 Relegation Probability: 0.0%
==================================================
```
### How It Works
The program follows a four-stage pipeline:
1. Fetch: Pulls every match for a given La Liga season from the football-data.org API and caches the raw JSON locally to avoid redundant API calls.
2. Normalization: Converts raw JSON into a clean CSV with one row per match: date, home team, away team, and the scoreline. Matches that haven't been played yet are preserved with empty score fields.
3. Simulation: Splits matches into played and remaining. From the played matches, it computes each team's average goals scored and conceded per game. It then simulates every remaining match by generating random goal counts, awards points (3 for a win, 1 for a draw, 0 for a loss), and produces a complete final league table.
4. Predict: Repeats the simulation 10,000 times and aggregates the results: average points, finishing position, title probability, top-4 probability, and relegation probability.

### The Math: Poisson Distribution
The core of the simulation utilizes the Poisson distribution to model goal-scoring. Poisson was the most natural fit for football I found because goals are:

Rare: teams typically score 0–4 goals, not dozens
Independent: one goal doesn't mechanically cause another
Defined by an average rate: each team has a measurable scoring rate per game

For each simulated match, the model computes expected goals by averaging the attacking team's scoring rate with the opposing team's concession rate:<br>
``
home_expected = (home_attack_avg + away_concede_avg) / 2
away_expected = (away_attack_avg + home_concede_avg) / 2
``

This makes every matchup unique — a strong attack against a weak defense produces more expected goals than against a strong defense. The Poisson distribution then generates a realistic random scoreline centered around that expectation.
Running this 10,000 times produces a distribution of outcomes that accounts for the inherent randomness of football that we know and love.

### Project Structure
```
src/
├── cli.py          # Entry point 
├── config.py       # Central configuration (API, paths, simulation settings)
├── fetch.py        # API data retrieval and caching
├── normalize.py    # JSON → CSV conversion
├── simulate.py     # Single season simulation engine
└── predict.py      # Monte Carlo loop and result aggregation
```

### Setup
Prerequisites: A free API key from [football-data.org](https://www.football-data.org/)
```
# Clone the repo
git clone https://github.com/sserran0/Real-Madrid-Predictor.git
cd Real-Madrid-Predictor/src

# Install dependencies
pip3 install requests python-dotenv numpy

# Add your API key
echo "footballAPI=your_api_key_here" > .env

# Run the predictor
python3 cli.py
```
### CLI Options
```
python3 cli.py                            # Full run with defaults
python3 cli.py --skip-fetch               # Reuse cached data
python3 cli.py --season 2023              # Predict a different season
python3 cli.py --sims 5000                # Adjust simulation count
```
### What I Learned

- Monte Carlo methods: using repeated random sampling to estimate outcomes 
- Poisson distribution: modeling rare, independent events with a known average rate, and how it applies to football scoring
- API integration: working with REST APIs, handling caching responses and parsing nested JSON
- Data pipeline design: structuring a project as a series of modular transformation steps, organizing linear code production (fetch → normalization → simulation → predict)
- CLI design with argparse: building flexible command-line interfaces with optional flags and sensible defaults, first time using to expand CLI programming a bit more.

### Possible Future Enhancements

- Player of the Season prediction using individual player stats
- Highest Goal Scorer
- Head-to-head history weighting for rivalry matches
- Elo rating system for dynamic team strength assessment

### Tech Stack
Python · NumPy · Requests · football-data.org API · Poisson Distribution · Monte Carlo Simulation

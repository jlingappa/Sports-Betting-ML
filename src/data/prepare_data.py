import pandas as pd
from pathlib import Path
from datetime import timedelta

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

print("Loading data...")
# Load Necessary Raw CSV Data
players_df = pd.read_csv(RAW_DIR / "PlayerStatistics.csv", low_memory=False)
teams_df = pd.read_csv(RAW_DIR / "TeamStatistics.csv")

print(f"Loaded {len(players_df)} player rows")

# Create Player_Name Feature
players_df["playerName"] = players_df["firstName"] + " " + players_df["lastName"]

print("Converting dates...")
# CRITICAL: Strip 'Z' and 'T' to normalize all date formats
players_df["gameDate"] = players_df["gameDate"].astype(str).str.replace('Z', '').str.replace('T', ' ')
teams_df["gameDate"] = teams_df["gameDate"].astype(str).str.replace('Z', '').str.replace('T', ' ')

# Now convert to datetime
players_df["gameDate"] = pd.to_datetime(players_df["gameDate"], errors="coerce")
teams_df["gameDate"] = pd.to_datetime(teams_df["gameDate"], errors="coerce")

print("\n=== BEFORE FILTERING ===")
print(f"Total player rows: {len(players_df)}")
print(f"Player date range: {players_df['gameDate'].min()} to {players_df['gameDate'].max()}")
print(f"NaT values: {players_df['gameDate'].isna().sum()}")

# Create datetime for comparison
today = pd.Timestamp.now()
last_ten = today - timedelta(days=365 * 10)

print(f"\nCutoff date (10 years ago): {last_ten}")
print(f"Rows that will pass filter: {(players_df['gameDate'] >= last_ten).sum()}")

# Filter
players_df = players_df[players_df["gameDate"] >= last_ten]
teams_df = teams_df[teams_df["gameDate"] >= last_ten]

print(f"\n=== AFTER FILTERING ===")
print(f"Remaining player rows: {len(players_df)}")
print(f"Player date range: {players_df['gameDate'].min()} to {players_df['gameDate'].max()}")

# Keep Necessary Statistics
player_logs = players_df[[
    "playerName", "gameDate", "playerteamName", "opponentteamName", "seriesGameNumber",
    "win", "home", "numMinutes", "points", "assists", "blocks", "steals", "fieldGoalsAttempted",
    "fieldGoalsMade", "fieldGoalsPercentage", "threePointersAttempted", "threePointersMade", 
    "threePointersPercentage", "freeThrowsAttempted", "freeThrowsMade", "freeThrowsPercentage",
    "foulsPersonal", "turnovers"
]]

print("\nCalculating defensive team stats...")
defensiveTeam_stats = (
    teams_df.groupby("teamName").agg({
        "opponentScore": "mean",
        "reboundsDefensive": "mean",
        "steals": "mean",
        "blocks": "mean",
        "turnovers": "mean"
    }).rename(columns={
        "opponentScore": "opp_avg_score",
        "reboundsDefensive": "opp_avg_def_rebounds",
        "steals": "opp_avg_steals",
        "blocks": "opp_avg_blocks",
        "turnovers": "opp_avg_turnovers"
    })
) 

print("Merging with opponent stats...")
player_logs = player_logs.merge(
    defensiveTeam_stats,
    left_on="opponentteamName",
    right_index=True,
    how="left"
)

out_path = PROCESSED_DIR / "player_game_logs.csv"
player_logs.to_csv(out_path, index=False)

print(f"\n✓ Processed player logs saved to {out_path}")
print(f"✓ Final output rows: {len(player_logs):,}")

print(players_df.head())
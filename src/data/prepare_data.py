import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Load Necessary Raw CSV Data
players_df = pd.read_csv(RAW_DIR / "PlayerStatistics.csv", low_memory=False)
teams_df = pd.read_csv(RAW_DIR / "TeamStatistics.csv")

# Create Player_Name Feature
players_df["playerName"] = players_df["firstName"] + " " + players_df["lastName"]

# Convert GAME_DATE to datetime with UTC normalization
players_df["gameDate"] = pd.to_datetime(players_df["gameDate"], errors="coerce", utc=True)
teams_df["gameDate"] = pd.to_datetime(teams_df["gameDate"], errors="coerce", utc=True)

# Create timezone-aware datetime for comparison
today = pd.Timestamp.now(tz='UTC')
last_ten = today - timedelta(days=365 * 10)

players_df = players_df[players_df["gameDate"] >= last_ten]
teams_df = teams_df[teams_df["gameDate"] >= last_ten]

# Keep Necessary Statistics
player_logs = players_df[[
    "playerName", "gameDate", "playerteamName", "opponentteamName", "seriesGameNumber",
    "win", "home", "numMinutes", "points", "assists", "blocks", "steals", "fieldGoalsAttempted",
    "fieldGoalsMade", "fieldGoalsPercentage", "threePointersAttempted", "threePointersMade", 
    "threePointersPercentage", "freeThrowsAttempted", "freeThrowsMade", "freeThrowsPercentage",
    "foulsPersonal", "turnovers"
]]

defensiveTeam_stats = (
    teams_df.groupby("teamName").agg({
        "opponentScore": "mean",
        "reboundsDefensive": "mean",
        "steals": "mean",
        "blocks": "mean",
        "turnovers": "mean"
    })
) 

player_logs = player_logs.merge(
    defensiveTeam_stats,
    left_on="opponentteamName",
    right_index=True,
    how="left"
)

out_path = PROCESSED_DIR / "player_game_logs.csv"
player_logs.to_csv(out_path, index=False)

print(f"Processed player logs with opponent features saved to {out_path}")
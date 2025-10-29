from kaggle.api.kaggle_api_extended import KaggleApi
import os

DATASET = "eoinamoore/historical-nba-data-and-player-box-scores"
RAW_DIR = "data/raw"

os.makedirs(RAW_DIR, exist_ok=True)

api = KaggleApi()
api.authenticate()  # reads ~/.kaggle/kaggle.json or env vars
api.dataset_download_files(DATASET, path=RAW_DIR, unzip=True, force=True)

print("✅ Downloaded latest NBA dataset to data/raw/")

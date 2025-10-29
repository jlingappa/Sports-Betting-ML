# 🏀 Sports Betting ML (NBA)

## Overview
Predicts probabilities of NBA bets hitting based on historical box scores and game data.

## Features
- Daily data refresh via KaggleHub
- Automated preprocessing and feature extraction
- ML models (Logistic Regression, XGBoost)
- Evaluation metrics and dashboards

## Setup
```bash
conda env create -f environment.yml
conda activate sports-betting-ml
python src/data/refresh_data.py
```
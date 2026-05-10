"""
Mitma HRCommander · Onboarding App
Dataset 5: Weekly Sentiment Data
Output: data/sentiment_data.csv

Requires:
  data/new_hires.csv   (run 01_generate_new_hires.py first)

Weekly sentiment scores derived from check-in language.
In the live app, VADER analyses the actual check-in comments.
This script generates synthetic weekly scores that mirror
what VADER would produce, for use in the HR sentiment trend chart.
Scale: 1.0 (very negative) to 5.0 (very positive)
"""

import pandas as pd
import random
import os

random.seed(42)

OUTPUT_DIR = "data/data_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# BASE SENTIMENT BY DEPARTMENT
# Slightly lower than check-in scores —
# weekly sentiment captures day-to-day mood,
# check-ins capture considered reflection
# ─────────────────────────────────────────────
sentiment_base = {
    "Marketing":  3.8,
    "Finance":    4.0,
    "IT":         3.4,
    "Operations": 3.1,
    "Commercial": 2.7,
}

# ─────────────────────────────────────────────
# BUILD DATASET
# One row per new hire per week employed (up to 12 weeks)
# ─────────────────────────────────────────────
df_hires = pd.read_csv(f"{OUTPUT_DIR}/new_hires.csv")
records  = []

for _, hire in df_hires.iterrows():
    days         = hire["days_employed"]
    base         = sentiment_base[hire["department"]]
    weeks_active = min(12, days // 7)

    for week in range(1, weeks_active + 1):
        # Gradual improvement as new hire settles in
        progression = (week / 12) * 0.8
        score = round(
            min(5.0, max(1.0, base + progression + random.uniform(-0.4, 0.4))),
            2
        )
        records.append({
            "hire_id":         hire["hire_id"],
            "hire_name":       hire["full_name"],
            "department":      hire["department"],
            "manager_name":    hire["manager_name"],
            "week":            week,
            "sentiment_score": score,
        })

df = pd.DataFrame(records)
df.to_csv(f"{OUTPUT_DIR}/sentiment_data.csv", index=False)
print(f"✓ sentiment_data.csv — {len(df)} records saved to {OUTPUT_DIR}/")
print("\nAvg sentiment score by department:")
print(df.groupby("department")["sentiment_score"].mean().round(2).rename("avg_score").to_string())
print("\nAvg sentiment score by week (all depts):")
print(df.groupby("week")["sentiment_score"].mean().round(2).rename("avg_score").to_string())

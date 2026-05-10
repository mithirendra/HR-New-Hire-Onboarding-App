"""
Mitma HRCommander · Onboarding App
Dataset 4: Check-In Responses
Output: data/checkin_responses.csv

Requires:
  data/new_hires.csv   (run 01_generate_new_hires.py first)

Check-ins occur at Day 30, 60, and 90.
Each response includes a satisfaction score (1-5) and open text comment.
Scores are used as input to VADER sentiment analysis in the app.
"""

import pandas as pd
import random
import os

random.seed(42)

OUTPUT_DIR = "data/data_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# COMMENT BANK
# Grouped by sentiment level
# ─────────────────────────────────────────────
positive_comments = [
    "Really enjoying the team and the culture so far. Everyone has been so welcoming.",
    "Feeling confident in my role. The buddy system has been incredibly helpful.",
    "Great support from my manager. I feel like I know what is expected of me.",
    "The onboarding process is well structured. I always know what to do next.",
    "Loving the work. The team is collaborative and I feel valued already.",
    "I feel like I am making a real contribution. Very happy with how things are going.",
    "Excellent experience. I feel settled and excited about the months ahead.",
    "My manager has been fantastic. Clear expectations and great communication.",
]

neutral_comments = [
    "Getting there. Some tasks were unclear but my buddy helped me through.",
    "Settling in. It has been a busy start but I am finding my feet.",
    "Good so far. Would appreciate a bit more clarity on some processes.",
    "Making progress. A few IT access issues slowed me down early on.",
    "Finding my rhythm. Would love more feedback from my manager.",
    "Okay so far. The team is friendly but I still feel like an outsider.",
    "Doing well enough. Some of the onboarding materials were hard to find.",
]

negative_comments = [
    "Finding it a bit challenging. Not entirely sure what is expected of me.",
    "Struggling with some of the processes. Would welcome more guidance.",
    "It has been tough. I feel a bit lost without clear direction from my manager.",
    "Not quite settled yet. The team has been busy and I have felt a bit isolated.",
    "Overwhelmed with the amount to learn. Some clearer structure would help.",
    "My manager has not had much time for me. I feel like I am figuring it out alone.",
]

# ─────────────────────────────────────────────
# BASE SATISFACTION SCORES BY DEPARTMENT
# Reflects realistic variance across teams
# ─────────────────────────────────────────────
base_scores = {
    "Marketing":  4.0,
    "Finance":    4.2,
    "IT":         3.5,
    "Operations": 3.2,
    "Commercial": 2.8,
}

# ─────────────────────────────────────────────
# BUILD DATASET
# ─────────────────────────────────────────────
df_hires = pd.read_csv(f"{OUTPUT_DIR}/new_hires.csv")
records  = []

for _, hire in df_hires.iterrows():
    days = hire["days_employed"]
    base = base_scores[hire["department"]]

    for checkin_day in [30, 60, 90]:
        if days < checkin_day:
            continue  # new hire hasn't reached this check-in yet

        # Scores improve over time as people settle in
        time_boost = (checkin_day / 90) * 0.5
        score      = round(min(5.0, base + time_boost + random.uniform(-0.6, 0.6)), 1)

        # Select comment based on score band
        if score >= 3.8:
            comment = random.choice(positive_comments)
        elif score >= 2.8:
            comment = random.choice(neutral_comments)
        else:
            comment = random.choice(negative_comments)

        records.append({
            "hire_id":     hire["hire_id"],
            "hire_name":   hire["full_name"],
            "department":  hire["department"],
            "manager_name": hire["manager_name"],
            "checkin_day": checkin_day,
            "score":       score,
            "comment":     comment,
        })

df = pd.DataFrame(records)
df.to_csv(f"{OUTPUT_DIR}/checkin_responses.csv", index=False)
print(f"✓ checkin_responses.csv — {len(df)} records saved to {OUTPUT_DIR}/")
print("\nAvg score by department and check-in day:")
print(df.groupby(["department", "checkin_day"])["score"].mean().round(2).to_string())

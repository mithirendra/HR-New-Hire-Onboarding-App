"""
Mitma HRCommander · Onboarding App
Dataset 3: Task Completion
Output: data/task_completion.csv

Requires:
  data/new_hires.csv          (run 01_generate_new_hires.py first)
  data/onboarding_tasks.csv   (run 02_generate_onboarding_tasks.py first)
"""

import pandas as pd
from datetime import datetime, timedelta
import random
import os

random.seed(42)

OUTPUT_DIR = "data/data_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TODAY = datetime.today()

# ─────────────────────────────────────────────
# LOAD DEPENDENCIES
# ─────────────────────────────────────────────
df_hires = pd.read_csv(f"{OUTPUT_DIR}/new_hires.csv")
df_tasks  = pd.read_csv(f"{OUTPUT_DIR}/onboarding_tasks.csv")

# ─────────────────────────────────────────────
# COMPLETION PROBABILITY BY DEPARTMENT
# Reflects realistic variance in onboarding quality
# ─────────────────────────────────────────────
dept_prob = {
    "Marketing":  0.82,
    "Finance":    0.88,
    "IT":         0.68,
    "Operations": 0.60,
    "Commercial": 0.45,
}

# ─────────────────────────────────────────────
# BUILD DATASET
# For each hire × task combination, determine status
# ─────────────────────────────────────────────
records = []

for _, hire in df_hires.iterrows():
    days  = hire["days_employed"]
    start = datetime.strptime(hire["start_date"], "%Y-%m-%d")
    prob  = dept_prob[hire["department"]]

    for _, task in df_tasks.iterrows():
        due_day  = task["due_day"]
        due_date = start + timedelta(days=due_day)

        # Task not yet in scope
        if due_day > days + 5:
            status = "upcoming"
            completion_date = None

        else:
            # Manager tasks slightly less likely to be completed
            p = prob * (0.85 if task["assigned_to"] == "manager" else 1.0)
            completed = random.random() < p

            if completed:
                # Completed within a small window around due date
                offset    = random.randint(-2, 4)
                comp_date = min(due_date + timedelta(days=offset), TODAY)
                status    = "complete"
                completion_date = comp_date.strftime("%Y-%m-%d")
            else:
                status          = "overdue" if due_date < TODAY else "pending"
                completion_date = None

        records.append({
            "hire_id":         hire["hire_id"],
            "hire_name":       hire["full_name"],
            "department":      hire["department"],
            "manager_name":    hire["manager_name"],
            "task_id":         task["task_id"],
            "category":        task["category"],
            "description":     task["description"],
            "due_day":         due_day,
            "due_date":        (start + timedelta(days=due_day)).strftime("%Y-%m-%d"),
            "assigned_to":     task["assigned_to"],
            "status":          status,
            "completion_date": completion_date,
        })

df = pd.DataFrame(records)
df.to_csv(f"{OUTPUT_DIR}/task_completion.csv", index=False)
print(f"✓ task_completion.csv — {len(df)} records saved to {OUTPUT_DIR}/")
print("\nStatus breakdown:")
print(df.groupby("status").size().rename("count").to_string())
print("\nCompletion rate by department:")
dept_summary = df[df["status"].isin(["complete","overdue","pending"])].copy()
dept_summary["done"] = dept_summary["status"] == "complete"
print(dept_summary.groupby("department")["done"].mean().mul(100).round(1).rename("completion_%").to_string())

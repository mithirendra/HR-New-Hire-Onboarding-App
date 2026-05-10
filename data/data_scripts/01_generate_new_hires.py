"""
Mitma HRCommander · Onboarding App
Dataset 1: New Hire Profiles
Output: data/new_hires.csv
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
# REFERENCE DATA
# ─────────────────────────────────────────────
departments = ["Marketing", "Finance", "IT", "Operations", "Commercial"]

managers = [
    {"manager_id": "M01", "name": "James Okafor",  "department": "Marketing"},
    {"manager_id": "M02", "name": "Clare Santos",  "department": "Finance"},
    {"manager_id": "M03", "name": "Dev Patel",     "department": "IT"},
    {"manager_id": "M04", "name": "Ruth Adeyemi",  "department": "Operations"},
    {"manager_id": "M05", "name": "Mark Lim",      "department": "Commercial"},
]

buddies = [
    {"buddy_id": "B01", "name": "Priya Nair",      "department": "Marketing"},
    {"buddy_id": "B02", "name": "Tom Walsh",        "department": "Marketing"},
    {"buddy_id": "B03", "name": "Amara Diallo",     "department": "Finance"},
    {"buddy_id": "B04", "name": "Sophie Grant",     "department": "Finance"},
    {"buddy_id": "B05", "name": "Kenji Tanaka",     "department": "IT"},
    {"buddy_id": "B06", "name": "Lena Hoffmann",    "department": "IT"},
    {"buddy_id": "B07", "name": "Carlos Rivera",    "department": "Operations"},
    {"buddy_id": "B08", "name": "Fatima Al-Hassan", "department": "Operations"},
    {"buddy_id": "B09", "name": "Grace O'Brien",    "department": "Commercial"},
    {"buddy_id": "B10", "name": "Sam Nguyen",       "department": "Commercial"},
]

roles_by_dept = {
    "Marketing":  ["Marketing Executive", "Content Writer", "Digital Analyst", "Brand Coordinator"],
    "Finance":    ["Finance Analyst", "Accounts Executive", "FP&A Analyst", "Treasury Coordinator"],
    "IT":         ["Software Engineer", "Systems Analyst", "DevOps Engineer", "IT Support Specialist"],
    "Operations": ["Operations Analyst", "Supply Chain Coordinator", "Process Improvement Lead", "Logistics Executive"],
    "Commercial": ["Sales Executive", "Account Manager", "Business Development Analyst", "Commercial Coordinator"],
}

hire_names = [
    ("Sarah", "Lee"), ("Raj", "Kumar"), ("Aisha", "Bello"), ("Liam", "Chen"), ("Nina", "Ferreira"),
    ("Omar", "Hassan"), ("Chloe", "Martin"), ("Daniel", "Park"), ("Yemi", "Adeyinka"), ("Isla", "MacLeod"),
    ("Andre", "Dumont"), ("Zara", "Khan"), ("Ben", "Osei"), ("Maya", "Rossi"), ("Tom", "Fitzgerald"),
    ("Layla", "Nkosi"), ("Hugo", "Brandt"), ("Fatou", "Diallo"), ("James", "Wu"), ("Elena", "Petrova"),
    ("Kofi", "Mensah"), ("Anna", "Johansson"), ("Luis", "Reyes"), ("Hana", "Suzuki"), ("Patrick", "Murphy"),
]

# ─────────────────────────────────────────────
# START DATE SPREAD
# Distributes new hires across all 5 journey phases
# ─────────────────────────────────────────────
def random_start_date(i):
    if i < 3:
        return TODAY + timedelta(days=random.randint(3, 14))    # pre-boarding
    elif i < 8:
        return TODAY - timedelta(days=random.randint(1, 14))    # week 1-2
    elif i < 15:
        return TODAY - timedelta(days=random.randint(15, 45))   # month 1
    elif i < 21:
        return TODAY - timedelta(days=random.randint(46, 75))   # month 2
    else:
        return TODAY - timedelta(days=random.randint(76, 90))   # month 3

# ─────────────────────────────────────────────
# BUILD DATASET
# ─────────────────────────────────────────────
dept_managers = {m["department"]: m for m in managers}
dept_buddies  = {d: [b for b in buddies if b["department"] == d] for d in departments}
dept_cycle    = departments * 5  # 5 hires per department

new_hires = []
for i, (first, last) in enumerate(hire_names):
    dept       = dept_cycle[i]
    mgr        = dept_managers[dept]
    bddy       = random.choice(dept_buddies[dept])
    role       = random.choice(roles_by_dept[dept])
    start_date = random_start_date(i)
    days_since = max(0, (TODAY - start_date).days)

    new_hires.append({
        "hire_id":       f"NH{i+1:03d}",
        "first_name":    first,
        "last_name":     last,
        "full_name":     f"{first} {last}",
        "role":          role,
        "department":    dept,
        "manager_id":    mgr["manager_id"],
        "manager_name":  mgr["name"],
        "buddy_id":      bddy["buddy_id"],
        "buddy_name":    bddy["name"],
        "start_date":    start_date.strftime("%Y-%m-%d"),
        "days_employed": days_since,
        "email":         f"{first.lower()}.{last.lower()}@mitma.com",
    })

df = pd.DataFrame(new_hires)
df.to_csv(f"{OUTPUT_DIR}/new_hires.csv", index=False)
print(f"✓ new_hires.csv — {len(df)} records saved to {OUTPUT_DIR}/")
print(df[["hire_id", "full_name", "role", "department", "start_date", "days_employed"]].to_string(index=False))

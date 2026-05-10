"""
Mitma HRCommander · Onboarding App
Dataset 6: Managers and Buddies Reference Data
Output: data/managers.csv
        data/buddies.csv

These are static reference tables used across all views.
No dependencies — run this first or alongside Dataset 1.
"""

import pandas as pd
import os

OUTPUT_DIR = "data/data_files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────
# MANAGERS — one per department
# ─────────────────────────────────────────────
managers = [
    {"manager_id": "M01", "name": "James Okafor",  "department": "Marketing",  "email": "james.okafor@mitma.com"},
    {"manager_id": "M02", "name": "Clare Santos",  "department": "Finance",    "email": "clare.santos@mitma.com"},
    {"manager_id": "M03", "name": "Dev Patel",     "department": "IT",         "email": "dev.patel@mitma.com"},
    {"manager_id": "M04", "name": "Ruth Adeyemi",  "department": "Operations", "email": "ruth.adeyemi@mitma.com"},
    {"manager_id": "M05", "name": "Mark Lim",      "department": "Commercial", "email": "mark.lim@mitma.com"},
]

# ─────────────────────────────────────────────
# BUDDIES — two per department
# ─────────────────────────────────────────────
buddies = [
    {"buddy_id": "B01", "name": "Priya Nair",       "department": "Marketing",  "email": "priya.nair@mitma.com"},
    {"buddy_id": "B02", "name": "Tom Walsh",         "department": "Marketing",  "email": "tom.walsh@mitma.com"},
    {"buddy_id": "B03", "name": "Amara Diallo",      "department": "Finance",    "email": "amara.diallo@mitma.com"},
    {"buddy_id": "B04", "name": "Sophie Grant",      "department": "Finance",    "email": "sophie.grant@mitma.com"},
    {"buddy_id": "B05", "name": "Kenji Tanaka",      "department": "IT",         "email": "kenji.tanaka@mitma.com"},
    {"buddy_id": "B06", "name": "Lena Hoffmann",     "department": "IT",         "email": "lena.hoffmann@mitma.com"},
    {"buddy_id": "B07", "name": "Carlos Rivera",     "department": "Operations", "email": "carlos.rivera@mitma.com"},
    {"buddy_id": "B08", "name": "Fatima Al-Hassan",  "department": "Operations", "email": "fatima.alhassan@mitma.com"},
    {"buddy_id": "B09", "name": "Grace O'Brien",     "department": "Commercial", "email": "grace.obrien@mitma.com"},
    {"buddy_id": "B10", "name": "Sam Nguyen",        "department": "Commercial", "email": "sam.nguyen@mitma.com"},
]

df_managers = pd.DataFrame(managers)
df_buddies  = pd.DataFrame(buddies)

df_managers.to_csv(f"{OUTPUT_DIR}/managers.csv", index=False)
df_buddies.to_csv(f"{OUTPUT_DIR}/buddies.csv", index=False)

print(f"✓ managers.csv — {len(df_managers)} records saved to {OUTPUT_DIR}/")
print(df_managers.to_string(index=False))
print(f"\n✓ buddies.csv  — {len(df_buddies)} records saved to {OUTPUT_DIR}/")
print(df_buddies.to_string(index=False))

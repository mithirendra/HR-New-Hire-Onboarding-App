"""
Mitma HRCommander · Onboarding App
MASTER DATA GENERATOR — runs all 6 scripts in order

Usage:
    python run_all.py

Output: all CSV files saved to data/data_files
"""

import subprocess
import sys
import os

scripts = [
    ("06_generate_managers_buddies.py", "Managers & Buddies"),
    ("01_generate_new_hires.py",        "New Hire Profiles"),
    ("02_generate_onboarding_tasks.py", "Onboarding Tasks"),
    ("03_generate_task_completion.py",  "Task Completion"),
    ("04_generate_checkin_responses.py","Check-In Responses"),
    ("05_generate_sentiment_data.py",   "Weekly Sentiment"),
]

print("=" * 52)
print("  Mitma Onboarding App · Generating Synthetic Data")
print("=" * 52)

for script, label in scripts:
    print(f"\n── {label} ──")
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    if result.returncode == 0:
        for line in result.stdout.strip().split("\n"):
            if line.startswith("✓"):
                print(f"  {line}")
    else:
        print(f"  ERROR in {script}:")
        print(result.stderr)
        sys.exit(1)

print("\n" + "=" * 52)
print("  All datasets generated successfully")
print(f"  Location: {os.path.abspath('data')}/")
files = [f for f in os.listdir("data") if f.endswith(".csv")]
for f in sorted(files):
    size = os.path.getsize(f"data/{f}")
    print(f"    {f:<35} {size:>8,} bytes")
print("=" * 52)

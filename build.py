"""
Master build script for Car Maintenance Scheduler

This script:
1. Auto-detects all car CSV files in Data/ folder
2. Generates script.js with all car data
3. Updates index.html dropdown with all cars

To add a new car:
1. Add CSV file to Data/ folder: "Car Maintenance for app - [CarName]-General.csv"
2. Run this script: python build.py
"""

import subprocess
import sys

print("=" * 60)
print("Building Car Maintenance Scheduler")
print("=" * 60)

# Step 1: Generate script.js
print("\n[1/2] Generating script.js from CSV files...")
result = subprocess.run([sys.executable, 'generate_script.py'], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("ERROR:", result.stderr)
    sys.exit(1)

# Step 2: Update index.html dropdown
print("\n[2/2] Updating index.html dropdown...")
result = subprocess.run([sys.executable, 'update_dropdown.py'], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("ERROR:", result.stderr)
    sys.exit(1)

print("\n" + "=" * 60)
print("Build complete! ✓")
print("=" * 60)
print("\nTo add a new car:")
print("  1. Add CSV to Data/ folder")
print("  2. Run: python build.py")

import glob
import os
import re

# Auto-detect all CSV files in Data folder
csv_files = glob.glob('Data/*.csv')
cars = []

for csv_file in csv_files:
    filename = os.path.basename(csv_file)
    if 'Car Maintenance for app' in filename:
        # Extract car name: "Car Maintenance for app - IS300-Malaysia-General.csv" -> "IS300"
        car_name = filename.split(' - ')[1].split('-')[0].strip()
        car_key = car_name.lower().replace(' ', '_')
        cars.append({'key': car_key, 'name': car_name})

# Read current HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Generate dropdown options HTML
options_html = '\n'.join([f'          <option value="{car["key"]}">{car["name"]}</option>' for car in cars])

# Replace the select options
pattern = r'(<select id="carSelect">)(.*?)(</select>)'
replacement = r'\1\n' + options_html + r'\n        \3'
new_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# Write updated HTML
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("index.html updated successfully!")
print(f"Cars in dropdown: {', '.join([c['name'] for c in cars])}")

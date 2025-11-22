# Car Maintenance Scheduler

A simple web-based car maintenance scheduler that calculates the next service based on current mileage.

## Features

- **Multi-car support** - Easy to add new cars
- **Three schedule types** - Manufacturer, Your Service, Yours + Recommended
- **Dynamic calculations** - Next service mileage and expected date
- **Action categories** - Replace, Inspect, Test, Tighten, Reset

## Adding a New Car

1. **Prepare your CSV file** with the naming format:
   ```
   Car Maintenance for app - [CarName]-General.csv
   ```

2. **CSV Format Requirements**:
   - Row 1: MANUFACTURER SERVICE KM with mileage intervals
   - Row 2: YOUR SERVICE KM with mileage intervals  
   - Row 3: YOURS + RECOMMENDED SERVICE KM with mileage intervals
   - Row 4: Action, Maintenance (header row)
   - Row 5+: Action type (Replace/Inspect/Test/Tighten/Reset), Item name, followed by Y/blank for each interval

3. **Important**: Data columns must be provided for ALL three schedule types
   - If all schedules use the same data, duplicate the columns
   - Total columns = 2 (labels) + intervals × 3 (for each schedule type)

4. **Save the CSV** to the `Data/` folder

5. **Run the build script**:
   ```bash
   python build.py
   ```

This will automatically:
- Generate `script.js` with the new car's data
- Update the dropdown in `index.html`

## Development

### File Structure
```
├── index.html          # Main UI
├── style.css           # Styling
├── script.js           # Generated JavaScript (don't edit manually)
├── Data/               # Car maintenance CSV files
│   ├── Car Maintenance for app - IS300-Malaysia-General.csv
│   └── Car Maintenance for app - Ativa-General.csv
├── build.py            # Master build script
├── generate_script.py  # CSV to JavaScript generator
└── update_dropdown.py  # HTML dropdown updater
```

### Build Scripts

- `build.py` - Run this to rebuild everything after adding/updating CSVs
- `generate_script.py` - Generates `script.js` from CSV files
- `update_dropdown.py` - Updates car dropdown in `index.html`

### Date Calculation

The scheduler uses a conversion rate of:
- **8000 km = 6 months**

Adjust this in `generate_script.py` if needed (search for `calculateExpectedDate`).

## Deployment

The site is deployed on GitHub Pages at:
https://saifulanu.github.io/carmate/

To deploy updates:
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

## License

Private project

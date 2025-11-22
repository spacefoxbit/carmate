import csv
import json
import os
import glob

def parse_csv_schedule(filepath):
    """Parse a CSV file and extract schedule data with action types"""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Find the row with "MANUFACTURER SERVICE KM"
    schedule_start_row = None
    for i, row in enumerate(rows):
        if len(row) > 1 and 'MANUFACTURER SERVICE KM' in row[1]:
            schedule_start_row = i
            break
    
    if schedule_start_row is None:
        raise ValueError("Could not find MANUFACTURER SERVICE KM row")
    
    # Extract intervals
    manufacturer_intervals = [int(x) for x in rows[schedule_start_row][2:] if x.strip() and x.strip().isdigit()]
    yours_intervals = [int(x) for x in rows[schedule_start_row + 1][2:] if x.strip() and x.strip().isdigit()]
    recommended_intervals = [int(x) for x in rows[schedule_start_row + 2][2:] if x.strip() and x.strip().isdigit()]
    
    # Find the row with "Action" header
    action_row = None
    for i, row in enumerate(rows[schedule_start_row:]):
        if len(row) > 0 and 'Action' in row[0]:
            action_row = schedule_start_row + i
            break
    
    if action_row is None:
        raise ValueError("Could not find Action row")
    
    # Extract maintenance items by action type
    manufacturer_data = {'Replace': {}, 'Inspect': {}, 'Test': {}, 'Tighten': {}, 'Reset': {}}
    yours_data = {'Replace': {}, 'Inspect': {}, 'Test': {}, 'Tighten': {}, 'Reset': {}}
    recommended_data = {'Replace': {}, 'Inspect': {}, 'Test': {}, 'Tighten': {}, 'Reset': {}}
    
    for row in rows[action_row + 1:]:
        if not row or len(row) < 2 or not row[1].strip():
            continue
        
        action = row[0].strip()
        if not action or action not in ['Replace', 'Inspect', 'Test', 'Tighten', 'Reset']:
            continue
            
        item_name = row[1].strip()
        
        # Manufacturer data (starts at column 2)
        manufacturer_data[action][item_name] = row[2:2+len(manufacturer_intervals)]
        
        # Yours data
        yours_start = 2 + len(manufacturer_intervals)
        yours_data[action][item_name] = row[yours_start:yours_start+len(yours_intervals)]
        
        # Recommended data
        rec_start = yours_start + len(yours_intervals)
        recommended_data[action][item_name] = row[rec_start:rec_start+len(recommended_intervals)]
    
    return {
        'manufacturer': {
            'intervals': manufacturer_intervals,
            'data': manufacturer_data
        },
        'yours': {
            'intervals': yours_intervals,
            'data': yours_data
        },
        'recommended': {
            'intervals': recommended_intervals,
            'data': recommended_data
        }
    }

# Auto-detect all CSV files in Data folder
csv_files = glob.glob('Data/*.csv')
schedules_data = {}

for csv_file in csv_files:
    # Extract car key from filename: "Car Maintenance for app - IS300-Malaysia-General.csv" -> "is300"
    filename = os.path.basename(csv_file)
    if 'Car Maintenance for app' in filename:
        # Extract the part between " - " and the next "-" or ".csv"
        car_name = filename.split(' - ')[1].split('-')[0].strip()
        car_key = car_name.lower().replace(' ', '_')
        
        print(f"Processing {car_name}...")
        schedules_data[car_key] = {
            'name': car_name,
            'scheduleTypes': parse_csv_schedule(csv_file)
        }

# Generate JavaScript file
js_content = '''// Car Maintenance Scheduler - Generated from CSV files

const schedules = ''' + json.dumps(schedules_data, indent=2) + ''';

// Calculate expected date based on mileage difference
function calculateExpectedDate(currentMileage, nextMileage) {
  const mileageDiff = nextMileage - currentMileage;
  const monthsToAdd = Math.round((mileageDiff / 8000) * 6);
  
  const today = new Date();
  today.setMonth(today.getMonth() + monthsToAdd);
  
  return today.toLocaleDateString('en-MY', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
}

// Find next maintenance interval and items
function findNextMaintenance(currentMileage, carKey, scheduleType) {
  const car = schedules[carKey];
  if (!car) return null;
  
  const schedule = car.scheduleTypes[scheduleType];
  if (!schedule) return null;
  
  // Find next interval
  const nextInterval = schedule.intervals.find(interval => interval > currentMileage);
  if (!nextInterval) {
    return {
      found: false,
      message: 'No future scheduled maintenance found.'
    };
  }
  
  // Find items by action type
  const intervalIndex = schedule.intervals.indexOf(nextInterval);
  const replaceItems = [];
  const inspectItems = [];
  const testItems = [];
  const tightenItems = [];
  const resetItems = [];
  
  // Get Replace items
  if (schedule.data.Replace) {
    for (const [itemName, values] of Object.entries(schedule.data.Replace)) {
      const value = values[intervalIndex];
      if (value && value.trim().toUpperCase() === 'Y') {
        replaceItems.push(itemName);
      }
    }
  }
  
  // Get Inspect items
  if (schedule.data.Inspect) {
    for (const [itemName, values] of Object.entries(schedule.data.Inspect)) {
      const value = values[intervalIndex];
      if (value && value.trim().toUpperCase() === 'Y') {
        inspectItems.push(itemName);
      }
    }
  }
  
  // Get Test items
  if (schedule.data.Test) {
    for (const [itemName, values] of Object.entries(schedule.data.Test)) {
      const value = values[intervalIndex];
      if (value && value.trim().toUpperCase() === 'Y') {
        testItems.push(itemName);
      }
    }
  }
  
  // Get Tighten items
  if (schedule.data.Tighten) {
    for (const [itemName, values] of Object.entries(schedule.data.Tighten)) {
      const value = values[intervalIndex];
      if (value && value.trim().toUpperCase() === 'Y') {
        tightenItems.push(itemName);
      }
    }
  }
  
  // Get Reset items
  if (schedule.data.Reset) {
    for (const [itemName, values] of Object.entries(schedule.data.Reset)) {
      const value = values[intervalIndex];
      if (value && value.trim().toUpperCase() === 'Y') {
        resetItems.push(itemName);
      }
    }
  }
  
  return {
    found: true,
    nextMileage: nextInterval,
    expectedDate: calculateExpectedDate(currentMileage, nextInterval),
    replaceItems: replaceItems,
    inspectItems: inspectItems,
    testItems: testItems,
    tightenItems: tightenItems,
    resetItems: resetItems
  };
}

// UI event handlers
document.addEventListener('DOMContentLoaded', function() {
  const calcBtn = document.getElementById('calcBtn');
  const mileageInput = document.getElementById('mileage');
  const carSelect = document.getElementById('carSelect');
  const resultDiv = document.getElementById('result');
  
  calcBtn.addEventListener('click', function() {
    const currentMileage = parseInt(mileageInput.value);
    const carKey = carSelect.value;
    
    // Get selected schedule type
    const scheduleTypeRadios = document.getElementsByName('scheduleType');
    let scheduleType = 'manufacturer';
    for (const radio of scheduleTypeRadios) {
      if (radio.checked) {
        scheduleType = radio.value;
        break;
      }
    }
    
    if (!currentMileage || currentMileage <= 0) {
      alert('Please enter a valid mileage.');
      return;
    }
    
    const result = findNextMaintenance(currentMileage, carKey, scheduleType);
    
    if (!result.found) {
      resultDiv.style.display = 'none';
      alert(result.message);
      return;
    }
    
    // Update UI
    document.getElementById('nextMileage').textContent = result.nextMileage.toLocaleString() + ' km';
    document.getElementById('nextDate').textContent = result.expectedDate;
    
    // Clear previous columns
    const colsContainer = document.querySelector('.cols');
    colsContainer.innerHTML = '';
    
    // Add columns for each action type
    const actionTypes = [
      { name: 'Replace', items: result.replaceItems },
      { name: 'Inspect', items: result.inspectItems },
      { name: 'Test', items: result.testItems },
      { name: 'Tighten', items: result.tightenItems },
      { name: 'Reset', items: result.resetItems }
    ];
    
    actionTypes.forEach(actionType => {
      if (actionType.items.length > 0) {
        const col = document.createElement('div');
        col.className = 'col';
        col.innerHTML = '<h3>' + actionType.name + '</h3><ul>' + 
          actionType.items.map(item => `<li>${item}</li>`).join('') + 
          '</ul>';
        colsContainer.appendChild(col);
      }
    });
    
    resultDiv.style.display = 'block';
  });
});

console.log('Maintenance scheduler loaded. Data for', Object.keys(schedules).length, 'cars.');
'''

# Write to script.js
with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("\nscript.js generated successfully!")
print(f"Total cars: {len(schedules_data)}")
for key, data in schedules_data.items():
    print(f"  - {data['name']} (key: {key}): {len(data['scheduleTypes']['manufacturer']['intervals'])} manufacturer intervals")

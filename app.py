import os
import json
import csv
from flask import Flask, request, jsonify, render_template

# --- Configuration ---
app = Flask(__name__, static_folder='.', static_url_path='')
DATA_FOLDER = 'data'
USERS_FILE = 'users.txt'
# CSV Header: date, sector, total_kg, scope1_kg, scope2_kg, scope3_kg, full_data_json
CSV_HEADER = ['date', 'sector', 'total_kg', 'scope1_kg', 'scope2_kg', 'scope3_kg', 'full_data_json']

# --- Helper Functions ---

def read_users():
    """Reads the users.txt file and returns a dictionary."""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def write_users(users_db):
    """Writes the dictionary to the users.txt file."""
    with open(USERS_FILE, 'w') as f:
        json.dump(users_db, f, indent=4)

def get_user_csv_path(username):
    """Generates the file path for a user's CSV."""
    # Sanitize username to be a safe filename
    safe_filename = "".join(c for c in username if c.isalnum() or c in (' ', '_')).rstrip()
    return os.path.join(DATA_FOLDER, f"{safe_filename}.csv")

def read_user_data(username):
    """Reads a user's CSV and returns a list of data entries."""
    csv_path = get_user_csv_path(username)
    if not os.path.exists(csv_path):
        return []
    
    entries = []
    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Re-hydrate the full entry from the JSON column
                full_data = json.loads(row['full_data_json'])
                entries.append(full_data)
            except json.JSONDecodeError:
                print(f"Warning: Skipping malformed row in {csv_path}")
                continue
    return entries

def append_user_data(username, new_entry):
    """Appends a new entry to a user's CSV file."""
    csv_path = get_user_csv_path(username)
    file_exists = os.path.exists(csv_path)
    
    try:
        with open(csv_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
            
            if not file_exists:
                writer.writeheader()
            
            # Extract main data for CSV columns
            totals = new_entry.get('calculations', {}).get('totals', {})
            row = {
                'date': new_entry.get('date'),
                'sector': new_entry.get('sector'),
                'total_kg': totals.get('total', 0),
                'scope1_kg': totals.get('scope1', 0),
                'scope2_kg': totals.get('scope2', 0),
                'scope3_kg': totals.get('scope3', 0),
                'full_data_json': json.dumps(new_entry) # Store the complete object
            }
            writer.writerow(row)
        return True
    except Exception as e:
        print(f"Error appending data to {csv_path}: {e}")
        return False

def calculate_recommendations(current_entry, previous_entry):
    """Analyzes two entries and generates recommendation data."""
    if not current_entry or not previous_entry:
        return { "totalDelta": 0, "topIncreases": [], "topDecreases": [] }
    
    current_calcs = current_entry.get('calculations', {})
    previous_calcs = previous_entry.get('calculations', {})
    
    total_delta = current_calcs.get('totals', {}).get('total', 0) - previous_calcs.get('totals', {}).get('total', 0)

    # Aggregate all emission sources
    all_current_sources = { **current_calcs.get('scope1', {}), **current_calcs.get('scope2', {}), **current_calcs.get('scope3', {}) }
    all_previous_sources = { **previous_calcs.get('scope1', {}), **previous_calcs.get('scope2', {}), **previous_calcs.get('scope3', {}) }
    
    all_keys = set(all_current_sources.keys()) | set(all_previous_sources.keys())
    
    deltas = []
    for key in all_keys:
        current_val = all_current_sources.get(key, 0)
        previous_val = all_previous_sources.get(key, 0)
        delta = current_val - previous_val
        
        if abs(delta) > 0.1: # Only track meaningful changes
            deltas.append({
                'key': key,
                'delta': delta,
                'current': current_val,
                'previous': previous_val
            })
            
    deltas.sort(key=lambda x: x['delta'], reverse=True) # Sort by largest increase
    
    top_increases = deltas[:3]
    top_decreases = sorted([d for d in deltas if d['delta'] < 0], key=lambda x: x['delta'])[:3]
    
    return {
        "totalDelta": total_delta,
        "topIncreases": top_increases,
        "topDecreases": top_decreases
    }

# --- API Routes ---

@app.route('/')
def serve_index():
    """Serves the main HTML file."""
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    """Handles user login."""
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"status": "error", "message": "Username required"}), 400

    users_db = read_users()
    
    if username in users_db:
        return jsonify({
            "status": "success", 
            "user": {
                "username": username, 
                "sector": users_db[username]
            }
        })
    else:
        return jsonify({"status": "error", "message": "User not found"}), 404

@app.route('/api/register', methods=['POST'])
def api_register():
    """Handles new user registration."""
    data = request.json
    username = data.get('username')
    sector = data.get('sector')
    
    if not username or not sector:
        return jsonify({"status": "error", "message": "Username and sector required"}), 400

    users_db = read_users()
    
    if username in users_db:
        return jsonify({"status": "error", "message": "User already exists"}), 409

    users_db[username] = sector
    write_users(users_db)
    
    # Create the data folder if it doesn't exist
    os.makedirs(DATA_FOLDER, exist_ok=True)
    
    # Create the user's empty CSV file with a header
    csv_path = get_user_csv_path(username)
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()

    return jsonify({
        "status": "success",
        "user": {
            "username": username,
            "sector": sector
        }
    }), 201

@app.route('/api/dashboard', methods=['POST'])
def api_get_dashboard_data():
    """Fetches all data needed to render the dashboard."""
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({"status": "error", "message": "Username required"}), 400
    
    user_data = read_user_data(username)
    
    if not user_data:
        return jsonify({
            "status": "success",
            "dashboard_data": {
                "latest_entry": None,
                "history": [],
                "recommendations": None,
                "previous_entry": None # For consistency
            }
        })

    latest_entry = user_data[-1]
    previous_entry = user_data[-2] if len(user_data) > 1 else None
    history = user_data[-3:] # Get last 3 entries
    
    recommendations = calculate_recommendations(latest_entry, previous_entry)
    
    return jsonify({
        "status": "success",
        "dashboard_data": {
            "latest_entry": latest_entry,
            "history": history,
            "recommendations": recommendations,
            "previous_entry": previous_entry # Pass previous for history color coding
        }
    })

@app.route('/api/data', methods=['POST'])
def api_add_data():
    """Adds a new weekly data entry for a user."""
    data = request.json
    username = data.get('username')
    new_entry = data.get('entry')
    
    if not username or not new_entry:
        return jsonify({"status": "error", "message": "Invalid data"}), 400
        
    if append_user_data(username, new_entry):
        return jsonify({"status": "success", "message": "Data saved"})
    else:
        return jsonify({"status": "error", "message": "Failed to save data"}), 500

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)

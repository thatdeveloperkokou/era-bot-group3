from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import csv
import os
import hashlib
import jwt
from functools import wraps
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# CORS configuration - allow specific frontend URL in production, all origins in development
frontend_url = os.environ.get('FRONTEND_URL', '*')
if frontend_url == '*':
    # Development: allow all origins
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
else:
    # Production: allow specific frontend URL
    CORS(app, resources={r"/api/*": {"origins": frontend_url}}, supports_credentials=True)

# File paths - use absolute paths based on this file's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, 'users.json')
DATA_DIR = os.path.join(BASE_DIR, 'data')
POWER_LOGS_FILE = os.path.join(DATA_DIR, 'power_logs.csv')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize CSV file if it doesn't exist
if not os.path.exists(POWER_LOGS_FILE):
    with open(POWER_LOGS_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['user_id', 'event_type', 'timestamp', 'date'])

# Load users from JSON file
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(user_id):
    token = jwt.encode({'user_id': user_id}, app.config['SECRET_KEY'], algorithm='HS256')
    # PyJWT 2.0+ returns string directly, but handle both cases
    if isinstance(token, bytes):
        return token.decode('utf-8')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Handle OPTIONS requests for CORS preflight
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'error': f'Token is invalid: {str(e)}'}), 401
        except Exception as e:
            return jsonify({'error': f'Authentication error: {str(e)}'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'Electricity Supply Logger API is running',
        'endpoints': {
            'register': '/api/register',
            'login': '/api/login',
            'log-power': '/api/log-power',
            'stats': '/api/stats',
            'recent-events': '/api/recent-events'
        }
    }), 200

@app.route('/api', methods=['GET'])
def api_info():
    return jsonify({
        'status': 'ok',
        'message': 'Electricity Supply Logger API',
        'version': '1.0.0'
    }), 200

@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json() or request.json
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    users = load_users()
    if username in users:
        return jsonify({'error': 'Username already exists'}), 400
    
    users[username] = {
        'password': hash_password(password),
        'created_at': datetime.now().isoformat()
    }
    save_users(users)
    
    token = generate_token(username)
    return jsonify({
        'message': 'User registered successfully',
        'token': token,
        'username': username
    }), 201

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.get_json() or request.json
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    users = load_users()
    if username not in users:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if users[username]['password'] != hash_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = generate_token(username)
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'username': username
    }), 200

@app.route('/api/log-power', methods=['POST', 'OPTIONS'])
@token_required
def log_power(current_user):
    data = request.get_json() or request.json
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400
    
    event_type = data.get('event_type')  # 'on' or 'off'
    
    if event_type not in ['on', 'off']:
        return jsonify({'error': 'event_type must be "on" or "off"'}), 400
    
    timestamp = datetime.now()
    date = timestamp.date().isoformat()
    
    # Write to CSV
    with open(POWER_LOGS_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([current_user, event_type, timestamp.isoformat(), date])
    
    return jsonify({
        'message': f'Power {event_type} logged successfully',
        'timestamp': timestamp.isoformat(),
        'date': date
    }), 200

@app.route('/api/stats', methods=['GET', 'OPTIONS'])
@token_required
def get_stats(current_user):
    period = request.args.get('period', 'week')  # 'day', 'week', 'month'
    
    # Read power logs
    logs = []
    with open(POWER_LOGS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['user_id'] == current_user:
                logs.append(row)
    
    # Calculate date range
    now = datetime.now()
    if period == 'day':
        start_date = now.date()
    elif period == 'week':
        start_date = (now - timedelta(days=7)).date()
    elif period == 'month':
        start_date = (now - timedelta(days=30)).date()
    else:
        start_date = (now - timedelta(days=7)).date()
    
    # Filter logs by date range
    filtered_logs = []
    for log in logs:
        log_date = datetime.fromisoformat(log['timestamp']).date()
        if log_date >= start_date:
            filtered_logs.append(log)
    
    # Calculate hours per day
    daily_stats = {}
    sorted_logs = sorted(filtered_logs, key=lambda x: x['timestamp'])
    
    current_on_time = None
    for log in sorted_logs:
        log_time = datetime.fromisoformat(log['timestamp'])
        log_date = log_time.date().isoformat()
        
        if log_date not in daily_stats:
            daily_stats[log_date] = {'hours': 0, 'events': []}
        
        daily_stats[log_date]['events'].append({
            'type': log['event_type'],
            'timestamp': log['timestamp']
        })
        
        if log['event_type'] == 'on':
            current_on_time = log_time
        elif log['event_type'] == 'off' and current_on_time:
            duration = (log_time - current_on_time).total_seconds() / 3600
            daily_stats[log_date]['hours'] += duration
            current_on_time = None
    
    # If power is still on, calculate until now
    if current_on_time:
        last_date = sorted_logs[-1]['date'] if sorted_logs else now.date().isoformat()
        if last_date in daily_stats:
            duration = (now - current_on_time).total_seconds() / 3600
            daily_stats[last_date]['hours'] += duration
    
    # Calculate total hours
    total_hours = sum(day['hours'] for day in daily_stats.values())
    
    # Format for chart
    chart_data = []
    for date, stats in sorted(daily_stats.items()):
        chart_data.append({
            'date': date,
            'hours': round(stats['hours'], 2)
        })
    
    return jsonify({
        'period': period,
        'total_hours': round(total_hours, 2),
        'daily_stats': chart_data,
        'events': filtered_logs[-10:]  # Last 10 events
    }), 200

@app.route('/api/recent-events', methods=['GET', 'OPTIONS'])
@token_required
def get_recent_events(current_user):
    limit = int(request.args.get('limit', 10))
    
    logs = []
    with open(POWER_LOGS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['user_id'] == current_user:
                logs.append(row)
    
    # Sort by timestamp and get most recent
    sorted_logs = sorted(logs, key=lambda x: x['timestamp'], reverse=True)
    recent = sorted_logs[:limit]
    
    return jsonify({'events': recent}), 200

@app.route('/api/report', methods=['GET', 'OPTIONS'])
@token_required
def get_report(current_user):
    # Get stats for all periods
    logs = []
    with open(POWER_LOGS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['user_id'] == current_user:
                logs.append(row)
    
    now = datetime.now()
    
    # Calculate stats for different periods
    def calculate_period_stats(days):
        start_date = (now - timedelta(days=days)).date()
        filtered = [log for log in logs if datetime.fromisoformat(log['timestamp']).date() >= start_date]
        
        sorted_logs = sorted(filtered, key=lambda x: x['timestamp'])
        current_on_time = None
        total_hours = 0
        
        for log in sorted_logs:
            log_time = datetime.fromisoformat(log['timestamp'])
            if log['event_type'] == 'on':
                current_on_time = log_time
            elif log['event_type'] == 'off' and current_on_time:
                duration = (log_time - current_on_time).total_seconds() / 3600
                total_hours += duration
                current_on_time = None
        
        # If power is still on, calculate until now
        if current_on_time and sorted_logs:
            duration = (now - current_on_time).total_seconds() / 3600
            total_hours += duration
        
        return round(total_hours, 2), len(filtered)
    
    today_hours, today_events = calculate_period_stats(1)
    week_hours, week_events = calculate_period_stats(7)
    month_hours, month_events = calculate_period_stats(30)
    
    # Get last event
    if logs:
        last_event = sorted(logs, key=lambda x: x['timestamp'], reverse=True)[0]
        last_event_time = datetime.fromisoformat(last_event['timestamp'])
        last_event_type = last_event['event_type']
        time_ago = now - last_event_time
        hours_ago = round(time_ago.total_seconds() / 3600, 1)
    else:
        last_event_type = None
        hours_ago = None
    
    # Calculate average hours per day for week
    avg_daily_hours = round(week_hours / 7, 2) if week_hours > 0 else 0
    
    report = {
        'summary': {
            'today_hours': today_hours,
            'week_hours': week_hours,
            'month_hours': month_hours,
            'avg_daily_hours': avg_daily_hours,
            'last_event': {
                'type': last_event_type,
                'hours_ago': hours_ago
            }
        },
        'totals': {
            'today_events': today_events,
            'week_events': week_events,
            'month_events': month_events
        }
    }
    
    return jsonify(report), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    print("Starting Electricity Supply Logger API...")
    print(f"API will be available at http://localhost:{port}")
    print("Available endpoints:")
    print("  - GET  /               - Health check")
    print("  - GET  /api            - API info")
    print("  - POST /api/register   - Register user")
    print("  - POST /api/login      - Login user")
    print("  - POST /api/log-power  - Log power event")
    print("  - GET  /api/stats      - Get statistics")
    print("  - GET  /api/recent-events - Get recent events")
    print("  - GET  /api/report     - Get brief report summary")
    app.run(debug=debug, port=port, host='0.0.0.0')


from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import hashlib
import jwt
from functools import wraps
import uuid
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_, and_, func
from database import db, User, PowerLog, DeviceId, init_db

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Initialize database
init_db(app)

# CORS configuration - allow specific frontend URL in production, all origins in development
frontend_url = os.environ.get('FRONTEND_URL', '*')
if frontend_url == '*':
    # Development: allow all origins
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    print("🌐 CORS: Allowing all origins (development mode)")
else:
    # Production: allow specific frontend URL(s)
    # Support multiple URLs separated by comma
    origins = [url.strip() for url in frontend_url.split(',')]
    CORS(app, resources={r"/api/*": {"origins": origins}}, supports_credentials=True, allow_headers=['Content-Type', 'Authorization'])
    print(f"🌐 CORS: Allowing origins: {origins}")

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
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'ok',
        'message': 'Electricity Supply Logger API is running',
        'database': db_status,
        'endpoints': {
            'register': '/api/register',
            'login': '/api/login',
            'log-power': '/api/log-power',
            'stats': '/api/stats',
            'recent-events': '/api/recent-events',
            'report': '/api/report'
        }
    }), 200

@app.route('/api', methods=['GET'])
def api_info():
    return jsonify({
        'status': 'ok',
        'message': 'Electricity Supply Logger API',
        'version': '1.0.0',
        'database': 'PostgreSQL'
    }), 200

@app.route('/api/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json() or request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        location = data.get('location', '')
        
        if not username or not password or not email:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400
        
        # Check if email is already registered
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return jsonify({'error': 'Email already registered'}), 400
        
        username = username.strip()
        email = email.strip()
        hashed_password = hash_password(password)
        location = location.strip() if isinstance(location, str) else ''

        user = User(
            username=username,
            password=hashed_password,
            email=email,
            location=location,
            email_verified=True,
            created_at=datetime.utcnow()
        )
        db.session.add(user)

        device_id = str(uuid.uuid4())
        device_record = DeviceId(
            user_id=username,
            device_id=device_id
        )
        db.session.add(device_record)

        db.session.commit()

        token = generate_token(username)
        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'username': username,
            'deviceId': device_id
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error: User or email already exists'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        print(f"Error in register: {str(e)}")
        return jsonify({'error': 'An error occurred during registration'}), 500

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json() or request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        username_or_email = (data.get('username') or data.get('email') or '').strip()
        password = data.get('password')
        device_id = data.get('deviceId')
        
        if not username_or_email or not password:
            return jsonify({'error': 'Email/Username and password are required'}), 400
        
        # Try to find user by username or email
        user = User.query.filter(
            or_(User.username == username_or_email, User.email == username_or_email)
        ).first()
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if user.password != hash_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        response_device_id = device_id if device_id else str(uuid.uuid4())
        device_exists = False

        if device_id:
            existing_device = DeviceId.query.filter_by(
                user_id=user.username,
                device_id=device_id
            ).first()
            device_exists = existing_device is not None

        if not device_exists:
            db.session.add(DeviceId(
                user_id=user.username,
                device_id=response_device_id
            ))
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                # Device already stored by another concurrent request
                existing_device = DeviceId.query.filter_by(
                    user_id=user.username,
                    device_id=response_device_id
                ).first()
                if not existing_device:
                    raise
        token = generate_token(user.username)
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'username': user.username,
            'deviceId': response_device_id
        }), 200
                
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        print(f"Error in login: {str(e)}")
        return jsonify({'error': 'An error occurred during login'}), 500

@app.route('/api/log-power', methods=['POST', 'OPTIONS'])
@token_required
def log_power(current_user):
    try:
        data = request.get_json() or request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        event_type = data.get('event_type')  # 'on' or 'off'
        location = data.get('location', '')
        
        if event_type not in ['on', 'off']:
            return jsonify({'error': 'event_type must be "on" or "off"'}), 400
        
        # Get user
        user = User.query.filter_by(username=current_user).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get user location if not provided
        if not location:
            location = user.location or ''
        
        timestamp = datetime.utcnow()
        date = timestamp.date()
        
        # Save to database
        power_log = PowerLog(
            user_id=current_user,
            event_type=event_type,
            timestamp=timestamp,
            date=date,
            location=location
        )
        db.session.add(power_log)
        db.session.commit()
        
        return jsonify({
            'message': f'Power {event_type} logged successfully',
            'timestamp': timestamp.isoformat(),
            'date': date.isoformat(),
            'location': location
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        print(f"Error in log_power: {str(e)}")
        return jsonify({'error': 'An error occurred while logging power event'}), 500

@app.route('/api/stats', methods=['GET', 'OPTIONS'])
@token_required
def get_stats(current_user):
    try:
        period = request.args.get('period', 'week')  # 'day', 'week', 'month'
        
        # Calculate date range
        now = datetime.utcnow()
        if period == 'day':
            start_date = now.date()
        elif period == 'week':
            start_date = (now - timedelta(days=7)).date()
        elif period == 'month':
            start_date = (now - timedelta(days=30)).date()
        else:
            start_date = (now - timedelta(days=7)).date()
        
        # Get power logs for user
        logs = PowerLog.query.filter(
            and_(
                PowerLog.user_id == current_user,
                PowerLog.date >= start_date
            )
        ).order_by(PowerLog.timestamp).all()
        
        # Convert to dictionaries
        log_dicts = [log.to_dict() for log in logs]
        
        # Calculate hours per day
        daily_stats = {}
        current_on_time = None
        
        for log in logs:
            log_time = log.timestamp
            log_date = log_time.date().isoformat()
            
            if log_date not in daily_stats:
                daily_stats[log_date] = {'hours': 0, 'events': []}
            
            daily_stats[log_date]['events'].append({
                'type': log.event_type,
                'timestamp': log.timestamp.isoformat()
            })
            
            if log.event_type == 'on':
                current_on_time = log_time
            elif log.event_type == 'off' and current_on_time:
                duration = (log_time - current_on_time).total_seconds() / 3600
                daily_stats[log_date]['hours'] += duration
                current_on_time = None
        
        # If power is still on, calculate until now
        if current_on_time:
            last_date = logs[-1].date.isoformat() if logs else now.date().isoformat()
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
            'events': [log.to_dict() for log in logs[-10:]]  # Last 10 events
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        print(f"Error in get_stats: {str(e)}")
        return jsonify({'error': 'An error occurred while fetching statistics'}), 500

@app.route('/api/recent-events', methods=['GET', 'OPTIONS'])
@token_required
def get_recent_events(current_user):
    try:
        limit = int(request.args.get('limit', 10))
        
        # Get recent power logs for user
        logs = PowerLog.query.filter_by(user_id=current_user)\
            .order_by(PowerLog.timestamp.desc())\
            .limit(limit)\
            .all()
        
        return jsonify({'events': [log.to_dict() for log in logs]}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        print(f"Error in get_recent_events: {str(e)}")
        return jsonify({'error': 'An error occurred while fetching recent events'}), 500

@app.route('/api/report', methods=['GET', 'OPTIONS'])
@token_required
def get_report(current_user):
    try:
        # Get all power logs for user
        logs = PowerLog.query.filter_by(user_id=current_user)\
            .order_by(PowerLog.timestamp)\
            .all()
        
        now = datetime.utcnow()
        
        # Calculate stats for different periods
        def calculate_period_stats(days):
            start_date = (now - timedelta(days=days)).date()
            filtered = [log for log in logs if log.date >= start_date]
            
            current_on_time = None
            total_hours = 0
            
            for log in filtered:
                log_time = log.timestamp
                if log.event_type == 'on':
                    current_on_time = log_time
                elif log.event_type == 'off' and current_on_time:
                    duration = (log_time - current_on_time).total_seconds() / 3600
                    total_hours += duration
                    current_on_time = None
            
            # If power is still on, calculate until now
            if current_on_time and filtered:
                duration = (now - current_on_time).total_seconds() / 3600
                total_hours += duration
            
            return round(total_hours, 2), len(filtered)
        
        today_hours, today_events = calculate_period_stats(1)
        week_hours, week_events = calculate_period_stats(7)
        month_hours, month_events = calculate_period_stats(30)
        
        # Get last event
        if logs:
            last_log = logs[-1]
            last_event_time = last_log.timestamp
            last_event_type = last_log.event_type
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
        
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        print(f"Error in get_report: {str(e)}")
        return jsonify({'error': 'An error occurred while fetching report'}), 500

# Set the port to the value of the PORT environment variable or default to 5000
port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    debug = os.environ.get('FLASK_ENV') == 'development'
    print("Starting Electricity Supply Logger API...")
    print(f"API will be available at http://localhost:{port}")
    print("Database: PostgreSQL")
    print("Available endpoints:")
    print("  - GET  /                      - Health check")
    print("  - GET  /api                   - API info")
    print("  - POST /api/register          - Register user")
    print("  - POST /api/login             - Login user")
    print("  - POST /api/verify-email      - Verify email")
    print("  - POST /api/verify-device     - Verify device")
    print("  - POST /api/resend-verification - Resend verification code")
    print("  - POST /api/log-power         - Log power event")
    print("  - GET  /api/stats             - Get statistics")
    print("  - GET  /api/recent-events     - Get recent events")
    print("  - GET  /api/report            - Get brief report summary")
    app.run(debug=debug, port=port, host='0.0.0.0')

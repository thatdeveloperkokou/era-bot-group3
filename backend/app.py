from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from datetime import datetime, timedelta
try:
    from flask_migrate import Migrate
    FLASK_MIGRATE_AVAILABLE = True
except ImportError:
    FLASK_MIGRATE_AVAILABLE = False
    Migrate = None
import os
import hashlib
import jwt
from functools import wraps
import secrets
import uuid
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_, and_, func
from database import db, User, PowerLog, VerificationCode, DeviceId, RegionProfile, init_db
from region_mapper import infer_region_from_location

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
mail_use_tls = os.environ.get('MAIL_USE_TLS', 'true').lower()
app.config['MAIL_USE_TLS'] = mail_use_tls == 'true'
app.config['MAIL_USE_SSL'] = mail_use_tls == 'false' and int(os.environ.get('MAIL_PORT', 587)) == 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', '')
app.config['MAIL_SUPPRESS_SEND'] = os.environ.get('MAIL_SUPPRESS_SEND', 'false').lower() == 'true'
# Add timeout settings for Railway deployment
app.config['MAIL_TIMEOUT'] = 10  # 10 second timeout for SMTP operations

try:
    mail = Mail(app)
except Exception as e:
    print(f"⚠️  Warning: Mail initialization error: {str(e)}")
    print("   Email functionality may not work, but continuing...")
    mail = None

# Initialize database
try:
    init_db(app)
    # Initialize Flask-Migrate if available
    if FLASK_MIGRATE_AVAILABLE and Migrate:
        migrate = Migrate(app, db)
except Exception as e:
    print(f"❌ Fatal: Database initialization failed: {str(e)}")
    print("   Application cannot start without database connection")
    raise

# CORS configuration - allow specific frontend URL in production, all origins in development
try:
    frontend_url = os.environ.get('FRONTEND_URL', '*')
    dev_origins_raw = os.environ.get('DEV_FRONTEND_URLS', 'http://localhost:3000,http://127.0.0.1:3000')
    dev_origins = [url.strip() for url in dev_origins_raw.split(',') if url.strip()]
    allow_dev_origins = os.environ.get('ALLOW_DEV_ORIGINS', 'true').lower() == 'true'

    if frontend_url == '*':
        # Development: allow all origins
        CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
        print("🌐 CORS: Allowing all origins (development mode)")
    else:
        # Production: allow specific frontend URL(s)
        # Support multiple URLs separated by comma
        origins = [url.strip() for url in frontend_url.split(',') if url.strip()]

        if allow_dev_origins:
            for dev_origin in dev_origins:
                if dev_origin not in origins:
                    origins.append(dev_origin)

        CORS(
            app,
            resources={r"/api/*": {"origins": origins}},
            supports_credentials=True,
            allow_headers=['Content-Type', 'Authorization']
        )
        print(f"🌐 CORS: Allowing origins: {origins}")
    print("✅ Application initialized successfully")
except Exception as e:
    print(f"❌ Fatal: CORS initialization failed: {str(e)}")
    import traceback
    traceback.print_exc()
    raise

# Add a marker to confirm app module loaded completely
print("✅ Flask app module loaded successfully - ready for gunicorn")


def resolve_region_id(location: str | None) -> str | None:
    """Map raw location text to one of the seeded region profile IDs."""
    return infer_region_from_location(location)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_verification_code():
    return str(secrets.randbelow(1000000)).zfill(6)

def send_verification_email(email, code):
    """
    Send verification email to user.
    Returns True if email was sent successfully or if email is not configured (for development).
    Returns False if email sending failed.
    """
    try:
        # Check if mail object is None (initialization failed)
        if mail is None:
            print(f"⚠️  Mail not initialized. Verification code for {email}: {code}")
            return True
        
        if app.config.get('MAIL_SUPPRESS_SEND'):
            print(f"📧 MAIL_SUPPRESS_SEND enabled. Skipping actual email send for {email}. Verification code: {code}")
            return True
        
        # Check if email is configured
        mail_username = app.config.get('MAIL_USERNAME', '')
        mail_password = app.config.get('MAIL_PASSWORD', '')
        mail_server = app.config.get('MAIL_SERVER', '')
        
        print(f"📧 Email config check: MAIL_SERVER={mail_server}, MAIL_USERNAME={'SET' if mail_username else 'NOT SET'}, MAIL_PASSWORD={'SET' if mail_password else 'NOT SET'}")
        
        if not mail_username or not mail_password:
            print(f"⚠️  Email not configured. Verification code for {email}: {code}")
            print(f"   To enable email, configure MAIL_USERNAME and MAIL_PASSWORD in Railway environment variables")
            print(f"   See EMAIL_SETUP.md for instructions")
            return True  # Return True for development (allow registration to continue)
        
        print(f"📧 Creating email message for {email}")
        # Create email message
        msg = Message(
            subject='Verify Your Email - Electricity Supply Logger',
            recipients=[email],
            html=f'''
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #f9f9f9;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 20px;
                        text-align: center;
                        border-radius: 10px 10px 0 0;
                    }}
                    .content {{
                        background: white;
                        padding: 30px;
                        border-radius: 0 0 10px 10px;
                    }}
                    .code {{
                        font-size: 32px;
                        font-weight: bold;
                        color: #667eea;
                        text-align: center;
                        padding: 20px;
                        background: #f0f4ff;
                        border-radius: 8px;
                        margin: 20px 0;
                        letter-spacing: 5px;
                    }}
                    .footer {{
                        margin-top: 20px;
                        padding-top: 20px;
                        border-top: 1px solid #e0e0e0;
                        font-size: 12px;
                        color: #666;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔌 Electricity Supply Logger</h1>
                    </div>
                    <div class="content">
                        <h2>Email Verification</h2>
                        <p>Thank you for registering! Please use the verification code below to verify your email address:</p>
                        <div class="code">{code}</div>
                        <p><strong>This code will expire in 10 minutes.</strong></p>
                        <p>If you didn't request this verification code, please ignore this email.</p>
                        <div class="footer">
                            <p>This is an automated message. Please do not reply to this email.</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            '''
        )
        
        print(f"📧 Attempting to send email via {mail_server}:{app.config.get('MAIL_PORT', 587)}...")
        # Send email with timeout handling - use threading to prevent blocking
        import threading
        import queue
        
        result_queue = queue.Queue()
        error_queue = queue.Queue()
        
        def send_email_thread():
            try:
                mail.send(msg)
                result_queue.put(True)
            except Exception as e:
                error_queue.put(e)
        
        # Start email sending in a separate thread
        email_thread = threading.Thread(target=send_email_thread, daemon=True)
        email_thread.start()
        
        # Wait for result with timeout (5 seconds)
        email_thread.join(timeout=5.0)
        
        if not result_queue.empty():
            print(f"✅ Verification email sent successfully to {email}")
            return True
        elif not error_queue.empty():
            error = error_queue.get()
            print(f"❌ Error during mail.send(): {type(error).__name__}: {str(error)}")
            raise error
        else:
            # Timeout - email sending is taking too long
            print(f"⚠️  Email sending timeout after 5 seconds. Email may still be sent, but continuing...")
            print(f"   Verification code for {email}: {code}")
            # Return False to indicate email may not have been sent
            # This will trigger the fallback to return code in response
            return False
        
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        print(f"❌ Error sending email to {email}")
        print(f"   Error type: {error_type}")
        print(f"   Error message: {error_msg}")
        print(f"   MAIL_SERVER: {app.config['MAIL_SERVER']}")
        print(f"   MAIL_PORT: {app.config['MAIL_PORT']}")
        print(f"   MAIL_USE_TLS: {app.config['MAIL_USE_TLS']}")
        print(f"   MAIL_USERNAME: {'set' if app.config['MAIL_USERNAME'] else 'NOT SET'}")
        print(f"   MAIL_PASSWORD: {'set' if app.config['MAIL_PASSWORD'] else 'NOT SET'}")
        print(f"   MAIL_DEFAULT_SENDER: {app.config['MAIL_DEFAULT_SENDER']}")
        
        # Provide helpful error messages
        if "Authentication failed" in error_msg or "535" in error_msg or "534" in error_msg:
            print(f"   💡 Tip: Authentication failed - Make sure you're using an App Password, not your regular password")
            print(f"   💡 For Gmail: https://myaccount.google.com/apppasswords")
            print(f"   💡 For Outlook: https://account.microsoft.com/security")
        elif "Connection" in error_msg or "timeout" in error_msg.lower() or "refused" in error_msg.lower():
            print(f"   💡 Tip: Connection issue - Check SMTP server and port settings")
            print(f"   💡 Try: MAIL_SERVER={app.config['MAIL_SERVER']}, MAIL_PORT={app.config['MAIL_PORT']}")
        elif "550" in error_msg or "553" in error_msg:
            print(f"   💡 Tip: Sender verification failed - Verify MAIL_DEFAULT_SENDER is correct")
        elif "SSL" in error_msg or "TLS" in error_msg:
            print(f"   💡 Tip: SSL/TLS issue - Try MAIL_USE_TLS=true for port 587, or MAIL_USE_SSL=true for port 465")
        
        # In development, print the code so registration can continue
        print(f"   📧 Verification code for {email}: {code}")
        print(f"   ⚠️  Email sending failed, but code is displayed above for development")
        
        # Return False to indicate email sending failed
        # But still allow the code to be used (code is saved in database)
        return False

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
            'verify-email': '/api/verify-email',
            'verify-device': '/api/verify-device',
            'resend-verification': '/api/resend-verification',
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
        print("📨 Received OPTIONS request for /api/register")
        return jsonify({}), 200
    
    print(f"📨 Received POST request to /api/register from origin: {request.headers.get('Origin', 'unknown')}")
    try:
        data = request.get_json() or request.json
        print(f"📨 Request data received: username={data.get('username') if data else 'None'}, email={data.get('email') if data else 'None'}")
        if not data:
            print("❌ No JSON data in request")
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        location = data.get('location', '')
        region_id = resolve_region_id(location)
        
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
        
        # Email verification flow
        verification_code = generate_verification_code()
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        
        # Store verification code (this will be used to create user after email verification)
        verif_code = VerificationCode(
            email=email,
            code=verification_code,
            username=username,
            password=hash_password(password),
            location=location,
            region_id=region_id,
            expires_at=expires_at
        )
        db.session.add(verif_code)
        db.session.commit()
        
        # Attempt to send email (non-blocking - don't wait for it)
        email_sent = send_verification_email(email, verification_code)
        
        # Return response immediately (don't wait for email)
        response_data = {
            'message': 'Verification code sent to your email',
            'requires_verification': True,
            'email': email
        }
        
        # If email sending failed, include code in response (for development/fallback)
        if not email_sent:
            response_data['fallback_code'] = verification_code
            response_data['message'] = 'Email sending failed. Please check your email configuration or use the code below.'
            print(f"⚠️  Email sending failed - returning code in response for {email}")
        
        return jsonify(response_data), 200
            
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
        
        username_or_email = data.get('username') or data.get('email')
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
        
        # TEMPORARILY DISABLED: Device verification removed for now
        # Allow login directly without device verification
        token = generate_token(user.username)
        
        # Store device ID if provided
        if device_id:
            # Check if device ID already exists
            existing_device = DeviceId.query.filter_by(
                user_id=user.username,
                device_id=device_id
            ).first()
            
            if not existing_device:
                device_id_record = DeviceId(
                    user_id=user.username,
                    device_id=device_id
                )
                db.session.add(device_id_record)
                db.session.commit()
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'username': user.username
        }), 200
        
        # TODO: Re-enable device verification later
        # Old code for device verification (commented out for easy restoration):
        # verified_devices = user.verified_devices or []
        # if device_id and device_id in verified_devices:
        #     # Device verified, allow login
        # else:
        #     # Require email verification for new device
        #     send_verification_email(user.email, verification_code)
                
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
        
        # Get user location if not provided and refresh region assignment
        if not location:
            location = user.location or ''
        elif location and location != user.location:
            user.location = location
        inferred_region = resolve_region_id(location or user.location)
        if inferred_region and inferred_region != user.region_id:
            user.region_id = inferred_region
        
        timestamp = datetime.utcnow()
        date = timestamp.date()
        
        # Save to database
        power_log = PowerLog(
            user_id=current_user,
            event_type=event_type,
            timestamp=timestamp,
            date=date,
            location=location,
            region_id=user.region_id,
            auto_generated=False
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
            'events': [log.to_dict() for log in logs[-20:]]  # Last 20 events (to include more auto-generated logs)
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


@app.route('/api/region-profiles', methods=['GET', 'OPTIONS'])
def list_region_profiles():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    try:
        profiles = RegionProfile.query.order_by(RegionProfile.disco_name).all()
        return jsonify({
            'regions': [profile.to_dict() for profile in profiles]
        }), 200
    except Exception as e:
        print(f"Error fetching region profiles: {str(e)}")
        return jsonify({'error': 'Failed to load region profiles'}), 500

@app.route('/api/verify-email', methods=['POST', 'OPTIONS'])
def verify_email():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json() or request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        email = data.get('email')
        code = data.get('code')
        
        if not email or not code:
            return jsonify({'error': 'Email and verification code are required'}), 400
        
        # Get verification code
        verif_code = VerificationCode.query.filter_by(email=email).first()
        if not verif_code:
            return jsonify({'error': 'Invalid verification code'}), 400
        
        if datetime.utcnow() > verif_code.expires_at:
            db.session.delete(verif_code)
            db.session.commit()
            return jsonify({'error': 'Verification code has expired'}), 400
        
        if verif_code.code != code:
            return jsonify({'error': 'Invalid verification code'}), 400
        
        # Create user account
        user = User(
            username=verif_code.username,
            password=verif_code.password,
            email=email,
            location=verif_code.location,
            region_id=verif_code.region_id,
            email_verified=True,
            created_at=datetime.utcnow()
        )
        db.session.add(user)
        
        # Generate device ID
        device_id = str(uuid.uuid4())
        device_id_record = DeviceId(
            user_id=verif_code.username,
            device_id=device_id
        )
        db.session.add(device_id_record)
        
        # Remove verification code
        db.session.delete(verif_code)
        db.session.commit()
        
        token = generate_token(verif_code.username)
        return jsonify({
            'message': 'Email verified successfully',
            'verified': True,
            'token': token,
            'username': verif_code.username,
            'deviceId': device_id
        }), 200
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'User already exists'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        print(f"Error in verify_email: {str(e)}")
        return jsonify({'error': 'An error occurred during email verification'}), 500

@app.route('/api/resend-verification', methods=['POST', 'OPTIONS'])
def resend_verification():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json() or request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        email = data.get('email')
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Get verification code
        verif_code = VerificationCode.query.filter_by(email=email).first()
        if not verif_code:
            return jsonify({'error': 'No pending verification found for this email'}), 400
        
        # Generate new code
        verification_code = generate_verification_code()
        verif_code.code = verification_code
        verif_code.expires_at = datetime.utcnow() + timedelta(minutes=10)
        db.session.commit()
        
        # Attempt to send email (non-blocking)
        email_sent = send_verification_email(email, verification_code)
        
        if email_sent:
            return jsonify({'message': 'Verification code resent to your email'}), 200
        else:
            # Email sending failed - return code in response as fallback
            return jsonify({
                'message': 'Email sending failed. Please check your email configuration.',
                'fallback_code': verification_code
            }), 200
            
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        print(f"Error in resend_verification: {str(e)}")
        return jsonify({'error': 'An error occurred while resending verification code'}), 500

@app.route('/api/verify-device', methods=['POST', 'OPTIONS'])
def verify_device():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json() or request.json
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
        
        email = data.get('email')
        code = data.get('code')
        
        if not email or not code:
            return jsonify({'error': 'Email and verification code are required'}), 400
        
        code_key = f"{email}_device"
        
        # Get verification code
        verif_code = VerificationCode.query.filter_by(email=code_key).first()
        if not verif_code:
            return jsonify({'error': 'Invalid verification code'}), 400
        
        if datetime.utcnow() > verif_code.expires_at:
            db.session.delete(verif_code)
            db.session.commit()
            return jsonify({'error': 'Verification code has expired'}), 400
        
        if verif_code.code != code:
            return jsonify({'error': 'Invalid verification code'}), 400
        
        # Verify device
        username = verif_code.username
        device_id = verif_code.device_id or str(uuid.uuid4())
        
        # Get user
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Add device to verified devices
        if device_id not in (user.verified_devices or []):
            if user.verified_devices is None:
                user.verified_devices = []
            user.verified_devices.append(device_id)
        
        # Save device ID
        existing_device = DeviceId.query.filter_by(
            user_id=username,
            device_id=device_id
        ).first()
        if not existing_device:
            device_id_record = DeviceId(
                user_id=username,
                device_id=device_id
            )
            db.session.add(device_id_record)
        
        # Remove verification code
        db.session.delete(verif_code)
        db.session.commit()
        
        token = generate_token(username)
        return jsonify({
            'message': 'Device verified successfully',
            'token': token,
            'username': username,
            'deviceId': device_id
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        print(f"Error in verify_device: {str(e)}")
        return jsonify({'error': 'An error occurred during device verification'}), 500

# Set the port to the value of the PORT environment variable or default to 5000
port = int(os.environ.get("PORT", 5000))

# Final check - confirm module loaded completely
print("✅ All routes and functions defined - app module is ready")

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
    
    # Make migrate available as Flask CLI command
    @app.cli.command()
    def migrate():
        """Run database migrations"""
        from flask_migrate import upgrade
        upgrade()
        print("✅ Database migrations applied")
    
    app.run(debug=debug, port=port, host='0.0.0.0')

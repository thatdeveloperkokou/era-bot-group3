from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import os
import hashlib
import jwt
from functools import wraps
import secrets
import uuid
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_, and_, func
from database import db, User, PowerLog, VerificationCode, DeviceId, init_db

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

mail = Mail(app)

# Initialize database
init_db(app)

# CORS configuration - allow specific frontend URL in production, all origins in development
frontend_url = os.environ.get('FRONTEND_URL', '*')
if frontend_url == '*':
    # Development: allow all origins
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
else:
    # Production: allow specific frontend URL
    CORS(app, resources={r"/api/*": {"origins": frontend_url}}, supports_credentials=True)

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
        # Check if email is configured
        if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
            print(f"⚠️  Email not configured. Verification code for {email}: {code}")
            print(f"   To enable email, configure MAIL_USERNAME and MAIL_PASSWORD in Railway environment variables")
            print(f"   See EMAIL_SETUP.md for instructions")
            print(f"   Current config: MAIL_SERVER={app.config['MAIL_SERVER']}, MAIL_USERNAME={'set' if app.config['MAIL_USERNAME'] else 'NOT SET'}, MAIL_PASSWORD={'set' if app.config['MAIL_PASSWORD'] else 'NOT SET'}")
            return True  # Return True for development (allow registration to continue)
        
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
        
        # Send email
        mail.send(msg)
        print(f"✅ Verification email sent successfully to {email}")
        return True
        
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
        
        # Generate verification code
        verification_code = generate_verification_code()
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        
        # Save verification code to database
        verif_code = VerificationCode(
            email=email,
            code=verification_code,
            expires_at=expires_at,
            username=username,
            password=hash_password(password),
            location=location
        )
        db.session.add(verif_code)
        db.session.commit()
        
        # Send verification email
        if send_verification_email(email, verification_code):
            return jsonify({
                'message': 'Verification email sent',
                'email': email
            }), 200
        else:
            return jsonify({'error': 'Failed to send verification email. Please check your email configuration.'}), 500
            
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
        
        # Check if device is verified
        verified_devices = user.verified_devices or []
        
        # For backward compatibility: if user has no email, allow login without verification
        if not user.email:
            # Old user without email - allow login
            token = generate_token(user.username)
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'username': user.username
            }), 200
        
        if device_id and device_id in verified_devices:
            # Device is verified, allow login
            token = generate_token(user.username)
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'username': user.username
            }), 200
        else:
            # New device or no device ID, require email verification
            # Generate verification code for device
            verification_code = generate_verification_code()
            expires_at = datetime.utcnow() + timedelta(minutes=10)
            
            # Delete old device verification code if exists
            VerificationCode.query.filter_by(email=f"{user.email}_device").delete()
            
            # Save new verification code
            verif_code = VerificationCode(
                email=f"{user.email}_device",
                code=verification_code,
                expires_at=expires_at,
                username=user.username,
                device_id=device_id
            )
            db.session.add(verif_code)
            db.session.commit()
            
            # Send verification email
            if send_verification_email(user.email, verification_code):
                return jsonify({
                    'requiresVerification': True,
                    'email': user.email,
                    'message': 'Device verification required. Check your email.'
                }), 200
            else:
                return jsonify({'error': 'Failed to send verification email'}), 500
                
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
        
        if send_verification_email(email, verification_code):
            return jsonify({'message': 'Verification code resent'}), 200
        else:
            return jsonify({'error': 'Failed to send verification email'}), 500
            
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

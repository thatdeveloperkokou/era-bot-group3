"""
Database models and configuration for PostgreSQL
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()


class RegionProfile(db.Model):
    """Regional/distribution company profile derived from NERC data"""
    __tablename__ = 'region_profiles'

    id = db.Column(db.String(50), primary_key=True)
    disco_name = db.Column(db.String(150), nullable=False)
    states = db.Column(db.JSON, nullable=False, default=list)
    keywords = db.Column(db.JSON, nullable=False, default=list)
    avg_offtake_mwh_per_hour = db.Column(db.Float, nullable=False)
    avg_available_pcc_mwh_per_hour = db.Column(db.Float, nullable=False)
    utilisation_percent = db.Column(db.Float, nullable=False)
    estimated_daily_mwh = db.Column(db.Float, nullable=False)
    estimated_full_load_hours = db.Column(db.Float, nullable=False)
    schedule_template = db.Column(db.JSON, nullable=True)
    source = db.Column(db.String(255), default='NERC Q2 2025')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    users = db.relationship('User', backref='region_profile', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'disco_name': self.disco_name,
            'states': self.states,
            'keywords': self.keywords,
            'avg_offtake_mwh_per_hour': self.avg_offtake_mwh_per_hour,
            'avg_available_pcc_mwh_per_hour': self.avg_available_pcc_mwh_per_hour,
            'utilisation_percent': self.utilisation_percent,
            'estimated_daily_mwh': self.estimated_daily_mwh,
            'estimated_full_load_hours': self.estimated_full_load_hours,
            'schedule_template': self.schedule_template,
            'source': self.source,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)  # Allow null for backward compatibility
    location = db.Column(db.String(500), nullable=True)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    region_id = db.Column(db.String(50), db.ForeignKey('region_profiles.id'), nullable=True)
    
    # Relationships
    power_logs = db.relationship('PowerLog', backref='user', lazy=True, cascade='all, delete-orphan')
    device_ids = db.relationship('DeviceId', backref='user', lazy=True, cascade='all, delete-orphan')
    
    @property
    def verified_devices(self):
        """Get list of verified device IDs"""
        return [device.device_id for device in self.device_ids]
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'username': self.username,
            'email': self.email,
            'location': self.location,
            'email_verified': self.email_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'region_id': self.region_id,
            'verified_devices': self.verified_devices
        }

class PowerLog(db.Model):
    """Power log model"""
    __tablename__ = 'power_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), db.ForeignKey('users.username'), nullable=False)
    event_type = db.Column(db.String(10), nullable=False)  # 'on' or 'off'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(500), nullable=True)
    region_id = db.Column(db.String(50), db.ForeignKey('region_profiles.id'), nullable=True)
    auto_generated = db.Column(db.Boolean, default=False, nullable=False)

    region = db.relationship('RegionProfile', lazy=True)
    
    def to_dict(self):
        """Convert power log to dictionary"""
        return {
            'user_id': self.user_id,
            'event_type': self.event_type,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'date': self.date.isoformat() if self.date else None,
            'location': self.location,
            'region_id': self.region_id,
            'auto_generated': self.auto_generated
        }

class VerificationCode(db.Model):
    """Verification code model"""
    __tablename__ = 'verification_codes'
    
    email = db.Column(db.String(255), primary_key=True)
    code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    username = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(500), nullable=True)
    region_id = db.Column(db.String(50), db.ForeignKey('region_profiles.id'), nullable=True)
    device_id = db.Column(db.String(255), nullable=True)
    
    def is_expired(self):
        """Check if verification code is expired"""
        return datetime.utcnow() > self.expires_at
    
    def to_dict(self):
        """Convert verification code to dictionary"""
        return {
            'email': self.email,
            'code': self.code,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'username': self.username,
            'location': self.location,
            'device_id': self.device_id
        }

class DeviceId(db.Model):
    """Device ID model"""
    __tablename__ = 'device_ids'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), db.ForeignKey('users.username'), nullable=False)
    device_id = db.Column(db.String(255), nullable=False)
    
    # Unique constraint on user_id and device_id combination
    __table_args__ = (db.UniqueConstraint('user_id', 'device_id', name='unique_user_device'),)
    
    def to_dict(self):
        """Convert device ID to dictionary"""
        return {
            'user_id': self.user_id,
            'device_id': self.device_id
        }

def init_db(app):
    """Initialize database"""
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Fallback to local PostgreSQL if DATABASE_URL not set
        db_user = os.environ.get('DB_USER', 'postgres')
        db_password = os.environ.get('DB_PASSWORD', 'postgres')
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_port = os.environ.get('DB_PORT', '5432')
        db_name = os.environ.get('DB_NAME', 'electricity_logger')
        
        database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        print(f"⚠️  DATABASE_URL not set, using local PostgreSQL: {db_host}:{db_port}/{db_name}")
    else:
        print(f"✅ Using DATABASE_URL from environment")
        
        # Validate DATABASE_URL format
        if database_url.startswith('postgresql://') or database_url.startswith('postgres://'):
            # Extract hostname to check if it's complete
            try:
                # Parse the URL to check hostname
                if '@' in database_url:
                    host_part = database_url.split('@')[1].split('/')[0]
                    if ':' in host_part:
                        hostname = host_part.split(':')[0]
                    else:
                        hostname = host_part
                    
                    # Check if hostname looks incomplete (missing domain)
                    if hostname.startswith('dpg-') and '.' not in hostname:
                        print(f"⚠️  WARNING: DATABASE_URL hostname appears incomplete!")
                        print(f"   Hostname: {hostname}")
                        print(f"   Render PostgreSQL hostnames should include the full domain (e.g., .oregon-postgres.render.com)")
                        print(f"   Please check your DATABASE_URL in Render dashboard:")
                        print(f"   1. Go to your PostgreSQL service in Render")
                        print(f"   2. Go to 'Info' tab")
                        print(f"   3. Copy the complete 'Internal Database URL' or 'External Connection String'")
                        print(f"   4. Make sure it includes the full domain (e.g., dpg-xxxxx-a.oregon-postgres.render.com)")
            except Exception as e:
                print(f"⚠️  Could not parse DATABASE_URL for validation: {str(e)}")
        
        # Check if using internal hostname (Railway/Render) and suggest using public URL if connection fails
        if 'railway.internal' in database_url:
            print(f"⚠️  Warning: Using Railway internal hostname. If connection fails, use the public DATABASE_URL from PostgreSQL service Variables tab")
        if 'onrender.com' in database_url and 'internal' in database_url.lower():
            print(f"⚠️  Note: Using Render internal database URL. This should work for services in the same Render account.")
    
    # Handle cloud provider DATABASE_URL format (may include postgres:// instead of postgresql://)
    # Render, Railway, Heroku, etc. may provide postgres:// which needs to be postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    db.init_app(app)
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"⚠️  Error creating database tables: {str(e)}")
            print(f"   Make sure PostgreSQL is running and DATABASE_URL is correct")
            raise


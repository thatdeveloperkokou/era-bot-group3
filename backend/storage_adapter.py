"""
Storage adapter that routes operations to PostgreSQL or file storage
based on STORAGE_MODE setting.
"""
from database import STORAGE_MODE, db, User, PowerLog, VerificationCode, DeviceId, RegionProfile
from datetime import datetime, date
from typing import Optional, List, Dict

def get_storage():
    """Get the appropriate storage backend"""
    if STORAGE_MODE == 'file':
        from file_storage import get_file_storage
        return get_file_storage()
    return None  # Use PostgreSQL (SQLAlchemy)


# User operations
def get_user_by_username(username: str):
    """Get user by username"""
    if STORAGE_MODE == 'file':
        storage = get_storage()
        user_data = storage.get_user_by_username(username)
        if user_data:
            # Convert to User-like object
            class FileUser:
                def __init__(self, data):
                    self.username = data.get('username')
                    self.password = data.get('password')
                    self.email = data.get('email')
                    self.location = data.get('location')
                    self.email_verified = data.get('email_verified', False)
                    self.region_id = data.get('region_id')
                    self.created_at = data.get('created_at')
            return FileUser(user_data)
    else:
        return User.query.filter_by(username=username).first()
    return None


def get_user_by_email(email: str):
    """Get user by email"""
    if STORAGE_MODE == 'file':
        storage = get_storage()
        user_data = storage.get_user_by_email(email)
        if user_data:
            class FileUser:
                def __init__(self, data):
                    self.username = data.get('username')
                    self.password = data.get('password')
                    self.email = data.get('email')
                    self.location = data.get('location')
                    self.email_verified = data.get('email_verified', False)
                    self.region_id = data.get('region_id')
            return FileUser(user_data)
    else:
        return User.query.filter_by(email=email).first()
    return None


def create_user(user_data: Dict):
    """Create a new user"""
    if STORAGE_MODE == 'file':
        storage = get_storage()
        return storage.create_user(user_data)
    else:
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user


# Verification code operations
def get_verification_code_by_email(email: str):
    """Get verification code by email"""
    if STORAGE_MODE == 'file':
        storage = get_storage()
        code_data = storage.get_verification_code_by_email(email)
        if code_data:
            class FileVerificationCode:
                def __init__(self, data):
                    self.email = data.get('email')
                    self.code = data.get('code')
                    self.username = data.get('username')
                    self.password = data.get('password')
                    self.location = data.get('location')
                    self.region_id = data.get('region_id')
                    self.device_id = data.get('device_id')
                    expires_at_str = data.get('expires_at')
                    if expires_at_str:
                        self.expires_at = datetime.fromisoformat(expires_at_str.replace('Z', '+00:00'))
                    else:
                        self.expires_at = None
                
                def is_expired(self):
                    if not self.expires_at:
                        return True
                    return datetime.utcnow() > self.expires_at.replace(tzinfo=None)
            return FileVerificationCode(code_data)
    else:
        return VerificationCode.query.filter_by(email=email).first()
    return None


def get_verification_code_by_username(username: str):
    """Get verification code by username"""
    if STORAGE_MODE == 'file':
        storage = get_storage()
        for code_data in storage.verification_codes:
            if code_data.get('username') == username:
                class FileVerificationCode:
                    def __init__(self, data):
                        self.email = data.get('email')
                        self.code = data.get('code')
                        self.username = data.get('username')
                        self.password = data.get('password')
                        self.location = data.get('location')
                        self.region_id = data.get('region_id')
                        self.device_id = data.get('device_id')
                        expires_at_str = data.get('expires_at')
                        if expires_at_str:
                            self.expires_at = datetime.fromisoformat(expires_at_str.replace('Z', '+00:00'))
                        else:
                            self.expires_at = None
                    
                    def is_expired(self):
                        if not self.expires_at:
                            return True
                        return datetime.utcnow() > self.expires_at.replace(tzinfo=None)
                return FileVerificationCode(code_data)
    else:
        return VerificationCode.query.filter_by(username=username).first()
    return None


def create_or_update_verification_code(code_data: Dict):
    """Create or update verification code"""
    if STORAGE_MODE == 'file':
        storage = get_storage()
        return storage.create_or_update_verification_code(code_data)
    else:
        existing = VerificationCode.query.filter_by(email=code_data['email']).first()
        if existing:
            for key, value in code_data.items():
                setattr(existing, key, value)
        else:
            existing = VerificationCode(**code_data)
            db.session.add(existing)
        db.session.commit()
        return existing


def delete_verification_code(email: str):
    """Delete verification code"""
    if STORAGE_MODE == 'file':
        storage = get_storage()
        storage.delete_verification_code(email)
    else:
        code = VerificationCode.query.filter_by(email=email).first()
        if code:
            db.session.delete(code)
            db.session.commit()


# Power log operations
def create_power_log(log_data: Dict):
    """Create a power log"""
    if STORAGE_MODE == 'file':
        storage = get_storage()
        return storage.create_power_log(log_data)
    else:
        log = PowerLog(**log_data)
        db.session.add(log)
        db.session.commit()
        return log


def get_power_logs_by_user(user_id: str, start_date=None, end_date=None):
    """Get power logs for a user"""
    if STORAGE_MODE == 'file':
        storage = get_storage()
        logs = storage.get_power_logs_by_user(user_id, start_date, end_date)
        # Convert to PowerLog-like objects
        class FilePowerLog:
            def __init__(self, data):
                self.id = data.get('id')
                self.user_id = data.get('user_id')
                self.event_type = data.get('event_type')
                self.timestamp = datetime.fromisoformat(data.get('timestamp', '').replace('Z', '+00:00'))
                date_str = data.get('date')
                if isinstance(date_str, str):
                    self.date = date.fromisoformat(date_str)
                else:
                    self.date = date_str
                self.location = data.get('location')
                self.region_id = data.get('region_id')
                self.auto_generated = data.get('auto_generated', False)
            
            def to_dict(self):
                return {
                    'user_id': self.user_id,
                    'event_type': self.event_type,
                    'timestamp': self.timestamp.isoformat() if self.timestamp else None,
                    'date': self.date.isoformat() if self.date else None,
                    'location': self.location,
                    'region_id': self.region_id,
                    'auto_generated': self.auto_generated
                }
        return [FilePowerLog(log) for log in logs]
    else:
        query = PowerLog.query.filter_by(user_id=user_id)
        if start_date:
            query = query.filter(PowerLog.date >= start_date)
        if end_date:
            query = query.filter(PowerLog.date <= end_date)
        return query.order_by(PowerLog.timestamp).all()


def get_recent_power_logs(user_id: str, limit: int = 20):
    """Get recent power logs"""
    if STORAGE_MODE == 'file':
        storage = get_storage()
        logs = storage.get_recent_power_logs(user_id, limit)
        class FilePowerLog:
            def __init__(self, data):
                self.id = data.get('id')
                self.user_id = data.get('user_id')
                self.event_type = data.get('event_type')
                timestamp_str = data.get('timestamp', '')
                if timestamp_str:
                    self.timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                else:
                    self.timestamp = None
                date_str = data.get('date')
                if isinstance(date_str, str):
                    self.date = date.fromisoformat(date_str)
                else:
                    self.date = date_str
                self.location = data.get('location')
                self.region_id = data.get('region_id')
                self.auto_generated = data.get('auto_generated', False)
            
            def to_dict(self):
                return {
                    'user_id': self.user_id,
                    'event_type': self.event_type,
                    'timestamp': self.timestamp.isoformat() if self.timestamp else None,
                    'date': self.date.isoformat() if self.date else None,
                    'location': self.location,
                    'region_id': self.region_id,
                    'auto_generated': self.auto_generated
                }
        return [FilePowerLog(log) for log in logs]
    else:
        return PowerLog.query.filter_by(user_id=user_id).order_by(PowerLog.timestamp.desc()).limit(limit).all()


# Device ID operations
def create_device_id(device_data: Dict):
    """Create device ID"""
    if STORAGE_MODE == 'file':
        storage = get_storage()
        return storage.create_device_id(device_data)
    else:
        device = DeviceId(**device_data)
        db.session.add(device)
        db.session.commit()
        return device


def get_device_ids_by_user(user_id: str):
    """Get device IDs for a user"""
    if STORAGE_MODE == 'file':
        storage = get_storage()
        return storage.get_device_ids_by_user(user_id)
    else:
        devices = DeviceId.query.filter_by(user_id=user_id).all()
        return [device.device_id for device in devices]


# Region profile operations
def get_all_region_profiles():
    """Get all region profiles"""
    if STORAGE_MODE == 'file':
        storage = get_storage()
        return storage.get_all_region_profiles()
    else:
        return RegionProfile.query.order_by(RegionProfile.disco_name).all()


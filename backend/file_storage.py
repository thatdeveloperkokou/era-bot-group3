"""
File-based storage fallback when PostgreSQL is unavailable.
Stores data in JSON files in backend/data/ directory.
"""
import json
import os
from datetime import datetime, date
from typing import List, Dict, Optional
import hashlib

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = os.path.join(DATA_DIR, 'users.json')
POWER_LOGS_FILE = os.path.join(DATA_DIR, 'power_logs.json')
VERIFICATION_CODES_FILE = os.path.join(DATA_DIR, 'verification_codes.json')
DEVICE_IDS_FILE = os.path.join(DATA_DIR, 'device_ids.json')
REGION_PROFILES_FILE = os.path.join(DATA_DIR, 'region_profiles.json')


def _load_json(filepath: str, default: list = None) -> list:
    """Load JSON file, return default if file doesn't exist"""
    if default is None:
        default = []
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    except Exception as e:
        print(f"⚠️  Error loading {filepath}: {e}")
        return default


def _save_json(filepath: str, data: list):
    """Save data to JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    except Exception as e:
        print(f"❌ Error saving {filepath}: {e}")
        raise


def _serialize_datetime(obj):
    """Convert datetime/date objects to ISO strings for JSON"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


class FileStorage:
    """File-based storage implementation"""
    
    def __init__(self):
        self.users = _load_json(USERS_FILE, [])
        self.power_logs = _load_json(POWER_LOGS_FILE, [])
        self.verification_codes = _load_json(VERIFICATION_CODES_FILE, [])
        self.device_ids = _load_json(DEVICE_IDS_FILE, [])
        self.region_profiles = _load_json(REGION_PROFILES_FILE, [])
        print("✅ File storage initialized (PostgreSQL fallback mode)")
    
    def save_users(self):
        _save_json(USERS_FILE, self.users)
    
    def save_power_logs(self):
        _save_json(POWER_LOGS_FILE, self.power_logs)
    
    def save_verification_codes(self):
        _save_json(VERIFICATION_CODES_FILE, self.verification_codes)
    
    def save_device_ids(self):
        _save_json(DEVICE_IDS_FILE, self.device_ids)
    
    # User operations
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        for user in self.users:
            if user.get('username') == username:
                return user
        return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        for user in self.users:
            if user.get('email') == email:
                return user
        return None
    
    def create_user(self, user_data: Dict):
        # Check if user already exists
        if self.get_user_by_username(user_data.get('username')):
            raise ValueError(f"User {user_data.get('username')} already exists")
        if user_data.get('email') and self.get_user_by_email(user_data.get('email')):
            raise ValueError(f"Email {user_data.get('email')} already exists")
        
        user_data['created_at'] = datetime.utcnow().isoformat()
        self.users.append(user_data)
        self.save_users()
        return user_data
    
    # Power log operations
    def create_power_log(self, log_data: Dict):
        log_data['id'] = len(self.power_logs) + 1
        log_data['timestamp'] = datetime.utcnow().isoformat()
        if isinstance(log_data.get('date'), date):
            log_data['date'] = log_data['date'].isoformat()
        self.power_logs.append(log_data)
        self.save_power_logs()
        return log_data
    
    def get_power_logs_by_user(self, user_id: str, start_date=None, end_date=None) -> List[Dict]:
        logs = [log for log in self.power_logs if log.get('user_id') == user_id]
        
        if start_date:
            if isinstance(start_date, date):
                start_date = start_date.isoformat()
            logs = [log for log in logs if log.get('date', '') >= start_date]
        
        if end_date:
            if isinstance(end_date, date):
                end_date = end_date.isoformat()
            logs = [log for log in logs if log.get('date', '') <= end_date]
        
        # Sort by timestamp
        logs.sort(key=lambda x: x.get('timestamp', ''))
        return logs
    
    def get_recent_power_logs(self, user_id: str, limit: int = 20) -> List[Dict]:
        logs = self.get_power_logs_by_user(user_id)
        return logs[-limit:]
    
    # Verification code operations
    def get_verification_code_by_email(self, email: str) -> Optional[Dict]:
        for code in self.verification_codes:
            if code.get('email') == email:
                return code
        return None
    
    def create_or_update_verification_code(self, code_data: Dict):
        existing = self.get_verification_code_by_email(code_data['email'])
        if existing:
            # Update existing
            existing.update(code_data)
            existing['expires_at'] = code_data.get('expires_at', datetime.utcnow().isoformat())
        else:
            # Create new
            code_data['expires_at'] = code_data.get('expires_at', datetime.utcnow().isoformat())
            self.verification_codes.append(code_data)
        self.save_verification_codes()
        return code_data
    
    def delete_verification_code(self, email: str):
        self.verification_codes = [c for c in self.verification_codes if c.get('email') != email]
        self.save_verification_codes()
    
    # Device ID operations
    def create_device_id(self, device_data: Dict):
        device_data['id'] = len(self.device_ids) + 1
        self.device_ids.append(device_data)
        self.save_device_ids()
        return device_data
    
    def get_device_ids_by_user(self, user_id: str) -> List[str]:
        return [d.get('device_id') for d in self.device_ids if d.get('user_id') == user_id]
    
    # Region profile operations
    def get_region_profile(self, region_id: str) -> Optional[Dict]:
        for region in self.region_profiles:
            if region.get('id') == region_id:
                return region
        return None
    
    def get_all_region_profiles(self) -> List[Dict]:
        return self.region_profiles


# Global file storage instance
file_storage = None

def get_file_storage():
    """Get or create file storage instance"""
    global file_storage
    if file_storage is None:
        file_storage = FileStorage()
    return file_storage


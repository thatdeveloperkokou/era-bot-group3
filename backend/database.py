"""
File-based storage using JSON files
All data is stored in backend/data/ directory
"""
from datetime import datetime
import os

# Storage mode is always 'file' now
STORAGE_MODE = 'file'

# Dummy db object for compatibility (not used)
db = None

# Dummy model classes for compatibility (not used with file storage)
# These are kept for import compatibility but are not actually used
class RegionProfile:
    """Dummy class for compatibility"""
    pass

class User:
    """Dummy class for compatibility"""
    pass

class PowerLog:
    """Dummy class for compatibility"""
    pass

class VerificationCode:
    """Dummy class for compatibility"""
    pass

class DeviceId:
    """Dummy class for compatibility"""
    pass

def init_db(app):
    """Initialize file-based storage"""
    global STORAGE_MODE
    STORAGE_MODE = 'file'
    
    try:
        from file_storage import get_file_storage
        file_storage = get_file_storage()
        print("✅ File-based storage initialized")
        print("   Data will be stored in backend/data/ directory")
        print("   Files: users.json, power_logs.json, verification_codes.json, device_ids.json")
    except Exception as file_error:
        print(f"❌ File storage initialization failed: {file_error}")
        print("   Application cannot start without storage")
        raise


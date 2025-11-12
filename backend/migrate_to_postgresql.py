"""
Migration script to migrate data from JSON/CSV files to PostgreSQL
Run this script once to migrate existing data to PostgreSQL
"""
import os
import json
import csv
from datetime import datetime
from dotenv import load_dotenv
from database import db, User, PowerLog, VerificationCode, DeviceId, init_db
from app import app, hash_password

load_dotenv()

def migrate_users():
    """Migrate users from users.json to PostgreSQL"""
    users_file = os.path.join(os.path.dirname(__file__), 'users.json')
    
    if not os.path.exists(users_file):
        print("⚠️  users.json not found, skipping user migration")
        return
    
    print("📦 Migrating users from users.json...")
    
    with open(users_file, 'r') as f:
        users = json.load(f)
    
    migrated = 0
    skipped = 0
    
    for username, user_data in users.items():
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                print(f"  ⏭️  User {username} already exists, skipping")
                skipped += 1
                continue
            
            # Create user
            user = User(
                username=username,
                password=user_data.get('password', ''),
                email=user_data.get('email', ''),
                location=user_data.get('location', ''),
                email_verified=user_data.get('email_verified', False),
                created_at=datetime.fromisoformat(user_data.get('created_at', datetime.utcnow().isoformat()))
            )
            db.session.add(user)
            db.session.flush()  # Flush to get user ID
            
            # Migrate verified devices
            verified_devices = user_data.get('verified_devices', [])
            for device_id in verified_devices:
                device_id_record = DeviceId(
                    user_id=username,
                    device_id=device_id
                )
                db.session.add(device_id_record)
            
            migrated += 1
            print(f"  ✅ Migrated user: {username}")
            
        except Exception as e:
            print(f"  ❌ Error migrating user {username}: {str(e)}")
            db.session.rollback()
    
    db.session.commit()
    print(f"✅ Migrated {migrated} users, skipped {skipped} existing users")

def migrate_power_logs():
    """Migrate power logs from power_logs.csv to PostgreSQL"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    logs_file = os.path.join(data_dir, 'power_logs.csv')
    
    if not os.path.exists(logs_file):
        print("⚠️  power_logs.csv not found, skipping power logs migration")
        return
    
    print("📦 Migrating power logs from power_logs.csv...")
    
    logs = []
    with open(logs_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            logs.append(row)
    
    migrated = 0
    skipped = 0
    
    for log in logs:
        try:
            user_id = log.get('user_id')
            if not user_id:
                continue
            
            # Check if user exists
            user = User.query.filter_by(username=user_id).first()
            if not user:
                print(f"  ⚠️  User {user_id} not found, skipping log")
                skipped += 1
                continue
            
            # Parse timestamp
            try:
                timestamp = datetime.fromisoformat(log['timestamp'])
            except:
                timestamp = datetime.utcnow()
            
            # Parse date
            try:
                if 'date' in log and log['date']:
                    date = datetime.fromisoformat(log['date']).date()
                else:
                    date = timestamp.date()
            except:
                date = timestamp.date()
            
            # Check if log already exists (same user, event_type, timestamp)
            existing_log = PowerLog.query.filter_by(
                user_id=user_id,
                event_type=log['event_type'],
                timestamp=timestamp
            ).first()
            
            if existing_log:
                skipped += 1
                continue
            
            # Create power log
            power_log = PowerLog(
                user_id=user_id,
                event_type=log['event_type'],
                timestamp=timestamp,
                date=date,
                location=log.get('location', '')
            )
            db.session.add(power_log)
            migrated += 1
            
        except Exception as e:
            print(f"  ❌ Error migrating log: {str(e)}")
            db.session.rollback()
    
    db.session.commit()
    print(f"✅ Migrated {migrated} power logs, skipped {skipped} existing logs")

def migrate_device_ids():
    """Migrate device IDs from device_ids.json to PostgreSQL"""
    device_ids_file = os.path.join(os.path.dirname(__file__), 'device_ids.json')
    
    if not os.path.exists(device_ids_file):
        print("⚠️  device_ids.json not found, skipping device IDs migration")
        return
    
    print("📦 Migrating device IDs from device_ids.json...")
    
    with open(device_ids_file, 'r') as f:
        device_ids = json.load(f)
    
    migrated = 0
    skipped = 0
    
    for username, device_id_list in device_ids.items():
        try:
            # Check if user exists
            user = User.query.filter_by(username=username).first()
            if not user:
                print(f"  ⚠️  User {username} not found, skipping device IDs")
                skipped += 1
                continue
            
            for device_id in device_id_list:
                # Check if device ID already exists
                existing_device = DeviceId.query.filter_by(
                    user_id=username,
                    device_id=device_id
                ).first()
                
                if existing_device:
                    skipped += 1
                    continue
                
                # Create device ID
                device_id_record = DeviceId(
                    user_id=username,
                    device_id=device_id
                )
                db.session.add(device_id_record)
                migrated += 1
            
            print(f"  ✅ Migrated device IDs for user: {username}")
            
        except Exception as e:
            print(f"  ❌ Error migrating device IDs for {username}: {str(e)}")
            db.session.rollback()
    
    db.session.commit()
    print(f"✅ Migrated {migrated} device IDs, skipped {skipped} existing device IDs")

def main():
    """Main migration function"""
    print("🚀 Starting migration to PostgreSQL...")
    print("=" * 50)
    
    # Initialize database
    init_db(app)
    
    with app.app_context():
        # Migrate users
        migrate_users()
        print()
        
        # Migrate power logs
        migrate_power_logs()
        print()
        
        # Migrate device IDs
        migrate_device_ids()
        print()
        
        print("=" * 50)
        print("✅ Migration completed!")
        print()
        print("📝 Note: Original files (users.json, power_logs.csv, device_ids.json)")
        print("   have not been deleted. You can delete them manually after verifying")
        print("   that the migration was successful.")

if __name__ == '__main__':
    main()


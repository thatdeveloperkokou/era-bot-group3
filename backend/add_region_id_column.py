#!/usr/bin/env python3
"""
Quick script to add region_id column to verification_codes table.
This can be run directly without Flask-Migrate.
"""
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def get_database_url():
    """Get database URL from environment"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Fallback to individual parameters
        db_user = os.environ.get('DB_USER', 'postgres')
        db_password = os.environ.get('DB_PASSWORD', 'postgres')
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_port = os.environ.get('DB_PORT', '5432')
        db_name = os.environ.get('DB_NAME', 'electricity_logger')
        database_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    
    # Handle Railway/Heroku format
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return database_url

def add_region_id_column():
    """Add region_id column to verification_codes table if it doesn't exist"""
    database_url = get_database_url()
    
    print(f"🔗 Connecting to database...")
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as conn:
            # Check if column already exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='verification_codes' AND column_name='region_id'
            """))
            
            if result.fetchone():
                print("✅ Column 'region_id' already exists in verification_codes table")
                return True
            
            # Add the column
            print("🔄 Adding region_id column to verification_codes table...")
            conn.execute(text("""
                ALTER TABLE verification_codes 
                ADD COLUMN region_id VARCHAR(50)
            """))
            conn.commit()
            print("✅ Successfully added region_id column to verification_codes table")
            return True
            
    except Exception as e:
        error_msg = str(e)
        if "already exists" in error_msg.lower() or "duplicate" in error_msg.lower():
            print("✅ Column 'region_id' already exists (checked via error message)")
            return True
        else:
            print(f"❌ Error adding column: {error_msg}")
            raise
    finally:
        engine.dispose()

if __name__ == '__main__':
    try:
        add_region_id_column()
        print("\n✅ Migration complete! The region_id column has been added.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        sys.exit(1)

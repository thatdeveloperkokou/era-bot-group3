#!/usr/bin/env python3
"""
Flask-Migrate CLI wrapper for database migrations.

Usage:
    python migrate.py init              # Initialize migrations (first time only)
    python migrate.py migrate [message]  # Create a new migration
    python migrate.py upgrade          # Apply migrations
    python migrate.py downgrade         # Rollback last migration
    python migrate.py current           # Show current migration version
    python migrate.py history           # Show migration history
    python migrate.py stamp [revision]  # Stamp database with revision
"""
import os
import sys
from flask_migrate import Migrate, upgrade, migrate, init, stamp, current, downgrade, history, show
from app import app, db
from database import init_db

# Initialize database connection
init_db(app)

# Initialize Flask-Migrate
migrate_obj = Migrate(app, db)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    # Run Flask-Migrate commands
    with app.app_context():
        if command == 'init':
            init()
            print("✅ Migrations initialized")
        elif command == 'migrate':
            message = sys.argv[2] if len(sys.argv) > 2 else 'Auto migration'
            migrate(message=message)
            print(f"✅ Migration created: {message}")
        elif command == 'upgrade':
            revision = sys.argv[2] if len(sys.argv) > 2 else 'head'
            upgrade(revision=revision)
            print(f"✅ Database upgraded to: {revision}")
        elif command == 'downgrade':
            revision = sys.argv[2] if len(sys.argv) > 2 else '-1'
            downgrade(revision=revision)
            print(f"✅ Database downgraded")
        elif command == 'current':
            current()
        elif command == 'history':
            history()
        elif command == 'show':
            revision = sys.argv[2] if len(sys.argv) > 2 else 'current'
            show(revision=revision)
        elif command == 'stamp':
            revision = sys.argv[2] if len(sys.argv) > 2 else 'head'
            stamp(revision=revision)
            print(f"✅ Database stamped with: {revision}")
        else:
            print(f"❌ Unknown command: {command}")
            print(__doc__)
            sys.exit(1)


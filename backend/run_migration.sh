#!/bin/bash
# Quick script to run database migrations
# Usage: ./run_migration.sh

cd "$(dirname "$0")"

echo "🔄 Running database migrations..."

# Check if migrations folder exists
if [ ! -d "migrations" ]; then
    echo "📦 Initializing migrations..."
    python migrate.py db init
fi

# Create migration for current changes
echo "📝 Creating migration..."
python migrate.py db migrate -m "Auto migration"

# Apply migration
echo "⬆️  Applying migration..."
python migrate.py db upgrade

echo "✅ Migration complete!"


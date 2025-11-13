#!/bin/sh
# Start script to ensure PORT is numeric and to run gunicorn
# This script will also execute any passed-in command under a shell
# so environment variables like $PORT are expanded if the platform
# supplies a literal command (eg: "gunicorn ... $PORT").

# Default PORT to 5000 if not set or if it contains non-numeric characters
# Check if PORT is empty, equals literal "$PORT", or is not numeric
if [ -z "$PORT" ] || [ "$PORT" = "\$PORT" ] || [ "$PORT" = '$PORT' ]; then
	PORT=5000
elif ! [ "$PORT" -eq "$PORT" ] 2>/dev/null; then
	# PORT is not numeric, default to 5000
	PORT=5000
fi

# If arguments are provided, execute them under a shell so that
# variables like $PORT are expanded (handles Railway startCommand overrides)
if [ "$#" -gt 0 ]; then
	echo "start.sh: executing provided command: $*"
	exec sh -lc "$*"
fi

echo "Starting gunicorn on 0.0.0.0:${PORT}"

exec gunicorn app:app --bind "0.0.0.0:${PORT}"

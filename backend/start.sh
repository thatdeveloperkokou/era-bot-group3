#!/bin/sh
# Start script to ensure PORT is numeric and to run gunicorn

# Default PORT to 5000 if not set
: "${PORT:=5000}"

echo "Starting gunicorn on 0.0.0.0:${PORT}"

exec gunicorn app:app --bind "0.0.0.0:${PORT}"

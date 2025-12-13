#!/bin/bash

echo "Starting QuizFlow with Gunicorn (Production Mode)"
echo "==============================================="

# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')

# Run with Gunicorn
# - workers: 4 (adjust based on CPU cores: 2 * cores + 1)
# - threads: 2 per worker
# - Total capacity: 8 concurrent requests minimum
gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 4 \
    --threads 2 \
    --worker-class sync \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 120 \
    --graceful-timeout 30 \
    --keepalive 5 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    wsgi:app

# For high load (100+ students), use:
# --workers 8 --threads 4
#!/bin/bash
# Ledgerly Bookkeeping — Pelican startup script

cd /home/container
export PATH="/home/container/.local/bin:$PATH"

DB="${DATABASE_PATH:-site.db}"

# First-run: seed database if it doesn't exist
if [ ! -f "$DB" ]; then
    echo "--- First run: seeding database with default content ---"
    python seed.py
    echo "--- Seed complete ---"
fi

PORT="${PORT:-8081}"

echo "--- Starting Ledgerly on port ${PORT} ---"
exec python -m gunicorn \
    --workers 2 \
    --bind "0.0.0.0:${PORT}" \
    --timeout 60 \
    --access-logfile - \
    app:app

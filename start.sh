#!/bin/bash

# Exit the script if any command fails
set -e

# Run migrations if using Alembic
# alembic upgrade head

# Start the app with Gunicorn + Uvicorn worker
exec gunicorn app.main:app \
    --workers 1 \
    --bind 0.0.0.0:10000 \
    -k uvicorn.workers.UvicornWorker

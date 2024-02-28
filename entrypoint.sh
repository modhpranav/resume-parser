#!/bin/sh

# Run Alembic Upgrade to head
echo "Running Alembic Upgrade to head..."
alembic upgrade head

# Start the main process.
echo "Starting the main process..."
exec "$@"

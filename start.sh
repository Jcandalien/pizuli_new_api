#!/bin/bash

# Extract database connection details from DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
    echo "DATABASE_URL is not set. Exiting."
    exit 1
fi

# Parse the DATABASE_URL
USER=$(echo $DATABASE_URL | awk -F[:@] '{print $2}')
PASS=$(echo $DATABASE_URL | awk -F[:@] '{print $3}')
HOST=$(echo $DATABASE_URL | awk -F[@:/] '{print $4}')
PORT=$(echo $DATABASE_URL | awk -F[@:/] '{print $5}')
DB=$(echo $DATABASE_URL | awk -F[@:/] '{print $6}')

echo "Connecting to database..."

# Wait for the database to be ready
until PGPASSWORD=$PASS psql -h $HOST -U $USER -d $DB -c '\q'; do
  echo "Waiting for database to be ready..."
  sleep 2
done

echo "Database is ready."

# Run the FastAPI application
uvicorn pizuli.main:app --host 0.0.0.0 --port 8000
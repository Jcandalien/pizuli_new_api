#!/bin/bash

# Start PostgreSQL service
service postgresql start

# Wait for PostgreSQL to start
until pg_isready; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

# Set a password for the postgres user
su - postgres -c "psql -c \"ALTER USER postgres WITH PASSWORD 'postgres';\""

# Create database and user
su - postgres -c "psql -c \"CREATE DATABASE pizuli;\""
su - postgres -c "psql -c \"CREATE USER jc WITH PASSWORD '76765767';\""
su - postgres -c "psql -c \"ALTER ROLE jc SET client_encoding TO 'utf8';\""
su - postgres -c "psql -c \"ALTER ROLE jc SET default_transaction_isolation TO 'read committed';\""
su - postgres -c "psql -c \"ALTER ROLE jc SET timezone TO 'UTC';\""
su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE pizuli TO jc;\""

# Update the pg_hba.conf file to use md5 authentication for all local connections
sed -i 's/peer/md5/g' /etc/postgresql/*/main/pg_hba.conf
sed -i 's/ident/md5/g' /etc/postgresql/*/main/pg_hba.conf

# Restart PostgreSQL to apply changes
service postgresql restart

# Wait for PostgreSQL to restart
until pg_isready; do
  echo "Waiting for PostgreSQL to restart..."
  sleep 2
done

# Run the FastAPI application
uvicorn main:app --host 0.0.0.0 --port 8000
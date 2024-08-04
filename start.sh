#!/bin/bash

# Start PostgreSQL service
service postgresql start

# Wait for PostgreSQL to start
until pg_isready; do
  echo "Waiting for PostgreSQL to start..."
  sleep 2
done

# Set a password for the postgres user and perform other operations
PGPASSWORD=postgres psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'postgres';"
PGPASSWORD=postgres psql -U postgres -c "CREATE DATABASE pizuli;"
PGPASSWORD=postgres psql -U postgres -c "CREATE USER jc WITH PASSWORD '76765767';"
PGPASSWORD=postgres psql -U postgres -c "ALTER ROLE jc SET client_encoding TO 'utf8';"
PGPASSWORD=postgres psql -U postgres -c "ALTER ROLE jc SET default_transaction_isolation TO 'read committed';"
PGPASSWORD=postgres psql -U postgres -c "ALTER ROLE jc SET timezone TO 'UTC';"
PGPASSWORD=postgres psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE pizuli TO jc;"

# Grant necessary permissions to jc user
PGPASSWORD=postgres psql -U postgres -d pizuli -c "GRANT ALL ON SCHEMA public TO jc;"
PGPASSWORD=postgres psql -U postgres -d pizuli -c "GRANT ALL ON ALL TABLES IN SCHEMA public TO jc;"
PGPASSWORD=postgres psql -U postgres -d pizuli -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO jc;"
PGPASSWORD=postgres psql -U postgres -d pizuli -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO jc;"

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
uvicorn pizuli.main:app --host 0.0.0.0 --port 8000
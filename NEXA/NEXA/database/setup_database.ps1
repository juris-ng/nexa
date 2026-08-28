# NEXA Database Setup Script
# Run this after PostgreSQL is installed and running

# Set variables
 = "nexa_db"
 = "nexa"
 = "nexa"

Write-Host "Creating database ..." -ForegroundColor Cyan

# Create database and user (adjust for your environment)
# psql -U postgres -c "CREATE DATABASE ;"
# psql -U postgres -c "CREATE USER  WITH PASSWORD '';"
# psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE  TO ;"

Write-Host "Running migrations..." -ForegroundColor Cyan

# Apply migration
# psql -U  -d  -f "database\migrations\001_initial_schema.sql"

Write-Host "Database setup complete!" -ForegroundColor Green

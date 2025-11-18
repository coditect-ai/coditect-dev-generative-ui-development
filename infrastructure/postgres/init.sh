#!/bin/bash
# PostgreSQL initialization script
# Runs inside Docker container during first startup
#
# Author: AZ1.AI CODITECT Team
# Project: CODITECT Rollout Master - MEMORY-CONTEXT Consolidation
# Date: 2025-11-17

set -e

echo "=================================================="
echo "CODITECT MEMORY-CONTEXT PostgreSQL Initialization"
echo "=================================================="
echo ""

# Database connection info
PGUSER="${POSTGRES_USER:-coditect_admin}"
PGDB="${POSTGRES_DB:-coditect_memory_context}"

echo "Database: $PGDB"
echo "User: $PGUSER"
echo ""

# Check if database exists
if psql -U "$PGUSER" -lqt | cut -d \| -f 1 | grep -qw "$PGDB"; then
    echo "✓ Database '$PGDB' exists"
else
    echo "✗ Database '$PGDB' does not exist (should be created by postgres image)"
    exit 1
fi

# Connect to database and create extensions
echo ""
echo "Creating PostgreSQL extensions..."
psql -v ON_ERROR_STOP=1 --username "$PGUSER" --dbname "$PGDB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pg_trgm";
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
EOSQL

echo "✓ Extensions created successfully"

# Verify extensions
echo ""
echo "Verifying extensions..."
psql -v ON_ERROR_STOP=1 --username "$PGUSER" --dbname "$PGDB" <<-EOSQL
    SELECT extname FROM pg_extension WHERE extname IN ('uuid-ossp', 'pg_trgm', 'pgcrypto');
EOSQL

echo ""
echo "=================================================="
echo "PostgreSQL initialization complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Schema migration will run automatically from schema-migration.sql"
echo "2. Verify tables created: docker exec -it coditect-postgres psql -U $PGUSER -d $PGDB -c '\dt'"
echo "3. Check metadata: docker exec -it coditect-postgres psql -U $PGUSER -d $PGDB -c 'SELECT * FROM db_metadata;'"
echo ""

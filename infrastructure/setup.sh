#!/bin/bash
# CODITECT MEMORY-CONTEXT Infrastructure Setup
# Automated setup for PostgreSQL, ChromaDB, and Redis
#
# Author: AZ1.AI CODITECT Team
# Project: CODITECT Rollout Master - MEMORY-CONTEXT Consolidation
# Date: 2025-11-17
# Version: 1.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$SCRIPT_DIR/.env"

echo -e "${BLUE}=================================================="
echo "CODITECT MEMORY-CONTEXT Infrastructure Setup"
echo -e "==================================================${NC}"
echo ""

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker is not installed${NC}"
    echo "  Install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo -e "${GREEN}✓ Docker is installed${NC}"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ Docker Compose is not installed${NC}"
    echo "  Install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose is installed${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    echo "  Install Python 3.11+: https://www.python.org/downloads/"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} is installed${NC}"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}✗ pip3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ pip3 is installed${NC}"

echo ""

# Create .env file if it doesn't exist
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${BLUE}Creating .env file with default configuration...${NC}"
    cat > "$ENV_FILE" <<EOF
# CODITECT MEMORY-CONTEXT Environment Configuration
# Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

# PostgreSQL Configuration
POSTGRES_PASSWORD=changeme_dev_only_$(openssl rand -hex 8)
POSTGRES_DB=coditect_memory_context
POSTGRES_USER=coditect_admin

# Redis Configuration
REDIS_PASSWORD=changeme_dev_only_$(openssl rand -hex 8)

# ChromaDB Configuration
CHROMA_TELEMETRY=false

# Context API Configuration (for Day 2-3)
API_KEY=dev_api_key_$(openssl rand -hex 16)
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}  IMPORTANT: Update passwords in $ENV_FILE for production!${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

echo ""

# Install Python dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip3 install -q chromadb sentence-transformers requests psycopg2-binary || {
    echo -e "${YELLOW}Note: Some packages may require system dependencies${NC}"
    echo -e "${YELLOW}  macOS: brew install postgresql${NC}"
    echo -e "${YELLOW}  Ubuntu: sudo apt-get install libpq-dev${NC}"
}
echo -e "${GREEN}✓ Python dependencies installed${NC}"

echo ""

# Stop existing containers (if any)
echo -e "${BLUE}Stopping existing containers...${NC}"
cd "$SCRIPT_DIR"
docker-compose down 2>/dev/null || true
echo -e "${GREEN}✓ Existing containers stopped${NC}"

echo ""

# Start Docker Compose services
echo -e "${BLUE}Starting Docker Compose services...${NC}"
docker-compose up -d

echo ""

# Wait for PostgreSQL to be ready
echo -e "${BLUE}Waiting for PostgreSQL to be ready...${NC}"
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if docker exec coditect-postgres pg_isready -U coditect_admin -d coditect_memory_context &> /dev/null; then
        echo -e "${GREEN}✓ PostgreSQL is ready${NC}"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo -e "  Waiting... (attempt $RETRY_COUNT/$MAX_RETRIES)"
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo -e "${RED}✗ PostgreSQL failed to start after $MAX_RETRIES attempts${NC}"
    docker-compose logs postgres
    exit 1
fi

# Verify PostgreSQL schema
echo ""
echo -e "${BLUE}Verifying PostgreSQL schema...${NC}"
TABLES_COUNT=$(docker exec coditect-postgres psql -U coditect_admin -d coditect_memory_context -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")

if [ "$TABLES_COUNT" -ge 9 ]; then
    echo -e "${GREEN}✓ Schema created successfully ($TABLES_COUNT tables)${NC}"
else
    echo -e "${RED}✗ Schema creation incomplete (only $TABLES_COUNT tables)${NC}"
    exit 1
fi

# Verify PostgreSQL extensions
echo ""
echo -e "${BLUE}Verifying PostgreSQL extensions...${NC}"
EXTENSIONS=$(docker exec coditect-postgres psql -U coditect_admin -d coditect_memory_context -tAc "SELECT extname FROM pg_extension WHERE extname IN ('uuid-ossp', 'pg_trgm', 'pgcrypto') ORDER BY extname;")
echo "$EXTENSIONS" | while read ext; do
    if [ -n "$ext" ]; then
        echo -e "${GREEN}✓ Extension: $ext${NC}"
    fi
done

# Wait for ChromaDB to be ready
echo ""
echo -e "${BLUE}Waiting for ChromaDB to be ready...${NC}"
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s -f http://localhost:8000/api/v1/heartbeat &> /dev/null; then
        echo -e "${GREEN}✓ ChromaDB is ready${NC}"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo -e "  Waiting... (attempt $RETRY_COUNT/$MAX_RETRIES)"
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo -e "${RED}✗ ChromaDB failed to start after $MAX_RETRIES attempts${NC}"
    docker-compose logs chromadb
    exit 1
fi

# Set up ChromaDB collections
echo ""
echo -e "${BLUE}Setting up ChromaDB collections...${NC}"
python3 "$SCRIPT_DIR/chromadb/setup-collections.py" || {
    echo -e "${RED}✗ ChromaDB collection setup failed${NC}"
    exit 1
}

# Wait for Redis to be ready
echo ""
echo -e "${BLUE}Verifying Redis...${NC}"
if docker exec coditect-redis redis-cli ping &> /dev/null; then
    echo -e "${GREEN}✓ Redis is ready${NC}"
else
    echo -e "${YELLOW}⚠ Redis connection test failed (may require password)${NC}"
fi

# Display connection information
echo ""
echo -e "${GREEN}=================================================="
echo "Infrastructure Setup Complete!"
echo -e "==================================================${NC}"
echo ""
echo "Services running:"
echo -e "  ${GREEN}✓${NC} PostgreSQL: localhost:5432"
echo -e "  ${GREEN}✓${NC} ChromaDB:   localhost:8000"
echo -e "  ${GREEN}✓${NC} Redis:      localhost:6379"
echo ""
echo "Database Information:"
echo "  Database: coditect_memory_context"
echo "  User:     coditect_admin"
echo "  Password: (see $ENV_FILE)"
echo ""
echo "Connection Examples:"
echo ""
echo "  # PostgreSQL (psql)"
echo "  docker exec -it coditect-postgres psql -U coditect_admin -d coditect_memory_context"
echo ""
echo "  # List tables"
echo "  docker exec -it coditect-postgres psql -U coditect_admin -d coditect_memory_context -c '\dt'"
echo ""
echo "  # Check metadata"
echo "  docker exec -it coditect-postgres psql -U coditect_admin -d coditect_memory_context -c 'SELECT * FROM db_metadata;'"
echo ""
echo "  # ChromaDB health check"
echo "  curl http://localhost:8000/api/v1/heartbeat"
echo ""
echo "  # View logs"
echo "  docker-compose logs -f postgres"
echo "  docker-compose logs -f chromadb"
echo "  docker-compose logs -f redis"
echo ""
echo "Next Steps:"
echo "  1. Run integration tests: cd infrastructure/tests && python3 test-day1.py"
echo "  2. Begin Context API development (Day 2-3)"
echo "  3. See docs/MEMORY-CONTEXT-WEEK1-IMPLEMENTATION.md for details"
echo ""
echo -e "${YELLOW}NOTE: For production, update passwords in $ENV_FILE${NC}"
echo ""

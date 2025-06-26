#!/bin/bash

# Formulated - Local Test Runner
# This script runs Django tests locally (without Docker)

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🏎️  Formulated Django Test Runner${NC}"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "api/manage.py" ]; then
    echo -e "${RED}Error: This script must be run from the project root directory${NC}"
    exit 1
fi

# Check for help option first
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo -e "${BLUE}Usage: $0 [OPTION]${NC}"
    echo ""
    echo -e "${YELLOW}Options:${NC}"
    echo "  --verbose, -v     Run tests with verbose output"
    echo "  --coverage, -c    Run tests with coverage report"
    echo "  --app, -a <name>  Run tests for specific app"
    echo "  --help, -h        Show this help message"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  $0                # Run all tests"
    echo "  $0 --verbose      # Run with verbose output"
    echo "  $0 --coverage     # Run with coverage"
    echo "  $0 --app teams    # Run tests for teams app"
    echo ""
    echo -e "${BLUE}💡 Note: This script runs tests locally (outside Docker).${NC}"
    echo -e "${BLUE}For the most reliable testing, use Docker instead:${NC}"
    echo -e "   ${GREEN}make test${NC} or ${GREEN}docker-compose exec api python manage.py test${NC}"
    echo ""
    exit 0
fi

# Check Python version
if command -v python3 &> /dev/null; then
    python_cmd="python3"
    python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
elif command -v python &> /dev/null; then
    python_cmd="python"
    python_version=$(python --version 2>&1 | cut -d' ' -f2)
else
    echo -e "${RED}❌ Python not found. Please install Python 3.x${NC}"
    exit 1
fi

echo -e "${BLUE}🐍 Python version: $python_version${NC}"

# Set up environment variables for testing
export DJANGO_SECRET_KEY='test-secret-key-for-local-testing'
export DEBUG='False'
export DATABASE_URL='sqlite:///test_db.sqlite3'
export ALLOWED_HOSTS='localhost,127.0.0.1'
export CORS_ALLOW_ALL_ORIGINS='True'

# Change to API directory
cd api

echo -e "${YELLOW}📦 Installing dependencies...${NC}"

# Try to install dependencies with better error handling
if pip install -r requirements.txt > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies locally${NC}"
    echo ""
    echo -e "${YELLOW}💡 This is likely because:${NC}"
    echo "  • Some dependencies require system-level packages (PostgreSQL dev libraries)"
    echo "  • Your Python environment may not be compatible"
    echo "  • You might need to use a virtual environment"
    echo ""
    echo -e "${BLUE}🐳 Recommended alternatives:${NC}"
    echo "  1. Use Docker (recommended): ${GREEN}make test${NC}"
    echo "  2. Use docker-compose directly: ${GREEN}docker-compose exec api python manage.py test${NC}"
    echo "  3. Set up a virtual environment with system dependencies:"
    echo "     ${GREEN}python -m venv venv && source venv/bin/activate${NC}"
    echo "     ${GREEN}# Install PostgreSQL dev libraries first${NC}"
    echo "     ${GREEN}pip install -r requirements.txt${NC}"
    echo ""
    echo -e "${YELLOW}🔧 For macOS: ${GREEN}brew install postgresql${NC}"
    echo -e "${YELLOW}🔧 For Ubuntu/Debian: ${GREEN}sudo apt-get install libpq-dev python3-dev${NC}"
    echo -e "${YELLOW}🔧 For CentOS/RHEL: ${GREEN}sudo yum install postgresql-devel python3-devel${NC}"
    echo ""
    exit 1
fi

echo -e "${YELLOW}🔧 Creating logs directory...${NC}"
mkdir -p logs

echo -e "${YELLOW}🗄️  Running migrations...${NC}"
if $python_cmd manage.py migrate --verbosity=0; then
    echo -e "${GREEN}✅ Migrations completed successfully${NC}"
else
    echo -e "${RED}❌ Migration failed${NC}"
    echo -e "${YELLOW}💡 This might be due to database connectivity issues${NC}"
    exit 1
fi

echo -e "${YELLOW}🧪 Running Django tests...${NC}"
echo ""

# Run tests with appropriate verbosity
if [ "$1" = "--verbose" ] || [ "$1" = "-v" ]; then
    $python_cmd manage.py test --verbosity=2
elif [ "$1" = "--coverage" ] || [ "$1" = "-c" ]; then
    echo -e "${YELLOW}📊 Running tests with coverage...${NC}"
    if pip install coverage > /dev/null 2>&1; then
        coverage run --source='.' manage.py test
        echo ""
        echo -e "${YELLOW}📈 Coverage Report:${NC}"
        coverage report --skip-covered
        coverage html
        echo -e "${GREEN}📄 HTML coverage report generated in htmlcov/index.html${NC}"
    else
        echo -e "${RED}❌ Failed to install coverage package${NC}"
        echo -e "${YELLOW}Running tests without coverage...${NC}"
        $python_cmd manage.py test --verbosity=1
    fi
elif [ "$1" = "--app" ] || [ "$1" = "-a" ]; then
    if [ -z "$2" ]; then
        echo -e "${RED}Error: Please specify an app name (teams, races, interactions, data_loader)${NC}"
        exit 1
    fi
    echo -e "${YELLOW}🎯 Running tests for app: $2${NC}"
    $python_cmd manage.py test $2 --verbosity=2
else
    $python_cmd manage.py test --verbosity=1
fi

echo ""
echo -e "${GREEN}✅ Tests completed successfully!${NC}"

# Clean up test database
if [ -f "test_db.sqlite3" ]; then
    rm test_db.sqlite3
    echo -e "${YELLOW}🧹 Cleaned up test database${NC}"
fi

echo ""
echo -e "${BLUE}💡 Pro tip: For a more consistent environment, use Docker:${NC}"
echo -e "   ${GREEN}make test${NC} or ${GREEN}docker-compose exec api python manage.py test${NC}" 
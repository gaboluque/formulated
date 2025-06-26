#!/bin/bash

# Formulated - CI Validation Script
# This script validates that all requirements for GitHub Actions CI are met

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Formulated CI Validation${NC}"
echo "============================"
echo ""

# Check if we're in the right directory
if [ ! -f "api/manage.py" ] || [ ! -f ".github/workflows/django-tests.yml" ]; then
    echo -e "${RED}❌ Error: This script must be run from the project root directory${NC}"
    echo -e "${RED}   Make sure both api/manage.py and .github/workflows/django-tests.yml exist${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Checking CI requirements...${NC}"
echo ""

# Check Python requirements file
if [ -f "api/requirements.txt" ]; then
    echo -e "${GREEN}✅ requirements.txt found${NC}"
    echo -e "   📦 Dependencies: $(wc -l < api/requirements.txt) packages"
else
    echo -e "${RED}❌ api/requirements.txt not found${NC}"
    exit 1
fi

# Check Django settings
if [ -f "api/formulated/settings.py" ]; then
    echo -e "${GREEN}✅ Django settings found${NC}"
else
    echo -e "${RED}❌ api/formulated/settings.py not found${NC}"
    exit 1
fi

# Check for test files
test_files=$(find api -name "*test*.py" -type f | wc -l)
if [ "$test_files" -gt 0 ]; then
    echo -e "${GREEN}✅ Test files found: $test_files files${NC}"
else
    echo -e "${YELLOW}⚠️  No test files found${NC}"
fi

# Check GitHub Actions workflow
if [ -f ".github/workflows/django-tests.yml" ]; then
    echo -e "${GREEN}✅ GitHub Actions workflow found${NC}"
    
    # Check if workflow has required elements
    if grep -q "postgres:" ".github/workflows/django-tests.yml"; then
        echo -e "${GREEN}✅ PostgreSQL service configured${NC}"
    else
        echo -e "${RED}❌ PostgreSQL service not found in workflow${NC}"
    fi
    
    if grep -q "python manage.py test" ".github/workflows/django-tests.yml"; then
        echo -e "${GREEN}✅ Test execution configured${NC}"
    else
        echo -e "${RED}❌ Test execution not found in workflow${NC}"
    fi
else
    echo -e "${RED}❌ GitHub Actions workflow not found${NC}"
    exit 1
fi

# Check for required Django apps
echo ""
echo -e "${YELLOW}🔍 Checking Django apps...${NC}"

required_apps=("teams" "races" "interactions" "data_loader")
for app in "${required_apps[@]}"; do
    if [ -d "api/$app" ]; then
        echo -e "${GREEN}✅ $app app found${NC}"
    else
        echo -e "${YELLOW}⚠️  $app app not found${NC}"
    fi
done

# Test local environment setup
echo ""
echo -e "${YELLOW}🧪 Testing local environment...${NC}"

cd api

# Check if Django can be imported and basic commands work
if python -c "import django; print('Django version:', django.VERSION)" 2>/dev/null; then
    echo -e "${GREEN}✅ Django is available${NC}"
else
    echo -e "${RED}❌ Django is not available or cannot be imported${NC}"
    echo -e "${YELLOW}   Run: pip install -r requirements.txt${NC}"
fi

# Test if manage.py works
if python manage.py help > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Django manage.py is working${NC}"
else
    echo -e "${RED}❌ Django manage.py has issues${NC}"
fi

echo ""
echo -e "${BLUE}📊 CI Validation Summary${NC}"
echo "========================"
echo ""

# Final validation
if [ -f "../.github/workflows/django-tests.yml" ] && [ -f "requirements.txt" ] && [ -f "formulated/settings.py" ]; then
    echo -e "${GREEN}🎉 CI setup looks good!${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "1. Commit and push your changes"
    echo "2. GitHub Actions will automatically run tests"
    echo "3. Check the Actions tab in your GitHub repository"
else
    echo -e "${RED}❌ CI setup has issues that need to be resolved${NC}"
    exit 1
fi 
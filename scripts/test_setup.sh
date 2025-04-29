#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "Testing AgroGPT Uganda Setup..."

# Check Python installation
echo -n "Checking Python installation... "
if command -v python3 &>/dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Node.js installation
echo -n "Checking Node.js installation... "
if command -v node &>/dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
    echo "Please install Node.js 16 or higher"
    exit 1
fi

# Check Docker installation
echo -n "Checking Docker installation... "
if command -v docker &>/dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC}"
    echo "Please install Docker"
    exit 1
fi

# Check if .env file exists
echo -n "Checking .env file... "
if [ -f .env ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}MISSING${NC}"
    echo "Creating .env from template..."
    cp .env.example .env
fi

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python scripts/init_db.py

# Download ML models
echo "Downloading ML models..."
python scripts/download_models.py

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Install mobile dependencies
echo "Installing mobile dependencies..."
cd mobile
npm install
cd ..

# Test Docker setup
echo "Testing Docker setup..."
docker-compose build

echo -e "\n${GREEN}Setup completed!${NC}"
echo "You can now start the services with:"
echo "1. Backend: cd backend && uvicorn main:app --reload"
echo "2. Frontend: cd frontend && npm start"
echo "3. Mobile: cd mobile && npm start"
echo "Or use Docker: docker-compose up" 
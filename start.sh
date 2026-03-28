#!/bin/bash

# Academic Search API Startup Script

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "Installing dependencies..."
pip install -r requirements.txt -q

echo ""
echo "========================================"
echo "   Academic Search API"
echo "========================================"
echo ""
echo "API will be available at:"
echo "  - Base URL: http://localhost:8111"
echo "  - Docs:     http://localhost:8111/docs"
echo "  - ReDoc:    http://localhost:8111/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8111

#!/bin/bash
# AQL Builder startup script

# Activate virtual environment
source venv/bin/activate

# Run the app
echo "Starting AQL Builder Web UI..."
echo "Open http://localhost:5000 in your browser"
python3 app.py

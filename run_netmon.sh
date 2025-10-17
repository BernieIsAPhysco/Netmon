#!/bin/bash
clear
echo "=============================="
echo "   Launching NetMon Tool"
echo "=============================="
echo

# Optional: activate venv
# source venv/bin/activate

# Check python
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not found. Please install it first."
    exit 1
fi

# Install dependencies if missing
echo "Installing required packages..."
pip3 install -r requirements.txt >/dev/null 2>&1

echo "Starting NetMon..."
echo "(Press Ctrl+C to stop)"
echo

sudo python3 main.py

echo
echo "=============================="
echo "NetMon stopped."

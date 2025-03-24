#!/bin/bash

# Exit on error
set -e

# Navigate to the script's directory
cd "$(dirname "$0")" || exit 1

# Ensure the script is executable
chmod +x ./oac.py

# Check if Python 3.7, 3.8, or 3.9 are installed, and select the first available
runPython() {
    if command -v $1 >/dev/null 2>&1; then
        echo "Running oac.py with $1"
        $1 ./oac.py
        exit 0
    fi
}

# Run Python with different versions (in order)
runPython python3.9
runPython python3.8
runPython python3.7

# If no Python version is found, report an error
echo "Error: No suitable Python version found. Please install Python 3.7, 3.8, or 3.9."
exit 1

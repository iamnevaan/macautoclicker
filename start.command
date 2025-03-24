#!/bin/sh

# Navigate to the directory where the script is located
cd "$(dirname "$0")" || exit

# Ensure the virtual environment is activated (if needed)
if [ -d "bin" ]; then
    if [ -f "./bin/activate" ]; then
        source ./bin/activate
        echo "Virtual environment activated."
    else
        echo "Virtual environment not found."
    fi
fi

# Run Python script using an available Python version
if command -v python3.9 >/dev/null 2>&1; then
    python3.9 oac.py
elif command -v python3.8 >/dev/null 2>&1; then
    python3.8 oac.py
elif command -v python3.7 >/dev/null 2>&1; then
    python3.7 oac.py
else
    echo "No suitable Python version found!"
    exit 1
fi

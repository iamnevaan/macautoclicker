#!/bin/bash

# Ensure the script runs in the correct directory
cd "$(dirname "$0")" || exit

# Activate virtual environment if it exists
if [ -d "bin" ]; then
    if [ -f "./bin/activate" ]; then
        source ./bin/activate
        echo "Virtual environment activated."
    else
        echo "Virtual environment not found."
    fi
else
    echo "Virtual environment directory 'bin' does not exist."
fi

# Check if Python versions are available and run the script
runPython() {
    if command -v $1 >/dev/null 2>&1; then
        echo "Running Python with $1"
        $1 oac.py
        exit 0  # Exit successfully after running the script
    else
        echo "Python version $1 not found!"
    fi
}

# Try different Python versions
runPython python3.9
runPython python3.8
runPython python3.7

# If no version is found, exit with an error
echo "No valid Python versions found!"
exit 1

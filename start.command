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
else
    echo "Virtual environment directory 'bin' does not exist."
fi

# Check if Python versions are available and run the script
runPython() {
    if command -v $1 >/dev/null 2>&1; then
        echo "Running Python with $1"
        $1 oac.py
    else
        echo "Python version $1 not found!"
    fi
}

# Run Python with different versions if available
runPython python3.9
runPython python3.8
runPython python3.7

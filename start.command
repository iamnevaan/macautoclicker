#!/bin/sh
# Attempt to kill Python processes if the user has permissions
kill_process() {
  if [ "$(id -u)" -eq 0 ]; then
    # Only attempt to kill processes if run by root (admin privileges)
    pkill -9 Python
    pkill -9 Python3
    pkill -9 Python3.9
    pkill -9 Python3.8
    pkill -9 Python3.7
  else
    echo "Insufficient privileges to kill processes. You need admin access."
  fi
}

# Get system information
chip=$(arch)
os_ver=$(sw_vers -productVersion)

python_ver="3.9"
if [ $chip = 'i386' ]; then
    if echo -e "$os_ver \n10.15.0" | sort -V | tail -n1 | grep -Fq "10.15.0"; then
        python_ver="3.7"
        printf "Correct python ver: 3.7\n"
    elif echo -e "$os_ver \n12.0.0" | sort -V | tail -n1 | grep -Fq "12.0.0"; then
        python_ver="3.8"
        printf "Correct python ver: 3.8\n"
    fi
fi

cd "$(dirname "$0")"

# Check if virtual environment directory exists before activating
if [ -d "bin" ]; then
   if [ -f "./bin/activate" ]; then
       source ./bin/activate
       printf "Activating virtual environment...\n"
   else
       echo "Virtual environment not found in 'bin'."
   fi
else
   echo "Virtual environment directory 'bin' does not exist."
fi

# Function to run Python script
runPython() {
    if command -v $1 >/dev/null 2>&1; then
        $1 oac.py
    else
        echo "Python version $1 not found."
    fi
}

# Navigate to source directory
cd src || { echo "Source directory not found"; exit 1; }

# Run different versions of Python if they exist
runPython python3.7
runPython python3.8
runPython python3.9

# Kill Python processes if the script has sufficient privileges
kill_process

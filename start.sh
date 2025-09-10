#!/bin/bash

# Step 1: Environment Check
if [ -d "python" ]; then
    echo "Python is already installed."
else
    echo "Installing Python..."
    # Download python installer if it does not exist
    if [ ! -f "python_installer.zip" ]; then
        echo "Downloading Python installer..."
        curl -L https://github.com/europeanplaice/distribute-embeddable-python/releases/download/v3.11.0/python-3.11.0-embed-amd64.zip -o python_installer.zip
    fi

    # Step 2: Unzipping
    unzip python_installer.zip
    echo "Python installation complete."
fi

# Step 3: Virtual Environment Creation
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    ./python/python -m venv venv
    echo "Virtual environment created."
fi

# Step 4: Install Core Dependencies
echo "Installing dependencies..."
./venv/bin/pip install -r requirements.txt

# Step 5: Launch the application
echo "Starting the application..."
./venv/bin/python app.py

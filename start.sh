#!/bin/bash

# Download python installer if it does not exist
if [ ! -f "python_installer.zip" ]; then
    echo "Downloading Python installer..."
    curl -L https://github.com/europeanplaice/distribute-embeddable-python/releases/download/v3.11.0/python-3.11.0-embed-amd64.zip -o python_installer.zip
fi

# Step 2: Unzipping
unzip python_installer.zip
echo "Python installation complete."

ls -lR

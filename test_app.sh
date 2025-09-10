#!/bin/bash

# Create a virtual environment using the pre-installed python
python3 -m venv venv

# Install dependencies
./venv/bin/pip install -r requirements.txt

# Run the application in test mode
./venv/bin/python app.py --test "https://github.com/realpython/flask-boilerplate"

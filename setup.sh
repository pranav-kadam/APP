#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "Installing required system packages..."
sudo apt install -y python3 python3-venv python3-pip ffmpeg

echo "Creating and activating a virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install Flask werkzeug

echo "Setup complete! To start your app, run:"
echo "source venv/bin/activate && python app.py"

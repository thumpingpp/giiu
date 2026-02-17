#!/bin/bash
set -e

# Permissions check fix
if [ "$EUID" -ne 0 ]; then
    SUDO="sudo"
else
    SUDO=""
fi

CHROMEDRIVER_VERSION="133.0.6943.126" # Latest stable version check karein

# Dependencies
$SUDO apt-get update && $SUDO apt-get install -y curl unzip wget

echo "⬇ Downloading ChromeDriver..."
curl -L -o chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip"

echo "📂 Extracting..."
unzip -o chromedriver.zip
chmod +x chromedriver-linux64/chromedriver
$SUDO mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver

rm -rf chromedriver-linux64 chromedriver.zip

echo "⬇ Installing Google Chrome..."
wget -q -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$SUDO apt-get install -y ./google-chrome.deb

echo "✅ Success!"


set -e

if [ "$EUID" -ne 0 ] && ! command -v sudo &>/dev/null; then
    echo "❌ Must run as root or have sudo access."
    exit 1
fi

CHROMEDRIVER_VERSION="138.0.7204.183"
PLATFORM="linux64"

# Dependencies
if [ "$EUID" -eq 0 ]; then
    apt update && apt install -y curl unzip
else
    sudo apt update && sudo apt install -y curl unzip
fi

ZIP_URL="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip"

echo "⬇ Downloading ChromeDriver ${CHROMEDRIVER_VERSION}..."
curl -L -o chromedriver.zip "$ZIP_URL"

# Validate
if [ ! -s chromedriver.zip ] || [ $(stat -c%s chromedriver.zip) -lt 1000 ]; then
    echo "❌ Download failed or file too small. Check URL/version."
    rm -f chromedriver.zip
    exit 1
fi

echo "📂 Extracting..."
unzip -o chromedriver.zip -d tmp_chromedriver
chmod +x tmp_chromedriver/chromedriver-linux64/chromedriver

if [ "$EUID" -eq 0 ]; then
    mv tmp_chromedriver/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
else
    sudo mv tmp_chromedriver/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
fi

rm -rf tmp_chromedriver chromedriver.zip

echo "⬇ Installing Google Chrome..."
wget -q -O google-chrome-stable_current_amd64.deb \
    https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

if [ "$EUID" -eq 0 ]; then
    apt install -y ./google-chrome-stable_current_amd64.deb
else
    sudo apt install -y ./google-chrome-stable_current_amd64.deb
fi

echo "✅ Installed ChromeDriver:"
chromedriver --version
echo "✅ Installed Google Chrome:"
google-chrome --version
echo "🎉 Installation completed successfully!"

set -o errexit

# Install system dependencies
apt-get update
apt-get install -y tesseract-ocr

# Then proceed with your Python package installation
pip install -r requirements.txt
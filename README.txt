# Steps to run lowes_scraper

# Create new virtual environment
cd /opt/python/venv/
virtualenv lowes_venv

# Activate virtual environment
source /opt/python/venv/lowes_venv/bin/activate

# Install requirement from requirements.txt file
cd ~/lowes_scraper
pip install -r requirement.txt

# Run script based on target
# Scrape all products and their details
python run.py -target=product

# Scrape all store details from store directory
python run.py -target=store


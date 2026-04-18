import requests
import json
import time
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import os

from scripts import RTrader
from scripts import GridStrategy
from scripts import build_sample_grid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():

    # API Configuration
    API_KEY = "YOUR_API_KEY"  # Get from R StocksTrader -> Settings -> API Integration
    ACCOUNT_ID = "YOUR_ACCOUNT_ID"  # Your RoboMarkets account ID
    BASE_URL = "https://api.stockstrader.com/api/v1/"
    
    # Create example grid file for testing
    build_sample_grid()
    
    # Initialize API client
    client = RTrader(
        api_key=API_KEY,
        account_id=ACCOUNT_ID,
        base_url=BASE_URL
    )
   
    # Initialize grid strategy
    strategy = GridStrategy(client, grid_file="grid.txt")
        

if __name__ == "__main__":
    main()
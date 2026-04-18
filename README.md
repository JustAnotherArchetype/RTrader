# RTrader
A Python-based grid trading bot for [RoboMarkets API](https://api-doc.stockstrader.com/)

## Description
This trading bot takes in the user configured grid of orders to be automatically maintained and replaced when executed at take profit levels.

## How to use
1. Add your API credentials to the `main.py` or `main.ipynb`

2. Ensure Python is installed

3. Ensure the `requests` module is installed

4. Generate your `.json` grid

5. Run either with jupyter notebook or simple
   ```bash
   python main.py
   ```

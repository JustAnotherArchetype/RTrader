def main():

    # API Configuration
    API_KEY = "YOUR_API_KEY"  # Get from R StocksTrader -> Settings -> API Integration
    ACCOUNT_ID = "YOUR_ACCOUNT_ID"  # Your RoboMarkets account ID
    BASE_URL = "https://api.stockstrader.com/api/v1/"
    
    # Create example grid file for testing
    create_example_grid_file()
    
    # Initialize API client
    client = RoboMarketsGridTrader(
        api_key=API_KEY,
        account_id=ACCOUNT_ID,
        base_url=BASE_URL
    )
   
    # Initialize grid strategy
    strategy = GridStrategy(client, grid_file="grid.txt")
    
    # Parse command line arguments
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--sync":
            # One-time sync only
            strategy.sync_orders()
        elif sys.argv[1] == "--monitor":
            # Continuous monitoring with default 60 second interval
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            strategy.run_monitoring_loop(check_interval=interval)
        else:
            print("Usage:")
            print("  python robomarkets_grid.py --sync        # One-time order sync")
            print("  python robomarkets_grid.py --monitor [N] # Monitor every N seconds")
    else:
        # Default: one-time sync
        strategy.sync_orders()

if __name__ == "__main__":
    main()
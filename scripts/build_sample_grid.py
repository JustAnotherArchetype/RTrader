import json

def build_sample_grid():
    """
    Create an example grid.txt file with sample limit orders
    """
    example_orders = [
        {'ticker': 'NVDA.nq', 'side': 'buy', 'type': 'limit', 'volume': 10, 'price': 150.00, 'take_profit': 155.00, 'stop_loss': 148.00},
        {'ticker': 'NVDA.nq', 'side': 'buy', 'type': 'limit', 'volume': 10, 'price': 151.00, 'take_profit': 155.00, 'stop_loss': 148.00},
        {'ticker': 'NVDA.nq', 'side': 'buy', 'type': 'limit', 'volume': 10, 'price': 152.00, 'take_profit': 155.00, 'stop_loss': 148.00},
        {'ticker': 'NVDA.nq', 'side': 'buy', 'type': 'limit', 'volume': 10, 'price': 153.00, 'take_profit': 155.00, 'stop_loss': 148.00},
        {'ticker': 'NVDA.nq', 'side': 'buy', 'type': 'limit', 'volume': 10, 'price': 154.00, 'take_profit': 155.00, 'stop_loss': 148.00}
    ]
    
    with open('grid.txt', 'w') as f:
        json.dump(example_orders, f, indent=2)
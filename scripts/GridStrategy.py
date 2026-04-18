import json
import time
import logging
from typing import Dict, List, Optional, Any
import os

from scripts import RTrader

class GridStrategy():
    def __init__(self, api_client: RTrader, grid_file: str = 'grid.txt'):
        """
        Grid based strategy controller for the trader

        param api_client: instance of the trader class
        param grid_file: path to the grid configuration
        """
        self.api_client = api_client
        self.grid_file = grid_file
        
        self.active_order_ids = []
        self.active_order_keys = []
        self.filled_order_keys = []

        self.grid_orders = self.load_grid()
        self.grid_keys = [self.get_order_key(order) for order in self.grid_orders]

    
    @staticmethod
    def get_order_key(order: Dict) -> str:
        """
        Create local key for order tracking
        
        param order: order information
        :returns: local order key
        """
        return f"{order['ticker']}_{order['side']}_{order['price']:.2f}"


    def load_grid(self) -> List[Dict]:
        """
        Load grid configuration from the specified file

        :returns: list of orders in configuration
        """
        if not os.path.exists(self.grid_file):
            logger.error(f"Grid file {self.grid_file} not found")
            return []
        
        orders = []
        
        try:
            with open(self.grid_file, 'r') as f:
                content = f.read().strip()
                
                #JSON format required
                orders = json.loads(content)
                        
            logger.info(f"Loaded {len(orders)} orders from {self.grid_file}")
            self.grid_orders = orders
            return orders
            
        except Exception as e:
            logger.error(f"Error loading grid file: {e}")
            return []


    def sync_state(self) -> bool:
        """
        Synchronize the server orders with local state

        :returns: True on success, False on failure
        """
        logger.info("Synchronizing strategy state with server")
        try:
            # Get current active a orders from the server
            active_orders = self.api_client.get_orders(status='active')
            filled_orders = self.api_client.get_orders(status='filled')
    
            # Write active ids and keys
            self.active_order_keys = [self.get_order_key(order) for order in active_orders]
            self.active_order_ids = [order['id'] for order in active_orders]
    
            # Write keys of filled orders
            self.filled_order_keys = [self.get_order_key(order) for order in filled_orders]
            
            return True

        except Exception as e:
            logger.error(f"`State synchronization error: {e}")
            return False
        

    def sync_orders(self) -> bool:
        """
        Synchronize the server orders with local grid configuration

        :returns: True on success, False on failure
        """
        logger.info("Synchronizing grid with server")
        
        if not self.grid_orders:
            logger.warning("No grid orders to process")
            return False

        if not self.sync_state():
            logger.error("Unable to syncronize local state")
            return False
        
        # Track which grid orders need to be placed
        orders_to_place = []
        
        for order in self.grid_orders:
            order_key = self.get_order_key(order)
            
            if order_key not in self.active_order_keys or order_key not in self.filled_order_keys:
                logger.info(f"Missing order detected: {order['ticker']} {order['side']} at {order['price']:.2f}")
                orders_to_place.append(order)
            else:
                logger.debug(f"Order already exists or has been filled: {order_key}")
        
        # Place missing orders
        if orders_to_place:
            logger.info(f"Placing {len(orders_to_place)} missing orders...")
            
            for order in orders_to_place:
                response = self.api_client.place_order(order)
                if response:
                    # Store order_id if returned
                    if 'order_id' in response['data']:
                        self.active_order_ids.append(response['data']['order_id'])
                else:
                    logger.error(f"Failed to place order: {order}")
                    
                # Small delay to avoid server side limits
                time.sleep(0.5)
        else:
            logger.info("All grid orders are already placed")
        
        logger.info("Grid synchronization completed")
        
        return True


    def remove_all_orders(self):
        """
        Remove all active orders based on local state

        :returns: True on success, False on failure
        """
        try:
            for order_id in self.active_order_ids:
                self.api_client.cancel_order(order_id)
            return True
            
        except Exception as e:
            logger.error(f"Error removing orders: {e}")
            return False
            

    def execute(self, check_interval: int = 30):
        """
        Execute strategy
        
        param check_interval: interval in seconds between checks
        """
        logger.info(f"Starting grid routine, interval: {check_interval} seconds)")
        
        try:
            while True:
                # Check for filled orders, add missing
                if not self.sync_orders():
                    logger.info("Unable to execute routine")
                    break
                
                # Wait before next check
                logger.info(f"Waiting {check_interval} seconds until next check...")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Monitoring loop error: {e}")
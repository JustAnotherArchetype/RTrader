import requests
import logging

from typing import Dict, List, Optional

logger = logging.getLogger()

class RTrader:
    def __init__(self, api_key: str, account_id: str,
                 base_url: str = 'https://api.stockstrader.com/api/v1/'):
        """
        API client class with basic functionality

        param api_key: personal API key
        param account_id: id of target account
        param base_url: prefix url for all endpoints
        """
        
        self.api_key = api_key
        self.account_id = account_id
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {api_key}',
                        'Content-Type': "application/json",
                        'Accept': "application/json"}

        
    def _make_request(self, method: str, endpoint: str, extra_headers: Dict = {}, data: Dict = {}):
        """
        Make request to the server

        param method: GET, POST or DELETE
        param endpoint: target endpoint of the schema
        param extra_headers: additional headers to add to the request
        param data: necessary data for the request

        :returns: json of the response
        """
        url = f'{self.base_url}{endpoint}'

        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers | extra_headers, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers | extra_headers, data=data, timeout=10)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=self.headers | extra_headers, timeout=10)
            else:
                logger.error(f"Unsupported HTTP method: {method}; currently only GET, POST, DELETE implemented")
                return None
                
            response.raise_for_status()
            return response.json() if response.content else None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"Response: {e.response.text}")
            return None


    def get_orders(self, status: str = 'active') -> List[Dict]:
        """
        Receive list of orders
        
        param sta
        :returns: list of all active limit orders
        """
        logger.info("Fetching open orders...")
        response = self._make_request("GET", f"accounts/{self.account_id}/orders", extra_headers={'status': status})
        
        if response and 'data' in response:
            
            # Filter for limit orders only
            limit_orders = [order for order in response['data'] if order['type'] == 'limit']
            logger.info(f"Found {len(limit_orders)} open limit orders")
            
            return limit_orders
            
        return []

    
    def place_order(self, order_params: Dict) -> Optional[Dict]:
        """
        Place an order

        param order_params: a dict of order parameters
        :returns: None if required parametrs missing else responce from _make_request
        """
        # Required parameters
        required_fields = ['ticker', 'side', 'type', 'volume', 'price']
        
        for field in required_fields:
            if field not in order_params.keys():
                logger.error(f"Missing required order parameter: {field}")
                return None
        
        # Prepare order structure
        order_data = {
            'ticker': order_params['ticker'],
            'side': order_params['side'],
            'type': order_params['type'],
            'price': order_params['price'],
            'volume': str(order_params['volume'])
        }
        
        # Add optional parameters
        if 'take_profit' in order_params:
            order_data['take_profit'] = str(order_params['take_profit'])
        if 'stop_loss' in order_params:
            order_data['stop_loss'] = str(order_params['stop_loss'])
            
        logger.info(f"Placing limit order: {order_data['side']} {order_data['volume']} "
                   f"{order_data['ticker']} @ {order_data['price']}")
        
        response = self._make_request('POST', f"accounts/{self.account_id}/orders", data=order_data)
        
        if response:
            logger.info(f"Order placed successfully: {response.get('data', 'unknown').get('order_id', 'unknown')}")
        else:
            logger.error("Failed to place order")
            
        return response

    
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel order

        param order_id: id of the order to cancel
        :returns: True on success, False on failure
        """
        
        logger.info(f"Cancelling order: {order_id}")
        response = self._make_request('DELETE', f"accounts/{self.account_id}/orders/{order_id}")
        
        if response is not None:
            logger.info(f"Order {order_id} cancelled successfully")
            return True
        else:
            logger.error(f"Failed to cancel order {order_id}")
            return False
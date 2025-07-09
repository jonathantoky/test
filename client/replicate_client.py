"""
Replicate API Client

This module provides authentication and client configuration for Replicate API.
"""

import os
import requests
from typing import Optional, Dict, Any
import json


class ReplicateClient:
    """Client for interacting with Replicate API"""
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize Replicate client
        
        Args:
            api_token: Replicate API token. If not provided, will look for REPLICATE_API_TOKEN env var
        """
        self.api_token = api_token or os.getenv('REPLICATE_API_TOKEN')
        if not self.api_token:
            raise ValueError("Replicate API token is required. Set REPLICATE_API_TOKEN environment variable or pass api_token parameter.")
        
        self.base_url = "https://api.replicate.com/v1"
        self.headers = {
            "Authorization": f"Token {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> requests.Response:
        """Make HTTP request to Replicate API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        if method.upper() == 'GET':
            response = requests.get(url, headers=self.headers, params=params)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=self.headers, json=data, params=params)
        elif method.upper() == 'PATCH':
            response = requests.patch(url, headers=self.headers, json=data, params=params)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=self.headers, params=params)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        return response
    
    def get_models(self, cursor: Optional[str] = None, limit: Optional[int] = 20) -> Dict[str, Any]:
        """Get list of available models"""
        params = {}
        if cursor:
            params['cursor'] = cursor
        if limit:
            params['limit'] = limit
        
        response = self._make_request('GET', '/models', params=params)
        response.raise_for_status()
        return response.json()
    
    def get_model(self, owner: str, name: str) -> Dict[str, Any]:
        """Get specific model details"""
        response = self._make_request('GET', f'/models/{owner}/{name}')
        response.raise_for_status()
        return response.json()
    
    def create_model(self, name: str, visibility: str, hardware: str, **kwargs) -> Dict[str, Any]:
        """Create a new model"""
        data = {
            "name": name,
            "visibility": visibility,
            "hardware": hardware,
            **kwargs
        }
        response = self._make_request('POST', '/models', data=data)
        response.raise_for_status()
        return response.json()
    
    def update_model(self, owner: str, name: str, **kwargs) -> Dict[str, Any]:
        """Update an existing model"""
        data = {k: v for k, v in kwargs.items() if v is not None}
        response = self._make_request('PATCH', f'/models/{owner}/{name}', data=data)
        response.raise_for_status()
        return response.json()
    
    def delete_model(self, owner: str, name: str) -> bool:
        """Delete a model"""
        response = self._make_request('DELETE', f'/models/{owner}/{name}')
        return response.status_code == 204
    
    def create_prediction(self, version: str, input_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Create a new prediction"""
        data = {
            "version": version,
            "input": input_data,
            **kwargs
        }
        response = self._make_request('POST', '/predictions', data=data)
        response.raise_for_status()
        return response.json()
    
    def get_prediction(self, prediction_id: str) -> Dict[str, Any]:
        """Get prediction details"""
        response = self._make_request('GET', f'/predictions/{prediction_id}')
        response.raise_for_status()
        return response.json()
    
    def cancel_prediction(self, prediction_id: str) -> Dict[str, Any]:
        """Cancel a prediction"""
        response = self._make_request('POST', f'/predictions/{prediction_id}/cancel')
        response.raise_for_status()
        return response.json()
    
    def get_predictions(self, cursor: Optional[str] = None, limit: Optional[int] = 20) -> Dict[str, Any]:
        """Get list of predictions"""
        params = {}
        if cursor:
            params['cursor'] = cursor
        if limit:
            params['limit'] = limit
        
        response = self._make_request('GET', '/predictions', params=params)
        response.raise_for_status()
        return response.json()
    
    def wait_for_prediction(self, prediction_id: str, timeout: int = 300, poll_interval: int = 5) -> Dict[str, Any]:
        """Wait for prediction to complete"""
        import time
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            prediction = self.get_prediction(prediction_id)
            status = prediction.get('status')
            
            if status in ['succeeded', 'failed', 'canceled']:
                return prediction
            
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Prediction {prediction_id} did not complete within {timeout} seconds")


def create_replicate_client(api_token: Optional[str] = None) -> ReplicateClient:
    """Factory function to create Replicate client"""
    return ReplicateClient(api_token)


# Authentication utilities
def validate_api_token(api_token: str) -> bool:
    """Validate Replicate API token"""
    try:
        client = ReplicateClient(api_token)
        client.get_models(limit=1)
        return True
    except Exception:
        return False


def get_api_token_from_env() -> Optional[str]:
    """Get API token from environment variables"""
    return os.getenv('REPLICATE_API_TOKEN')


def set_api_token_env(api_token: str) -> None:
    """Set API token in environment variables"""
    os.environ['REPLICATE_API_TOKEN'] = api_token


# Configuration utilities
class ReplicateConfig:
    """Configuration manager for Replicate settings"""
    
    def __init__(self):
        self.api_token = get_api_token_from_env()
        self.default_timeout = 300
        self.default_poll_interval = 5
        self.default_model = "meta/codellama-34b-instruct"
    
    def set_api_token(self, api_token: str) -> None:
        """Set API token"""
        self.api_token = api_token
        set_api_token_env(api_token)
    
    def get_client(self) -> ReplicateClient:
        """Get configured client"""
        return ReplicateClient(self.api_token)
    
    def validate_config(self) -> bool:
        """Validate current configuration"""
        if not self.api_token:
            return False
        return validate_api_token(self.api_token)


# Global configuration instance
config = ReplicateConfig()


def setup_replicate_auth(api_token: str) -> bool:
    """Setup Replicate authentication"""
    try:
        config.set_api_token(api_token)
        return config.validate_config()
    except Exception:
        return False
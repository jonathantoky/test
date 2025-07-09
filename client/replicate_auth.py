"""
Replicate Authentication Client

This module provides authentication utilities for the Replicate API,
including token validation, client initialization, and error handling.
"""

import os
import requests
import replicate
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ReplicateConfig:
    """Configuration class for Replicate client"""
    api_token: str
    base_url: str = "https://api.replicate.com/v1"
    timeout: int = 30
    max_retries: int = 3


class ReplicateAuthError(Exception):
    """Custom exception for Replicate authentication errors"""
    pass


class ReplicateClient:
    """
    Replicate API client with authentication and error handling
    """
    
    def __init__(self, config: ReplicateConfig):
        self.config = config
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Replicate client with authentication"""
        try:
            self.client = replicate.Client(api_token=self.config.api_token)
        except Exception as e:
            raise ReplicateAuthError(f"Failed to initialize Replicate client: {str(e)}")
    
    def validate_token(self) -> bool:
        """
        Validate the Replicate API token
        
        Returns:
            bool: True if token is valid, False otherwise
        """
        try:
            # Try to list models to validate token
            list(self.client.models.list())
            return True
        except Exception:
            return False
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information
        
        Returns:
            dict: Account information
        """
        try:
            # Make a simple API call to get account info
            response = requests.get(
                f"{self.config.base_url}/account",
                headers={"Authorization": f"Token {self.config.api_token}"},
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise ReplicateAuthError(f"Failed to get account info: {str(e)}")
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection to Replicate API
        
        Returns:
            dict: Connection test results
        """
        try:
            # Test basic connectivity
            models = list(self.client.models.list())
            model_count = len(models)
            
            return {
                "status": "success",
                "message": "Connection successful",
                "model_count": model_count,
                "api_version": "v1"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Connection failed: {str(e)}",
                "model_count": 0,
                "api_version": "unknown"
            }


def create_replicate_client(api_token: str, **kwargs) -> ReplicateClient:
    """
    Create a Replicate client with the provided token
    
    Args:
        api_token (str): Replicate API token
        **kwargs: Additional configuration options
    
    Returns:
        ReplicateClient: Configured client instance
    """
    config = ReplicateConfig(api_token=api_token, **kwargs)
    return ReplicateClient(config)


def get_token_from_env() -> Optional[str]:
    """
    Get Replicate API token from environment variables
    
    Returns:
        str: API token if found, None otherwise
    """
    return os.getenv("REPLICATE_API_TOKEN")


def validate_replicate_token(token: str) -> bool:
    """
    Validate a Replicate API token
    
    Args:
        token (str): API token to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        client = create_replicate_client(token)
        return client.validate_token()
    except Exception:
        return False


class ReplicateTokenManager:
    """
    Token manager for handling multiple Replicate tokens
    """
    
    def __init__(self):
        self.tokens = {}
        self.clients = {}
    
    def add_token(self, name: str, token: str) -> bool:
        """
        Add a token to the manager
        
        Args:
            name (str): Token identifier
            token (str): API token
        
        Returns:
            bool: True if token is valid and added, False otherwise
        """
        if validate_replicate_token(token):
            self.tokens[name] = token
            self.clients[name] = create_replicate_client(token)
            return True
        return False
    
    def get_client(self, name: str) -> Optional[ReplicateClient]:
        """
        Get a client by name
        
        Args:
            name (str): Token identifier
        
        Returns:
            ReplicateClient: Client instance if found, None otherwise
        """
        return self.clients.get(name)
    
    def remove_token(self, name: str) -> bool:
        """
        Remove a token from the manager
        
        Args:
            name (str): Token identifier
        
        Returns:
            bool: True if removed, False if not found
        """
        if name in self.tokens:
            del self.tokens[name]
            del self.clients[name]
            return True
        return False
    
    def list_tokens(self) -> list:
        """
        List all token names
        
        Returns:
            list: List of token names
        """
        return list(self.tokens.keys())
    
    def test_all_tokens(self) -> Dict[str, Dict[str, Any]]:
        """
        Test all managed tokens
        
        Returns:
            dict: Test results for all tokens
        """
        results = {}
        for name, client in self.clients.items():
            results[name] = client.test_connection()
        return results


# Authentication decorators
def require_replicate_auth(func):
    """
    Decorator to require Replicate authentication
    """
    def wrapper(*args, **kwargs):
        token = kwargs.get('token') or get_token_from_env()
        if not token:
            raise ReplicateAuthError("No Replicate API token provided")
        
        if not validate_replicate_token(token):
            raise ReplicateAuthError("Invalid Replicate API token")
        
        return func(*args, **kwargs)
    return wrapper


# Example usage and testing
if __name__ == "__main__":
    # Test token validation
    token = get_token_from_env()
    if token:
        print("Testing Replicate authentication...")
        
        # Create client
        client = create_replicate_client(token)
        
        # Test connection
        result = client.test_connection()
        print(f"Connection test: {result}")
        
        # Get account info
        try:
            account_info = client.get_account_info()
            print(f"Account info: {account_info}")
        except Exception as e:
            print(f"Could not get account info: {e}")
        
        # Test token manager
        manager = ReplicateTokenManager()
        if manager.add_token("default", token):
            print("Token added to manager successfully")
            
            # Test all tokens
            test_results = manager.test_all_tokens()
            print(f"Token test results: {test_results}")
        else:
            print("Failed to add token to manager")
    else:
        print("No REPLICATE_API_TOKEN environment variable found")
        print("Please set your Replicate API token in the environment:")
        print("export REPLICATE_API_TOKEN=your_token_here")
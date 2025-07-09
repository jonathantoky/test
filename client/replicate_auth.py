"""
Replicate Authentication Client

This module provides authentication and client setup for Replicate API integration.
"""

import os
import requests
from typing import Optional, Dict, Any
import json


class ReplicateAuthClient:
    """
    Client for handling Replicate API authentication and basic operations.
    """
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize the Replicate authentication client.
        
        Args:
            api_token (str, optional): Replicate API token. If not provided,
                                     will look for REPLICATE_API_TOKEN environment variable.
        """
        self.api_token = api_token or os.getenv('REPLICATE_API_TOKEN')
        if not self.api_token:
            raise ValueError("Replicate API token is required. Set REPLICATE_API_TOKEN environment variable or pass api_token parameter.")
        
        self.base_url = "https://api.replicate.com/v1"
        self.headers = {
            "Authorization": f"Token {self.api_token}",
            "Content-Type": "application/json",
            "User-Agent": "SwiftaskAgent/1.0"
        }
    
    def validate_token(self) -> bool:
        """
        Validate the API token by making a test request.
        
        Returns:
            bool: True if token is valid, False otherwise.
        """
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                params={"limit": 1}
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information for the authenticated user.
        
        Returns:
            dict: Account information or error details.
        """
        try:
            response = requests.get(
                f"{self.base_url}/account",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection to Replicate API.
        
        Returns:
            dict: Connection test results.
        """
        try:
            # Test basic connectivity
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                params={"limit": 1},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "message": "Successfully connected to Replicate API",
                    "models_available": len(data.get("results", [])),
                    "rate_limit_remaining": response.headers.get("X-RateLimit-Remaining"),
                    "rate_limit_reset": response.headers.get("X-RateLimit-Reset")
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Connection timeout - Replicate API is not responding"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Connection error - Unable to reach Replicate API"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def get_model_info(self, model_owner: str, model_name: str) -> Dict[str, Any]:
        """
        Get information about a specific model.
        
        Args:
            model_owner (str): Owner of the model
            model_name (str): Name of the model
            
        Returns:
            dict: Model information or error details.
        """
        try:
            response = requests.get(
                f"{self.base_url}/models/{model_owner}/{model_name}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_prediction(self, model_version: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a prediction using a model.
        
        Args:
            model_version (str): Model version ID
            input_data (dict): Input parameters for the model
            
        Returns:
            dict: Prediction creation result.
        """
        try:
            payload = {
                "version": model_version,
                "input": input_data
            }
            
            response = requests.post(
                f"{self.base_url}/predictions",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 201:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_prediction(self, prediction_id: str) -> Dict[str, Any]:
        """
        Get the status and results of a prediction.
        
        Args:
            prediction_id (str): ID of the prediction
            
        Returns:
            dict: Prediction details.
        """
        try:
            response = requests.get(
                f"{self.base_url}/predictions/{prediction_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def list_popular_models(self, limit: int = 10) -> Dict[str, Any]:
        """
        List popular models on Replicate.
        
        Args:
            limit (int): Number of models to return
            
        Returns:
            dict: List of popular models.
        """
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                params={"limit": limit}
            )
            
            if response.status_code == 200:
                data = response.json()
                models = data.get("results", [])
                
                # Sort by run count (popularity)
                popular_models = sorted(
                    models,
                    key=lambda x: x.get("run_count", 0),
                    reverse=True
                )
                
                return {
                    "success": True,
                    "data": popular_models[:limit],
                    "total_available": len(models)
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


def create_replicate_client(api_token: Optional[str] = None) -> ReplicateAuthClient:
    """
    Factory function to create a Replicate authentication client.
    
    Args:
        api_token (str, optional): Replicate API token
        
    Returns:
        ReplicateAuthClient: Configured client instance
    """
    return ReplicateAuthClient(api_token)


def validate_replicate_token(api_token: str) -> bool:
    """
    Validate a Replicate API token.
    
    Args:
        api_token (str): The API token to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        client = ReplicateAuthClient(api_token)
        return client.validate_token()
    except Exception:
        return False


# Example usage and testing
if __name__ == "__main__":
    # Example usage
    try:
        # Initialize client
        client = create_replicate_client()
        
        # Test connection
        print("Testing connection...")
        result = client.test_connection()
        print(f"Connection test: {result}")
        
        # Get account info
        print("\nGetting account info...")
        account_info = client.get_account_info()
        print(f"Account info: {account_info}")
        
        # List popular models
        print("\nListing popular models...")
        popular_models = client.list_popular_models(5)
        if popular_models["success"]:
            print(f"Found {len(popular_models['data'])} popular models:")
            for model in popular_models["data"]:
                print(f"  - {model['owner']}/{model['name']} (runs: {model.get('run_count', 0)})")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set REPLICATE_API_TOKEN environment variable or pass api_token parameter")
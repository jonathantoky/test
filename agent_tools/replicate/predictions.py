from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import json
import requests
import time
from .. import extract_token_from_data


# Create Prediction Tool
class CreatePredictionInput(BaseModel):
    model_version: str = Field(description="Model version ID or model owner/name:version format")
    input_data: Dict[str, Any] = Field(description="Input parameters for the model")
    webhook: Optional[str] = Field(None, description="Webhook URL to receive prediction results")
    webhook_events_filter: Optional[List[str]] = Field(None, description="List of webhook events to filter")


def create_replicate_prediction(name, description, token):
    """Creates a new prediction with a Replicate model."""
    tool_description = description or "Create a new prediction using a Replicate model"

    def create_prediction(
        model_version: str, 
        input_data: Dict[str, Any], 
        webhook: Optional[str] = None,
        webhook_events_filter: Optional[List[str]] = None
    ) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Prepare headers
            headers = {
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json"
            }
            
            # Prepare request body
            body = {
                "version": model_version,
                "input": input_data
            }
            
            if webhook:
                body["webhook"] = webhook
                
            if webhook_events_filter:
                body["webhook_events_filter"] = webhook_events_filter
            
            # Make API request
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=body
            )
            
            if response.status_code == 201:
                prediction = response.json()
                
                result = f"Prediction created successfully!\n"
                result += f"Prediction ID: {prediction.get('id')}\n"
                result += f"Status: {prediction.get('status')}\n"
                result += f"Model: {prediction.get('model')}\n"
                result += f"Version: {prediction.get('version')}\n"
                result += f"Created at: {prediction.get('created_at')}\n"
                
                if prediction.get('urls'):
                    result += f"Get URL: {prediction['urls'].get('get')}\n"
                    result += f"Cancel URL: {prediction['urls'].get('cancel')}\n"
                
                # If prediction is completed, show output
                if prediction.get('output'):
                    result += f"Output: {json.dumps(prediction['output'], indent=2)}\n"
                
                return result
            else:
                return f"Error creating prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to create prediction: {str(e)}"

    return StructuredTool.from_function(
        func=create_prediction,
        name=name,
        description=tool_description,
        args_schema=CreatePredictionInput,
        return_direct=True
    )


# Get Prediction Tool
class GetPredictionInput(BaseModel):
    prediction_id: str = Field(description="ID of the prediction to retrieve")


def get_replicate_prediction(name, description, token):
    """Gets status and results of a prediction."""
    tool_description = description or "Get the status and results of a Replicate prediction"

    def get_prediction(prediction_id: str) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Prepare headers
            headers = {
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json"
            }
            
            # Make API request
            response = requests.get(
                f"https://api.replicate.com/v1/predictions/{prediction_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                prediction = response.json()
                
                result = f"Prediction Details:\n"
                result += f"ID: {prediction.get('id')}\n"
                result += f"Status: {prediction.get('status')}\n"
                result += f"Model: {prediction.get('model')}\n"
                result += f"Version: {prediction.get('version')}\n"
                result += f"Created at: {prediction.get('created_at')}\n"
                result += f"Started at: {prediction.get('started_at', 'N/A')}\n"
                result += f"Completed at: {prediction.get('completed_at', 'N/A')}\n"
                
                # Show input
                if prediction.get('input'):
                    result += f"Input: {json.dumps(prediction['input'], indent=2)}\n"
                
                # Show output if available
                if prediction.get('output'):
                    result += f"Output: {json.dumps(prediction['output'], indent=2)}\n"
                
                # Show error if any
                if prediction.get('error'):
                    result += f"Error: {prediction['error']}\n"
                
                # Show logs if available
                if prediction.get('logs'):
                    result += f"Logs: {prediction['logs']}\n"
                
                # Show metrics if available
                if prediction.get('metrics'):
                    result += f"Metrics: {json.dumps(prediction['metrics'], indent=2)}\n"
                
                return result
            else:
                return f"Error getting prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to get prediction: {str(e)}"

    return StructuredTool.from_function(
        func=get_prediction,
        name=name,
        description=tool_description,
        args_schema=GetPredictionInput,
        return_direct=True
    )


# Cancel Prediction Tool
class CancelPredictionInput(BaseModel):
    prediction_id: str = Field(description="ID of the prediction to cancel")


def cancel_replicate_prediction(name, description, token):
    """Cancels a running prediction."""
    tool_description = description or "Cancel a running Replicate prediction"

    def cancel_prediction(prediction_id: str) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Prepare headers
            headers = {
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json"
            }
            
            # Make API request
            response = requests.post(
                f"https://api.replicate.com/v1/predictions/{prediction_id}/cancel",
                headers=headers
            )
            
            if response.status_code == 200:
                prediction = response.json()
                
                result = f"Prediction cancelled successfully!\n"
                result += f"ID: {prediction.get('id')}\n"
                result += f"Status: {prediction.get('status')}\n"
                result += f"Model: {prediction.get('model')}\n"
                
                return result
            else:
                return f"Error cancelling prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to cancel prediction: {str(e)}"

    return StructuredTool.from_function(
        func=cancel_prediction,
        name=name,
        description=tool_description,
        args_schema=CancelPredictionInput,
        return_direct=True
    )


# List Predictions Tool
class ListPredictionsInput(BaseModel):
    cursor: Optional[str] = Field(None, description="Pagination cursor")
    limit: Optional[int] = Field(20, description="Number of predictions to return")


def list_replicate_predictions(name, description, token):
    """Lists your predictions."""
    tool_description = description or "List your Replicate predictions"

    def list_predictions(cursor: Optional[str] = None, limit: Optional[int] = 20) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Prepare headers
            headers = {
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json"
            }
            
            # Prepare query parameters
            params = {"limit": min(limit, 100)}
            if cursor:
                params["cursor"] = cursor
            
            # Make API request
            response = requests.get(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                predictions = data.get("results", [])
                
                result = f"Found {len(predictions)} predictions:\n\n"
                for prediction in predictions:
                    result += f"• ID: {prediction.get('id')}\n"
                    result += f"  Status: {prediction.get('status')}\n"
                    result += f"  Model: {prediction.get('model')}\n"
                    result += f"  Created: {prediction.get('created_at')}\n"
                    result += f"  Completed: {prediction.get('completed_at', 'N/A')}\n\n"
                
                if data.get("next"):
                    result += f"Next cursor: {data.get('next')}\n"
                
                return result
            else:
                return f"Error listing predictions: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to list predictions: {str(e)}"

    return StructuredTool.from_function(
        func=list_predictions,
        name=name,
        description=tool_description,
        args_schema=ListPredictionsInput,
        return_direct=True
    )


# Get Prediction Logs Tool
class GetPredictionLogsInput(BaseModel):
    prediction_id: str = Field(description="ID of the prediction to get logs for")


def get_prediction_logs(name, description, token):
    """Gets logs from a prediction."""
    tool_description = description or "Get logs from a Replicate prediction"

    def get_logs(prediction_id: str) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Prepare headers
            headers = {
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json"
            }
            
            # Make API request
            response = requests.get(
                f"https://api.replicate.com/v1/predictions/{prediction_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                prediction = response.json()
                
                result = f"Logs for Prediction {prediction_id}:\n"
                result += f"Status: {prediction.get('status')}\n"
                result += f"Model: {prediction.get('model')}\n\n"
                
                # Show logs if available
                if prediction.get('logs'):
                    result += f"Logs:\n{prediction['logs']}\n"
                else:
                    result += "No logs available yet.\n"
                
                # Show error if any
                if prediction.get('error'):
                    result += f"Error: {prediction['error']}\n"
                
                return result
            else:
                return f"Error getting logs: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to get logs: {str(e)}"

    return StructuredTool.from_function(
        func=get_logs,
        name=name,
        description=tool_description,
        args_schema=GetPredictionLogsInput,
        return_direct=True
    )
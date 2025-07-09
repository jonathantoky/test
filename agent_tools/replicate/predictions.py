"""
Replicate Prediction Management Tools

This module provides tools for creating, managing, and monitoring Replicate predictions.
"""

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import requests
import json
import time


def extract_token_from_data(token_data):
    """Extract token from various token formats"""
    if isinstance(token_data, str):
        return token_data
    elif isinstance(token_data, dict):
        return token_data.get('token') or token_data.get('access_token') or token_data.get('api_key')
    return str(token_data)


class CreatePredictionInput(BaseModel):
    model_version: str = Field(description="Version ID of the model to run")
    input_data: Dict[str, Any] = Field(description="Input parameters for the model")
    webhook: Optional[str] = Field(None, description="Webhook URL for completion notification")
    webhook_events_filter: Optional[List[str]] = Field(None, description="List of events to send to webhook")


def create_replicate_prediction(name, description, token):
    """Create a new Replicate prediction"""
    tool_description = description or "Create a new prediction using a Replicate model"

    def create_prediction(
        model_version: str,
        input_data: Dict[str, Any],
        webhook: Optional[str] = None,
        webhook_events_filter: Optional[List[str]] = None
    ) -> str:
        try:
            access_token = extract_token_from_data(token)
            
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "version": model_version,
                "input": input_data
            }
            
            if webhook:
                data["webhook"] = webhook
            if webhook_events_filter:
                data["webhook_events_filter"] = webhook_events_filter
            
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                prediction = response.json()
                result = f"Prediction created successfully!\n"
                result += f"ID: {prediction.get('id')}\n"
                result += f"Status: {prediction.get('status')}\n"
                result += f"Model: {prediction.get('model')}\n"
                result += f"Version: {prediction.get('version')}\n"
                result += f"Created: {prediction.get('created_at')}\n"
                result += f"URLs: {prediction.get('urls', {})}\n"
                
                if prediction.get('status') == 'succeeded':
                    result += f"Output: {prediction.get('output')}\n"
                elif prediction.get('status') == 'failed':
                    result += f"Error: {prediction.get('error')}\n"
                
                return result
            else:
                return f"Error creating prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to create Replicate prediction: {str(e)}"

    return StructuredTool.from_function(
        func=create_prediction,
        name=name,
        description=tool_description,
        args_schema=CreatePredictionInput,
        return_direct=True
    )


class GetPredictionInput(BaseModel):
    prediction_id: str = Field(description="ID of the prediction to retrieve")


def get_replicate_prediction(name, description, token):
    """Get details of a specific Replicate prediction"""
    tool_description = description or "Get the status and results of a specific Replicate prediction"

    def get_prediction(prediction_id: str) -> str:
        try:
            access_token = extract_token_from_data(token)
            
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
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
                result += f"Created: {prediction.get('created_at')}\n"
                result += f"Started: {prediction.get('started_at', 'Not started')}\n"
                result += f"Completed: {prediction.get('completed_at', 'Not completed')}\n"
                
                # Input parameters
                input_data = prediction.get('input', {})
                if input_data:
                    result += f"Input: {json.dumps(input_data, indent=2)}\n"
                
                # Output or error
                if prediction.get('status') == 'succeeded':
                    output = prediction.get('output')
                    if output:
                        result += f"Output: {json.dumps(output, indent=2)}\n"
                elif prediction.get('status') == 'failed':
                    error = prediction.get('error')
                    if error:
                        result += f"Error: {error}\n"
                
                # Logs
                logs = prediction.get('logs')
                if logs:
                    result += f"Logs: {logs}\n"
                
                # Metrics
                metrics = prediction.get('metrics')
                if metrics:
                    result += f"Metrics: {json.dumps(metrics, indent=2)}\n"
                
                return result
            else:
                return f"Error getting prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to get Replicate prediction: {str(e)}"

    return StructuredTool.from_function(
        func=get_prediction,
        name=name,
        description=tool_description,
        args_schema=GetPredictionInput,
        return_direct=True
    )


class CancelPredictionInput(BaseModel):
    prediction_id: str = Field(description="ID of the prediction to cancel")


def cancel_replicate_prediction(name, description, token):
    """Cancel a running Replicate prediction"""
    tool_description = description or "Cancel a running Replicate prediction"

    def cancel_prediction(prediction_id: str) -> str:
        try:
            access_token = extract_token_from_data(token)
            
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"https://api.replicate.com/v1/predictions/{prediction_id}/cancel",
                headers=headers
            )
            
            if response.status_code == 200:
                prediction = response.json()
                result = f"Prediction cancelled successfully!\n"
                result += f"ID: {prediction.get('id')}\n"
                result += f"Status: {prediction.get('status')}\n"
                result += f"Cancelled at: {prediction.get('completed_at', 'Now')}\n"
                return result
            else:
                return f"Error cancelling prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to cancel Replicate prediction: {str(e)}"

    return StructuredTool.from_function(
        func=cancel_prediction,
        name=name,
        description=tool_description,
        args_schema=CancelPredictionInput,
        return_direct=True
    )


class ListPredictionsInput(BaseModel):
    cursor: Optional[str] = Field(None, description="Pagination cursor for next page")
    limit: Optional[int] = Field(20, description="Number of predictions to return")


def list_replicate_predictions(name, description, token):
    """List Replicate predictions"""
    tool_description = description or "List your Replicate predictions with pagination support"

    def list_predictions(cursor: Optional[str] = None, limit: Optional[int] = 20) -> str:
        try:
            access_token = extract_token_from_data(token)
            
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
            params = {}
            if cursor:
                params['cursor'] = cursor
            if limit:
                params['limit'] = limit
            
            response = requests.get(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                predictions = data.get('results', [])
                
                result = f"Found {len(predictions)} predictions:\n\n"
                for prediction in predictions:
                    result += f"• ID: {prediction.get('id')}\n"
                    result += f"  Status: {prediction.get('status')}\n"
                    result += f"  Model: {prediction.get('model')}\n"
                    result += f"  Created: {prediction.get('created_at')}\n"
                    result += f"  Completed: {prediction.get('completed_at', 'Not completed')}\n"
                    
                    if prediction.get('status') == 'failed':
                        result += f"  Error: {prediction.get('error', 'Unknown error')}\n"
                    
                    result += "\n"
                
                if data.get('next'):
                    result += f"Next page cursor: {data.get('next')}\n"
                
                return result
            else:
                return f"Error listing predictions: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to list Replicate predictions: {str(e)}"

    return StructuredTool.from_function(
        func=list_predictions,
        name=name,
        description=tool_description,
        args_schema=ListPredictionsInput,
        return_direct=True
    )


class StreamPredictionInput(BaseModel):
    prediction_id: str = Field(description="ID of the prediction to stream")
    timeout: Optional[int] = Field(300, description="Timeout in seconds (default: 300)")
    poll_interval: Optional[int] = Field(5, description="Polling interval in seconds (default: 5)")


def stream_replicate_prediction(name, description, token):
    """Stream a Replicate prediction until completion"""
    tool_description = description or "Stream a Replicate prediction and wait for completion"

    def stream_prediction(
        prediction_id: str,
        timeout: Optional[int] = 300,
        poll_interval: Optional[int] = 5
    ) -> str:
        try:
            access_token = extract_token_from_data(token)
            
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
            start_time = time.time()
            result = f"Streaming prediction {prediction_id}...\n\n"
            
            while True:
                # Check timeout
                if time.time() - start_time > timeout:
                    result += f"Timeout reached after {timeout} seconds\n"
                    break
                
                # Get prediction status
                response = requests.get(
                    f"https://api.replicate.com/v1/predictions/{prediction_id}",
                    headers=headers
                )
                
                if response.status_code != 200:
                    result += f"Error getting prediction: {response.status_code} - {response.text}\n"
                    break
                
                prediction = response.json()
                status = prediction.get('status')
                
                result += f"Status: {status} at {prediction.get('created_at', 'unknown time')}\n"
                
                # Check if completed
                if status in ['succeeded', 'failed', 'canceled']:
                    result += f"\nFinal Status: {status}\n"
                    
                    if status == 'succeeded':
                        output = prediction.get('output')
                        if output:
                            result += f"Output: {json.dumps(output, indent=2)}\n"
                    elif status == 'failed':
                        error = prediction.get('error')
                        if error:
                            result += f"Error: {error}\n"
                    
                    # Add logs if available
                    logs = prediction.get('logs')
                    if logs:
                        result += f"Logs: {logs}\n"
                    
                    # Add metrics if available
                    metrics = prediction.get('metrics')
                    if metrics:
                        result += f"Metrics: {json.dumps(metrics, indent=2)}\n"
                    
                    break
                
                # Wait before next poll
                time.sleep(poll_interval)
            
            return result
                
        except Exception as e:
            return f"Failed to stream Replicate prediction: {str(e)}"

    return StructuredTool.from_function(
        func=stream_prediction,
        name=name,
        description=tool_description,
        args_schema=StreamPredictionInput,
        return_direct=True
    )
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import json
import replicate
from .. import extract_token_from_data


# Create Prediction Tool
class CreatePredictionInput(BaseModel):
    version: str = Field(description="Version ID of the model to run")
    input: Dict[str, Any] = Field(description="Input parameters for the prediction")
    webhook: Optional[str] = Field(None, description="Webhook URL to receive prediction updates")
    webhook_events_filter: Optional[List[str]] = Field(None, description="List of webhook events to filter")


def create_prediction_replicate(name, description, token):
    """Creates a new prediction on Replicate."""
    tool_description = description or "Create a new prediction on Replicate"

    def create_prediction(version: str, input: Dict[str, Any], webhook: Optional[str] = None,
                         webhook_events_filter: Optional[List[str]] = None) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # Create prediction
            prediction = client.predictions.create(
                version=version,
                input=input,
                webhook=webhook,
                webhook_events_filter=webhook_events_filter
            )
            
            # Format response
            prediction_info = {
                "id": prediction.id,
                "version": prediction.version,
                "status": prediction.status,
                "input": prediction.input,
                "output": prediction.output,
                "error": prediction.error,
                "logs": prediction.logs,
                "metrics": prediction.metrics,
                "created_at": str(prediction.created_at) if prediction.created_at else None,
                "started_at": str(prediction.started_at) if prediction.started_at else None,
                "completed_at": str(prediction.completed_at) if prediction.completed_at else None,
                "urls": prediction.urls
            }
            
            return json.dumps(prediction_info, indent=2)
            
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
    id: str = Field(description="ID of the prediction to retrieve")


def get_prediction_replicate(name, description, token):
    """Gets details of a specific prediction on Replicate."""
    tool_description = description or "Get details of a specific prediction on Replicate"

    def get_prediction(id: str) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # Get prediction
            prediction = client.predictions.get(id)
            
            # Format response
            prediction_info = {
                "id": prediction.id,
                "version": prediction.version,
                "status": prediction.status,
                "input": prediction.input,
                "output": prediction.output,
                "error": prediction.error,
                "logs": prediction.logs,
                "metrics": prediction.metrics,
                "created_at": str(prediction.created_at) if prediction.created_at else None,
                "started_at": str(prediction.started_at) if prediction.started_at else None,
                "completed_at": str(prediction.completed_at) if prediction.completed_at else None,
                "urls": prediction.urls
            }
            
            return json.dumps(prediction_info, indent=2)
            
        except Exception as e:
            return f"Failed to get prediction: {str(e)}"

    return StructuredTool.from_function(
        func=get_prediction,
        name=name,
        description=tool_description,
        args_schema=GetPredictionInput,
        return_direct=True
    )


# List Predictions Tool
class ListPredictionsInput(BaseModel):
    cursor: Optional[str] = Field(None, description="Cursor for pagination")
    limit: Optional[int] = Field(20, description="Number of predictions to return (max 100)")


def list_predictions_replicate(name, description, token):
    """Lists predictions on Replicate."""
    tool_description = description or "List predictions on Replicate"

    def list_predictions(cursor: Optional[str] = None, limit: Optional[int] = 20) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # List predictions
            predictions = client.predictions.list()
            
            # Format response
            predictions_list = []
            count = 0
            for prediction in predictions:
                if count >= limit:
                    break
                predictions_list.append({
                    "id": prediction.id,
                    "version": prediction.version,
                    "status": prediction.status,
                    "input": prediction.input,
                    "output": prediction.output,
                    "error": prediction.error,
                    "logs": prediction.logs,
                    "metrics": prediction.metrics,
                    "created_at": str(prediction.created_at) if prediction.created_at else None,
                    "started_at": str(prediction.started_at) if prediction.started_at else None,
                    "completed_at": str(prediction.completed_at) if prediction.completed_at else None,
                    "urls": prediction.urls
                })
                count += 1
            
            return json.dumps(predictions_list, indent=2)
            
        except Exception as e:
            return f"Failed to list predictions: {str(e)}"

    return StructuredTool.from_function(
        func=list_predictions,
        name=name,
        description=tool_description,
        args_schema=ListPredictionsInput,
        return_direct=True
    )


# Cancel Prediction Tool
class CancelPredictionInput(BaseModel):
    id: str = Field(description="ID of the prediction to cancel")


def cancel_prediction_replicate(name, description, token):
    """Cancels a prediction on Replicate."""
    tool_description = description or "Cancel a prediction on Replicate"

    def cancel_prediction(id: str) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # Cancel prediction
            prediction = client.predictions.cancel(id)
            
            # Format response
            prediction_info = {
                "id": prediction.id,
                "version": prediction.version,
                "status": prediction.status,
                "input": prediction.input,
                "output": prediction.output,
                "error": prediction.error,
                "logs": prediction.logs,
                "metrics": prediction.metrics,
                "created_at": str(prediction.created_at) if prediction.created_at else None,
                "started_at": str(prediction.started_at) if prediction.started_at else None,
                "completed_at": str(prediction.completed_at) if prediction.completed_at else None,
                "urls": prediction.urls
            }
            
            return f"Prediction cancelled successfully: {json.dumps(prediction_info, indent=2)}"
            
        except Exception as e:
            return f"Failed to cancel prediction: {str(e)}"

    return StructuredTool.from_function(
        func=cancel_prediction,
        name=name,
        description=tool_description,
        args_schema=CancelPredictionInput,
        return_direct=True
    )


# Run Prediction Tool (Simplified interface)
class RunPredictionInput(BaseModel):
    model: str = Field(description="Model name in format 'owner/name' or 'owner/name:version'")
    input: Dict[str, Any] = Field(description="Input parameters for the prediction")
    wait: Optional[bool] = Field(True, description="Whether to wait for the prediction to complete")


def run_prediction_replicate(name, description, token):
    """Runs a prediction on Replicate using the simplified interface."""
    tool_description = description or "Run a prediction on Replicate using the simplified interface"

    def run_prediction(model: str, input: Dict[str, Any], wait: Optional[bool] = True) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # Run prediction
            if wait:
                output = client.run(model, input=input)
                return json.dumps({"output": output}, indent=2)
            else:
                prediction = client.predictions.create(
                    model=model,
                    input=input
                )
                prediction_info = {
                    "id": prediction.id,
                    "version": prediction.version,
                    "status": prediction.status,
                    "input": prediction.input,
                    "output": prediction.output,
                    "error": prediction.error,
                    "logs": prediction.logs,
                    "metrics": prediction.metrics,
                    "created_at": str(prediction.created_at) if prediction.created_at else None,
                    "started_at": str(prediction.started_at) if prediction.started_at else None,
                    "completed_at": str(prediction.completed_at) if prediction.completed_at else None,
                    "urls": prediction.urls
                }
                return json.dumps(prediction_info, indent=2)
            
        except Exception as e:
            return f"Failed to run prediction: {str(e)}"

    return StructuredTool.from_function(
        func=run_prediction,
        name=name,
        description=tool_description,
        args_schema=RunPredictionInput,
        return_direct=True
    )
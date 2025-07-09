"""
Replicate Model Management Tools

This module provides tools for managing Replicate models including listing,
creating, updating, and deleting models.
"""

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import requests
import json


def extract_token_from_data(token_data):
    """Extract token from various token formats"""
    if isinstance(token_data, str):
        return token_data
    elif isinstance(token_data, dict):
        return token_data.get('token') or token_data.get('access_token') or token_data.get('api_key')
    return str(token_data)


class ListModelsInput(BaseModel):
    cursor: Optional[str] = Field(None, description="Pagination cursor for next page")
    limit: Optional[int] = Field(20, description="Number of models to return (max 100)")


def list_replicate_models(name, description, token):
    """List available Replicate models"""
    tool_description = description or "List available Replicate models with pagination support"

    def list_models(cursor: Optional[str] = None, limit: Optional[int] = 20) -> str:
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
                params['limit'] = min(limit, 100)  # API limit is 100
            
            response = requests.get(
                "https://api.replicate.com/v1/models",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('results', [])
                
                result = f"Found {len(models)} models:\n\n"
                for model in models:
                    result += f"• {model.get('owner')}/{model.get('name')}\n"
                    result += f"  Description: {model.get('description', 'No description')}\n"
                    result += f"  Visibility: {model.get('visibility', 'unknown')}\n"
                    result += f"  URL: {model.get('url', 'N/A')}\n\n"
                
                if data.get('next'):
                    result += f"Next page cursor: {data.get('next')}\n"
                
                return result
            else:
                return f"Error listing models: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to list Replicate models: {str(e)}"

    return StructuredTool.from_function(
        func=list_models,
        name=name,
        description=tool_description,
        args_schema=ListModelsInput,
        return_direct=True
    )


class GetModelInput(BaseModel):
    model_owner: str = Field(description="Owner of the model")
    model_name: str = Field(description="Name of the model")


def get_replicate_model(name, description, token):
    """Get details of a specific Replicate model"""
    tool_description = description or "Get detailed information about a specific Replicate model"

    def get_model(model_owner: str, model_name: str) -> str:
        try:
            access_token = extract_token_from_data(token)
            
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"https://api.replicate.com/v1/models/{model_owner}/{model_name}",
                headers=headers
            )
            
            if response.status_code == 200:
                model = response.json()
                
                result = f"Model: {model.get('owner')}/{model.get('name')}\n"
                result += f"Description: {model.get('description', 'No description')}\n"
                result += f"Visibility: {model.get('visibility', 'unknown')}\n"
                result += f"GitHub URL: {model.get('github_url', 'N/A')}\n"
                result += f"Paper URL: {model.get('paper_url', 'N/A')}\n"
                result += f"License URL: {model.get('license_url', 'N/A')}\n"
                result += f"Cover Image: {model.get('cover_image_url', 'N/A')}\n"
                result += f"Default Example: {model.get('default_example', 'N/A')}\n"
                
                # Latest version info
                latest_version = model.get('latest_version')
                if latest_version:
                    result += f"\nLatest Version:\n"
                    result += f"  ID: {latest_version.get('id')}\n"
                    result += f"  Created: {latest_version.get('created_at')}\n"
                    result += f"  COG Version: {latest_version.get('cog_version')}\n"
                    
                    # Schema info
                    schema = latest_version.get('openapi_schema', {})
                    if schema:
                        components = schema.get('components', {})
                        if components:
                            result += f"  Input Schema: Available\n"
                            result += f"  Output Schema: Available\n"
                
                return result
            else:
                return f"Error getting model: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to get Replicate model: {str(e)}"

    return StructuredTool.from_function(
        func=get_model,
        name=name,
        description=tool_description,
        args_schema=GetModelInput,
        return_direct=True
    )


class CreateModelInput(BaseModel):
    model_name: str = Field(description="Name of the model to create")
    visibility: str = Field(description="Visibility of the model (public or private)")
    hardware: str = Field(description="Hardware to run the model on (e.g., 'gpu-t4', 'gpu-a40-small')")
    description: Optional[str] = Field(None, description="Description of the model")
    github_url: Optional[str] = Field(None, description="GitHub repository URL")
    paper_url: Optional[str] = Field(None, description="Paper URL")
    license_url: Optional[str] = Field(None, description="License URL")
    cover_image_url: Optional[str] = Field(None, description="Cover image URL")


def create_replicate_model(name, description, token):
    """Create a new Replicate model"""
    tool_description = description or "Create a new Replicate model with specified configuration"

    def create_model(
        model_name: str,
        visibility: str,
        hardware: str,
        description: Optional[str] = None,
        github_url: Optional[str] = None,
        paper_url: Optional[str] = None,
        license_url: Optional[str] = None,
        cover_image_url: Optional[str] = None
    ) -> str:
        try:
            access_token = extract_token_from_data(token)
            
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "name": model_name,
                "visibility": visibility,
                "hardware": hardware
            }
            
            if description:
                data["description"] = description
            if github_url:
                data["github_url"] = github_url
            if paper_url:
                data["paper_url"] = paper_url
            if license_url:
                data["license_url"] = license_url
            if cover_image_url:
                data["cover_image_url"] = cover_image_url
            
            response = requests.post(
                "https://api.replicate.com/v1/models",
                headers=headers,
                json=data
            )
            
            if response.status_code == 201:
                model = response.json()
                result = f"Model created successfully!\n"
                result += f"Name: {model.get('owner')}/{model.get('name')}\n"
                result += f"URL: {model.get('url')}\n"
                result += f"Visibility: {model.get('visibility')}\n"
                return result
            else:
                return f"Error creating model: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to create Replicate model: {str(e)}"

    return StructuredTool.from_function(
        func=create_model,
        name=name,
        description=tool_description,
        args_schema=CreateModelInput,
        return_direct=True
    )


class UpdateModelInput(BaseModel):
    model_owner: str = Field(description="Owner of the model")
    model_name: str = Field(description="Name of the model")
    visibility: Optional[str] = Field(None, description="New visibility (public or private)")
    hardware: Optional[str] = Field(None, description="New hardware configuration")
    description: Optional[str] = Field(None, description="New description")
    github_url: Optional[str] = Field(None, description="New GitHub URL")
    paper_url: Optional[str] = Field(None, description="New paper URL")
    license_url: Optional[str] = Field(None, description="New license URL")
    cover_image_url: Optional[str] = Field(None, description="New cover image URL")


def update_replicate_model(name, description, token):
    """Update an existing Replicate model"""
    tool_description = description or "Update an existing Replicate model's configuration"

    def update_model(
        model_owner: str,
        model_name: str,
        visibility: Optional[str] = None,
        hardware: Optional[str] = None,
        description: Optional[str] = None,
        github_url: Optional[str] = None,
        paper_url: Optional[str] = None,
        license_url: Optional[str] = None,
        cover_image_url: Optional[str] = None
    ) -> str:
        try:
            access_token = extract_token_from_data(token)
            
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
            data = {}
            if visibility:
                data["visibility"] = visibility
            if hardware:
                data["hardware"] = hardware
            if description:
                data["description"] = description
            if github_url:
                data["github_url"] = github_url
            if paper_url:
                data["paper_url"] = paper_url
            if license_url:
                data["license_url"] = license_url
            if cover_image_url:
                data["cover_image_url"] = cover_image_url
            
            if not data:
                return "No updates provided. Please specify at least one field to update."
            
            response = requests.patch(
                f"https://api.replicate.com/v1/models/{model_owner}/{model_name}",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                model = response.json()
                result = f"Model updated successfully!\n"
                result += f"Name: {model.get('owner')}/{model.get('name')}\n"
                result += f"URL: {model.get('url')}\n"
                result += f"Visibility: {model.get('visibility')}\n"
                return result
            else:
                return f"Error updating model: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to update Replicate model: {str(e)}"

    return StructuredTool.from_function(
        func=update_model,
        name=name,
        description=tool_description,
        args_schema=UpdateModelInput,
        return_direct=True
    )


class DeleteModelInput(BaseModel):
    model_owner: str = Field(description="Owner of the model")
    model_name: str = Field(description="Name of the model to delete")


def delete_replicate_model(name, description, token):
    """Delete a Replicate model"""
    tool_description = description or "Delete a Replicate model permanently"

    def delete_model(model_owner: str, model_name: str) -> str:
        try:
            access_token = extract_token_from_data(token)
            
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.delete(
                f"https://api.replicate.com/v1/models/{model_owner}/{model_name}",
                headers=headers
            )
            
            if response.status_code == 204:
                return f"Model {model_owner}/{model_name} deleted successfully!"
            else:
                return f"Error deleting model: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to delete Replicate model: {str(e)}"

    return StructuredTool.from_function(
        func=delete_model,
        name=name,
        description=tool_description,
        args_schema=DeleteModelInput,
        return_direct=True
    )
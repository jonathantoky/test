from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json
import requests
from .. import extract_token_from_data


# List Models Tool
class ListModelsInput(BaseModel):
    cursor: Optional[str] = Field(None, description="Pagination cursor for listing models")
    limit: Optional[int] = Field(20, description="Number of models to return (max 100)")


def list_replicate_models(name, description, token):
    """Lists available models on Replicate."""
    tool_description = description or "List available models on Replicate platform"

    def list_models(cursor: Optional[str] = None, limit: Optional[int] = 20) -> str:
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
                "https://api.replicate.com/v1/models",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                models = data.get("results", [])
                
                result = f"Found {len(models)} models:\n\n"
                for model in models:
                    result += f"• {model.get('owner')}/{model.get('name')}\n"
                    result += f"  Description: {model.get('description', 'No description')}\n"
                    result += f"  Visibility: {model.get('visibility', 'unknown')}\n"
                    result += f"  GitHub URL: {model.get('github_url', 'N/A')}\n"
                    result += f"  Paper URL: {model.get('paper_url', 'N/A')}\n"
                    result += f"  License URL: {model.get('license_url', 'N/A')}\n"
                    result += f"  Run count: {model.get('run_count', 0)}\n\n"
                
                if data.get("next"):
                    result += f"Next cursor: {data.get('next')}\n"
                
                return result
            else:
                return f"Error listing models: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to list models: {str(e)}"

    return StructuredTool.from_function(
        func=list_models,
        name=name,
        description=tool_description,
        args_schema=ListModelsInput,
        return_direct=True
    )


# Get Model Tool
class GetModelInput(BaseModel):
    model_owner: str = Field(description="Owner of the model (e.g., 'stability-ai')")
    model_name: str = Field(description="Name of the model (e.g., 'stable-diffusion')")


def get_replicate_model(name, description, token):
    """Gets details of a specific Replicate model."""
    tool_description = description or "Get detailed information about a specific Replicate model"

    def get_model(model_owner: str, model_name: str) -> str:
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
                result += f"Run count: {model.get('run_count', 0)}\n"
                result += f"Cover image URL: {model.get('cover_image_url', 'N/A')}\n"
                result += f"Default example: {model.get('default_example', 'N/A')}\n"
                
                # Latest version info
                latest_version = model.get('latest_version')
                if latest_version:
                    result += f"\nLatest Version:\n"
                    result += f"  ID: {latest_version.get('id')}\n"
                    result += f"  Created: {latest_version.get('created_at')}\n"
                    result += f"  CogVersion: {latest_version.get('cog_version')}\n"
                    
                    # Schema info
                    schema = latest_version.get('openapi_schema', {})
                    if schema:
                        components = schema.get('components', {})
                        if components:
                            result += f"  Input Schema: {json.dumps(components.get('schemas', {}).get('Input', {}), indent=2)}\n"
                            result += f"  Output Schema: {json.dumps(components.get('schemas', {}).get('Output', {}), indent=2)}\n"
                
                return result
            else:
                return f"Error getting model: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to get model: {str(e)}"

    return StructuredTool.from_function(
        func=get_model,
        name=name,
        description=tool_description,
        args_schema=GetModelInput,
        return_direct=True
    )


# Search Models Tool
class SearchModelsInput(BaseModel):
    query: str = Field(description="Search query for models")
    limit: Optional[int] = Field(20, description="Number of models to return (max 100)")


def search_replicate_models(name, description, token):
    """Searches for models on Replicate."""
    tool_description = description or "Search for models on Replicate platform"

    def search_models(query: str, limit: Optional[int] = 20) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Prepare headers
            headers = {
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json"
            }
            
            # Prepare query parameters
            params = {
                "query": query,
                "limit": min(limit, 100)
            }
            
            # Make API request
            response = requests.get(
                "https://api.replicate.com/v1/models",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                models = data.get("results", [])
                
                result = f"Found {len(models)} models matching '{query}':\n\n"
                for model in models:
                    result += f"• {model.get('owner')}/{model.get('name')}\n"
                    result += f"  Description: {model.get('description', 'No description')}\n"
                    result += f"  Run count: {model.get('run_count', 0)}\n\n"
                
                return result
            else:
                return f"Error searching models: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to search models: {str(e)}"

    return StructuredTool.from_function(
        func=search_models,
        name=name,
        description=tool_description,
        args_schema=SearchModelsInput,
        return_direct=True
    )


# Get Model Versions Tool
class GetModelVersionsInput(BaseModel):
    model_owner: str = Field(description="Owner of the model")
    model_name: str = Field(description="Name of the model")


def get_model_versions(name, description, token):
    """Gets versions of a specific model."""
    tool_description = description or "Get all versions of a specific Replicate model"

    def get_versions(model_owner: str, model_name: str) -> str:
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
                f"https://api.replicate.com/v1/models/{model_owner}/{model_name}/versions",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                versions = data.get("results", [])
                
                result = f"Found {len(versions)} versions for {model_owner}/{model_name}:\n\n"
                for version in versions:
                    result += f"• Version ID: {version.get('id')}\n"
                    result += f"  Created: {version.get('created_at')}\n"
                    result += f"  Cog Version: {version.get('cog_version')}\n"
                    result += f"  Status: {version.get('status', 'unknown')}\n\n"
                
                return result
            else:
                return f"Error getting model versions: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to get model versions: {str(e)}"

    return StructuredTool.from_function(
        func=get_versions,
        name=name,
        description=tool_description,
        args_schema=GetModelVersionsInput,
        return_direct=True
    )


# Get Model Version Details Tool
class GetModelVersionDetailsInput(BaseModel):
    model_owner: str = Field(description="Owner of the model")
    model_name: str = Field(description="Name of the model")
    version_id: str = Field(description="Version ID to get details for")


def get_model_version_details(name, description, token):
    """Gets details of a specific model version."""
    tool_description = description or "Get detailed information about a specific model version"

    def get_version_details(model_owner: str, model_name: str, version_id: str) -> str:
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
                f"https://api.replicate.com/v1/models/{model_owner}/{model_name}/versions/{version_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                version = response.json()
                
                result = f"Version Details for {model_owner}/{model_name}:\n"
                result += f"Version ID: {version.get('id')}\n"
                result += f"Created: {version.get('created_at')}\n"
                result += f"Cog Version: {version.get('cog_version')}\n"
                result += f"Status: {version.get('status', 'unknown')}\n"
                
                # Schema info
                schema = version.get('openapi_schema', {})
                if schema:
                    components = schema.get('components', {})
                    if components:
                        schemas = components.get('schemas', {})
                        if 'Input' in schemas:
                            result += f"\nInput Schema:\n{json.dumps(schemas['Input'], indent=2)}\n"
                        if 'Output' in schemas:
                            result += f"\nOutput Schema:\n{json.dumps(schemas['Output'], indent=2)}\n"
                
                return result
            else:
                return f"Error getting version details: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to get version details: {str(e)}"

    return StructuredTool.from_function(
        func=get_version_details,
        name=name,
        description=tool_description,
        args_schema=GetModelVersionDetailsInput,
        return_direct=True
    )
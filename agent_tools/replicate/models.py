from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json
import replicate
from .. import extract_token_from_data


# List Models Tool
class ListModelsInput(BaseModel):
    cursor: Optional[str] = Field(None, description="Cursor for pagination")
    limit: Optional[int] = Field(20, description="Number of models to return (max 100)")


def list_models_replicate(name, description, token):
    """Lists available models on Replicate."""
    tool_description = description or "List available models on Replicate platform"

    def list_models(cursor: Optional[str] = None, limit: Optional[int] = 20) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # List models
            models = client.models.list()
            
            # Format response
            models_list = []
            count = 0
            for model in models:
                if count >= limit:
                    break
                models_list.append({
                    "owner": model.owner,
                    "name": model.name,
                    "description": model.description,
                    "visibility": model.visibility,
                    "github_url": model.github_url,
                    "paper_url": model.paper_url,
                    "license_url": model.license_url,
                    "cover_image_url": model.cover_image_url,
                    "created_at": str(model.created_at) if model.created_at else None,
                    "updated_at": str(model.updated_at) if model.updated_at else None
                })
                count += 1
            
            return json.dumps(models_list, indent=2)
            
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
    owner: str = Field(description="Owner of the model")
    name: str = Field(description="Name of the model")


def get_model_replicate(name, description, token):
    """Gets details of a specific model on Replicate."""
    tool_description = description or "Get details of a specific model on Replicate"

    def get_model(owner: str, name: str) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # Get model
            model = client.models.get(f"{owner}/{name}")
            
            # Format response
            model_info = {
                "owner": model.owner,
                "name": model.name,
                "description": model.description,
                "visibility": model.visibility,
                "github_url": model.github_url,
                "paper_url": model.paper_url,
                "license_url": model.license_url,
                "cover_image_url": model.cover_image_url,
                "created_at": str(model.created_at) if model.created_at else None,
                "updated_at": str(model.updated_at) if model.updated_at else None,
                "latest_version": {
                    "id": model.latest_version.id if model.latest_version else None,
                    "created_at": str(model.latest_version.created_at) if model.latest_version and model.latest_version.created_at else None,
                    "cog_version": model.latest_version.cog_version if model.latest_version else None,
                    "openapi_schema": model.latest_version.openapi_schema if model.latest_version else None
                } if model.latest_version else None
            }
            
            return json.dumps(model_info, indent=2)
            
        except Exception as e:
            return f"Failed to get model: {str(e)}"

    return StructuredTool.from_function(
        func=get_model,
        name=name,
        description=tool_description,
        args_schema=GetModelInput,
        return_direct=True
    )


# Create Model Tool
class CreateModelInput(BaseModel):
    owner: str = Field(description="Owner of the model")
    name: str = Field(description="Name of the model")
    description: str = Field(description="Description of the model")
    visibility: str = Field(description="Visibility of the model (public or private)")
    hardware: str = Field(description="Hardware to run the model on")
    github_url: Optional[str] = Field(None, description="GitHub URL of the model")
    paper_url: Optional[str] = Field(None, description="Paper URL of the model")
    license_url: Optional[str] = Field(None, description="License URL of the model")
    cover_image_url: Optional[str] = Field(None, description="Cover image URL of the model")


def create_model_replicate(name, description, token):
    """Creates a new model on Replicate."""
    tool_description = description or "Create a new model on Replicate"

    def create_model(owner: str, name: str, description: str, visibility: str, hardware: str,
                    github_url: Optional[str] = None, paper_url: Optional[str] = None,
                    license_url: Optional[str] = None, cover_image_url: Optional[str] = None) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # Create model
            model = client.models.create(
                owner=owner,
                name=name,
                description=description,
                visibility=visibility,
                hardware=hardware,
                github_url=github_url,
                paper_url=paper_url,
                license_url=license_url,
                cover_image_url=cover_image_url
            )
            
            # Format response
            model_info = {
                "owner": model.owner,
                "name": model.name,
                "description": model.description,
                "visibility": model.visibility,
                "github_url": model.github_url,
                "paper_url": model.paper_url,
                "license_url": model.license_url,
                "cover_image_url": model.cover_image_url,
                "created_at": str(model.created_at) if model.created_at else None,
                "updated_at": str(model.updated_at) if model.updated_at else None
            }
            
            return f"Model created successfully: {json.dumps(model_info, indent=2)}"
            
        except Exception as e:
            return f"Failed to create model: {str(e)}"

    return StructuredTool.from_function(
        func=create_model,
        name=name,
        description=tool_description,
        args_schema=CreateModelInput,
        return_direct=True
    )


# Get Model Versions Tool
class GetModelVersionsInput(BaseModel):
    owner: str = Field(description="Owner of the model")
    name: str = Field(description="Name of the model")


def get_model_versions_replicate(name, description, token):
    """Gets all versions of a model on Replicate."""
    tool_description = description or "Get all versions of a model on Replicate"

    def get_model_versions(owner: str, name: str) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # Get model versions
            model = client.models.get(f"{owner}/{name}")
            versions = list(model.versions.list())
            
            # Format response
            versions_list = []
            for version in versions:
                versions_list.append({
                    "id": version.id,
                    "created_at": str(version.created_at) if version.created_at else None,
                    "cog_version": version.cog_version,
                    "openapi_schema": version.openapi_schema
                })
            
            return json.dumps(versions_list, indent=2)
            
        except Exception as e:
            return f"Failed to get model versions: {str(e)}"

    return StructuredTool.from_function(
        func=get_model_versions,
        name=name,
        description=tool_description,
        args_schema=GetModelVersionsInput,
        return_direct=True
    )


# Get Model Version Tool
class GetModelVersionInput(BaseModel):
    owner: str = Field(description="Owner of the model")
    name: str = Field(description="Name of the model")
    version: str = Field(description="Version ID of the model")


def get_model_version_replicate(name, description, token):
    """Gets details of a specific model version on Replicate."""
    tool_description = description or "Get details of a specific model version on Replicate"

    def get_model_version(owner: str, name: str, version: str) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # Get model version
            model_version = client.models.get(f"{owner}/{name}").versions.get(version)
            
            # Format response
            version_info = {
                "id": model_version.id,
                "created_at": str(model_version.created_at) if model_version.created_at else None,
                "cog_version": model_version.cog_version,
                "openapi_schema": model_version.openapi_schema
            }
            
            return json.dumps(version_info, indent=2)
            
        except Exception as e:
            return f"Failed to get model version: {str(e)}"

    return StructuredTool.from_function(
        func=get_model_version,
        name=name,
        description=tool_description,
        args_schema=GetModelVersionInput,
        return_direct=True
    )
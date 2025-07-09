from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import Optional, List
import requests

# Model retrieval tools
class ListModelsInput(BaseModel):
    pass

def list_models_replicate(name, description, token):
    """
    Lists all available models in Replicate.
    """
    def list_models() -> List[str]:
        headers = {'Authorization': f'Token {token}'}
        response = requests.get('https://api.replicate.com/v1/models', headers=headers)
        return response.json()
    return StructuredTool.from_function(
        func=list_models,
        name=name,
        description=description,
        args_schema=ListModelsInput,
        return_direct=True,
    )

class GetModelInput(BaseModel):
    model_id: str = Field(description="The ID of the model to retrieve.")

def get_model_replicate(name, description, token):
    """
    Retrieves details of a specific model.
    """
    def get_model(model_id: str) -> dict:
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(f'https://api.replicate.com/v1/models/{model_id}', headers=headers)
        return response.json()
    return StructuredTool.from_function(
        func=get_model,
        name=name,
        description=description,
        args_schema=GetModelInput,
        return_direct=True,
    )

# Additional model-related functions would go here...
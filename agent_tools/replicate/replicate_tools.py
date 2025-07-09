"""
Replicate Agent Tools - Main Tool Factory

This module provides the main factory function to create all Replicate tools
with proper authentication and configuration.
"""

from .models import (
    list_replicate_models, get_replicate_model, create_replicate_model,
    update_replicate_model, delete_replicate_model
)
from .predictions import (
    create_replicate_prediction, get_replicate_prediction, cancel_replicate_prediction,
    list_replicate_predictions, stream_replicate_prediction
)
from .code_generation import (
    generate_code_replicate, optimize_code_replicate, debug_code_replicate,
    explain_code_replicate, convert_code_replicate
)


def create_replicate_tools(name, token, description=None):
    """
    Creates and returns a list of all Replicate tools.

    Args:
        name (str): Base name for the tools, will be prefixed to each tool name
        token (str): Replicate API token for authentication
        description (str, optional): Description for the tools

    Returns:
        list: List of Replicate tools including:
            - Model management tools (5 tools)
            - Prediction execution tools (5 tools)
            - Code generation tools (5 tools)
    """
    tools = []

    # Model Management Tools
    model_tools = [
        list_replicate_models(f"{name}_list_models", description, token),
        get_replicate_model(f"{name}_get_model", description, token),
        create_replicate_model(f"{name}_create_model", description, token),
        update_replicate_model(f"{name}_update_model", description, token),
        delete_replicate_model(f"{name}_delete_model", description, token)
    ]
    tools.extend(model_tools)

    # Prediction Execution Tools
    prediction_tools = [
        create_replicate_prediction(f"{name}_create_prediction", description, token),
        get_replicate_prediction(f"{name}_get_prediction", description, token),
        cancel_replicate_prediction(f"{name}_cancel_prediction", description, token),
        list_replicate_predictions(f"{name}_list_predictions", description, token),
        stream_replicate_prediction(f"{name}_stream_prediction", description, token)
    ]
    tools.extend(prediction_tools)

    # Code Generation Tools
    code_tools = [
        generate_code_replicate(f"{name}_generate_code", description, token),
        optimize_code_replicate(f"{name}_optimize_code", description, token),
        debug_code_replicate(f"{name}_debug_code", description, token),
        explain_code_replicate(f"{name}_explain_code", description, token),
        convert_code_replicate(f"{name}_convert_code", description, token)
    ]
    tools.extend(code_tools)

    return tools


# Utility function to get tool categories
def get_replicate_tool_categories():
    """
    Returns information about available tool categories.
    
    Returns:
        dict: Dictionary containing tool categories and their descriptions
    """
    return {
        "models": {
            "description": "Tools for managing Replicate models",
            "count": 5,
            "tools": [
                "list_models", "get_model", "create_model", 
                "update_model", "delete_model"
            ]
        },
        "predictions": {
            "description": "Tools for executing and managing predictions",
            "count": 5,
            "tools": [
                "create_prediction", "get_prediction", "cancel_prediction",
                "list_predictions", "stream_prediction"
            ]
        },
        "code_generation": {
            "description": "Tools for AI-powered code generation and optimization",
            "count": 5,
            "tools": [
                "generate_code", "optimize_code", "debug_code",
                "explain_code", "convert_code"
            ]
        }
    }


# Version and metadata
__version__ = "1.0.0"
__author__ = "Jonathan Toky"
__description__ = "Comprehensive Replicate API tools for AI model management and code generation"
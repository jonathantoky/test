"""
Load Tools - Replicate Integration

This module provides utilities for loading and integrating Replicate tools
into the agent tools ecosystem.
"""

import os
import sys
from typing import List, Dict, Any, Optional
import importlib.util

# Add the current directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import Replicate tools
try:
    from agent_tools.replicate import create_replicate_tools
    from agent_tools.replicate.models import (
        list_replicate_models, get_replicate_model, create_replicate_model,
        update_replicate_model, delete_replicate_model
    )
    from agent_tools.replicate.predictions import (
        create_replicate_prediction, get_replicate_prediction, cancel_replicate_prediction,
        list_replicate_predictions, stream_replicate_prediction
    )
    from agent_tools.replicate.code_generation import (
        generate_code_replicate, optimize_code_replicate, debug_code_replicate,
        explain_code_replicate, convert_code_replicate
    )
    from client.replicate_client import ReplicateClient, validate_api_token
    
    REPLICATE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Replicate tools not available: {e}")
    REPLICATE_AVAILABLE = False


def load_replicate_tools(config: Dict[str, Any]) -> List[Any]:
    """
    Load Replicate tools with configuration
    
    Args:
        config: Configuration dictionary containing:
            - api_token: Replicate API token
            - name: Base name for tools (optional)
            - description: Description for tools (optional)
            - categories: List of tool categories to load (optional)
    
    Returns:
        List of loaded Replicate tools
    """
    if not REPLICATE_AVAILABLE:
        raise ImportError("Replicate tools are not available. Please install required dependencies.")
    
    api_token = config.get('api_token')
    if not api_token:
        raise ValueError("Replicate API token is required in config")
    
    # Validate API token
    if not validate_api_token(api_token):
        raise ValueError("Invalid Replicate API token")
    
    name = config.get('name', 'replicate')
    description = config.get('description', 'Replicate AI tools')
    categories = config.get('categories', ['models', 'predictions', 'code_generation'])
    
    tools = []
    
    # Load model management tools
    if 'models' in categories:
        model_tools = [
            list_replicate_models(f"{name}_list_models", description, api_token),
            get_replicate_model(f"{name}_get_model", description, api_token),
            create_replicate_model(f"{name}_create_model", description, api_token),
            update_replicate_model(f"{name}_update_model", description, api_token),
            delete_replicate_model(f"{name}_delete_model", description, api_token)
        ]
        tools.extend(model_tools)
    
    # Load prediction tools
    if 'predictions' in categories:
        prediction_tools = [
            create_replicate_prediction(f"{name}_create_prediction", description, api_token),
            get_replicate_prediction(f"{name}_get_prediction", description, api_token),
            cancel_replicate_prediction(f"{name}_cancel_prediction", description, api_token),
            list_replicate_predictions(f"{name}_list_predictions", description, api_token),
            stream_replicate_prediction(f"{name}_stream_prediction", description, api_token)
        ]
        tools.extend(prediction_tools)
    
    # Load code generation tools
    if 'code_generation' in categories:
        code_tools = [
            generate_code_replicate(f"{name}_generate_code", description, api_token),
            optimize_code_replicate(f"{name}_optimize_code", description, api_token),
            debug_code_replicate(f"{name}_debug_code", description, api_token),
            explain_code_replicate(f"{name}_explain_code", description, api_token),
            convert_code_replicate(f"{name}_convert_code", description, api_token)
        ]
        tools.extend(code_tools)
    
    return tools


def load_all_replicate_tools(api_token: str, name: str = 'replicate', description: Optional[str] = None) -> List[Any]:
    """
    Load all Replicate tools (convenience function)
    
    Args:
        api_token: Replicate API token
        name: Base name for tools
        description: Description for tools
    
    Returns:
        List of all Replicate tools
    """
    if not REPLICATE_AVAILABLE:
        raise ImportError("Replicate tools are not available. Please install required dependencies.")
    
    return create_replicate_tools(name, api_token, description)


def get_replicate_tool_info() -> Dict[str, Any]:
    """
    Get information about available Replicate tools
    
    Returns:
        Dictionary containing tool information
    """
    if not REPLICATE_AVAILABLE:
        return {
            "available": False,
            "error": "Replicate tools not available"
        }
    
    return {
        "available": True,
        "categories": {
            "models": {
                "description": "Model management tools",
                "tools": [
                    "list_models", "get_model", "create_model", 
                    "update_model", "delete_model"
                ]
            },
            "predictions": {
                "description": "Prediction execution tools",
                "tools": [
                    "create_prediction", "get_prediction", "cancel_prediction",
                    "list_predictions", "stream_prediction"
                ]
            },
            "code_generation": {
                "description": "AI code generation tools",
                "tools": [
                    "generate_code", "optimize_code", "debug_code",
                    "explain_code", "convert_code"
                ]
            }
        },
        "total_tools": 15,
        "version": "1.0.0"
    }


def validate_replicate_config(config: Dict[str, Any]) -> bool:
    """
    Validate Replicate configuration
    
    Args:
        config: Configuration dictionary
    
    Returns:
        True if configuration is valid
    """
    if not REPLICATE_AVAILABLE:
        return False
    
    api_token = config.get('api_token')
    if not api_token:
        return False
    
    return validate_api_token(api_token)


def create_replicate_client(api_token: str) -> Optional[ReplicateClient]:
    """
    Create Replicate client instance
    
    Args:
        api_token: Replicate API token
    
    Returns:
        ReplicateClient instance or None if not available
    """
    if not REPLICATE_AVAILABLE:
        return None
    
    try:
        return ReplicateClient(api_token)
    except Exception:
        return None


# Tool loading registry
TOOL_LOADERS = {
    'replicate': load_replicate_tools,
    'replicate_all': load_all_replicate_tools,
}


def load_tools_by_type(tool_type: str, config: Dict[str, Any]) -> List[Any]:
    """
    Load tools by type
    
    Args:
        tool_type: Type of tools to load
        config: Configuration for tools
    
    Returns:
        List of loaded tools
    """
    if tool_type not in TOOL_LOADERS:
        raise ValueError(f"Unknown tool type: {tool_type}")
    
    loader = TOOL_LOADERS[tool_type]
    return loader(config)


def get_available_tool_types() -> List[str]:
    """
    Get list of available tool types
    
    Returns:
        List of available tool types
    """
    return list(TOOL_LOADERS.keys())


# Example usage and testing
if __name__ == "__main__":
    print("Replicate Tools Loader")
    print("=" * 50)
    
    # Check availability
    print(f"Replicate tools available: {REPLICATE_AVAILABLE}")
    
    if REPLICATE_AVAILABLE:
        # Get tool info
        info = get_replicate_tool_info()
        print(f"Total tools: {info['total_tools']}")
        print(f"Categories: {list(info['categories'].keys())}")
        
        # Test with dummy config (will fail validation)
        test_config = {
            'api_token': 'test_token',
            'name': 'test_replicate',
            'description': 'Test Replicate tools'
        }
        
        print(f"Config valid: {validate_replicate_config(test_config)}")
        
        # Show available tool types
        print(f"Available tool types: {get_available_tool_types()}")
    
    print("\nTo use these tools, provide a valid Replicate API token in the configuration.")
    print("Example:")
    print("""
    config = {
        'api_token': 'r8_your_token_here',
        'name': 'my_replicate',
        'description': 'My Replicate tools'
    }
    tools = load_replicate_tools(config)
    """)
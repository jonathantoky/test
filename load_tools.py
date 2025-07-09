"""
Load Tools - Replicate Agent Tools Integration

This file demonstrates how to import and use the Replicate agent tools
in your application.
"""

from agent_tools.replicate import create_replicate_tools
from agent_tools.replicate.models import (
    list_models_replicate,
    get_model_replicate,
    create_model_replicate,
    get_model_versions_replicate,
    get_model_version_replicate
)
from agent_tools.replicate.predictions import (
    create_prediction_replicate,
    get_prediction_replicate,
    list_predictions_replicate,
    cancel_prediction_replicate,
    run_prediction_replicate
)
from agent_tools.replicate.code_generation import (
    generate_code_replicate,
    optimize_code_replicate,
    debug_code_replicate,
    generate_dockerfile_replicate,
    generate_requirements_replicate
)


def load_replicate_tools(token: str, name: str = "replicate", description: str = None):
    """
    Load all Replicate tools with the provided token.
    
    Args:
        token (str): Replicate API token
        name (str): Base name for the tools (default: "replicate")
        description (str): Optional description for the tools
    
    Returns:
        list: List of all Replicate tools
    """
    return create_replicate_tools(name, token, description)


def load_replicate_model_tools(token: str, name: str = "replicate_models"):
    """
    Load only the model management tools.
    
    Args:
        token (str): Replicate API token
        name (str): Base name for the tools
    
    Returns:
        list: List of model management tools
    """
    tools = []
    
    # Model management tools
    tools.append(list_models_replicate(f"{name}_list", "List models", token))
    tools.append(get_model_replicate(f"{name}_get", "Get model details", token))
    tools.append(create_model_replicate(f"{name}_create", "Create model", token))
    tools.append(get_model_versions_replicate(f"{name}_versions", "Get model versions", token))
    tools.append(get_model_version_replicate(f"{name}_version", "Get model version", token))
    
    return tools


def load_replicate_prediction_tools(token: str, name: str = "replicate_predictions"):
    """
    Load only the prediction management tools.
    
    Args:
        token (str): Replicate API token
        name (str): Base name for the tools
    
    Returns:
        list: List of prediction management tools
    """
    tools = []
    
    # Prediction management tools
    tools.append(create_prediction_replicate(f"{name}_create", "Create prediction", token))
    tools.append(get_prediction_replicate(f"{name}_get", "Get prediction", token))
    tools.append(list_predictions_replicate(f"{name}_list", "List predictions", token))
    tools.append(cancel_prediction_replicate(f"{name}_cancel", "Cancel prediction", token))
    tools.append(run_prediction_replicate(f"{name}_run", "Run prediction", token))
    
    return tools


def load_replicate_code_tools(token: str, name: str = "replicate_code"):
    """
    Load only the code generation tools.
    
    Args:
        token (str): Replicate API token
        name (str): Base name for the tools
    
    Returns:
        list: List of code generation tools
    """
    tools = []
    
    # Code generation tools
    tools.append(generate_code_replicate(f"{name}_generate", "Generate code", token))
    tools.append(optimize_code_replicate(f"{name}_optimize", "Optimize code", token))
    tools.append(debug_code_replicate(f"{name}_debug", "Debug code", token))
    tools.append(generate_dockerfile_replicate(f"{name}_dockerfile", "Generate Dockerfile", token))
    tools.append(generate_requirements_replicate(f"{name}_requirements", "Generate requirements", token))
    
    return tools


# Example usage
if __name__ == "__main__":
    # Replace with your actual Replicate API token
    REPLICATE_TOKEN = "your_replicate_api_token_here"
    
    # Load all tools
    print("Loading all Replicate tools...")
    all_tools = load_replicate_tools(REPLICATE_TOKEN)
    print(f"Loaded {len(all_tools)} tools")
    
    # Load specific tool categories
    print("\nLoading model management tools...")
    model_tools = load_replicate_model_tools(REPLICATE_TOKEN)
    print(f"Loaded {len(model_tools)} model tools")
    
    print("\nLoading prediction tools...")
    prediction_tools = load_replicate_prediction_tools(REPLICATE_TOKEN)
    print(f"Loaded {len(prediction_tools)} prediction tools")
    
    print("\nLoading code generation tools...")
    code_tools = load_replicate_code_tools(REPLICATE_TOKEN)
    print(f"Loaded {len(code_tools)} code generation tools")
    
    # Display tool names
    print("\nAll available tools:")
    for i, tool in enumerate(all_tools, 1):
        print(f"{i}. {tool.name} - {tool.description}")


# Integration with LangChain agents
def create_replicate_agent(token: str, model_name: str = "gpt-3.5-turbo"):
    """
    Create a LangChain agent with Replicate tools.
    
    Args:
        token (str): Replicate API token
        model_name (str): Language model to use for the agent
    
    Returns:
        Agent with Replicate tools
    """
    try:
        from langchain.agents import initialize_agent, AgentType
        from langchain.llms import OpenAI
        
        # Load Replicate tools
        tools = load_replicate_tools(token)
        
        # Initialize LLM
        llm = OpenAI(temperature=0)
        
        # Create agent
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
        
        return agent
        
    except ImportError:
        print("LangChain not installed. Install with: pip install langchain")
        return None


# Configuration examples
REPLICATE_TOOL_CONFIGS = {
    "basic": {
        "name": "replicate_basic",
        "description": "Basic Replicate tools for model interaction"
    },
    "advanced": {
        "name": "replicate_advanced",
        "description": "Advanced Replicate tools with code generation"
    },
    "code_focus": {
        "name": "replicate_code",
        "description": "Code-focused Replicate tools for development"
    }
}


def load_replicate_tools_by_config(token: str, config_name: str = "basic"):
    """
    Load Replicate tools based on predefined configurations.
    
    Args:
        token (str): Replicate API token
        config_name (str): Configuration name (basic, advanced, code_focus)
    
    Returns:
        list: List of configured tools
    """
    if config_name not in REPLICATE_TOOL_CONFIGS:
        raise ValueError(f"Unknown configuration: {config_name}")
    
    config = REPLICATE_TOOL_CONFIGS[config_name]
    
    if config_name == "basic":
        # Basic tools: models and predictions
        tools = []
        tools.extend(load_replicate_model_tools(token, f"{config['name']}_models"))
        tools.extend(load_replicate_prediction_tools(token, f"{config['name']}_predictions"))
        return tools
    
    elif config_name == "advanced":
        # All tools
        return load_replicate_tools(token, config["name"], config["description"])
    
    elif config_name == "code_focus":
        # Code generation tools only
        return load_replicate_code_tools(token, config["name"])
    
    else:
        return load_replicate_tools(token, config["name"], config["description"])
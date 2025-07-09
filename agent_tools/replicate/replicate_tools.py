from agent_tools.replicate.models import (
    list_models_replicate, get_model_replicate, create_model_replicate,
    get_model_versions_replicate, get_model_version_replicate
)
from agent_tools.replicate.predictions import (
    create_prediction_replicate, get_prediction_replicate, list_predictions_replicate,
    cancel_prediction_replicate, run_prediction_replicate
)
from agent_tools.replicate.code_generation import (
    generate_code_replicate, optimize_code_replicate, debug_code_replicate,
    generate_dockerfile_replicate, generate_requirements_replicate
)

def create_replicate_tools(name, token, description=None):
    """
    Creates and returns a list of all Replicate tools.

    Args:
        name (str): Base name for the tools, will be prefixed to each tool name
        token (str): API token for Replicate
        description (str, optional): Description for the tools

    Returns:
        list: List of Replicate tools including:
            - List models
            - Get model details
            - Create model
            - Get model versions
            - Get model version details
            - Create prediction
            - Get prediction
            - List predictions
            - Cancel prediction
            - Run prediction (simplified)
            - Generate code
            - Optimize code
            - Debug code
            - Generate Dockerfile
            - Generate requirements
    """
    tools = []

    # Model management tools
    list_models_name = f"{name}_list_models"
    list_models_desc = description if description else "List available models on Replicate"
    list_models_tool = list_models_replicate(list_models_name, list_models_desc, token)
    tools.append(list_models_tool)

    get_model_name = f"{name}_get_model"
    get_model_desc = description if description else "Get details of a specific model on Replicate"
    get_model_tool = get_model_replicate(get_model_name, get_model_desc, token)
    tools.append(get_model_tool)

    create_model_name = f"{name}_create_model"
    create_model_desc = description if description else "Create a new model on Replicate"
    create_model_tool = create_model_replicate(create_model_name, create_model_desc, token)
    tools.append(create_model_tool)

    get_model_versions_name = f"{name}_get_model_versions"
    get_model_versions_desc = description if description else "Get all versions of a model on Replicate"
    get_model_versions_tool = get_model_versions_replicate(get_model_versions_name, get_model_versions_desc, token)
    tools.append(get_model_versions_tool)

    get_model_version_name = f"{name}_get_model_version"
    get_model_version_desc = description if description else "Get details of a specific model version on Replicate"
    get_model_version_tool = get_model_version_replicate(get_model_version_name, get_model_version_desc, token)
    tools.append(get_model_version_tool)

    # Prediction tools
    create_prediction_name = f"{name}_create_prediction"
    create_prediction_desc = description if description else "Create a new prediction on Replicate"
    create_prediction_tool = create_prediction_replicate(create_prediction_name, create_prediction_desc, token)
    tools.append(create_prediction_tool)

    get_prediction_name = f"{name}_get_prediction"
    get_prediction_desc = description if description else "Get details of a specific prediction on Replicate"
    get_prediction_tool = get_prediction_replicate(get_prediction_name, get_prediction_desc, token)
    tools.append(get_prediction_tool)

    list_predictions_name = f"{name}_list_predictions"
    list_predictions_desc = description if description else "List predictions on Replicate"
    list_predictions_tool = list_predictions_replicate(list_predictions_name, list_predictions_desc, token)
    tools.append(list_predictions_tool)

    cancel_prediction_name = f"{name}_cancel_prediction"
    cancel_prediction_desc = description if description else "Cancel a prediction on Replicate"
    cancel_prediction_tool = cancel_prediction_replicate(cancel_prediction_name, cancel_prediction_desc, token)
    tools.append(cancel_prediction_tool)

    run_prediction_name = f"{name}_run_prediction"
    run_prediction_desc = description if description else "Run a prediction on Replicate using simplified interface"
    run_prediction_tool = run_prediction_replicate(run_prediction_name, run_prediction_desc, token)
    tools.append(run_prediction_tool)

    # Code generation tools
    generate_code_name = f"{name}_generate_code"
    generate_code_desc = description if description else "Generate code using Replicate AI models"
    generate_code_tool = generate_code_replicate(generate_code_name, generate_code_desc, token)
    tools.append(generate_code_tool)

    optimize_code_name = f"{name}_optimize_code"
    optimize_code_desc = description if description else "Optimize existing code using Replicate AI models"
    optimize_code_tool = optimize_code_replicate(optimize_code_name, optimize_code_desc, token)
    tools.append(optimize_code_tool)

    debug_code_name = f"{name}_debug_code"
    debug_code_desc = description if description else "Debug and fix code using Replicate AI models"
    debug_code_tool = debug_code_replicate(debug_code_name, debug_code_desc, token)
    tools.append(debug_code_tool)

    generate_dockerfile_name = f"{name}_generate_dockerfile"
    generate_dockerfile_desc = description if description else "Generate Dockerfile using Replicate AI models"
    generate_dockerfile_tool = generate_dockerfile_replicate(generate_dockerfile_name, generate_dockerfile_desc, token)
    tools.append(generate_dockerfile_tool)

    generate_requirements_name = f"{name}_generate_requirements"
    generate_requirements_desc = description if description else "Generate requirements.txt using Replicate AI models"
    generate_requirements_tool = generate_requirements_replicate(generate_requirements_name, generate_requirements_desc, token)
    tools.append(generate_requirements_tool)

    return tools
from agent_tools.replicate.models import (
    list_replicate_models, get_replicate_model, search_replicate_models,
    get_model_versions, get_model_version_details
)
from agent_tools.replicate.predictions import (
    create_replicate_prediction, get_replicate_prediction, cancel_replicate_prediction,
    list_replicate_predictions, get_prediction_logs
)
from agent_tools.replicate.code_generation import (
    generate_code_with_replicate, generate_python_code, generate_javascript_code,
    generate_api_code, code_completion_replicate
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
            - Search models
            - Get model versions
            - Get model version details
            - Create prediction
            - Get prediction
            - Cancel prediction
            - List predictions
            - Get prediction logs
            - Generate code
            - Generate Python code
            - Generate JavaScript code
            - Generate API code
            - Code completion
    """
    tools = []

    # Model tools
    list_models_name = f"{name}_list_models"
    list_models_desc = description if description else "List available models on Replicate"
    list_models_tool = list_replicate_models(list_models_name, list_models_desc, token)
    tools.append(list_models_tool)

    get_model_name = f"{name}_get_model"
    get_model_desc = description if description else "Get details of a specific Replicate model"
    get_model_tool = get_replicate_model(get_model_name, get_model_desc, token)
    tools.append(get_model_tool)

    search_models_name = f"{name}_search_models"
    search_models_desc = description if description else "Search for models on Replicate"
    search_models_tool = search_replicate_models(search_models_name, search_models_desc, token)
    tools.append(search_models_tool)

    get_versions_name = f"{name}_get_model_versions"
    get_versions_desc = description if description else "Get versions of a specific model"
    get_versions_tool = get_model_versions(get_versions_name, get_versions_desc, token)
    tools.append(get_versions_tool)

    get_version_details_name = f"{name}_get_version_details"
    get_version_details_desc = description if description else "Get details of a specific model version"
    get_version_details_tool = get_model_version_details(get_version_details_name, get_version_details_desc, token)
    tools.append(get_version_details_tool)

    # Prediction tools
    create_prediction_name = f"{name}_create_prediction"
    create_prediction_desc = description if description else "Create a new prediction with a Replicate model"
    create_prediction_tool = create_replicate_prediction(create_prediction_name, create_prediction_desc, token)
    tools.append(create_prediction_tool)

    get_prediction_name = f"{name}_get_prediction"
    get_prediction_desc = description if description else "Get status and results of a prediction"
    get_prediction_tool = get_replicate_prediction(get_prediction_name, get_prediction_desc, token)
    tools.append(get_prediction_tool)

    cancel_prediction_name = f"{name}_cancel_prediction"
    cancel_prediction_desc = description if description else "Cancel a running prediction"
    cancel_prediction_tool = cancel_replicate_prediction(cancel_prediction_name, cancel_prediction_desc, token)
    tools.append(cancel_prediction_tool)

    list_predictions_name = f"{name}_list_predictions"
    list_predictions_desc = description if description else "List your predictions"
    list_predictions_tool = list_replicate_predictions(list_predictions_name, list_predictions_desc, token)
    tools.append(list_predictions_tool)

    get_logs_name = f"{name}_get_prediction_logs"
    get_logs_desc = description if description else "Get logs from a prediction"
    get_logs_tool = get_prediction_logs(get_logs_name, get_logs_desc, token)
    tools.append(get_logs_tool)

    # Code generation tools
    generate_code_name = f"{name}_generate_code"
    generate_code_desc = description if description else "Generate code using Replicate models"
    generate_code_tool = generate_code_with_replicate(generate_code_name, generate_code_desc, token)
    tools.append(generate_code_tool)

    generate_python_name = f"{name}_generate_python"
    generate_python_desc = description if description else "Generate Python code using Replicate"
    generate_python_tool = generate_python_code(generate_python_name, generate_python_desc, token)
    tools.append(generate_python_tool)

    generate_js_name = f"{name}_generate_javascript"
    generate_js_desc = description if description else "Generate JavaScript code using Replicate"
    generate_js_tool = generate_javascript_code(generate_js_name, generate_js_desc, token)
    tools.append(generate_js_tool)

    generate_api_name = f"{name}_generate_api_code"
    generate_api_desc = description if description else "Generate API integration code using Replicate"
    generate_api_tool = generate_api_code(generate_api_name, generate_api_desc, token)
    tools.append(generate_api_tool)

    code_completion_name = f"{name}_code_completion"
    code_completion_desc = description if description else "Complete code snippets using Replicate"
    code_completion_tool = code_completion_replicate(code_completion_name, code_completion_desc, token)
    tools.append(code_completion_tool)

    return tools
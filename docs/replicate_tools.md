# Replicate Agent Tools Documentation

## Overview

The Replicate Agent Tools provide comprehensive integration with the Replicate API, enabling AI model interaction, prediction management, and code generation capabilities. These tools are designed to work seamlessly with the SwiftAsk Agent framework.

## Features

### 🤖 Model Management
- **List Models**: Browse available AI models on Replicate
- **Get Model Details**: Retrieve detailed information about specific models
- **Search Models**: Find models using keywords
- **Version Management**: Access model versions and their details

### 🔮 Prediction Management
- **Create Predictions**: Run AI models with custom inputs
- **Monitor Predictions**: Track prediction status and results
- **Cancel Predictions**: Stop running predictions
- **Prediction Logs**: Access detailed logs for debugging

### 💻 Code Generation
- **General Code Generation**: Generate code in multiple programming languages
- **Python Code Generation**: Create Python code with specific formatting
- **JavaScript Code Generation**: Generate JavaScript with framework support
- **API Code Generation**: Create API integration code
- **Code Completion**: Complete partial code snippets

## Installation

### Prerequisites

- Python 3.7+
- Required packages: `requests`, `langchain-core`, `pydantic`

### Setup

1. Install the required dependencies:
```bash
pip install requests langchain-core pydantic
```

2. Get your Replicate API token:
   - Visit [Replicate Account Settings](https://replicate.com/account)
   - Create or copy your API token

3. Set up authentication:
```python
# Option 1: Environment variable
export REPLICATE_API_TOKEN="r8_your_token_here"

# Option 2: Pass directly to tools
token = "r8_your_token_here"
```

## Usage

### Basic Usage

```python
from agent_tools.replicate import create_replicate_tools

# Create tools with your API token
tools = create_replicate_tools(
    name="my_replicate",
    token="r8_your_token_here",
    description="Custom Replicate tools"
)

# Use individual tools
list_models_tool = tools[0]  # First tool is list_models
result = list_models_tool.func(limit=10)
print(result)
```

### Model Management

#### List Available Models

```python
# Get the list models tool
list_models_tool = next(tool for tool in tools if "list_models" in tool.name)

# List models with pagination
result = list_models_tool.func(limit=20, cursor=None)
```

#### Get Model Details

```python
# Get the get model tool
get_model_tool = next(tool for tool in tools if "get_model" in tool.name)

# Get details for a specific model
result = get_model_tool.func(
    model_owner="stability-ai",
    model_name="stable-diffusion"
)
```

#### Search Models

```python
# Get the search models tool
search_tool = next(tool for tool in tools if "search_models" in tool.name)

# Search for models
result = search_tool.func(
    query="text generation",
    limit=10
)
```

### Prediction Management

#### Create a Prediction

```python
# Get the create prediction tool
create_pred_tool = next(tool for tool in tools if "create_prediction" in tool.name)

# Create a prediction
result = create_pred_tool.func(
    model_version="stability-ai/stable-diffusion:version_id",
    input_data={
        "prompt": "A beautiful sunset over mountains",
        "width": 512,
        "height": 512,
        "num_inference_steps": 50
    }
)
```

#### Monitor Prediction

```python
# Get the get prediction tool
get_pred_tool = next(tool for tool in tools if "get_prediction" in tool.name)

# Check prediction status
result = get_pred_tool.func(prediction_id="prediction_id_here")
```

#### Cancel Prediction

```python
# Get the cancel prediction tool
cancel_tool = next(tool for tool in tools if "cancel_prediction" in tool.name)

# Cancel a running prediction
result = cancel_tool.func(prediction_id="prediction_id_here")
```

### Code Generation

#### Generate Python Code

```python
# Get the Python code generation tool
python_tool = next(tool for tool in tools if "generate_python" in tool.name)

# Generate Python code
result = python_tool.func(
    prompt="Create a function to calculate fibonacci numbers",
    include_comments=True,
    include_docstrings=True,
    style="pep8"
)
```

#### Generate JavaScript Code

```python
# Get the JavaScript code generation tool
js_tool = next(tool for tool in tools if "generate_javascript" in tool.name)

# Generate JavaScript code
result = js_tool.func(
    prompt="Create a React component for a todo list",
    framework="react",
    es_version="es6",
    include_types=True
)
```

#### Generate API Code

```python
# Get the API code generation tool
api_tool = next(tool for tool in tools if "generate_api_code" in tool.name)

# Generate API integration code
result = api_tool.func(
    api_description="REST API for user management with CRUD operations",
    api_type="rest",
    language="python",
    authentication="jwt"
)
```

#### Code Completion

```python
# Get the code completion tool
completion_tool = next(tool for tool in tools if "code_completion" in tool.name)

# Complete code snippet
result = completion_tool.func(
    code_snippet="def fibonacci(n):\n    if n <= 1:\n        return n\n    else:",
    language="python",
    context="Recursive implementation of fibonacci sequence"
)
```

## Tool Reference

### Model Tools

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `list_models` | List available models | `cursor`, `limit` |
| `get_model` | Get model details | `model_owner`, `model_name` |
| `search_models` | Search for models | `query`, `limit` |
| `get_model_versions` | Get model versions | `model_owner`, `model_name` |
| `get_version_details` | Get version details | `model_owner`, `model_name`, `version_id` |

### Prediction Tools

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `create_prediction` | Create new prediction | `model_version`, `input_data`, `webhook` |
| `get_prediction` | Get prediction status | `prediction_id` |
| `cancel_prediction` | Cancel prediction | `prediction_id` |
| `list_predictions` | List predictions | `cursor`, `limit` |
| `get_prediction_logs` | Get prediction logs | `prediction_id` |

### Code Generation Tools

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `generate_code` | Generate code | `prompt`, `language`, `model`, `max_tokens`, `temperature` |
| `generate_python` | Generate Python code | `prompt`, `include_comments`, `include_docstrings`, `style` |
| `generate_javascript` | Generate JavaScript code | `prompt`, `framework`, `es_version`, `include_types` |
| `generate_api_code` | Generate API code | `api_description`, `api_type`, `language`, `authentication` |
| `code_completion` | Complete code snippet | `code_snippet`, `language`, `context` |

## Authentication

### API Token Setup

1. **Get Token**: Visit [Replicate Account](https://replicate.com/account) to get your API token
2. **Format**: Tokens start with `r8_` followed by alphanumeric characters
3. **Security**: Keep your token secure and never commit it to version control

### Authentication Methods

#### Environment Variable (Recommended)
```bash
export REPLICATE_API_TOKEN="r8_your_token_here"
```

#### Direct Token Passing
```python
tools = create_replicate_tools("my_tools", "r8_your_token_here")
```

#### Using Authentication Client
```python
from client.replicate_auth import create_replicate_client

client = create_replicate_client("r8_your_token_here")
is_valid = client.validate_token()
```

## Error Handling

The tools include comprehensive error handling:

```python
# Example error handling
try:
    result = tool.func(parameters)
    if "Error" in result:
        print(f"Tool error: {result}")
    else:
        print(f"Success: {result}")
except Exception as e:
    print(f"Exception: {e}")
```

Common error scenarios:
- Invalid API token
- Model not found
- Prediction timeout
- Network connectivity issues
- Rate limiting

## Best Practices

### 1. Token Management
- Use environment variables for tokens
- Implement token rotation for production
- Monitor token usage and limits

### 2. Error Handling
- Always check for errors in tool responses
- Implement retry logic for transient failures
- Log errors for debugging

### 3. Performance
- Use pagination for large result sets
- Cache model information when possible
- Monitor prediction costs

### 4. Security
- Never expose API tokens in logs
- Use secure storage for tokens
- Implement proper access controls

## Examples

### Complete Workflow Example

```python
from agent_tools.replicate import create_replicate_tools

# Initialize tools
tools = create_replicate_tools("example", "r8_your_token_here")

# 1. Search for a code generation model
search_tool = next(tool for tool in tools if "search_models" in tool.name)
models = search_tool.func(query="code generation", limit=5)
print("Available models:", models)

# 2. Generate Python code
python_tool = next(tool for tool in tools if "generate_python" in tool.name)
code = python_tool.func(
    prompt="Create a class for handling HTTP requests with retry logic",
    include_comments=True,
    include_docstrings=True
)
print("Generated code:", code)

# 3. Complete the code if needed
completion_tool = next(tool for tool in tools if "code_completion" in tool.name)
completed = completion_tool.func(
    code_snippet="class HTTPClient:\n    def __init__(self, base_url):",
    language="python",
    context="HTTP client with retry logic"
)
print("Completed code:", completed)
```

### Image Generation Example

```python
# Create prediction for image generation
create_pred_tool = next(tool for tool in tools if "create_prediction" in tool.name)

result = create_pred_tool.func(
    model_version="stability-ai/stable-diffusion:version_id",
    input_data={
        "prompt": "A futuristic city at sunset, digital art",
        "width": 768,
        "height": 768,
        "num_inference_steps": 50,
        "guidance_scale": 7.5
    }
)

# Monitor the prediction
get_pred_tool = next(tool for tool in tools if "get_prediction" in tool.name)
status = get_pred_tool.func(prediction_id=result["prediction_id"])
print("Prediction status:", status)
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify API token is correct
   - Check token has necessary permissions
   - Ensure token is not expired

2. **Model Not Found**
   - Verify model owner and name
   - Check if model is public
   - Use search to find correct model names

3. **Prediction Timeouts**
   - Increase timeout values
   - Check model complexity
   - Monitor system resources

4. **Rate Limiting**
   - Implement exponential backoff
   - Monitor API usage
   - Consider upgrading plan

### Debug Mode

Enable debug mode for detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Tools will now provide detailed debug information
```

## Support

For issues and questions:
- Check the [Replicate Documentation](https://replicate.com/docs)
- Review error messages carefully
- Test with simpler examples first
- Contact support with specific error details

## License

This tool is part of the SwiftAsk Agent framework and follows the same licensing terms.
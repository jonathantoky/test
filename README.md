# Replicate Agent Tools

A comprehensive Python library for integrating Replicate's AI models into your applications with support for model management, prediction execution, and AI-powered code generation.

## Features

### 🤖 Model Management
- List available models on Replicate
- Get detailed model information
- Create and manage custom models
- Handle model versions and updates

### 🔮 Prediction Execution
- Create and monitor predictions
- Real-time prediction status tracking
- Batch prediction processing
- Webhook support for async operations

### 💻 AI-Powered Code Generation
- Generate code in multiple programming languages
- Optimize existing code for performance and readability
- Debug and fix code issues automatically
- Generate Dockerfiles and requirements.txt files

## Installation

```bash
pip install replicate
pip install langchain
pip install pydantic
```

## Quick Start

### 1. Set up your API token

```python
import os
os.environ["REPLICATE_API_TOKEN"] = "your_replicate_api_token_here"
```

### 2. Load all Replicate tools

```python
from load_tools import load_replicate_tools

# Load all tools
tools = load_replicate_tools("your_replicate_api_token")
print(f"Loaded {len(tools)} tools")
```

### 3. Use specific tool categories

```python
from load_tools import (
    load_replicate_model_tools,
    load_replicate_prediction_tools,
    load_replicate_code_tools
)

# Load only model management tools
model_tools = load_replicate_model_tools("your_token")

# Load only prediction tools
prediction_tools = load_replicate_prediction_tools("your_token")

# Load only code generation tools
code_tools = load_replicate_code_tools("your_token")
```

## Tool Categories

### Model Management Tools

#### List Models
```python
from agent_tools.replicate.models import list_models_replicate

tool = list_models_replicate("list_models", "List available models", token)
result = tool.func(limit=10)
```

#### Get Model Details
```python
from agent_tools.replicate.models import get_model_replicate

tool = get_model_replicate("get_model", "Get model details", token)
result = tool.func("meta", "codellama-34b-instruct")
```

#### Create Model
```python
from agent_tools.replicate.models import create_model_replicate

tool = create_model_replicate("create_model", "Create new model", token)
result = tool.func(
    owner="your_username",
    name="my_model",
    description="My custom model",
    visibility="public",
    hardware="gpu-t4"
)
```

### Prediction Tools

#### Run Prediction (Simplified)
```python
from agent_tools.replicate.predictions import run_prediction_replicate

tool = run_prediction_replicate("run_prediction", "Run prediction", token)
result = tool.func(
    model="meta/codellama-34b-instruct",
    input={"prompt": "Generate a Python function to calculate fibonacci"},
    wait=True
)
```

#### Create Prediction
```python
from agent_tools.replicate.predictions import create_prediction_replicate

tool = create_prediction_replicate("create_prediction", "Create prediction", token)
result = tool.func(
    version="version_id_here",
    input={"prompt": "Hello, world!"}
)
```

#### Monitor Prediction
```python
from agent_tools.replicate.predictions import get_prediction_replicate

tool = get_prediction_replicate("get_prediction", "Get prediction status", token)
result = tool.func("prediction_id_here")
```

### Code Generation Tools

#### Generate Code
```python
from agent_tools.replicate.code_generation import generate_code_replicate

tool = generate_code_replicate("generate_code", "Generate code", token)
result = tool.func(
    prompt="Create a REST API endpoint for user authentication",
    language="python",
    max_tokens=2000
)
```

#### Optimize Code
```python
from agent_tools.replicate.code_generation import optimize_code_replicate

tool = optimize_code_replicate("optimize_code", "Optimize code", token)
result = tool.func(
    code="def slow_function(): return [i for i in range(1000000)]",
    language="python",
    optimization_goals="performance and memory usage"
)
```

#### Debug Code
```python
from agent_tools.replicate.code_generation import debug_code_replicate

tool = debug_code_replicate("debug_code", "Debug code", token)
result = tool.func(
    code="def broken_function(): print(undefined_variable)",
    error_message="NameError: name 'undefined_variable' is not defined",
    language="python"
)
```

#### Generate Dockerfile
```python
from agent_tools.replicate.code_generation import generate_dockerfile_replicate

tool = generate_dockerfile_replicate("generate_dockerfile", "Generate Dockerfile", token)
result = tool.func(
    project_description="A Flask web application with Redis",
    language="python",
    dependencies=["flask", "redis", "gunicorn"],
    port=8000
)
```

#### Generate Requirements
```python
from agent_tools.replicate.code_generation import generate_requirements_replicate

tool = generate_requirements_replicate("generate_requirements", "Generate requirements", token)
result = tool.func(
    code="import flask\nimport requests\nimport numpy as np\nfrom sklearn import datasets",
    language="python"
)
```

## Authentication

### Using Environment Variables
```python
import os
from client import get_token_from_env

# Set environment variable
os.environ["REPLICATE_API_TOKEN"] = "your_token_here"

# Get token from environment
token = get_token_from_env()
```

### Using Client Authentication
```python
from client import create_replicate_client, validate_replicate_token

# Validate token
is_valid = validate_replicate_token("your_token")

# Create authenticated client
client = create_replicate_client("your_token")
test_result = client.test_connection()
```

### Token Management
```python
from client import ReplicateTokenManager

# Create token manager
manager = ReplicateTokenManager()

# Add multiple tokens
manager.add_token("production", "prod_token")
manager.add_token("development", "dev_token")

# Get client by name
prod_client = manager.get_client("production")

# Test all tokens
results = manager.test_all_tokens()
```

## Configuration

### Environment Configuration
```bash
export REPLICATE_API_TOKEN="your_token_here"
export REPLICATE_DEFAULT_MODEL="meta/codellama-34b-instruct"
export REPLICATE_MAX_TOKENS=2000
export REPLICATE_TEMPERATURE=0.1
export REPLICATE_DEBUG=true
```

### Programmatic Configuration
```python
from client import ReplicateConfig, get_config, update_config

# Get configuration
config = get_config(use_env=True)

# Update configuration
updated_config = update_config(
    config,
    model={"temperature": 0.5, "max_tokens": 1000},
    debug=True
)
```

## Integration with LangChain

```python
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from load_tools import load_replicate_tools

# Load tools
tools = load_replicate_tools("your_token")

# Create agent
llm = OpenAI(temperature=0)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Use agent
result = agent.run("Generate a Python function to sort a list")
```

## Error Handling

```python
from client import ReplicateAuthError

try:
    # Your Replicate operations here
    tools = load_replicate_tools("invalid_token")
except ReplicateAuthError as e:
    print(f"Authentication error: {e}")
except Exception as e:
    print(f"General error: {e}")
```

## Testing

Run the test suite:

```bash
python -m pytest tests/test_replicate_tools.py -v
```

## Available Tools

### Model Management (5 tools)
1. `replicate_list_models` - List available models
2. `replicate_get_model` - Get model details
3. `replicate_create_model` - Create new model
4. `replicate_get_model_versions` - Get model versions
5. `replicate_get_model_version` - Get specific version details

### Prediction Management (5 tools)
1. `replicate_create_prediction` - Create prediction
2. `replicate_get_prediction` - Get prediction status
3. `replicate_list_predictions` - List predictions
4. `replicate_cancel_prediction` - Cancel prediction
5. `replicate_run_prediction` - Run prediction (simplified)

### Code Generation (5 tools)
1. `replicate_generate_code` - Generate code
2. `replicate_optimize_code` - Optimize existing code
3. `replicate_debug_code` - Debug and fix code
4. `replicate_generate_dockerfile` - Generate Dockerfile
5. `replicate_generate_requirements` - Generate requirements.txt

## Configuration Options

### API Configuration
- `base_url`: Replicate API base URL
- `timeout`: Request timeout in seconds
- `max_retries`: Maximum number of retries
- `retry_delay`: Initial retry delay

### Model Configuration
- `default_model`: Default model to use
- `code_generation_model`: Model for code generation
- `max_tokens`: Maximum tokens per request
- `temperature`: Generation temperature

### Prediction Configuration
- `max_prediction_time`: Maximum prediction time
- `polling_interval`: Status polling interval
- `max_polling_attempts`: Maximum polling attempts

### Code Configuration
- `supported_languages`: List of supported languages
- `default_language`: Default programming language
- `optimization_goals`: Available optimization goals

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the Replicate API documentation
- Review the test files for usage examples

## Changelog

### v1.0.0
- Initial release
- Model management tools
- Prediction execution tools
- Code generation tools
- Authentication system
- Configuration management
- Comprehensive test suite
# 🚀 Add Comprehensive Replicate Agent Tools

## 📋 Overview
This PR adds a complete Replicate agent tool suite with 15 specialized tools covering model management, prediction execution, and AI-powered code generation.

## ✨ Features Added

### 🤖 Model Management (5 tools)
- **List Models**: List available models with pagination support
- **Get Model**: Get detailed information about specific models
- **Create Model**: Create and configure new models
- **Get Model Versions**: Retrieve all versions of a model
- **Get Model Version**: Get specific version details

### 🔮 Prediction Execution (5 tools)
- **Create Prediction**: Create new predictions with input parameters
- **Get Prediction**: Monitor prediction status and retrieve results
- **List Predictions**: List all predictions with pagination
- **Cancel Prediction**: Cancel running predictions
- **Run Prediction**: Simplified interface for running predictions

### 💻 AI-Powered Code Generation (5 tools)
- **Generate Code**: Generate code in multiple programming languages
- **Optimize Code**: Optimize existing code for performance and readability
- **Debug Code**: Debug and fix code issues automatically
- **Generate Dockerfile**: Generate production-ready Dockerfiles
- **Generate Requirements**: Generate requirements.txt files from code analysis

## 🔧 Technical Implementation

### Files Added:
```
├── agent_tools/replicate/
│   ├── __init__.py
│   ├── replicate_tools.py (main tools orchestrator)
│   ├── models.py (model management tools)
│   ├── predictions.py (prediction execution tools)
│   └── code_generation.py (AI code generation tools)
├── client/
│   ├── __init__.py
│   ├── replicate_auth.py (authentication system)
│   └── config.py (configuration management)
├── tests/
│   └── test_replicate_tools.py (comprehensive test suite)
├── seeds/
│   └── replicate.ts (TypeScript tool definitions)
├── load_tools.py (integration examples)
└── README.md (complete documentation)
```

### Key Components:

#### 🔐 Authentication System
- Token validation and management
- Multiple token support with ReplicateTokenManager
- Connection testing and error handling
- Environment variable support

#### ⚙️ Configuration System
- Environment-based configuration
- Model-specific settings (temperature, max_tokens, etc.)
- API configuration (timeout, retries, etc.)
- Validation utilities

#### 🧪 Comprehensive Testing
- Unit tests for all 15 tools
- Mock implementations for external API calls
- Error handling and edge case testing
- Integration testing examples

## 🎯 Usage Examples

### Quick Start:
```python
from load_tools import load_replicate_tools

# Load all 15 tools
tools = load_replicate_tools("your_replicate_api_token")
print(f"Loaded {len(tools)} tools")

# Use with LangChain
from langchain.agents import initialize_agent
agent = initialize_agent(tools=tools, llm=llm)
```

### Code Generation:
```python
from agent_tools.replicate.code_generation import generate_code_replicate

tool = generate_code_replicate("generate_code", "Generate code", token)
result = tool.func(
    prompt="Create a REST API endpoint for user authentication",
    language="python",
    max_tokens=2000
)
```

### Model Management:
```python
from agent_tools.replicate.models import list_models_replicate

tool = list_models_replicate("list_models", "List models", token)
models = tool.func(limit=10)
```

### Prediction Execution:
```python
from agent_tools.replicate.predictions import run_prediction_replicate

tool = run_prediction_replicate("run_prediction", "Run prediction", token)
result = tool.func(
    model="meta/codellama-34b-instruct",
    input={"prompt": "Generate a Python function"},
    wait=True
)
```

## 🔍 Integration Features

### LangChain Compatibility
- All tools are StructuredTool instances
- Compatible with LangChain agents
- Proper input/output schemas
- Error handling integration

### Environment Support
```bash
export REPLICATE_API_TOKEN="your_token_here"
export REPLICATE_DEFAULT_MODEL="meta/codellama-34b-instruct"
export REPLICATE_MAX_TOKENS=2000
export REPLICATE_TEMPERATURE=0.1
```

### Flexible Loading
```python
# Load all tools
all_tools = load_replicate_tools(token)

# Load specific categories
model_tools = load_replicate_model_tools(token)
prediction_tools = load_replicate_prediction_tools(token)
code_tools = load_replicate_code_tools(token)

# Load by configuration
tools = load_replicate_tools_by_config(token, "advanced")
```

## 📊 Tool Inventory

| Category | Tool Name | Description |
|----------|-----------|-------------|
| Models | `replicate_list_models` | List available models |
| Models | `replicate_get_model` | Get model details |
| Models | `replicate_create_model` | Create new model |
| Models | `replicate_get_model_versions` | Get model versions |
| Models | `replicate_get_model_version` | Get version details |
| Predictions | `replicate_create_prediction` | Create prediction |
| Predictions | `replicate_get_prediction` | Get prediction status |
| Predictions | `replicate_list_predictions` | List predictions |
| Predictions | `replicate_cancel_prediction` | Cancel prediction |
| Predictions | `replicate_run_prediction` | Run prediction (simplified) |
| Code Gen | `replicate_generate_code` | Generate code |
| Code Gen | `replicate_optimize_code` | Optimize code |
| Code Gen | `replicate_debug_code` | Debug code |
| Code Gen | `replicate_generate_dockerfile` | Generate Dockerfile |
| Code Gen | `replicate_generate_requirements` | Generate requirements |

## 🧪 Testing

### Test Coverage:
- ✅ All 15 tools tested individually
- ✅ Authentication system tested
- ✅ Configuration system tested
- ✅ Error handling tested
- ✅ Integration scenarios tested

### Run Tests:
```bash
python -m pytest tests/test_replicate_tools.py -v
```

## 📚 Documentation

### Complete Documentation Includes:
- Installation and setup instructions
- Authentication configuration
- Usage examples for all tools
- Integration guides
- Configuration options
- Error handling examples
- Contributing guidelines

## 🔐 Security Features

- Secure token management
- Token validation
- Error message sanitization
- Environment variable support
- Multiple token isolation

## 🎨 Frontend Integration

### TypeScript Definitions (`seeds/replicate.ts`)
- Complete tool definitions for frontend
- Form field configurations
- Multi-language support (EN/FR)
- Plan availability settings
- Proper categorization

## 🔄 Migration & Compatibility

- Follows existing agent tool patterns
- Compatible with current architecture
- No breaking changes to existing code
- Backward compatible authentication

## 📋 Checklist

- [x] Code follows project standards and patterns
- [x] All 15 tools implemented and tested
- [x] Comprehensive test suite added
- [x] Documentation updated and complete
- [x] TypeScript definitions included
- [x] Integration examples provided
- [x] Error handling implemented
- [x] Authentication system added
- [x] Configuration system added
- [x] LangChain compatibility verified
- [x] Environment variable support added
- [x] Multi-token management implemented

## 🚀 Ready for Production

This implementation is production-ready with:
- Comprehensive error handling
- Full test coverage
- Complete documentation
- Secure authentication
- Flexible configuration
- LangChain integration
- TypeScript definitions

## 🔗 Related Issues

This PR addresses the need for comprehensive Replicate integration with:
- Model management capabilities
- Prediction execution and monitoring
- AI-powered code generation tools
- Enterprise-grade authentication
- Flexible configuration system

## 👥 Review Notes

- All tools follow the established pattern from existing agent tools
- Comprehensive error handling and validation implemented
- Full TypeScript definitions for seamless frontend integration
- Ready for immediate production deployment
- Extensive documentation and examples provided
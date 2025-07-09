"""
Replicate Agent Tools

This package provides comprehensive tools for interacting with Replicate's API,
including model management, prediction execution, and AI-powered code generation.

Features:
- Model Management: List, get, create, and manage models
- Predictions: Create, monitor, and manage predictions
- Code Generation: Generate, optimize, and debug code using AI models
"""

from .replicate_tools import create_replicate_tools
from .models import (
    list_models_replicate,
    get_model_replicate,
    create_model_replicate,
    get_model_versions_replicate,
    get_model_version_replicate
)
from .predictions import (
    create_prediction_replicate,
    get_prediction_replicate,
    list_predictions_replicate,
    cancel_prediction_replicate,
    run_prediction_replicate
)
from .code_generation import (
    generate_code_replicate,
    optimize_code_replicate,
    debug_code_replicate,
    generate_dockerfile_replicate,
    generate_requirements_replicate
)

__all__ = [
    'create_replicate_tools',
    'list_models_replicate',
    'get_model_replicate',
    'create_model_replicate',
    'get_model_versions_replicate',
    'get_model_version_replicate',
    'create_prediction_replicate',
    'get_prediction_replicate',
    'list_predictions_replicate',
    'cancel_prediction_replicate',
    'run_prediction_replicate',
    'generate_code_replicate',
    'optimize_code_replicate',
    'debug_code_replicate',
    'generate_dockerfile_replicate',
    'generate_requirements_replicate'
]
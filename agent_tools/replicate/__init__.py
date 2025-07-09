"""
Replicate Agent Tools Package

This package provides comprehensive tools for interacting with Replicate's API,
including model management, prediction execution, and AI code generation.
"""

from .replicate_tools import create_replicate_tools
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

__version__ = "1.0.0"
__author__ = "Jonathan Toky"
__email__ = "jonathan@example.com"

__all__ = [
    'create_replicate_tools',
    'list_replicate_models',
    'get_replicate_model',
    'create_replicate_model',
    'update_replicate_model',
    'delete_replicate_model',
    'create_replicate_prediction',
    'get_replicate_prediction',
    'cancel_replicate_prediction',
    'list_replicate_predictions',
    'stream_replicate_prediction',
    'generate_code_replicate',
    'optimize_code_replicate',
    'debug_code_replicate',
    'explain_code_replicate',
    'convert_code_replicate'
]
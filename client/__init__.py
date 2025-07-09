"""
Replicate Client Package

This package provides authentication, configuration, and client utilities
for interacting with the Replicate API.
"""

from .replicate_auth import (
    ReplicateClient,
    ReplicateAuthError,
    ReplicateConfig as AuthConfig,
    ReplicateTokenManager,
    create_replicate_client,
    get_token_from_env,
    validate_replicate_token,
    require_replicate_auth
)

from .config import (
    ReplicateConfig,
    ReplicateAPIConfig,
    ReplicateModelConfig,
    ReplicatePredictionConfig,
    ReplicateCodeConfig,
    DEFAULT_CONFIG,
    ENV_CONFIG,
    get_config,
    update_config,
    validate_config
)

__all__ = [
    # Authentication
    'ReplicateClient',
    'ReplicateAuthError',
    'AuthConfig',
    'ReplicateTokenManager',
    'create_replicate_client',
    'get_token_from_env',
    'validate_replicate_token',
    'require_replicate_auth',
    
    # Configuration
    'ReplicateConfig',
    'ReplicateAPIConfig',
    'ReplicateModelConfig',
    'ReplicatePredictionConfig',
    'ReplicateCodeConfig',
    'DEFAULT_CONFIG',
    'ENV_CONFIG',
    'get_config',
    'update_config',
    'validate_config'
]

# Version information
__version__ = "1.0.0"
__author__ = "Replicate Agent Tools"
__description__ = "Client utilities for Replicate API integration"
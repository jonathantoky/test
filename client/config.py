"""
Configuration for Replicate Client

This module contains configuration settings and utilities for the Replicate client.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ReplicateAPIConfig:
    """Configuration for Replicate API settings"""
    base_url: str = "https://api.replicate.com/v1"
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    max_retry_delay: float = 60.0
    backoff_factor: float = 2.0


@dataclass
class ReplicateModelConfig:
    """Configuration for default model settings"""
    default_model: str = "meta/codellama-34b-instruct"
    code_generation_model: str = "meta/codellama-34b-instruct"
    text_generation_model: str = "meta/llama-2-70b-chat"
    image_generation_model: str = "stability-ai/stable-diffusion"
    max_tokens: int = 2000
    temperature: float = 0.1
    top_p: float = 0.9


@dataclass
class ReplicatePredictionConfig:
    """Configuration for prediction settings"""
    default_webhook_events: list = field(default_factory=lambda: ["start", "output", "logs", "completed"])
    max_prediction_time: int = 300  # 5 minutes
    polling_interval: float = 1.0
    max_polling_attempts: int = 300


@dataclass
class ReplicateCodeConfig:
    """Configuration for code generation settings"""
    supported_languages: list = field(default_factory=lambda: [
        "python", "javascript", "typescript", "java", "c++", "c", "go", 
        "rust", "php", "ruby", "swift", "kotlin", "scala", "r", "sql"
    ])
    default_language: str = "python"
    code_optimization_goals: list = field(default_factory=lambda: [
        "performance", "readability", "maintainability", "security", "memory_usage"
    ])
    dockerfile_base_images: Dict[str, str] = field(default_factory=lambda: {
        "python": "python:3.9-slim",
        "node": "node:16-alpine",
        "java": "openjdk:11-jre-slim",
        "go": "golang:1.19-alpine",
        "rust": "rust:1.70-slim"
    })


@dataclass
class ReplicateConfig:
    """Main configuration class for Replicate client"""
    api: ReplicateAPIConfig = field(default_factory=ReplicateAPIConfig)
    model: ReplicateModelConfig = field(default_factory=ReplicateModelConfig)
    prediction: ReplicatePredictionConfig = field(default_factory=ReplicatePredictionConfig)
    code: ReplicateCodeConfig = field(default_factory=ReplicateCodeConfig)
    
    # Environment settings
    debug: bool = False
    log_level: str = "INFO"
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour
    
    @classmethod
    def from_env(cls) -> 'ReplicateConfig':
        """Create configuration from environment variables"""
        config = cls()
        
        # API configuration
        if os.getenv("REPLICATE_BASE_URL"):
            config.api.base_url = os.getenv("REPLICATE_BASE_URL")
        
        if os.getenv("REPLICATE_TIMEOUT"):
            config.api.timeout = int(os.getenv("REPLICATE_TIMEOUT"))
        
        if os.getenv("REPLICATE_MAX_RETRIES"):
            config.api.max_retries = int(os.getenv("REPLICATE_MAX_RETRIES"))
        
        # Model configuration
        if os.getenv("REPLICATE_DEFAULT_MODEL"):
            config.model.default_model = os.getenv("REPLICATE_DEFAULT_MODEL")
        
        if os.getenv("REPLICATE_CODE_MODEL"):
            config.model.code_generation_model = os.getenv("REPLICATE_CODE_MODEL")
        
        if os.getenv("REPLICATE_MAX_TOKENS"):
            config.model.max_tokens = int(os.getenv("REPLICATE_MAX_TOKENS"))
        
        if os.getenv("REPLICATE_TEMPERATURE"):
            config.model.temperature = float(os.getenv("REPLICATE_TEMPERATURE"))
        
        # Debug settings
        if os.getenv("REPLICATE_DEBUG"):
            config.debug = os.getenv("REPLICATE_DEBUG").lower() == "true"
        
        if os.getenv("REPLICATE_LOG_LEVEL"):
            config.log_level = os.getenv("REPLICATE_LOG_LEVEL")
        
        # Cache settings
        if os.getenv("REPLICATE_CACHE_ENABLED"):
            config.cache_enabled = os.getenv("REPLICATE_CACHE_ENABLED").lower() == "true"
        
        if os.getenv("REPLICATE_CACHE_TTL"):
            config.cache_ttl = int(os.getenv("REPLICATE_CACHE_TTL"))
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "api": {
                "base_url": self.api.base_url,
                "timeout": self.api.timeout,
                "max_retries": self.api.max_retries,
                "retry_delay": self.api.retry_delay,
                "max_retry_delay": self.api.max_retry_delay,
                "backoff_factor": self.api.backoff_factor
            },
            "model": {
                "default_model": self.model.default_model,
                "code_generation_model": self.model.code_generation_model,
                "text_generation_model": self.model.text_generation_model,
                "image_generation_model": self.model.image_generation_model,
                "max_tokens": self.model.max_tokens,
                "temperature": self.model.temperature,
                "top_p": self.model.top_p
            },
            "prediction": {
                "default_webhook_events": self.prediction.default_webhook_events,
                "max_prediction_time": self.prediction.max_prediction_time,
                "polling_interval": self.prediction.polling_interval,
                "max_polling_attempts": self.prediction.max_polling_attempts
            },
            "code": {
                "supported_languages": self.code.supported_languages,
                "default_language": self.code.default_language,
                "code_optimization_goals": self.code.code_optimization_goals,
                "dockerfile_base_images": self.code.dockerfile_base_images
            },
            "debug": self.debug,
            "log_level": self.log_level,
            "cache_enabled": self.cache_enabled,
            "cache_ttl": self.cache_ttl
        }


# Default configuration instance
DEFAULT_CONFIG = ReplicateConfig()

# Environment-based configuration
ENV_CONFIG = ReplicateConfig.from_env()


def get_config(use_env: bool = True) -> ReplicateConfig:
    """
    Get configuration instance
    
    Args:
        use_env (bool): Whether to use environment-based configuration
    
    Returns:
        ReplicateConfig: Configuration instance
    """
    return ENV_CONFIG if use_env else DEFAULT_CONFIG


def update_config(config: ReplicateConfig, **kwargs) -> ReplicateConfig:
    """
    Update configuration with provided values
    
    Args:
        config (ReplicateConfig): Base configuration
        **kwargs: Configuration updates
    
    Returns:
        ReplicateConfig: Updated configuration
    """
    # Create a copy of the config
    import copy
    new_config = copy.deepcopy(config)
    
    # Update API settings
    if "api" in kwargs:
        for key, value in kwargs["api"].items():
            if hasattr(new_config.api, key):
                setattr(new_config.api, key, value)
    
    # Update model settings
    if "model" in kwargs:
        for key, value in kwargs["model"].items():
            if hasattr(new_config.model, key):
                setattr(new_config.model, key, value)
    
    # Update prediction settings
    if "prediction" in kwargs:
        for key, value in kwargs["prediction"].items():
            if hasattr(new_config.prediction, key):
                setattr(new_config.prediction, key, value)
    
    # Update code settings
    if "code" in kwargs:
        for key, value in kwargs["code"].items():
            if hasattr(new_config.code, key):
                setattr(new_config.code, key, value)
    
    # Update top-level settings
    for key in ["debug", "log_level", "cache_enabled", "cache_ttl"]:
        if key in kwargs:
            setattr(new_config, key, kwargs[key])
    
    return new_config


# Configuration validation
def validate_config(config: ReplicateConfig) -> bool:
    """
    Validate configuration settings
    
    Args:
        config (ReplicateConfig): Configuration to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Validate API settings
        assert config.api.timeout > 0, "API timeout must be positive"
        assert config.api.max_retries >= 0, "Max retries must be non-negative"
        assert config.api.base_url.startswith("http"), "Base URL must be HTTP/HTTPS"
        
        # Validate model settings
        assert config.model.max_tokens > 0, "Max tokens must be positive"
        assert 0 <= config.model.temperature <= 2, "Temperature must be between 0 and 2"
        assert 0 <= config.model.top_p <= 1, "Top-p must be between 0 and 1"
        
        # Validate prediction settings
        assert config.prediction.max_prediction_time > 0, "Max prediction time must be positive"
        assert config.prediction.polling_interval > 0, "Polling interval must be positive"
        assert config.prediction.max_polling_attempts > 0, "Max polling attempts must be positive"
        
        # Validate code settings
        assert config.code.default_language in config.code.supported_languages, \
            "Default language must be in supported languages"
        
        return True
        
    except AssertionError as e:
        print(f"Configuration validation failed: {e}")
        return False


# Example usage
if __name__ == "__main__":
    # Test configuration
    print("Testing Replicate configuration...")
    
    # Default configuration
    default_config = get_config(use_env=False)
    print(f"Default configuration valid: {validate_config(default_config)}")
    
    # Environment configuration
    env_config = get_config(use_env=True)
    print(f"Environment configuration valid: {validate_config(env_config)}")
    
    # Print configuration
    print("\nConfiguration:")
    import json
    print(json.dumps(env_config.to_dict(), indent=2))
    
    # Test configuration update
    updated_config = update_config(
        env_config,
        model={"temperature": 0.5, "max_tokens": 1000},
        debug=True
    )
    print(f"\nUpdated configuration valid: {validate_config(updated_config)}")
    print(f"Updated temperature: {updated_config.model.temperature}")
    print(f"Updated debug: {updated_config.debug}")
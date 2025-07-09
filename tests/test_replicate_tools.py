"""
Test suite for Replicate Agent Tools

This module contains comprehensive tests for all Replicate tools including
model management, predictions, and code generation.
"""

import pytest
import os
import json
from unittest.mock import Mock, patch, MagicMock
import requests_mock

# Import the tools
from agent_tools.replicate.replicate_tools import create_replicate_tools
from agent_tools.replicate.models import (
    list_replicate_models, get_replicate_model, create_replicate_model,
    update_replicate_model, delete_replicate_model
)
from agent_tools.replicate.predictions import (
    create_replicate_prediction, get_replicate_prediction, cancel_replicate_prediction,
    list_replicate_predictions, stream_replicate_prediction
)
from agent_tools.replicate.code_generation import (
    generate_code_replicate, optimize_code_replicate, debug_code_replicate,
    explain_code_replicate, convert_code_replicate
)
from client.replicate_client import ReplicateClient, validate_api_token


class TestReplicateTools:
    """Test suite for Replicate tools factory"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_token = "test_token_123"
        self.test_name = "test_replicate"
        self.test_description = "Test Replicate tools"
    
    def test_create_replicate_tools(self):
        """Test creating all Replicate tools"""
        tools = create_replicate_tools(self.test_name, self.test_token, self.test_description)
        
        # Should return 15 tools total (5 model + 5 prediction + 5 code generation)
        assert len(tools) == 15
        
        # Check tool names
        tool_names = [tool.name for tool in tools]
        expected_names = [
            f"{self.test_name}_list_models",
            f"{self.test_name}_get_model",
            f"{self.test_name}_create_model",
            f"{self.test_name}_update_model",
            f"{self.test_name}_delete_model",
            f"{self.test_name}_create_prediction",
            f"{self.test_name}_get_prediction",
            f"{self.test_name}_cancel_prediction",
            f"{self.test_name}_list_predictions",
            f"{self.test_name}_stream_prediction",
            f"{self.test_name}_generate_code",
            f"{self.test_name}_optimize_code",
            f"{self.test_name}_debug_code",
            f"{self.test_name}_explain_code",
            f"{self.test_name}_convert_code"
        ]
        
        for expected_name in expected_names:
            assert expected_name in tool_names


class TestModelTools:
    """Test suite for model management tools"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_token = "test_token_123"
        self.base_url = "https://api.replicate.com/v1"
    
    @requests_mock.Mocker()
    def test_list_models_success(self, m):
        """Test listing models successfully"""
        # Mock API response
        mock_response = {
            "results": [
                {
                    "owner": "test_owner",
                    "name": "test_model",
                    "description": "Test model description",
                    "visibility": "public",
                    "url": "https://replicate.com/test_owner/test_model"
                }
            ],
            "next": None
        }
        
        m.get(f"{self.base_url}/models", json=mock_response)
        
        # Create and run tool
        tool = list_replicate_models("test_list_models", "Test description", self.test_token)
        result = tool.run({})
        
        assert "Found 1 models" in result
        assert "test_owner/test_model" in result
        assert "Test model description" in result
    
    @requests_mock.Mocker()
    def test_get_model_success(self, m):
        """Test getting specific model successfully"""
        mock_response = {
            "owner": "test_owner",
            "name": "test_model",
            "description": "Test model description",
            "visibility": "public",
            "github_url": "https://github.com/test/repo",
            "latest_version": {
                "id": "version_123",
                "created_at": "2023-01-01T00:00:00Z",
                "cog_version": "0.8.0"
            }
        }
        
        m.get(f"{self.base_url}/models/test_owner/test_model", json=mock_response)
        
        tool = get_replicate_model("test_get_model", "Test description", self.test_token)
        result = tool.run({"model_owner": "test_owner", "model_name": "test_model"})
        
        assert "Model: test_owner/test_model" in result
        assert "Test model description" in result
        assert "Latest Version:" in result
    
    @requests_mock.Mocker()
    def test_create_model_success(self, m):
        """Test creating model successfully"""
        mock_response = {
            "owner": "test_owner",
            "name": "new_model",
            "url": "https://replicate.com/test_owner/new_model",
            "visibility": "private"
        }
        
        m.post(f"{self.base_url}/models", json=mock_response, status_code=201)
        
        tool = create_replicate_model("test_create_model", "Test description", self.test_token)
        result = tool.run({
            "model_name": "new_model",
            "visibility": "private",
            "hardware": "gpu-t4",
            "description": "New test model"
        })
        
        assert "Model created successfully!" in result
        assert "test_owner/new_model" in result


class TestPredictionTools:
    """Test suite for prediction management tools"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_token = "test_token_123"
        self.base_url = "https://api.replicate.com/v1"
    
    @requests_mock.Mocker()
    def test_create_prediction_success(self, m):
        """Test creating prediction successfully"""
        mock_response = {
            "id": "prediction_123",
            "status": "starting",
            "model": "test_owner/test_model",
            "version": "version_123",
            "created_at": "2023-01-01T00:00:00Z",
            "urls": {
                "get": "https://api.replicate.com/v1/predictions/prediction_123",
                "cancel": "https://api.replicate.com/v1/predictions/prediction_123/cancel"
            }
        }
        
        m.post(f"{self.base_url}/predictions", json=mock_response, status_code=201)
        
        tool = create_replicate_prediction("test_create_prediction", "Test description", self.test_token)
        result = tool.run({
            "model_version": "version_123",
            "input_data": {"prompt": "Hello world"}
        })
        
        assert "Prediction created successfully!" in result
        assert "prediction_123" in result
        assert "starting" in result
    
    @requests_mock.Mocker()
    def test_get_prediction_success(self, m):
        """Test getting prediction successfully"""
        mock_response = {
            "id": "prediction_123",
            "status": "succeeded",
            "model": "test_owner/test_model",
            "version": "version_123",
            "created_at": "2023-01-01T00:00:00Z",
            "started_at": "2023-01-01T00:00:01Z",
            "completed_at": "2023-01-01T00:00:10Z",
            "input": {"prompt": "Hello world"},
            "output": ["Hello! How can I help you today?"],
            "logs": "Processing...",
            "metrics": {"predict_time": 9.0}
        }
        
        m.get(f"{self.base_url}/predictions/prediction_123", json=mock_response)
        
        tool = get_replicate_prediction("test_get_prediction", "Test description", self.test_token)
        result = tool.run({"prediction_id": "prediction_123"})
        
        assert "Prediction Details:" in result
        assert "prediction_123" in result
        assert "succeeded" in result
        assert "Hello! How can I help you today?" in result


class TestCodeGenerationTools:
    """Test suite for code generation tools"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_token = "test_token_123"
        self.base_url = "https://api.replicate.com/v1"
    
    @requests_mock.Mocker()
    def test_generate_code_success(self, m):
        """Test code generation successfully"""
        # Mock prediction creation
        create_response = {
            "id": "prediction_123",
            "status": "starting"
        }
        m.post(f"{self.base_url}/predictions", json=create_response, status_code=201)
        
        # Mock prediction status check
        status_response = {
            "id": "prediction_123",
            "status": "succeeded",
            "output": ["def hello_world():\n    print('Hello, World!')\n    return 'Hello, World!'"]
        }
        m.get(f"{self.base_url}/predictions/prediction_123", json=status_response)
        
        tool = generate_code_replicate("test_generate_code", "Test description", self.test_token)
        result = tool.run({
            "prompt": "Create a hello world function",
            "language": "python"
        })
        
        assert "Generated python code:" in result
        assert "def hello_world():" in result
        assert "Generation completed successfully!" in result
    
    @requests_mock.Mocker()
    def test_optimize_code_success(self, m):
        """Test code optimization successfully"""
        # Mock prediction creation
        create_response = {
            "id": "prediction_123",
            "status": "starting"
        }
        m.post(f"{self.base_url}/predictions", json=create_response, status_code=201)
        
        # Mock prediction status check
        status_response = {
            "id": "prediction_123",
            "status": "succeeded",
            "output": ["Optimized code:\n\ndef optimized_function():\n    # More efficient implementation\n    pass"]
        }
        m.get(f"{self.base_url}/predictions/prediction_123", json=status_response)
        
        tool = optimize_code_replicate("test_optimize_code", "Test description", self.test_token)
        result = tool.run({
            "code": "def slow_function(): pass",
            "language": "python",
            "optimization_focus": "performance"
        })
        
        assert "Code Optimization Results (performance):" in result
        assert "Optimized code:" in result
        assert "Optimization completed successfully!" in result


class TestReplicateClient:
    """Test suite for Replicate client"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_token = "test_token_123"
    
    def test_client_initialization(self):
        """Test client initialization"""
        client = ReplicateClient(self.test_token)
        assert client.api_token == self.test_token
        assert client.base_url == "https://api.replicate.com/v1"
        assert "Authorization" in client.headers
        assert f"Token {self.test_token}" in client.headers["Authorization"]
    
    def test_client_initialization_no_token(self):
        """Test client initialization without token"""
        with pytest.raises(ValueError, match="Replicate API token is required"):
            ReplicateClient()
    
    @requests_mock.Mocker()
    def test_validate_api_token_success(self, m):
        """Test API token validation success"""
        m.get("https://api.replicate.com/v1/models", json={"results": []})
        
        result = validate_api_token(self.test_token)
        assert result is True
    
    @requests_mock.Mocker()
    def test_validate_api_token_failure(self, m):
        """Test API token validation failure"""
        m.get("https://api.replicate.com/v1/models", status_code=401)
        
        result = validate_api_token(self.test_token)
        assert result is False


class TestIntegration:
    """Integration tests for Replicate tools"""
    
    def setup_method(self):
        """Setup test environment"""
        self.test_token = "test_token_123"
    
    def test_tool_creation_and_execution(self):
        """Test creating and executing tools"""
        tools = create_replicate_tools("integration_test", self.test_token)
        
        # Verify all tools are created
        assert len(tools) == 15
        
        # Verify tools have correct structure
        for tool in tools:
            assert hasattr(tool, 'name')
            assert hasattr(tool, 'description')
            assert hasattr(tool, 'args_schema')
            assert hasattr(tool, 'run')
    
    @patch('requests.get')
    def test_error_handling(self, mock_get):
        """Test error handling in tools"""
        # Mock API error
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response
        
        tool = list_replicate_models("test_error", "Test description", self.test_token)
        result = tool.run({})
        
        assert "Error listing models: 500" in result


# Test fixtures and utilities
@pytest.fixture
def mock_replicate_api():
    """Fixture for mocking Replicate API"""
    with requests_mock.Mocker() as m:
        # Mock common endpoints
        m.get("https://api.replicate.com/v1/models", json={"results": []})
        m.get("https://api.replicate.com/v1/predictions", json={"results": []})
        yield m


@pytest.fixture
def sample_model_data():
    """Fixture for sample model data"""
    return {
        "owner": "test_owner",
        "name": "test_model",
        "description": "Test model for unit tests",
        "visibility": "public",
        "github_url": "https://github.com/test/repo",
        "latest_version": {
            "id": "version_123",
            "created_at": "2023-01-01T00:00:00Z"
        }
    }


@pytest.fixture
def sample_prediction_data():
    """Fixture for sample prediction data"""
    return {
        "id": "prediction_123",
        "status": "succeeded",
        "model": "test_owner/test_model",
        "version": "version_123",
        "created_at": "2023-01-01T00:00:00Z",
        "input": {"prompt": "test prompt"},
        "output": ["test output"]
    }


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
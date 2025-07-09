"""
Test file for Replicate agent tools

This file contains comprehensive tests for all Replicate tools including:
- Model management
- Prediction execution
- Code generation features
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from agent_tools.replicate.replicate_tools import create_replicate_tools
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


class TestReplicateTools:
    """Test class for Replicate tools functionality"""

    def setup_method(self):
        """Setup test fixtures"""
        self.test_token = "test_replicate_token"
        self.test_name = "test_replicate"
        self.mock_client = Mock()

    @patch('agent_tools.replicate.models.replicate.Client')
    @patch('agent_tools.replicate.models.extract_token_from_data')
    def test_list_models_replicate(self, mock_extract_token, mock_client_class):
        """Test listing models on Replicate"""
        # Setup mocks
        mock_extract_token.return_value = self.test_token
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock model data
        mock_model = Mock()
        mock_model.owner = "test_owner"
        mock_model.name = "test_model"
        mock_model.description = "Test model description"
        mock_model.visibility = "public"
        mock_model.github_url = "https://github.com/test/repo"
        mock_model.paper_url = None
        mock_model.license_url = None
        mock_model.cover_image_url = None
        mock_model.created_at = None
        mock_model.updated_at = None
        
        mock_client.models.list.return_value = [mock_model]
        
        # Create tool and test
        tool = list_models_replicate(self.test_name, "Test description", self.test_token)
        result = tool.func()
        
        # Verify result
        assert isinstance(result, str)
        result_data = json.loads(result)
        assert len(result_data) == 1
        assert result_data[0]["owner"] == "test_owner"
        assert result_data[0]["name"] == "test_model"

    @patch('agent_tools.replicate.models.replicate.Client')
    @patch('agent_tools.replicate.models.extract_token_from_data')
    def test_get_model_replicate(self, mock_extract_token, mock_client_class):
        """Test getting a specific model on Replicate"""
        # Setup mocks
        mock_extract_token.return_value = self.test_token
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock model data
        mock_model = Mock()
        mock_model.owner = "test_owner"
        mock_model.name = "test_model"
        mock_model.description = "Test model description"
        mock_model.visibility = "public"
        mock_model.github_url = "https://github.com/test/repo"
        mock_model.paper_url = None
        mock_model.license_url = None
        mock_model.cover_image_url = None
        mock_model.created_at = None
        mock_model.updated_at = None
        mock_model.latest_version = None
        
        mock_client.models.get.return_value = mock_model
        
        # Create tool and test
        tool = get_model_replicate(self.test_name, "Test description", self.test_token)
        result = tool.func("test_owner", "test_model")
        
        # Verify result
        assert isinstance(result, str)
        result_data = json.loads(result)
        assert result_data["owner"] == "test_owner"
        assert result_data["name"] == "test_model"

    @patch('agent_tools.replicate.predictions.replicate.Client')
    @patch('agent_tools.replicate.predictions.extract_token_from_data')
    def test_create_prediction_replicate(self, mock_extract_token, mock_client_class):
        """Test creating a prediction on Replicate"""
        # Setup mocks
        mock_extract_token.return_value = self.test_token
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock prediction data
        mock_prediction = Mock()
        mock_prediction.id = "test_prediction_id"
        mock_prediction.version = "test_version"
        mock_prediction.status = "starting"
        mock_prediction.input = {"prompt": "test prompt"}
        mock_prediction.output = None
        mock_prediction.error = None
        mock_prediction.logs = ""
        mock_prediction.metrics = {}
        mock_prediction.created_at = None
        mock_prediction.started_at = None
        mock_prediction.completed_at = None
        mock_prediction.urls = {}
        
        mock_client.predictions.create.return_value = mock_prediction
        
        # Create tool and test
        tool = create_prediction_replicate(self.test_name, "Test description", self.test_token)
        result = tool.func("test_version", {"prompt": "test prompt"})
        
        # Verify result
        assert isinstance(result, str)
        result_data = json.loads(result)
        assert result_data["id"] == "test_prediction_id"
        assert result_data["status"] == "starting"

    @patch('agent_tools.replicate.predictions.replicate.Client')
    @patch('agent_tools.replicate.predictions.extract_token_from_data')
    def test_run_prediction_replicate(self, mock_extract_token, mock_client_class):
        """Test running a prediction with simplified interface"""
        # Setup mocks
        mock_extract_token.return_value = self.test_token
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock output
        mock_output = ["Generated", " code", " here"]
        mock_client.run.return_value = mock_output
        
        # Create tool and test
        tool = run_prediction_replicate(self.test_name, "Test description", self.test_token)
        result = tool.func("owner/model", {"prompt": "test prompt"}, True)
        
        # Verify result
        assert isinstance(result, str)
        result_data = json.loads(result)
        assert "output" in result_data
        assert result_data["output"] == mock_output

    @patch('agent_tools.replicate.code_generation.replicate.Client')
    @patch('agent_tools.replicate.code_generation.extract_token_from_data')
    def test_generate_code_replicate(self, mock_extract_token, mock_client_class):
        """Test code generation using Replicate"""
        # Setup mocks
        mock_extract_token.return_value = self.test_token
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock code generation output
        mock_output = ["def hello_world():", "\n    print('Hello, World!')"]
        mock_client.run.return_value = mock_output
        
        # Create tool and test
        tool = generate_code_replicate(self.test_name, "Test description", self.test_token)
        result = tool.func("Create a hello world function")
        
        # Verify result
        assert isinstance(result, str)
        result_data = json.loads(result)
        assert result_data["language"] == "python"
        assert result_data["prompt"] == "Create a hello world function"
        assert "generated_code" in result_data

    @patch('agent_tools.replicate.code_generation.replicate.Client')
    @patch('agent_tools.replicate.code_generation.extract_token_from_data')
    def test_optimize_code_replicate(self, mock_extract_token, mock_client_class):
        """Test code optimization using Replicate"""
        # Setup mocks
        mock_extract_token.return_value = self.test_token
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock optimization output
        mock_output = ["Optimized code with improvements..."]
        mock_client.run.return_value = mock_output
        
        # Create tool and test
        tool = optimize_code_replicate(self.test_name, "Test description", self.test_token)
        result = tool.func("def slow_function(): pass")
        
        # Verify result
        assert isinstance(result, str)
        result_data = json.loads(result)
        assert result_data["language"] == "python"
        assert result_data["original_code"] == "def slow_function(): pass"
        assert "optimized_result" in result_data

    @patch('agent_tools.replicate.code_generation.replicate.Client')
    @patch('agent_tools.replicate.code_generation.extract_token_from_data')
    def test_debug_code_replicate(self, mock_extract_token, mock_client_class):
        """Test code debugging using Replicate"""
        # Setup mocks
        mock_extract_token.return_value = self.test_token
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock debug output
        mock_output = ["Fixed code with bug explanations..."]
        mock_client.run.return_value = mock_output
        
        # Create tool and test
        tool = debug_code_replicate(self.test_name, "Test description", self.test_token)
        result = tool.func("def buggy_function(): print(undefined_var)", "NameError: name 'undefined_var' is not defined")
        
        # Verify result
        assert isinstance(result, str)
        result_data = json.loads(result)
        assert result_data["language"] == "python"
        assert "debug_result" in result_data
        assert result_data["error_message"] == "NameError: name 'undefined_var' is not defined"

    @patch('agent_tools.replicate.code_generation.replicate.Client')
    @patch('agent_tools.replicate.code_generation.extract_token_from_data')
    def test_generate_dockerfile_replicate(self, mock_extract_token, mock_client_class):
        """Test Dockerfile generation using Replicate"""
        # Setup mocks
        mock_extract_token.return_value = self.test_token
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock Dockerfile output
        mock_output = ["FROM python:3.9\nCOPY . /app\nWORKDIR /app\nRUN pip install -r requirements.txt\nEXPOSE 8000\nCMD ['python', 'app.py']"]
        mock_client.run.return_value = mock_output
        
        # Create tool and test
        tool = generate_dockerfile_replicate(self.test_name, "Test description", self.test_token)
        result = tool.func("A Python web application")
        
        # Verify result
        assert isinstance(result, str)
        result_data = json.loads(result)
        assert result_data["project_description"] == "A Python web application"
        assert result_data["language"] == "python"
        assert result_data["port"] == 8000
        assert "dockerfile" in result_data

    @patch('agent_tools.replicate.code_generation.replicate.Client')
    @patch('agent_tools.replicate.code_generation.extract_token_from_data')
    def test_generate_requirements_replicate(self, mock_extract_token, mock_client_class):
        """Test requirements.txt generation using Replicate"""
        # Setup mocks
        mock_extract_token.return_value = self.test_token
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock requirements output
        mock_output = ["flask==2.0.1\nrequests==2.25.1\nnumpy==1.21.0"]
        mock_client.run.return_value = mock_output
        
        # Create tool and test
        tool = generate_requirements_replicate(self.test_name, "Test description", self.test_token)
        result = tool.func("import flask\nimport requests\nimport numpy as np")
        
        # Verify result
        assert isinstance(result, str)
        result_data = json.loads(result)
        assert result_data["language"] == "python"
        assert "requirements" in result_data
        assert "analyzed_code" in result_data

    def test_create_replicate_tools(self):
        """Test creating all Replicate tools"""
        tools = create_replicate_tools(self.test_name, self.test_token)
        
        # Verify all tools are created
        assert len(tools) == 15  # Total number of tools
        
        # Verify tool names
        tool_names = [tool.name for tool in tools]
        expected_names = [
            f"{self.test_name}_list_models",
            f"{self.test_name}_get_model",
            f"{self.test_name}_create_model",
            f"{self.test_name}_get_model_versions",
            f"{self.test_name}_get_model_version",
            f"{self.test_name}_create_prediction",
            f"{self.test_name}_get_prediction",
            f"{self.test_name}_list_predictions",
            f"{self.test_name}_cancel_prediction",
            f"{self.test_name}_run_prediction",
            f"{self.test_name}_generate_code",
            f"{self.test_name}_optimize_code",
            f"{self.test_name}_debug_code",
            f"{self.test_name}_generate_dockerfile",
            f"{self.test_name}_generate_requirements"
        ]
        
        for expected_name in expected_names:
            assert expected_name in tool_names


class TestReplicateToolsIntegration:
    """Integration tests for Replicate tools"""

    def test_tool_error_handling(self):
        """Test error handling in tools"""
        # Test with invalid token
        with patch('agent_tools.replicate.models.extract_token_from_data') as mock_extract:
            mock_extract.return_value = "invalid_token"
            
            with patch('agent_tools.replicate.models.replicate.Client') as mock_client_class:
                mock_client = Mock()
                mock_client_class.return_value = mock_client
                mock_client.models.list.side_effect = Exception("Invalid token")
                
                tool = list_models_replicate("test", "Test", "invalid_token")
                result = tool.func()
                
                assert "Failed to list models" in result
                assert "Invalid token" in result

    def test_tool_descriptions(self):
        """Test that tools have proper descriptions"""
        tools = create_replicate_tools("test", "test_token")
        
        for tool in tools:
            assert hasattr(tool, 'description')
            assert tool.description is not None
            assert len(tool.description) > 0


if __name__ == "__main__":
    pytest.main([__file__])
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json
import replicate
from .. import extract_token_from_data


# Generate Code Tool
class GenerateCodeInput(BaseModel):
    prompt: str = Field(description="Description of the code to generate")
    language: Optional[str] = Field("python", description="Programming language for the code")
    model: Optional[str] = Field("meta/codellama-34b-instruct", description="Model to use for code generation")
    max_tokens: Optional[int] = Field(2000, description="Maximum number of tokens to generate")
    temperature: Optional[float] = Field(0.1, description="Temperature for generation (0.0 to 1.0)")


def generate_code_replicate(name, description, token):
    """Generates code using Replicate AI models."""
    tool_description = description or "Generate code using Replicate AI models"

    def generate_code(prompt: str, language: Optional[str] = "python", 
                     model: Optional[str] = "meta/codellama-34b-instruct",
                     max_tokens: Optional[int] = 2000, 
                     temperature: Optional[float] = 0.1) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # Prepare the prompt for code generation
            code_prompt = f"Generate {language} code for the following task:\n\n{prompt}\n\nCode:"
            
            # Generate code using the specified model
            output = client.run(
                model,
                input={
                    "prompt": code_prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": 0.9,
                    "stop_sequences": ["</code>", "```"]
                }
            )
            
            # Format the response
            if isinstance(output, list):
                generated_code = "".join(output)
            else:
                generated_code = str(output)
            
            result = {
                "language": language,
                "prompt": prompt,
                "generated_code": generated_code.strip(),
                "model_used": model
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Failed to generate code: {str(e)}"

    return StructuredTool.from_function(
        func=generate_code,
        name=name,
        description=tool_description,
        args_schema=GenerateCodeInput,
        return_direct=True
    )


# Optimize Code Tool
class OptimizeCodeInput(BaseModel):
    code: str = Field(description="Code to optimize")
    language: Optional[str] = Field("python", description="Programming language of the code")
    optimization_goals: Optional[str] = Field("performance and readability", description="Optimization goals")
    model: Optional[str] = Field("meta/codellama-34b-instruct", description="Model to use for code optimization")
    max_tokens: Optional[int] = Field(2000, description="Maximum number of tokens to generate")


def optimize_code_replicate(name, description, token):
    """Optimizes existing code using Replicate AI models."""
    tool_description = description or "Optimize existing code using Replicate AI models"

    def optimize_code(code: str, language: Optional[str] = "python",
                     optimization_goals: Optional[str] = "performance and readability",
                     model: Optional[str] = "meta/codellama-34b-instruct",
                     max_tokens: Optional[int] = 2000) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # Prepare the prompt for code optimization
            optimize_prompt = f"""Optimize the following {language} code for {optimization_goals}:

Original code:
```{language}
{code}
```

Please provide the optimized code with explanations of the improvements made:"""
            
            # Optimize code using the specified model
            output = client.run(
                model,
                input={
                    "prompt": optimize_prompt,
                    "max_tokens": max_tokens,
                    "temperature": 0.1,
                    "top_p": 0.9
                }
            )
            
            # Format the response
            if isinstance(output, list):
                optimized_result = "".join(output)
            else:
                optimized_result = str(output)
            
            result = {
                "language": language,
                "original_code": code,
                "optimization_goals": optimization_goals,
                "optimized_result": optimized_result.strip(),
                "model_used": model
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Failed to optimize code: {str(e)}"

    return StructuredTool.from_function(
        func=optimize_code,
        name=name,
        description=tool_description,
        args_schema=OptimizeCodeInput,
        return_direct=True
    )


# Debug Code Tool
class DebugCodeInput(BaseModel):
    code: str = Field(description="Code to debug")
    error_message: Optional[str] = Field(None, description="Error message if available")
    language: Optional[str] = Field("python", description="Programming language of the code")
    model: Optional[str] = Field("meta/codellama-34b-instruct", description="Model to use for debugging")
    max_tokens: Optional[int] = Field(2000, description="Maximum number of tokens to generate")


def debug_code_replicate(name, description, token):
    """Debugs and fixes code using Replicate AI models."""
    tool_description = description or "Debug and fix code using Replicate AI models"

    def debug_code(code: str, error_message: Optional[str] = None,
                  language: Optional[str] = "python",
                  model: Optional[str] = "meta/codellama-34b-instruct",
                  max_tokens: Optional[int] = 2000) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # Prepare the prompt for debugging
            debug_prompt = f"""Debug and fix the following {language} code:

Code:
```{language}
{code}
```
"""
            
            if error_message:
                debug_prompt += f"\nError message: {error_message}\n"
            
            debug_prompt += "\nPlease identify the issues and provide the corrected code with explanations:"
            
            # Debug code using the specified model
            output = client.run(
                model,
                input={
                    "prompt": debug_prompt,
                    "max_tokens": max_tokens,
                    "temperature": 0.1,
                    "top_p": 0.9
                }
            )
            
            # Format the response
            if isinstance(output, list):
                debug_result = "".join(output)
            else:
                debug_result = str(output)
            
            result = {
                "language": language,
                "original_code": code,
                "error_message": error_message,
                "debug_result": debug_result.strip(),
                "model_used": model
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Failed to debug code: {str(e)}"

    return StructuredTool.from_function(
        func=debug_code,
        name=name,
        description=tool_description,
        args_schema=DebugCodeInput,
        return_direct=True
    )


# Generate Dockerfile Tool
class GenerateDockerfileInput(BaseModel):
    project_description: str = Field(description="Description of the project")
    language: Optional[str] = Field("python", description="Main programming language")
    dependencies: Optional[List[str]] = Field(None, description="List of dependencies")
    port: Optional[int] = Field(8000, description="Port to expose")
    model: Optional[str] = Field("meta/codellama-34b-instruct", description="Model to use for Dockerfile generation")


def generate_dockerfile_replicate(name, description, token):
    """Generates Dockerfile using Replicate AI models."""
    tool_description = description or "Generate Dockerfile using Replicate AI models"

    def generate_dockerfile(project_description: str, language: Optional[str] = "python",
                           dependencies: Optional[List[str]] = None,
                           port: Optional[int] = 8000,
                           model: Optional[str] = "meta/codellama-34b-instruct") -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # Prepare the prompt for Dockerfile generation
            dockerfile_prompt = f"""Generate a Dockerfile for a {language} project with the following specifications:

Project description: {project_description}
Language: {language}
Port to expose: {port}
"""
            
            if dependencies:
                dockerfile_prompt += f"Dependencies: {', '.join(dependencies)}\n"
            
            dockerfile_prompt += "\nPlease provide a complete, production-ready Dockerfile:"
            
            # Generate Dockerfile using the specified model
            output = client.run(
                model,
                input={
                    "prompt": dockerfile_prompt,
                    "max_tokens": 1000,
                    "temperature": 0.1,
                    "top_p": 0.9
                }
            )
            
            # Format the response
            if isinstance(output, list):
                dockerfile_content = "".join(output)
            else:
                dockerfile_content = str(output)
            
            result = {
                "project_description": project_description,
                "language": language,
                "dependencies": dependencies,
                "port": port,
                "dockerfile": dockerfile_content.strip(),
                "model_used": model
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Failed to generate Dockerfile: {str(e)}"

    return StructuredTool.from_function(
        func=generate_dockerfile,
        name=name,
        description=tool_description,
        args_schema=GenerateDockerfileInput,
        return_direct=True
    )


# Generate Requirements Tool
class GenerateRequirementsInput(BaseModel):
    code: str = Field(description="Code to analyze for dependencies")
    language: Optional[str] = Field("python", description="Programming language")
    model: Optional[str] = Field("meta/codellama-34b-instruct", description="Model to use for requirements generation")


def generate_requirements_replicate(name, description, token):
    """Generates requirements.txt using Replicate AI models."""
    tool_description = description or "Generate requirements.txt using Replicate AI models"

    def generate_requirements(code: str, language: Optional[str] = "python",
                             model: Optional[str] = "meta/codellama-34b-instruct") -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Set up Replicate client
            client = replicate.Client(api_token=api_token)
            
            # Prepare the prompt for requirements generation
            requirements_prompt = f"""Analyze the following {language} code and generate a requirements.txt file with all necessary dependencies:

Code:
```{language}
{code}
```

Please provide a complete requirements.txt file with specific version numbers where appropriate:"""
            
            # Generate requirements using the specified model
            output = client.run(
                model,
                input={
                    "prompt": requirements_prompt,
                    "max_tokens": 1000,
                    "temperature": 0.1,
                    "top_p": 0.9
                }
            )
            
            # Format the response
            if isinstance(output, list):
                requirements_content = "".join(output)
            else:
                requirements_content = str(output)
            
            result = {
                "language": language,
                "analyzed_code": code,
                "requirements": requirements_content.strip(),
                "model_used": model
            }
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Failed to generate requirements: {str(e)}"

    return StructuredTool.from_function(
        func=generate_requirements,
        name=name,
        description=tool_description,
        args_schema=GenerateRequirementsInput,
        return_direct=True
    )
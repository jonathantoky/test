from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
import json
import requests
import time
from .. import extract_token_from_data


# Generate Code Tool
class GenerateCodeInput(BaseModel):
    prompt: str = Field(description="Code generation prompt describing what code to generate")
    language: Optional[str] = Field("python", description="Programming language (python, javascript, java, etc.)")
    model: Optional[str] = Field("meta/codellama-34b-instruct", description="Code generation model to use")
    max_tokens: Optional[int] = Field(1000, description="Maximum number of tokens to generate")
    temperature: Optional[float] = Field(0.1, description="Temperature for code generation (0.0 to 1.0)")


def generate_code_with_replicate(name, description, token):
    """Generates code using Replicate models."""
    tool_description = description or "Generate code using Replicate's code generation models"

    def generate_code(
        prompt: str, 
        language: Optional[str] = "python",
        model: Optional[str] = "meta/codellama-34b-instruct",
        max_tokens: Optional[int] = 1000,
        temperature: Optional[float] = 0.1
    ) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Prepare headers
            headers = {
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json"
            }
            
            # Format prompt for code generation
            formatted_prompt = f"Generate {language} code for the following request:\n\n{prompt}\n\nCode:"
            
            # Prepare request body
            body = {
                "version": model,
                "input": {
                    "prompt": formatted_prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": 0.9,
                    "top_k": 50
                }
            }
            
            # Make API request
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=body
            )
            
            if response.status_code == 201:
                prediction = response.json()
                prediction_id = prediction.get('id')
                
                # Wait for completion
                max_wait = 60  # 60 seconds timeout
                wait_time = 0
                
                while wait_time < max_wait:
                    # Check prediction status
                    status_response = requests.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers=headers
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get('status')
                        
                        if status == 'succeeded':
                            output = status_data.get('output', [])
                            if isinstance(output, list):
                                generated_code = ''.join(output)
                            else:
                                generated_code = str(output)
                            
                            result = f"Generated {language} code:\n\n```{language}\n{generated_code}\n```\n"
                            result += f"\nPrediction ID: {prediction_id}\n"
                            result += f"Model used: {model}\n"
                            
                            return result
                        elif status == 'failed':
                            error = status_data.get('error', 'Unknown error')
                            return f"Code generation failed: {error}"
                        elif status in ['starting', 'processing']:
                            time.sleep(2)
                            wait_time += 2
                        else:
                            return f"Unexpected status: {status}"
                    else:
                        return f"Error checking prediction status: {status_response.status_code}"
                
                return f"Code generation timed out after {max_wait} seconds. Prediction ID: {prediction_id}"
            else:
                return f"Error creating prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to generate code: {str(e)}"

    return StructuredTool.from_function(
        func=generate_code,
        name=name,
        description=tool_description,
        args_schema=GenerateCodeInput,
        return_direct=True
    )


# Generate Python Code Tool
class GeneratePythonCodeInput(BaseModel):
    prompt: str = Field(description="Description of the Python code to generate")
    include_comments: Optional[bool] = Field(True, description="Whether to include comments in the code")
    include_docstrings: Optional[bool] = Field(True, description="Whether to include docstrings")
    style: Optional[str] = Field("pep8", description="Code style (pep8, google, numpy)")


def generate_python_code(name, description, token):
    """Generates Python code using Replicate models."""
    tool_description = description or "Generate Python code with specific formatting and style"

    def generate_python(
        prompt: str, 
        include_comments: Optional[bool] = True,
        include_docstrings: Optional[bool] = True,
        style: Optional[str] = "pep8"
    ) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Prepare headers
            headers = {
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json"
            }
            
            # Format prompt for Python code generation
            style_instructions = ""
            if include_comments:
                style_instructions += "Include helpful comments. "
            if include_docstrings:
                style_instructions += "Include docstrings for functions and classes. "
            style_instructions += f"Follow {style} style guidelines. "
            
            formatted_prompt = f"""Generate Python code for the following request:

{prompt}

Requirements:
- {style_instructions}
- Write clean, readable, and well-structured code
- Include error handling where appropriate
- Use meaningful variable names

Python code:"""
            
            # Prepare request body
            body = {
                "version": "meta/codellama-34b-instruct",
                "input": {
                    "prompt": formatted_prompt,
                    "max_tokens": 1500,
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "top_k": 50
                }
            }
            
            # Make API request
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=body
            )
            
            if response.status_code == 201:
                prediction = response.json()
                prediction_id = prediction.get('id')
                
                # Wait for completion
                max_wait = 60
                wait_time = 0
                
                while wait_time < max_wait:
                    status_response = requests.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers=headers
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get('status')
                        
                        if status == 'succeeded':
                            output = status_data.get('output', [])
                            if isinstance(output, list):
                                generated_code = ''.join(output)
                            else:
                                generated_code = str(output)
                            
                            result = f"Generated Python code:\n\n```python\n{generated_code}\n```\n"
                            result += f"\nStyle: {style}\n"
                            result += f"Comments included: {include_comments}\n"
                            result += f"Docstrings included: {include_docstrings}\n"
                            
                            return result
                        elif status == 'failed':
                            error = status_data.get('error', 'Unknown error')
                            return f"Python code generation failed: {error}"
                        elif status in ['starting', 'processing']:
                            time.sleep(2)
                            wait_time += 2
                
                return f"Python code generation timed out after {max_wait} seconds."
            else:
                return f"Error creating prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to generate Python code: {str(e)}"

    return StructuredTool.from_function(
        func=generate_python,
        name=name,
        description=tool_description,
        args_schema=GeneratePythonCodeInput,
        return_direct=True
    )


# Generate JavaScript Code Tool
class GenerateJavaScriptCodeInput(BaseModel):
    prompt: str = Field(description="Description of the JavaScript code to generate")
    framework: Optional[str] = Field("vanilla", description="JavaScript framework (vanilla, react, vue, node)")
    es_version: Optional[str] = Field("es6", description="ECMAScript version (es5, es6, es2020)")
    include_types: Optional[bool] = Field(False, description="Whether to include TypeScript types")


def generate_javascript_code(name, description, token):
    """Generates JavaScript code using Replicate models."""
    tool_description = description or "Generate JavaScript code with specific framework and version"

    def generate_javascript(
        prompt: str, 
        framework: Optional[str] = "vanilla",
        es_version: Optional[str] = "es6",
        include_types: Optional[bool] = False
    ) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Prepare headers
            headers = {
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json"
            }
            
            # Format prompt for JavaScript code generation
            type_instruction = "Include TypeScript types" if include_types else "Use plain JavaScript"
            
            formatted_prompt = f"""Generate JavaScript code for the following request:

{prompt}

Requirements:
- Use {framework} JavaScript framework
- Target {es_version} ECMAScript version
- {type_instruction}
- Write clean, modern JavaScript code
- Include comments for complex logic
- Follow best practices

JavaScript code:"""
            
            # Prepare request body
            body = {
                "version": "meta/codellama-34b-instruct",
                "input": {
                    "prompt": formatted_prompt,
                    "max_tokens": 1500,
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "top_k": 50
                }
            }
            
            # Make API request
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=body
            )
            
            if response.status_code == 201:
                prediction = response.json()
                prediction_id = prediction.get('id')
                
                # Wait for completion
                max_wait = 60
                wait_time = 0
                
                while wait_time < max_wait:
                    status_response = requests.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers=headers
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get('status')
                        
                        if status == 'succeeded':
                            output = status_data.get('output', [])
                            if isinstance(output, list):
                                generated_code = ''.join(output)
                            else:
                                generated_code = str(output)
                            
                            file_extension = "ts" if include_types else "js"
                            result = f"Generated JavaScript code:\n\n```{file_extension}\n{generated_code}\n```\n"
                            result += f"\nFramework: {framework}\n"
                            result += f"ES Version: {es_version}\n"
                            result += f"TypeScript types: {include_types}\n"
                            
                            return result
                        elif status == 'failed':
                            error = status_data.get('error', 'Unknown error')
                            return f"JavaScript code generation failed: {error}"
                        elif status in ['starting', 'processing']:
                            time.sleep(2)
                            wait_time += 2
                
                return f"JavaScript code generation timed out after {max_wait} seconds."
            else:
                return f"Error creating prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to generate JavaScript code: {str(e)}"

    return StructuredTool.from_function(
        func=generate_javascript,
        name=name,
        description=tool_description,
        args_schema=GenerateJavaScriptCodeInput,
        return_direct=True
    )


# Generate API Code Tool
class GenerateAPICodeInput(BaseModel):
    api_description: str = Field(description="Description of the API to generate code for")
    api_type: Optional[str] = Field("rest", description="API type (rest, graphql, websocket)")
    language: Optional[str] = Field("python", description="Programming language for the API client")
    authentication: Optional[str] = Field("none", description="Authentication method (none, api_key, oauth, jwt)")


def generate_api_code(name, description, token):
    """Generates API integration code using Replicate models."""
    tool_description = description or "Generate API integration code for various services"

    def generate_api(
        api_description: str, 
        api_type: Optional[str] = "rest",
        language: Optional[str] = "python",
        authentication: Optional[str] = "none"
    ) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Prepare headers
            headers = {
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json"
            }
            
            # Format prompt for API code generation
            auth_instruction = ""
            if authentication != "none":
                auth_instruction = f"Include {authentication} authentication handling. "
            
            formatted_prompt = f"""Generate {language} code for {api_type.upper()} API integration:

API Description: {api_description}

Requirements:
- Create a {language} client for the {api_type.upper()} API
- {auth_instruction}
- Include error handling and response parsing
- Add proper documentation and comments
- Follow {language} best practices
- Include example usage

{language} API client code:"""
            
            # Prepare request body
            body = {
                "version": "meta/codellama-34b-instruct",
                "input": {
                    "prompt": formatted_prompt,
                    "max_tokens": 2000,
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "top_k": 50
                }
            }
            
            # Make API request
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=body
            )
            
            if response.status_code == 201:
                prediction = response.json()
                prediction_id = prediction.get('id')
                
                # Wait for completion
                max_wait = 90
                wait_time = 0
                
                while wait_time < max_wait:
                    status_response = requests.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers=headers
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get('status')
                        
                        if status == 'succeeded':
                            output = status_data.get('output', [])
                            if isinstance(output, list):
                                generated_code = ''.join(output)
                            else:
                                generated_code = str(output)
                            
                            result = f"Generated {language} API client code:\n\n```{language}\n{generated_code}\n```\n"
                            result += f"\nAPI Type: {api_type.upper()}\n"
                            result += f"Language: {language}\n"
                            result += f"Authentication: {authentication}\n"
                            
                            return result
                        elif status == 'failed':
                            error = status_data.get('error', 'Unknown error')
                            return f"API code generation failed: {error}"
                        elif status in ['starting', 'processing']:
                            time.sleep(3)
                            wait_time += 3
                
                return f"API code generation timed out after {max_wait} seconds."
            else:
                return f"Error creating prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to generate API code: {str(e)}"

    return StructuredTool.from_function(
        func=generate_api,
        name=name,
        description=tool_description,
        args_schema=GenerateAPICodeInput,
        return_direct=True
    )


# Code Completion Tool
class CodeCompletionInput(BaseModel):
    code_snippet: str = Field(description="Partial code snippet to complete")
    language: Optional[str] = Field("python", description="Programming language of the code")
    context: Optional[str] = Field("", description="Additional context about the code purpose")


def code_completion_replicate(name, description, token):
    """Completes code snippets using Replicate models."""
    tool_description = description or "Complete partial code snippets using Replicate"

    def complete_code(
        code_snippet: str, 
        language: Optional[str] = "python",
        context: Optional[str] = ""
    ) -> str:
        try:
            # Extract the API token
            api_token = extract_token_from_data(token)
            
            # Prepare headers
            headers = {
                "Authorization": f"Token {api_token}",
                "Content-Type": "application/json"
            }
            
            # Format prompt for code completion
            context_text = f"Context: {context}\n\n" if context else ""
            
            formatted_prompt = f"""Complete the following {language} code snippet:

{context_text}```{language}
{code_snippet}
```

Continue the code from where it left off:"""
            
            # Prepare request body
            body = {
                "version": "meta/codellama-34b-instruct",
                "input": {
                    "prompt": formatted_prompt,
                    "max_tokens": 800,
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "top_k": 50
                }
            }
            
            # Make API request
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=body
            )
            
            if response.status_code == 201:
                prediction = response.json()
                prediction_id = prediction.get('id')
                
                # Wait for completion
                max_wait = 45
                wait_time = 0
                
                while wait_time < max_wait:
                    status_response = requests.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers=headers
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get('status')
                        
                        if status == 'succeeded':
                            output = status_data.get('output', [])
                            if isinstance(output, list):
                                completion = ''.join(output)
                            else:
                                completion = str(output)
                            
                            result = f"Code completion:\n\n```{language}\n{code_snippet}{completion}\n```\n"
                            result += f"\nOriginal snippet:\n```{language}\n{code_snippet}\n```\n"
                            result += f"\nCompletion:\n```{language}\n{completion}\n```\n"
                            
                            return result
                        elif status == 'failed':
                            error = status_data.get('error', 'Unknown error')
                            return f"Code completion failed: {error}"
                        elif status in ['starting', 'processing']:
                            time.sleep(2)
                            wait_time += 2
                
                return f"Code completion timed out after {max_wait} seconds."
            else:
                return f"Error creating prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to complete code: {str(e)}"

    return StructuredTool.from_function(
        func=complete_code,
        name=name,
        description=tool_description,
        args_schema=CodeCompletionInput,
        return_direct=True
    )
"""
Replicate Code Generation Tools

This module provides AI-powered code generation tools using Replicate models
for generating, optimizing, debugging, explaining, and converting code.
"""

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import requests
import json
import time


def extract_token_from_data(token_data):
    """Extract token from various token formats"""
    if isinstance(token_data, str):
        return token_data
    elif isinstance(token_data, dict):
        return token_data.get('token') or token_data.get('access_token') or token_data.get('api_key')
    return str(token_data)


# Default code generation models
DEFAULT_CODE_MODELS = {
    "code_generation": "meta/codellama-34b-instruct",
    "code_optimization": "meta/codellama-34b-instruct",
    "code_debugging": "meta/codellama-34b-instruct",
    "code_explanation": "meta/codellama-34b-instruct",
    "code_conversion": "meta/codellama-34b-instruct"
}


class GenerateCodeInput(BaseModel):
    prompt: str = Field(description="Description of the code to generate")
    language: Optional[str] = Field("python", description="Programming language (default: python)")
    model: Optional[str] = Field(None, description="Specific model to use (optional)")
    max_tokens: Optional[int] = Field(2000, description="Maximum tokens in response")
    temperature: Optional[float] = Field(0.7, description="Temperature for generation (0.0-1.0)")


def generate_code_replicate(name, description, token):
    """Generate code using Replicate AI models"""
    tool_description = description or "Generate code using AI models on Replicate"

    def generate_code(
        prompt: str,
        language: Optional[str] = "python",
        model: Optional[str] = None,
        max_tokens: Optional[int] = 2000,
        temperature: Optional[float] = 0.7
    ) -> str:
        try:
            access_token = extract_token_from_data(token)
            
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
            # Use default model if none specified
            model_name = model or DEFAULT_CODE_MODELS["code_generation"]
            
            # Construct the generation prompt
            system_prompt = f"""You are an expert {language} programmer. Generate clean, efficient, and well-documented code based on the following requirements:

Requirements: {prompt}

Please provide:
1. Clean, readable code
2. Appropriate comments
3. Error handling where necessary
4. Best practices for {language}

Generate only the code, no additional explanations unless specifically requested."""

            input_data = {
                "prompt": system_prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
                "repetition_penalty": 1.1
            }
            
            # Create prediction
            prediction_data = {
                "version": model_name,
                "input": input_data
            }
            
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=prediction_data
            )
            
            if response.status_code == 201:
                prediction = response.json()
                prediction_id = prediction.get('id')
                
                # Poll for completion
                max_wait = 300  # 5 minutes
                poll_interval = 5
                start_time = time.time()
                
                while time.time() - start_time < max_wait:
                    status_response = requests.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers=headers
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get('status')
                        
                        if status == 'succeeded':
                            output = status_data.get('output')
                            if isinstance(output, list):
                                generated_code = ''.join(output)
                            else:
                                generated_code = str(output)
                            
                            result = f"Generated {language} code:\n\n"
                            result += f"```{language}\n{generated_code}\n```\n\n"
                            result += f"Model used: {model_name}\n"
                            result += f"Generation completed successfully!"
                            return result
                        
                        elif status == 'failed':
                            error = status_data.get('error', 'Unknown error')
                            return f"Code generation failed: {error}"
                        
                        elif status in ['starting', 'processing']:
                            time.sleep(poll_interval)
                            continue
                    
                    time.sleep(poll_interval)
                
                return "Code generation timed out after 5 minutes"
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


class OptimizeCodeInput(BaseModel):
    code: str = Field(description="Code to optimize")
    language: Optional[str] = Field("python", description="Programming language")
    optimization_focus: Optional[str] = Field("performance", description="Focus: performance, readability, memory, or security")
    model: Optional[str] = Field(None, description="Specific model to use")


def optimize_code_replicate(name, description, token):
    """Optimize code using Replicate AI models"""
    tool_description = description or "Optimize code for performance, readability, or other aspects using AI"

    def optimize_code(
        code: str,
        language: Optional[str] = "python",
        optimization_focus: Optional[str] = "performance",
        model: Optional[str] = None
    ) -> str:
        try:
            access_token = extract_token_from_data(token)
            
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
            model_name = model or DEFAULT_CODE_MODELS["code_optimization"]
            
            system_prompt = f"""You are an expert {language} programmer specializing in code optimization. 
Analyze the following code and optimize it for {optimization_focus}.

Original code:
```{language}
{code}
```

Please provide:
1. Optimized version of the code
2. Explanation of changes made
3. Performance/improvement benefits
4. Any trade-offs or considerations

Focus on: {optimization_focus}"""

            input_data = {
                "prompt": system_prompt,
                "max_tokens": 3000,
                "temperature": 0.3,
                "top_p": 0.9
            }
            
            prediction_data = {
                "version": model_name,
                "input": input_data
            }
            
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=prediction_data
            )
            
            if response.status_code == 201:
                prediction = response.json()
                prediction_id = prediction.get('id')
                
                # Poll for completion
                max_wait = 300
                poll_interval = 5
                start_time = time.time()
                
                while time.time() - start_time < max_wait:
                    status_response = requests.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers=headers
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get('status')
                        
                        if status == 'succeeded':
                            output = status_data.get('output')
                            if isinstance(output, list):
                                optimization_result = ''.join(output)
                            else:
                                optimization_result = str(output)
                            
                            result = f"Code Optimization Results ({optimization_focus}):\n\n"
                            result += f"{optimization_result}\n\n"
                            result += f"Model used: {model_name}\n"
                            result += f"Optimization completed successfully!"
                            return result
                        
                        elif status == 'failed':
                            error = status_data.get('error', 'Unknown error')
                            return f"Code optimization failed: {error}"
                        
                        elif status in ['starting', 'processing']:
                            time.sleep(poll_interval)
                            continue
                    
                    time.sleep(poll_interval)
                
                return "Code optimization timed out after 5 minutes"
            else:
                return f"Error creating prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to optimize code: {str(e)}"

    return StructuredTool.from_function(
        func=optimize_code,
        name=name,
        description=tool_description,
        args_schema=OptimizeCodeInput,
        return_direct=True
    )


class DebugCodeInput(BaseModel):
    code: str = Field(description="Code to debug")
    error_message: Optional[str] = Field(None, description="Error message or description of the issue")
    language: Optional[str] = Field("python", description="Programming language")
    model: Optional[str] = Field(None, description="Specific model to use")


def debug_code_replicate(name, description, token):
    """Debug code using Replicate AI models"""
    tool_description = description or "Debug code and find solutions to errors using AI"

    def debug_code(
        code: str,
        error_message: Optional[str] = None,
        language: Optional[str] = "python",
        model: Optional[str] = None
    ) -> str:
        try:
            access_token = extract_token_from_data(token)
            
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
            model_name = model or DEFAULT_CODE_MODELS["code_debugging"]
            
            error_context = f"\nError message: {error_message}" if error_message else ""
            
            system_prompt = f"""You are an expert {language} programmer and debugger. 
Analyze the following code and identify issues, bugs, or potential problems.

Code to debug:
```{language}
{code}
```{error_context}

Please provide:
1. Identification of issues/bugs
2. Corrected version of the code
3. Explanation of what was wrong
4. Best practices to avoid similar issues
5. Testing suggestions

Be thorough and provide working solutions."""

            input_data = {
                "prompt": system_prompt,
                "max_tokens": 3000,
                "temperature": 0.2,
                "top_p": 0.9
            }
            
            prediction_data = {
                "version": model_name,
                "input": input_data
            }
            
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=prediction_data
            )
            
            if response.status_code == 201:
                prediction = response.json()
                prediction_id = prediction.get('id')
                
                # Poll for completion
                max_wait = 300
                poll_interval = 5
                start_time = time.time()
                
                while time.time() - start_time < max_wait:
                    status_response = requests.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers=headers
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get('status')
                        
                        if status == 'succeeded':
                            output = status_data.get('output')
                            if isinstance(output, list):
                                debug_result = ''.join(output)
                            else:
                                debug_result = str(output)
                            
                            result = f"Code Debug Analysis:\n\n"
                            result += f"{debug_result}\n\n"
                            result += f"Model used: {model_name}\n"
                            result += f"Debug analysis completed successfully!"
                            return result
                        
                        elif status == 'failed':
                            error = status_data.get('error', 'Unknown error')
                            return f"Code debugging failed: {error}"
                        
                        elif status in ['starting', 'processing']:
                            time.sleep(poll_interval)
                            continue
                    
                    time.sleep(poll_interval)
                
                return "Code debugging timed out after 5 minutes"
            else:
                return f"Error creating prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to debug code: {str(e)}"

    return StructuredTool.from_function(
        func=debug_code,
        name=name,
        description=tool_description,
        args_schema=DebugCodeInput,
        return_direct=True
    )


class ExplainCodeInput(BaseModel):
    code: str = Field(description="Code to explain")
    language: Optional[str] = Field("python", description="Programming language")
    detail_level: Optional[str] = Field("medium", description="Detail level: basic, medium, or detailed")
    model: Optional[str] = Field(None, description="Specific model to use")


def explain_code_replicate(name, description, token):
    """Explain code using Replicate AI models"""
    tool_description = description or "Get detailed explanations of code functionality using AI"

    def explain_code(
        code: str,
        language: Optional[str] = "python",
        detail_level: Optional[str] = "medium",
        model: Optional[str] = None
    ) -> str:
        try:
            access_token = extract_token_from_data(token)
            
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
            model_name = model or DEFAULT_CODE_MODELS["code_explanation"]
            
            detail_instructions = {
                "basic": "Provide a brief, high-level explanation suitable for beginners",
                "medium": "Provide a detailed explanation with examples and context",
                "detailed": "Provide a comprehensive explanation with technical details, complexity analysis, and best practices"
            }
            
            instruction = detail_instructions.get(detail_level, detail_instructions["medium"])
            
            system_prompt = f"""You are an expert {language} programmer and teacher. 
Explain the following code in a clear and educational manner.

Code to explain:
```{language}
{code}
```

Instructions: {instruction}

Please provide:
1. Overall purpose and functionality
2. Step-by-step breakdown
3. Key concepts and techniques used
4. Input/output behavior
5. Time/space complexity (if applicable)
6. Potential use cases
7. Related concepts or improvements

Make it educational and easy to understand."""

            input_data = {
                "prompt": system_prompt,
                "max_tokens": 3000,
                "temperature": 0.3,
                "top_p": 0.9
            }
            
            prediction_data = {
                "version": model_name,
                "input": input_data
            }
            
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=prediction_data
            )
            
            if response.status_code == 201:
                prediction = response.json()
                prediction_id = prediction.get('id')
                
                # Poll for completion
                max_wait = 300
                poll_interval = 5
                start_time = time.time()
                
                while time.time() - start_time < max_wait:
                    status_response = requests.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers=headers
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get('status')
                        
                        if status == 'succeeded':
                            output = status_data.get('output')
                            if isinstance(output, list):
                                explanation = ''.join(output)
                            else:
                                explanation = str(output)
                            
                            result = f"Code Explanation ({detail_level} level):\n\n"
                            result += f"{explanation}\n\n"
                            result += f"Model used: {model_name}\n"
                            result += f"Explanation completed successfully!"
                            return result
                        
                        elif status == 'failed':
                            error = status_data.get('error', 'Unknown error')
                            return f"Code explanation failed: {error}"
                        
                        elif status in ['starting', 'processing']:
                            time.sleep(poll_interval)
                            continue
                    
                    time.sleep(poll_interval)
                
                return "Code explanation timed out after 5 minutes"
            else:
                return f"Error creating prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to explain code: {str(e)}"

    return StructuredTool.from_function(
        func=explain_code,
        name=name,
        description=tool_description,
        args_schema=ExplainCodeInput,
        return_direct=True
    )


class ConvertCodeInput(BaseModel):
    code: str = Field(description="Code to convert")
    source_language: str = Field(description="Source programming language")
    target_language: str = Field(description="Target programming language")
    model: Optional[str] = Field(None, description="Specific model to use")
    preserve_comments: Optional[bool] = Field(True, description="Whether to preserve comments")


def convert_code_replicate(name, description, token):
    """Convert code between programming languages using Replicate AI models"""
    tool_description = description or "Convert code from one programming language to another using AI"

    def convert_code(
        code: str,
        source_language: str,
        target_language: str,
        model: Optional[str] = None,
        preserve_comments: Optional[bool] = True
    ) -> str:
        try:
            access_token = extract_token_from_data(token)
            
            headers = {
                "Authorization": f"Token {access_token}",
                "Content-Type": "application/json"
            }
            
            model_name = model or DEFAULT_CODE_MODELS["code_conversion"]
            
            comment_instruction = "Preserve and convert comments appropriately" if preserve_comments else "Focus on code conversion, comments optional"
            
            system_prompt = f"""You are an expert programmer fluent in multiple programming languages. 
Convert the following {source_language} code to {target_language}.

Source code ({source_language}):
```{source_language}
{code}
```

Instructions:
1. Convert the code to idiomatic {target_language}
2. Maintain the same functionality and logic
3. Use {target_language} best practices and conventions
4. {comment_instruction}
5. Handle language-specific features appropriately
6. Provide equivalent libraries/modules where needed

Please provide:
1. Converted code
2. Notes about any significant changes or considerations
3. Required imports/dependencies for {target_language}
4. Any limitations or differences in behavior

Make sure the converted code is functional and follows {target_language} standards."""

            input_data = {
                "prompt": system_prompt,
                "max_tokens": 3000,
                "temperature": 0.2,
                "top_p": 0.9
            }
            
            prediction_data = {
                "version": model_name,
                "input": input_data
            }
            
            response = requests.post(
                "https://api.replicate.com/v1/predictions",
                headers=headers,
                json=prediction_data
            )
            
            if response.status_code == 201:
                prediction = response.json()
                prediction_id = prediction.get('id')
                
                # Poll for completion
                max_wait = 300
                poll_interval = 5
                start_time = time.time()
                
                while time.time() - start_time < max_wait:
                    status_response = requests.get(
                        f"https://api.replicate.com/v1/predictions/{prediction_id}",
                        headers=headers
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get('status')
                        
                        if status == 'succeeded':
                            output = status_data.get('output')
                            if isinstance(output, list):
                                conversion_result = ''.join(output)
                            else:
                                conversion_result = str(output)
                            
                            result = f"Code Conversion ({source_language} → {target_language}):\n\n"
                            result += f"{conversion_result}\n\n"
                            result += f"Model used: {model_name}\n"
                            result += f"Conversion completed successfully!"
                            return result
                        
                        elif status == 'failed':
                            error = status_data.get('error', 'Unknown error')
                            return f"Code conversion failed: {error}"
                        
                        elif status in ['starting', 'processing']:
                            time.sleep(poll_interval)
                            continue
                    
                    time.sleep(poll_interval)
                
                return "Code conversion timed out after 5 minutes"
            else:
                return f"Error creating prediction: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Failed to convert code: {str(e)}"

    return StructuredTool.from_function(
        func=convert_code,
        name=name,
        description=tool_description,
        args_schema=ConvertCodeInput,
        return_direct=True
    )
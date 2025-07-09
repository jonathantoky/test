from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import Any
import requests

# Code generation tools
class GenerateCodeInput(BaseModel):
    prompt: str = Field(description="Prompt for code generation.")

class OptimizeCodeInput(BaseModel):
    code: str = Field(description="Code to optimize.")

class DebugCodeInput(BaseModel):
    code: str = Field(description="Code to debug.")


def generate_code_replicate(name, description, token):
    """
    Generates code based on a prompt.
    """
    def generate_code(prompt: str) -> str:
        headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
        response = requests.post('https://api.replicate.com/v1/code/generate', headers=headers, json={
            'prompt': prompt
        })
        return response.json()
    return StructuredTool.from_function(
        func=generate_code,
        name=name,
        description=description,
        args_schema=GenerateCodeInput,
        return_direct=True,
    )


def optimize_code_replicate(name, description, token):
    """
    Optimizes existing code.
    """
    def optimize_code(code: str) -> str:
        headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
        response = requests.post('https://api.replicate.com/v1/code/optimize', headers=headers, json={
            'code': code
        })
        return response.json()
    return StructuredTool.from_function(
        func=optimize_code,
        name=name,
        description=description,
        args_schema=OptimizeCodeInput,
        return_direct=True,
    )


def debug_code_replicate(name, description, token):
    """
    Debugs provided code.
    """
    def debug_code(code: str) -> str:
        headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
        response = requests.post('https://api.replicate.com/v1/code/debug', headers=headers, json={
            'code': code
        })
        return response.json()
    return StructuredTool.from_function(
        func=debug_code,
        name=name,
        description=description,
        args_schema=DebugCodeInput,
        return_direct=True,
    )

# Additional code generation functions would go here...
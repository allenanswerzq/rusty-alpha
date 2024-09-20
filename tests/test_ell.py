import os
import ell

from openai import AzureOpenAI as AzureOpenAIClient
from typing import Optional, Dict, Any, List, Iterator

from azure.identity import DefaultAzureCredential
from azure.identity import get_bearer_token_provider


def register(client: AzureOpenAIClient):
    """Register OpenAI models with the provided client."""
    model_data = [
        ("gpt-4-turbo", "test"),
    ]
    for model_id, owned_by in model_data:
        ell.config.register_model(model_id, client)


token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

_client_params: Dict[str, Any] = {}
_client_params["azure_endpoint"] = os.getenv("AZURE_OPENAI_ENDPOINT")
_client_params["api_version"] = "2023-03-15-preview"
_client_params["azure_deployment"] = "gpt-4-turbo"
_client_params["azure_ad_token_provider"] = token_provider
default_client = AzureOpenAIClient(**_client_params)

register(default_client)
ell.config.default_client = default_client


@ell.simple(model="gpt-4-turbo")
def hello(name: str):
    """You are a helpful assistant."""  # System prompt
    return f"Say hello to {name}!"  # User prompt


greeting = hello("Sam Altman")
print(greeting)

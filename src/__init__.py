import ell
import os

from openai import AzureOpenAI as AzureOpenAIClient
from typing import Optional, Dict, Any, List, Iterator
from azure.identity import DefaultAzureCredential
from azure.identity import get_bearer_token_provider

token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

_client_params: Dict[str, Any] = {}
_client_params["azure_endpoint"] = os.getenv("AZURE_OPENAI_ENDPOINT")
_client_params["api_version"] = "2023-03-15-preview"
_client_params["azure_deployment"] = "gpt-4-turbo"
_client_params["azure_ad_token_provider"] = token_provider
default_client = AzureOpenAIClient(**_client_params)

ell.config.register_model('gpt-4-turbo', default_client)
# ell.init(store='./logdir')
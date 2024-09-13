import ell
import os
import json

from azure.identity import DefaultAzureCredential
from azure.identity import get_bearer_token_provider
from openai import AzureOpenAI as AzureOpenAIClient
from typing import Optional, Dict, Any, List, Iterator, Type, Tuple
from ell.provider import APICallResult, Provider
from ell.types import Message, ContentBlock, ToolCall
from ell.types._lstr import _lstr
from ell.configurator import config, register_provider
from ell.types.message import LMP
from ell.util.serialization import serialize_image

token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

_client_params: Dict[str, Any] = {}
_client_params["azure_endpoint"] = os.getenv("AZURE_OPENAI_ENDPOINT")
_client_params["api_version"] = "2023-03-15-preview"
_client_params["azure_deployment"] = "gpt-4-turbo"
_client_params["azure_ad_token_provider"] = token_provider

class MockAzureOpenAIClient:
    def __init__(self, **kwargs):
        self.api_key = "None"

    def chat_completions_create(self, **kwargs):
        return None

class MockProvider(Provider):
    @classmethod
    def call_model(
        cls,
        client: Any,
        model: str,
        messages: List[Message],
        api_params: Dict[str, Any],
        tools: Optional[list[LMP]] = None,
    ) -> APICallResult:
        final_call_params = api_params.copy()
        actual_n = api_params.get("n", 1)
        final_call_params["model"] = model
        final_call_params["messages"] = messages
        response = client.chat_completions_create(**final_call_params)
        return APICallResult(
            response=response,
            actual_streaming=False,
            actual_n=actual_n,
            final_call_params=final_call_params,
        )

    @classmethod
    def process_response(
        cls, 
        call_result: APICallResult, 
        _invocation_origin: str,  
        logger : Optional[Any] = None,  
        tools: Optional[List[LMP]] = None,
    ) -> Tuple[List[Message], Dict[str, Any]]:
        source_code = json.dumps(call_result.final_call_params['messages'][1].text)
        metdata = {}
        results = []
        results.append(
            Message(
                role=('user'),
                content = f"""{{
                    "explain": "Mock", 
                    "target_code": "Mock", 
                    "source_code": {source_code}
                }}"""
            )
        )
        return results, metdata

    @classmethod
    def supports_streaming(cls) -> bool:
        return False

    @classmethod
    def get_client_type(cls) -> Type:
        return MockAzureOpenAIClient


default_client = MockAzureOpenAIClient(**_client_params)
# default_client = AzureOpenAIClient
ell.config.register_provider(MockProvider)
ell.config.register_model('gpt-4-turbo', default_client)

# default_client = AzureOpenAIClient
# ell.config.register_model('gpt-4-turbo', default_client)
# ell.init(store='./logdir')

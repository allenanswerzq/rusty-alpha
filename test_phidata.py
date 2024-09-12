import os

from phi.assistant import Assistant
from phi.llm.azure import AzureOpenAIChat
from phi.utils.log import logger

from azure.identity import DefaultAzureCredential
from azure.identity import get_bearer_token_provider

token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

# Initialize the OpenAI chat model
chat_model = AzureOpenAIChat(
    model="gpt-3.5-turbo",
    max_tokens=500,
    temperature=0.7,
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment="gpt-4-turbo",
    api_version="2023-03-15-preview",
    azure_ad_token_provider=token_provider,
)

# Create an assistant
assistant = Assistant(
    name="Math Tutor",
    llm=chat_model,
    system_prompt="You are a helpful math tutor. Provide clear explanations for math problems.",
)

assistant.print_response("Whats happening in France?", markdown=True)


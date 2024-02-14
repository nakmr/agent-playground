import os
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, OpenAIChatCompletion

load_dotenv()

useAzureOpenAI = True

class SKModuleConfiguration:

    def add_azure_ai_to_kernel() -> Kernel:
        kernel = sk.Kernel()

        if useAzureOpenAI:
            deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            azure_chat_service = AzureChatCompletion(
                deployment_name=deployment,
                api_key=api_key,
                endpoint=endpoint
            )
            kernel.add_chat_service("chat_completion", azure_chat_service)
        else:
            ai_model = "gpt-3.5-turbo"
            api_key = os.getenv("OPENAI_API_KEY")
            openai_chat_service = OpenAIChatCompletion(
                model=ai_model,
                api_key=api_key
            )
            kernel.add_chat_service("chat-gpt", openai_chat_service)
        
        return kernel
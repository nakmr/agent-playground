from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.orchestration.kernel_context import KernelContext
from semantic_kernel.plugin_definition import (
    kernel_function,
    kernel_function_context_parameter,
)

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='/.env')

from googleapiclient.discovery import build
import json

class WebSearchPlugin(KernelBaseModel):
    """
    Description: A web search plugin.
    """

    @kernel_function(
        description="Performs a web search for a given query with Google",
        name="GoogleSearch",
    )
    @kernel_function_context_parameter(
        name="query",
        description="The search query",
    )
    async def google_search(self, query: str) -> str:
        # query = query or context.variables.get("query")[1]
        service = build(
            "customsearch",
            "v1",
            developerKey=os.getenv("GOOGLE_API_KEY"),
        )

        result = (
            service.cse().list(
                q=query,
                cx=os.getenv("GOOGLE_CSE_ID"),
                lr="lang_ja",
                num = 5,
                start = 1,
            ).execute()
        )

        # json形式の結果を整形
        organized_result = json.dumps(result, ensure_ascii = False, indent = 4)

        return organized_result
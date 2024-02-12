import logging
logging.basicConfig(level=logging.DEBUG)

from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.plugin_definition import (
    kernel_function,
    kernel_function_context_parameter
)

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='/.env')

class SlackPlugin:
    """
    SlackPlugin provides a way to send messages to a Slack channel.
    """

    @kernel_function(
        description="Send a message to a Slack channel.",
        name="SendMessage"
    )
    @kernel_function_context_parameter(
        name="text",
        description="Message to send."
    )
    def send_message(self, text: str) -> str:
        """
        Send a message to a Slack channel.
        The argument `text` should contain only the message to be sent.

        Args:
            text (str): The message to send.
        Returns:
            any: HTTP response from the Slack API.
        """

        slack_token = os.getenv("SLACK_USER_TOKEN")
        client = WebClient(token=slack_token)

        try:
            response = client.chat_postMessage(
                channel="#general",
                text=text
            )
            return "Message sent!"
        except SlackApiError as e:
            assert e.response["error"]
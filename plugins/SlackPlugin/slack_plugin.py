import logging
logging.basicConfig(level=logging.DEBUG)

from semantic_kernel.kernel_pydantic import KernelBaseModel
from semantic_kernel.plugin_definition import (
    kernel_function,
    kernel_function_context_parameter
)
from semantic_kernel import KernelContext

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='/.env')

class SlackPlugin(KernelBaseModel):
    """
    Description: Provides a way to send messages to a Slack channel.
    """

    @kernel_function(
        description="Send a message to a Slack channel.",
        name="SendMessage"
    )
    @kernel_function_context_parameter(
        name="message",
        description="The message body you want to send to Slack.",
    )
    # def send_message(self, context: KernelContext) -> str:
    def send_message(self, message: str) -> str:
        """
        Send a message to a Slack channel.
        The argument `message` should contain only the message to be sent.
        Do not include messages that should not be sent.

        Args:
            message (str): The message to send.
        Returns:
            str: HTTP response from the Slack API.
        """

        slack_token = os.getenv("SLACK_USER_TOKEN")
        client = WebClient(token=slack_token)

        try:
            response = client.chat_postMessage(
                channel="#general",
                # text=context["message"]
                text=message
            )
            return "Message sent!"
        except SlackApiError as e:
            assert e.response["error"]
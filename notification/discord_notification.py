import logging
import os

from discord_webhook import DiscordWebhook, DiscordEmbed
from starlette.requests import Request

ERROR_WEBHOOK_URL = os.getenv("AI_DISCORD_NOTIFICATION_WEBHOOK")


def notify_common_error(request: Request, exc: Exception):
    discord_message = DiscordEmbed(
        title="Internal Server Error",
        color=0xFF0000,
    )
    discord_message.add_embed_field(name="Request URL", value=f"◾️ {request.url}", inline=False)
    discord_message.add_embed_field(name="Request Method", value=f"◾️ {request.method}", inline=False)
    discord_message.add_embed_field(name="Exception", value=f"◾️ {exc!r}", inline=False)

    send_error_message(discord_message)


def notify_llm_error(function: str, question: str, chat_room_id: str, exc: Exception):
    discord_message = DiscordEmbed(
        title=f"LLM Error in {function}",
        color=0x0000FF,
    )
    discord_message.add_embed_field(name="Question", value=f"◾️ {question}", inline=False)
    discord_message.add_embed_field(name="Chat Room ID", value=f"◾️ {chat_room_id}", inline=False)
    discord_message.add_embed_field(name="Exception", value=f"◾️ {exc!r}", inline=False)

    send_error_message(discord_message)


def send_error_message(embeds: DiscordEmbed) -> None:
    webhook = DiscordWebhook(url=ERROR_WEBHOOK_URL, embeds=[embeds], content="")
    response = webhook.execute()
    if not response.ok:
        logging.error(f"Failed to send error message to Discord. response: {response.text}")

import requests
from decouple import config

DISCORD_WEBHOOK_URL = config("DISCORD_WEBHOOK_URL")


def send_message_to_discord(msg: str):
    """Notify in discord with webhook"""
    requests.post(DISCORD_WEBHOOK_URL, json={"content": msg, "tts": False})
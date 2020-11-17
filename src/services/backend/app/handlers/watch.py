import boto3
import requests
import yfinance
from decouple import config

from .utils import fetch_from_yahoo
from ..tools import Strategy

DISCORD_WEBHOOK_URL = config("DISCORD_WEBHOOK_URL")

yfinance.pdr_override()

dynamodb = boto3.resource('dynamodb')


def watch_handler(event, context):
    data = dynamodb.Table('bot').scan(Limit=1000)
    all_symbols = [item["symbol"] for item in data["Items"]]

    df = fetch_from_yahoo(all_symbols)
    for item in data["Items"]:
        symbol = item["symbol"]

        chart = df[symbol]
        strategy = Strategy.objects.get(name=item.get("strategy"))

        action = strategy().fit(chart).action()
        if action is not action.hold:
            # notify in discord with webhook
            requests.post(DISCORD_WEBHOOK_URL, json={"content": f"time to {action.value} {symbol}", "tts": False})

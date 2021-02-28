import boto3
import yfinance

from .utils import fetch_from_yahoo
from .models import Strategy
from .utils.message import send_message_to_discord

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
            send_message_to_discord(f"time to {action.value} {symbol}")

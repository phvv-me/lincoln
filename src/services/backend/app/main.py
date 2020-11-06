import boto3
import requests
import yfinance
from decouple import config
from ta.momentum import RSIIndicator
from pandas_datareader import data as pdr

DISCORD_WEBHOOK_URL = config("DISCORD_WEBHOOK_URL")

yfinance.pdr_override()

dynamodb = boto3.resource('dynamodb')


def handler(event, context):
    data = dynamodb.Table('bot').scan(Limit=1000)
    all_symbols = [item["symbol"] for item in data["Items"]]

    df = pdr.get_data_yahoo(" ".join(all_symbols), period="5d", interval="30m")

    for symbol, close in df["Close"].iteritems():
        rsi = RSIIndicator(close, n=14).rsi()

        last = rsi.iloc[-1]
        if last < 20:
            action = "buy"
        elif last > 80:
            action = "sell"
        else:
            continue

        # notify in discord with webhook
        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"time to {action} {symbol}", "tts": False})

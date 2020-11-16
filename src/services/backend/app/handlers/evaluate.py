import logging

import boto3
import yfinance
from decouple import config
from pandas_datareader import data as pdr

from .utils import fetch_from_yahoo
from ..tools.strategies.models import ALL_STRATEGIES

DISCORD_WEBHOOK_URL = config("DISCORD_WEBHOOK_URL")

yfinance.pdr_override()

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('bot')

# Set up logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_best_strategy(chart):
    best_strategy, best_profit = None, None
    for strategy in ALL_STRATEGIES:
        st = strategy().fit(chart)
        stp = st.profit(operation_tax=4.9, short_allowed=False)

        if stp.value > getattr(best_profit, 'value', 1):
            best_strategy = str(st)
            best_profit = stp

    if best_strategy:
        logger.info(f"strategy {best_strategy} had profit {best_profit.value:.3f} with {best_profit.number_operations} operations")

    return best_strategy


def evaluation_handler(event, context):
    """This function is responsible for choosing the
    best strategy, when there is one, for each item in the table.
    """
    data = table.scan(Limit=1000)
    # symbols_without_strategy = [item["symbol"] for item in data["Items"] if item.get("strategy") is None]
    all_symbols = [item["symbol"] for item in data["Items"]]

    df = fetch_from_yahoo(all_symbols)
    for symbol in all_symbols:
        chart = df[symbol]
        if (strategy := get_best_strategy(chart)) is not None:
            logger.info(f"symbol {symbol} found strategy {strategy}")
            table.put_item(Item={
                "symbol": str(symbol),
                "strategy": str(strategy)
            })

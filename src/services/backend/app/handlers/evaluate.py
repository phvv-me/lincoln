import logging

import boto3
import yfinance
from decouple import config
from pandas_datareader import data as pdr

from ..tools.strategies.models import ALL_STRATEGIES

DISCORD_WEBHOOK_URL = config("DISCORD_WEBHOOK_URL")

yfinance.pdr_override()

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('bot')

# Set up logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_best_strategy(chart):
    best_strategy, best_profit = None, 1
    for strategy in ALL_STRATEGIES:
        st = strategy().fit(chart)
        stp = st.profit(operation_tax=4.9, short_allowed=True)

        logger.debug(f"strategy {st} had profit {stp.value}")
        if profit := stp.value > best_profit:
            best_strategy = str(st)
            best_profit = profit

    return best_strategy


def evaluation_handler(event, context):
    """This function is responsible for choosing the
    best strategy, when there is one, for each item in the table.
    """
    data = table.scan(Limit=1000)
    symbols_without_strategy = [item["symbol"] for item in data["Items"] if item.get("strategy") is None]
    symbols_str = " ".join(symbols_without_strategy)

    df = pdr.get_data_yahoo(symbols_str, period="5d", interval="30m")

    for symbol in symbols_without_strategy:
        chart = df.swaplevel(axis=1)[symbol] if len(symbols_without_strategy) > 1 else df
        if strategy := get_best_strategy(chart) is not None:
            logger.debug(f"symbol {symbol} found strategy {strategy}")
            table.put_item(Item={
                "symbol": symbol,
                "strategy": strategy
            })

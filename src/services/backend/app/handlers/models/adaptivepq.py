import logging
from dataclasses import dataclass

from pandas import DataFrame, concat
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

from .abc import BaseStrategy, Action

logging.basicConfig()
logger = logging.getLogger(__name__)


@dataclass
class AdaptivePQ(BaseStrategy):
    rsi_n: int = 14  # rsi window
    ema_n: int = 12  # rsi ema window
    lb: int = 20  # lower bound
    ub: int = 80  # upper bound

    def choose(self, open, close, rsi, rsi_ema) -> Action:
        is_trend_changing = rsi_ema < self.lb or rsi_ema > self.ub

        # price is increasing
        if close > open and rsi > rsi_ema and is_trend_changing:
            return Action.buy
        # price is decreasing
        elif close < open and rsi < rsi_ema and is_trend_changing:
            return Action.sell
        return Action.hold

    def fit(self, df: DataFrame):
        rsi = RSIIndicator(df["Close"], n=self.rsi_n, fillna=False).rsi().fillna(method='ffill').fillna(value=0)
        rsi_ema = EMAIndicator(close=rsi, n=self.ema_n).ema_indicator().fillna(method='ffill').fillna(value=0)

        rsi[:self.ema_n - 1] = 0

        args = df[["Open", "Close"]].join(rsi).join(rsi_ema)

        super().apply_choose(args)
        return super().fit(df)

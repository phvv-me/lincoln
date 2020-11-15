from dataclasses import dataclass

from pandas import DataFrame
from ta.momentum import RSIIndicator

from ..base import Strategy, Action


@dataclass
class RSI(Strategy):
    n: int = 14  # window
    lb: int = 20  # lower bound
    ub: int = 80  # upper bound

    def choose(self, rsi: int) -> Action:
        if rsi < self.lb:
            return Action.sell
        elif rsi > self.ub:
            return Action.buy
        return Action.hold

    def fit(self, df: DataFrame):
        self._actions = RSIIndicator(df["Close"], n=14).rsi().apply(self.choose)
        return super().fit(df)
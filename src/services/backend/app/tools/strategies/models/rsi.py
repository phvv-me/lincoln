from dataclasses import dataclass

from pandas import DataFrame
from ta.momentum import RSIIndicator

from ..base import BaseStrategy, Action


@dataclass
class RSI(BaseStrategy):
    n: int = 14  # window
    lb: int = 20  # lower bound
    ub: int = 80  # upper bound

    def choose(self, rsi: float) -> Action:
        if rsi < self.lb:
            return Action.sell
        elif rsi > self.ub:
            return Action.buy
        return Action.hold

    def fit(self, df: DataFrame):
        args = RSIIndicator(df["Close"], n=self.n).rsi().to_frame()

        super().apply_choose(args)
        return super().fit(df)

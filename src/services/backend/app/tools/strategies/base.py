from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

from pandas import DataFrame, Series


class Action(Enum):
    buy = 'BUY'
    sell = 'SELL'
    hold = 'HOLD'


class State(Enum):
    none = 'NONE'
    long = 'LONG'
    short = 'SHORT'


class Profit:

    def __init__(self, operation_tax: Optional[float]):
        assert operation_tax >= 0 if operation_tax is not None else True
        self._state = State.none

        # TODO: how to make operation tax relevant but not 'overly' relevant
        self._gold = self._starting_gold = 100_000 if operation_tax else operation_tax * 100
        self._stock = 0
        self._tax = 0

        self.operation_tax = operation_tax

    @property
    def state(self) -> State:
        return self._state

    @property
    def value(self) -> float:
        """current profit"""
        assert self._stock == 0
        return (self._gold - self._tax) / self._starting_gold

    @property
    def tax(self) -> float:
        return self._tax

    @property
    def number_operations(self) -> int:
        return int(self._tax / self.operation_tax)

    def _pay_tax(self):
        self._tax += self.operation_tax

    def open_long_position(self, price):
        if self.state is State.long:
            # finish here and do nothing
            return

        self.close(price)
        self._state = State.long

        self._pay_tax()

        # spends all gold in stocks
        self._stock = self._gold / price
        self._gold = 0

    def close_long_position(self, price):
        assert self.state is State.long
        self._state = State.none

        self._pay_tax()

        # sells all stock
        self._gold = self._stock * price
        self._stock = 0

    def open_short_position(self, price):
        if self.state is State.short:
            # finish here and do nothing
            return

        self.close(price)
        self._state = State.short

        self._pay_tax()

        # rent stock in equal value to gold
        self._stock = -self._gold / price
        self._gold *= 2

    def close_short_position(self, price):
        assert self.state is State.short
        self._state = State.none

        self._pay_tax()

        # pays debt
        self._gold -= abs(self._stock * price)
        self._stock = 0

    def close(self, price):
        """closes current positions"""
        if self.state is State.long:
            self.close_long_position(price)
        elif self.state is State.short:
            self.close_short_position(price)


class Strategy(ABC):
    def __init__(self, *args, **kwargs):
        self._data: Optional[DataFrame] = None
        self._actions: Optional[Series] = None

    def __str__(self):
        return self.__class__.__name__

    @abstractmethod
    def choose(self, rsi: int) -> Action:
        raise NotImplementedError

    @abstractmethod
    def fit(self, df: DataFrame):
        self._data = df
        return self

    def action(self) -> Action:
        """returns last action"""
        return self._actions.iloc[-1]

    def profit(self, operation_tax=4.9, short_allowed=False) -> Profit:
        """evaluates strategy profit"""
        p = Profit(operation_tax)
        for c, a in zip(self._data["Close"], self._actions):
            if a is Action.buy:
                p.open_long_position(c)
            elif a is Action.sell:
                if short_allowed:
                    p.open_short_position(c)
                else:
                    p.close(c)

        # be sure to end all operations before seeing profit
        p.close(price=self._data["Close"].iloc[-1])
        return p

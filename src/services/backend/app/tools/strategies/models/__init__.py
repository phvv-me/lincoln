from typing import Type, Optional

from .adaptivepq import AdaptivePQ
from .rsi import RSI
from ..base import BaseStrategy

ALL_STRATEGIES = [
    RSI,
    AdaptivePQ
]

DEFAULT_STRATEGY = RSI


class Strategy:
    class objects:

        @staticmethod
        def all():
            return ALL_STRATEGIES

        @staticmethod
        def get(name: Optional[str]) -> Optional[Type[BaseStrategy]]:
            strategies_map = {s.__name__: s for s in ALL_STRATEGIES}
            return strategies_map.get(name, DEFAULT_STRATEGY)



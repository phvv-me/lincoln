from typing import Type, Optional

from .adaptivepq import AdaptivePQ
from .rsi import RSI
from ..base import Strategy

ALL_STRATEGIES = [
    RSI,
    AdaptivePQ
]

DEFAULT_STRATEGY = RSI


def get_strategy(name: Optional[str]) -> Optional[Type[Strategy]]:
    strategies_map = {s.__name__: s for s in ALL_STRATEGIES}
    return strategies_map.get(name, DEFAULT_STRATEGY)

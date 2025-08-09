
from abc import ABC, abstractmethod
import pandas as pd

class TradingStrategy(ABC):
    name: str = "Base"
    @abstractmethod
    def signal(self, df: pd.DataFrame) -> int:
        """Return -1 sell, 0 hold, 1 buy"""
        raise NotImplementedError

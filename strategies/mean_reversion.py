
import pandas as pd
from .base import TradingStrategy

class MeanReversion(TradingStrategy):
    name = "Mean Reversion"
    def signal(self, df: pd.DataFrame) -> int:
        last = df.iloc[-1]
        if last["close"] < last["bb_lower"] and last["rsi"] < 30:
            return 1
        if last["close"] > last["bb_upper"] and last["rsi"] > 70:
            return -1
        return 0

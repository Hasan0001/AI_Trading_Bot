
import pandas as pd
from .base import TradingStrategy

class Breakout(TradingStrategy):
    name = "Breakout"
    def signal(self, df: pd.DataFrame) -> int:
        # Simple breakout: price breaks prior N highs/lows scaled by ATR
        N = 20
        last = df.iloc[-1]
        recent = df.iloc[-N:]
        high = recent["high"].max()
        low = recent["low"].min()
        if last["close"] > high + last["atr"] * 0.1:
            return 1
        if last["close"] < low - last["atr"] * 0.1:
            return -1
        return 0

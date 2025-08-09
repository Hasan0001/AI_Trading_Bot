
import pandas as pd
from .base import TradingStrategy

class TrendFollowing(TradingStrategy):
    name = "Trend Following"
    def signal(self, df: pd.DataFrame) -> int:
        last = df.iloc[-1]
        # EMA crossover + MACD confirmation
        if last["ema_12"] > last["ema_26"] and last["macd"] > last["macd_signal"]:
            return 1
        if last["ema_12"] < last["ema_26"] and last["macd"] < last["macd_signal"]:
            return -1
        return 0

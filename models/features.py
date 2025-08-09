
import pandas as pd
import numpy as np

FEATURE_COLUMNS = [
    "returns","sma_10","sma_30","ema_12","ema_26","macd","macd_signal","macd_hist",
    "rsi","bb_upper","bb_mid","bb_lower","stoch_k","stoch_d","atr","volatility",
    "close","high","low","volume"
]

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    X = df[FEATURE_COLUMNS].copy()
    X = X.replace([np.inf, -np.inf], np.nan).fillna(method="ffill").fillna(method="bfill")
    return X

def build_labels_from_signals(signals: pd.Series) -> pd.Series:
    # map {-1,0,1} to {0,1,2} for sparse categorical (hold=0, buy=1, sell=2)
    mapping = {0:0, 1:1, -1:2}
    return signals.map(mapping)

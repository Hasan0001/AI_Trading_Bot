
import pandas as pd
import numpy as np
try:
    import talib
    TALIB_AVAILABLE = True
except Exception:
    TALIB_AVAILABLE = False
    import pandas_ta as ta
from logger_setup import setup_logger

logger = setup_logger("indicators")

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    close = d["close"].values

    # SMA / EMA
    if TALIB_AVAILABLE:
        d["sma_10"] = talib.SMA(close, timeperiod=10)
        d["sma_30"] = talib.SMA(close, timeperiod=30)
        d["ema_12"] = talib.EMA(close, timeperiod=12)
        d["ema_26"] = talib.EMA(close, timeperiod=26)
        macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        d["macd"] = macd; d["macd_signal"] = macdsignal; d["macd_hist"] = macdhist
        d["rsi"] = talib.RSI(close, timeperiod=14)
        upper, middle, lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        d["bb_upper"]=upper; d["bb_mid"]=middle; d["bb_lower"]=lower
        slowk, slowd = talib.STOCH(d["high"].values, d["low"].values, close)
        d["stoch_k"]=slowk; d["stoch_d"]=slowd
        d["atr"] = talib.ATR(d["high"].values, d["low"].values, close, timeperiod=14)
    else:
        d["sma_10"] = d["close"].rolling(10).mean()
        d["sma_30"] = d["close"].rolling(30).mean()
        d["ema_12"] = d["close"].ewm(span=12, adjust=False).mean()
        d["ema_26"] = d["close"].ewm(span=26, adjust=False).mean()
        macd = d["ema_12"] - d["ema_26"]
        d["macd"]=macd; d["macd_signal"]=macd.ewm(span=9, adjust=False).mean()
        d["macd_hist"]= d["macd"] - d["macd_signal"]
        d["rsi"] = ta.rsi(d["close"], length=14)
        bb = ta.bbands(d["close"], length=20, std=2)
        d["bb_upper"]=bb["BBU_20_2.0"]; d["bb_mid"]=bb["BBM_20_2.0"]; d["bb_lower"]=bb["BBL_20_2.0"]
        stoch = ta.stoch(d["high"], d["low"], d["close"])
        d["stoch_k"]=stoch["STOCHk_14_3_3"]; d["stoch_d"]=stoch["STOCHd_14_3_3"]
        d["atr"] = ta.atr(d["high"], d["low"], d["close"], length=14)

    d["volatility"] = d["returns"].rolling(20).std()
    d.dropna(inplace=True)
    return d

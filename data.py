
import pandas as pd
import numpy as np
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from typing import Optional
from logger_setup import setup_logger
import time

logger = setup_logger("data")

def make_client():
    if settings.testnet:
        client = Client(settings.api_key, settings.api_secret, testnet=True)
        # python-binance auto-picks testnet endpoint when testnet=True
    else:
        client = Client(settings.api_key, settings.api_secret)
    return client

def fetch_klines(client: Client, symbol: str, interval: str, limit: int = 500) -> Optional[pd.DataFrame]:
    try:
        raw = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Binance error fetching klines: {e}")
        return None
    cols = ["open_time","open","high","low","close","volume","close_time","quote_asset_volume",
            "number_of_trades","taker_buy_base","taker_buy_quote","ignore"]
    df = pd.DataFrame(raw, columns=cols)
    for c in ["open","high","low","close","volume"]:
        df[c] = df[c].astype(float)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    df.set_index("close_time", inplace=True)
    df["returns"] = np.log(df["close"]).diff()
    return df

def wait_for_next_candle(interval_sec: int = 300):
    # simple sleep to next multiple of interval
    now = int(time.time())
    sleep = interval_sec - (now % interval_sec) + 1
    time.sleep(min(max(sleep, 5), interval_sec))


from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Settings:
    api_key: str = os.getenv("BINANCE_API_KEY", "")
    api_secret: str = os.getenv("BINANCE_API_SECRET", "")
    testnet: bool = os.getenv("BINANCE_TESTNET", "true").lower() == "true"
    symbol: str = "BTCUSDT"
    interval: str = "5m"
    base_budget_usdt: float = 50.0
    retrain_every_trades: int = 10

settings = Settings()

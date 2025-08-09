# Advanced AI Trading Bot (Binance, GUI, ML)

**Features**
- Three strategies: Trend Following (SMA/EMA/MACD), Mean Reversion (Bollinger+RSI), Breakout (ATR+S/R)
- ML: RandomForest + Keras Neural Network (20 inputs, 2 hidden layers + dropout, 3-way output: hold/buy/sell)
- Paper & Real trading modes, dynamic position sizing, risk metrics, continuous learning
- Tkinter GUI (dark "web3" vibe): config, controls, live status, performance dashboard, real-time chart, log
- Modular design, threading, detailed logging, unit tests

## 1) Prerequisites
- Python 3.10 or 3.11 (recommended)
- TA-Lib system libs (if unavailable, the bot falls back to `pandas_ta` for most indicators)
  - **Windows**: install TA-Lib wheel matching your Python from e.g. Christoph Gohlke or use `pip install TA-Lib` if it works.
  - **macOS (brew)**: `brew install ta-lib`
  - **Linux (Debian/Ubuntu)**: `sudo apt-get install -y ta-lib` or build from source.
- A Binance account + API key/secret with **Enable Reading** and **Enable Spot & Margin Trading** (keep secret!)

## 2) Install
```bash
cd ai_trading_bot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3) Configure API keys
Create a `.env` file in the project root with:
```env
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
BINANCE_TESTNET=true  # set to false for real trading
```

## 4) Run (GUI)
```bash
python run.py
```
- Choose paper or real mode, select model (RF/NN), set budget per trade, pick the trading pair (e.g., BTCUSDT).
- Click **Start Bot**. The bot auto-collects initial data (five 5‑minute candles), trains models, and begins paper trading by default.

## 5) Tests
```bash
pytest -q
```

## Notes
- **Education only. Not financial advice.** Try **paper trading** before enabling real trades.
- The GUI uses a dark neon palette to evoke a web3 style.
- If TA-Lib is not present, indicator coverage is handled by `pandas_ta`; results may vary slightly.


## Windows quick install (no TA-Lib)

If TA-Lib gives you trouble on Windows, use the no-TA-Lib setup:

```bat
py -3 -m venv .venv
.venv\Scripts\activate
pip install -r requirements_no_talib.txt
```

The bot will automatically use `pandas_ta` for indicators. You can always install TA-Lib later.


### No file config needed
Enter your **API Key** and **Secret** directly in the GUI. The app will connect using those; `.env` is optional.

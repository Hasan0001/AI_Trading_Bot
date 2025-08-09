<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<meta name="color-scheme" content="dark light" />
</head>
<body>
<main class="wrap">
  <h1>AI Crypto Trading Bot (Binance, GUI, ML)</h1>
  <p class="small">&gt; Prototype trading bot (built with ChatGPT). Feedback and improvements welcome.</p>

  <div class="panel">
    <p>A Windows‑friendly trading bot for <strong>Binance Spot</strong> with a <strong>no‑coding GUI</strong>, multiple rule‑based strategies, <strong>machine learning</strong> (Random Forest + Neural Network), paper/live modes, dynamic risk sizing, and real‑time charts. Paste your <strong>API key/secret directly in the GUI</strong>no <code>.env</code> or code editing required.</p>
    <p class="warn"><strong>Education only — not financial advice.</strong> Always start in <strong>Paper (Testnet)</strong> mode.</p>
  </div>

  <h2 id="features">✨ Features</h2>
  <div class="grid cols-2">
    <div class="panel">
      <h3>Zero‑config GUI</h3>
      <ul>
        <li>Masked <strong>API Key/Secret</strong> fields (paste directly)</li>
        <li>Mode: <strong>Paper (Testnet)</strong> or <strong>Real (Mainnet)</strong></li>
        <li>Model selection: <strong>RF</strong> (Random Forest) / <strong>NN</strong> (Keras)</li>
        <li>Budget per trade (USDT) + Pair picker (e.g., <code>BTCUSDT</code>)</li>
        <li>Start/Stop, Train, Save Model</li>
        <li>Live status: connection, equity, drawdown, Sharpe, active strategy</li>
        <li>Real‑time chart (Close + SMA10/30) and activity log</li>
      </ul>
    </div>
    <div class="panel">
      <h3>Strategies (ensemble)</h3>
      <ul>
        <li><strong>Trend Following:</strong> EMA(12/26) + MACD confirmation</li>
        <li><strong>Mean Reversion:</strong> Bollinger Bands + RSI (30/70)</li>
        <li><strong>Breakout:</strong> ATR‑aware break of recent highs/lows</li>
      </ul>
      <h3>Machine Learning</h3>
      <ul>
        <li><strong>RandomForestClassifier</strong> (100 estimators)</li>
        <li><strong>Keras Neural Network:</strong> 20 inputs → 64 → 32 (dropout) → 3‑class (hold/buy/sell), <em>early stopping</em></li>
        <li>Model persistence (save/load)</li>
      </ul>
    </div>
  </div>

  <div class="panel">
    <h3>Risk &amp; Automation</h3>
    <ul>
      <li>Dynamic position sizing by recent volatility</li>
      <li>Initial data collection → <strong>auto‑train</strong></li>
      <li><strong>Continuous learning:</strong> retrain every N trades (default 10)</li>
      <li>Auto strategy evaluation on a rolling window</li>
    </ul>
    <h3>Execution</h3>
    <ul>
      <li><strong>Paper trades</strong> on Binance <strong>Testnet</strong></li>
      <li><strong>Real trades</strong> on Binance <strong>Mainnet</strong> (MARKET orders)</li>
      <li>Exchange <strong>filters</strong>: respects <code>LOT_SIZE</code> and <code>MIN_NOTIONAL</code></li>
    </ul>
  </div>

  <h2 id="structure">📦 Project Structure</h2>
  <pre><code>ai_trading_bot/
├─ run.py                 # App entrypoint (GUI)
├─ gui.py                 # Tkinter GUI (web3-ish dark theme)
├─ trading_bot.py         # Main orchestration loop
├─ data.py                # Binance client &amp; klines
├─ indicators.py          # TA-Lib (if available) or pandas_ta fallback
├─ execution.py           # Paper/Real order placement with filters
├─ performance.py         # Equity, drawdown, Sharpe
├─ risk.py                # Dynamic sizing by volatility
├─ logger_setup.py        # Logging
├─ config.py              # Defaults (interval, retrain cadence)
├─ models/
│  ├─ features.py         # Feature engineering (20 inputs)
│  ├─ manager.py          # Model selection &amp; IO
│  ├─ rf_model.py         # RandomForest wrapper
│  └─ nn_model.py         # Keras NN wrapper
├─ strategies/
│  ├─ base.py
│  ├─ trend.py
│  ├─ mean_reversion.py
│  └─ breakout.py
├─ requirements.txt             # Full (TA‑Lib optional)
├─ requirements_no_talib.txt    # Windows‑friendly (uses pandas_ta)
└─ tests/
   └─ test_imports.py
</code></pre>

  <h2 id="quickstart">🖥️ Quick Start (Windows, zero‑config)</h2>
  <div class="callout">
    <p><strong>Recommended Python:</strong> 3.11 (64‑bit). Many ML/data packages don’t ship wheels for 3.13 on Windows yet.</p>
  </div>
  <ol>
    <li>
      <strong>Install Python 3.11 (64‑bit)</strong>
      <pre><code>winget install Python.Python.3.11</code></pre>
    </li>
    <li>
      <strong>Create venv &amp; install deps (no TA‑Lib needed)</strong>
      <pre><code>py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install --only-binary=:all: numpy==1.26.4 pandas==2.2.2 scipy==1.14.1 scikit-learn==1.5.1 matplotlib==3.9.0
pip install python-binance==1.0.19 python-dotenv==1.0.1 pandas_ta==0.3.14b0 pillow==10.4.0 tensorflow==2.16.1</code></pre>
      <p class="small">If you want TA‑Lib later, install the system library first; otherwise the bot automatically uses <code>pandas_ta</code>.</p>
    </li>
    <li>
      <strong>Run</strong>
      <pre><code>python run.py</code></pre>
    </li>
    <li>
      <strong>In the GUI</strong>
      <ul>
        <li>Paste <strong>API Key</strong> and <strong>Secret</strong> (masked)</li>
        <li>Choose <strong>Paper</strong> (Testnet) or <strong>Real</strong> (Mainnet)</li>
        <li>Pick <strong>RF</strong> or <strong>NN</strong>, set <strong>Budget</strong> and <strong>Pair</strong></li>
        <li>Click <strong>Start Bot</strong></li>
      </ul>
    </li>
  </ol>

  <h2 id="binance">🔑 Binance API (fast guide)</h2>
  <ul>
    <li><strong>Mainnet:</strong> Profile → <em>API Management</em> → Create API. Permissions: <strong>Read</strong> + <strong>Spot &amp; Margin Trading</strong> (no withdrawals).</li>
    <li><strong>Testnet:</strong> Use <em>Binance Spot Testnet</em> (separate login &amp; keys).</li>
    <li>Keys are <strong>not interchangeable</strong> between testnet and mainnet.</li>
    <li>If restricting by IP, add your current IP or leave off while testing.</li>
  </ul>

  <h2 id="flow">🧠 How it works (data → decision → trade)</h2>
  <ol>
    <li><strong>Data:</strong> 5‑minute klines from Binance.</li>
    <li><strong>Indicators:</strong> SMA/EMA, MACD, RSI, Bollinger, Stochastic, ATR, volatility.</li>
    <li><strong>Strategies:</strong> Signals from trend, mean‑reversion, breakout.</li>
    <li><strong>ML:</strong> 20‑feature vector → RF/NN predicts hold/buy/sell.</li>
    <li><strong>Risk:</strong> Dynamic size scaled by volatility.</li>
    <li><strong>Execution:</strong> MARKET order (paper/real) with lot/min-notional checks.</li>
    <li><strong>Tracking:</strong> Equity, drawdown, Sharpe, strategy performance.</li>
    <li><strong>Learning:</strong> Periodic retraining as new data arrives.</li>
  </ol>

  <h2 id="config">⚙️ Configuration Notes</h2>
  <ul>
    <li><strong>No files to edit</strong>—everything is in the GUI.</li>
    <li>Default interval = <strong>5m</strong> (change in <code>config.py</code> if needed).</li>
    <li>Retrain cadence (default <strong>every 10 trades</strong>) is in <code>config.py</code>.</li>
  </ul>

  <h2 id="testing">🧪 Testing</h2>
  <pre><code>.venv\Scripts\activate
pytest -q</code></pre>

  <h2 id="troubleshooting">🛟 Troubleshooting</h2>
  <ul>
    <li><strong>Import errors on Windows:</strong> Use Python <strong>3.11 (64‑bit)</strong> and the <em>binary‑only</em> installs shown above.</li>
    <li><strong>Timestamp / recvWindow:</strong> Sync Windows clock (Settings → Time &amp; Language → Sync now).</li>
    <li><strong>“MIN_NOTIONAL” / “LOT_SIZE”:</strong> Increase budget per trade; bot rounds quantity to allowed step.</li>
    <li><strong>Auth fails:</strong> Confirm permissions; use testnet keys in Paper, mainnet in Real; check IP restrictions.</li>
  </ul>

  <h2 id="security">🔒 Security</h2>
  <ul>
    <li>Never share your <strong>Secret Key</strong>.</li>
    <li>Keep <strong>withdrawals disabled</strong> for the API key.</li>
    <li>Prefer <strong>IP restriction</strong> once stable.</li>
    <li>Start on <strong>Testnet</strong> and paper trade first.</li>
  </ul>

  <h2 id="roadmap">🗺️ Roadmap</h2>
  <ul>
    <li>Stop‑loss / take‑profit orders</li>
    <li>Multi‑pair portfolio view &amp; position sizing</li>
    <li>More strategies (e.g., momentum + regime filters)</li>
    <li>Backtesting module</li>
    <li>Sentiment/news signals</li>
    <li>Cloud deploy for 24/7 uptime</li>
  </ul>

  <h2 id="contrib">🤝 Contributing</h2>
  <p>Issues and PRs welcome! Please keep features modular (new <code>Strategy</code> classes, separate model wrappers), include basic tests and docs, and preserve the GUI zero‑config workflow.</p>

  <h2 id="license">📜 License</h2>
  <p>MIT (or your preferred license)</p>

  <h2 id="credits">🙏 Credits</h2>
  <ul>
    <li>Built with help from <strong>ChatGPT</strong></li>
    <li>Indicators: <strong>TA‑Lib</strong> (optional) and <strong>pandas_ta</strong> fallback</li>
    <li>Exchange: <strong>Binance</strong></li>
  </ul>

  <hr />
</main>
</body>
</html>

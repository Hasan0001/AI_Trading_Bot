import threading
from logger_setup import setup_logger
from data import make_client, fetch_klines, wait_for_next_candle
from indicators import add_indicators
from strategies.trend import TrendFollowing
from strategies.mean_reversion import MeanReversion
from strategies.breakout import Breakout
from models.manager import ModelManager
from risk import dynamic_position_size
from performance import PerfTracker
from execution import Trader
from config import settings

logger = setup_logger("bot")


class AdvancedTradingBot:
    def __init__(self, gui_callback=None):
        self.client = None
        self.symbol = settings.symbol
        self.interval = settings.interval
        self.paper = True
        self.model_type = "RF"
        self.budget_usdt = 50.0
        self.model_mgr = None
        self.trader = None
        self.perf = PerfTracker(cash=1000.0)
        self.active_strategy_name = "Trend Following"
        self.strategies = {
            "Trend Following": TrendFollowing(),
            "Mean Reversion": MeanReversion(),
            "Breakout": Breakout(),
        }
        self.trade_count_since_train = 0
        self.thread = None
        self.running = False
        self.gui_callback = gui_callback

    def configure(self, symbol, paper, model_type, budget_usdt, api_key, api_secret):
        self.symbol = symbol
        self.paper = paper
        self.budget_usdt = float(budget_usdt)
        self.client = make_client(api_key, api_secret, paper)
        self.trader = Trader(client=self.client, symbol=self.symbol, paper=paper)
        self.model_type = model_type
        self.model_mgr = ModelManager(model_type)

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

    def _loop(self):
        hist = fetch_klines(self.client, self.symbol, self.interval, limit=210)
        if hist is None:
            logger.error("No historical data; stopping.")
            self.running = False
            return

        df = add_indicators(hist)
        sig_series = df.apply(self._blend_strategies_signal, axis=1)
        self.model_mgr.train(df, sig_series)
        self._emit_status("Model trained on initial batch.")

        while self.running:
            wait_for_next_candle(300)
            hist = fetch_klines(self.client, self.symbol, self.interval, limit=210)
            if hist is None:
                continue

            df = add_indicators(hist)
            last = df.iloc[-1]
            self.active_strategy_name = self._select_best_strategy(df.tail(120))
            model_pred = self._predict_action(last)

            volatility = float(df["volatility"].iloc[-1])
            usdt = dynamic_position_size(volatility, self.budget_usdt)
            price = float(last["close"])
            qty = max(usdt / price, 1e-6)

            side = None
            if model_pred == 1:
                side = "BUY"
            elif model_pred == 2:
                side = "SELL"

            if side:
                order = self.trader.place_order(side, qty, price)
                self.perf.update_on_trade(order.side, order.qty, order.price)
                self.trade_count_since_train += 1
                if self.trade_count_since_train >= settings.retrain_every_trades:
                    sig_series = df.apply(self._blend_strategies_signal, axis=1)
                    self.model_mgr.train(df, sig_series)
                    self.trade_count_since_train = 0
                    self._emit_status("Model retrained.")

            self._emit_metrics(df)

        self._emit_status("Stopped.")

    def _emit_status(self, msg):
        logger.info(msg)
        if self.gui_callback:
            self.gui_callback({"type": "status", "message": msg})

    def _emit_metrics(self, df):
        if self.gui_callback:
            self.gui_callback({
                "type": "metrics",
                "equity": self.perf.equity,
                "cash": self.perf.cash,
                "coin": self.perf.coin,
                "drawdown": self.perf.max_drawdown(),
                "sharpe": self.perf.sharpe(),
                "strategy": self.active_strategy_name,
                "price": float(df.iloc[-1]["close"]),
            })

    def _blend_strategies_signal(self, row):
        vals = []
        import pandas as pd
        for s in self.strategies.values():
            mini = pd.DataFrame([row.values], columns=row.index)
            vals.append(s.signal(mini))
        ssum = sum(vals)
        if ssum > 0:
            return 1
        if ssum < 0:
            return -1
        return 0

    def _select_best_strategy(self, df_window):
        best_name = None
        best_score = -1e9
        price = df_window["close"].values
        import numpy as np
        for name, strat in self.strategies.items():
            signals = []
            for i in range(1, len(df_window)):
                signals.append(strat.signal(df_window.iloc[:i]))
            sig = np.array([0] + signals)
            rets = np.diff(price) / price[:-1]
            pnl = (sig[:-1] * rets).sum()
            if pnl > best_score:
                best_score = pnl
                best_name = name
        return best_name

    def _predict_action(self, last_row):
        pred = self.model_mgr.predict(last_row)
        return pred

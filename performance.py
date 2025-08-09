
from dataclasses import dataclass, field
import numpy as np

@dataclass
class PerfTracker:
    equity: float = 0.0
    cash: float = 1000.0
    coin: float = 0.0
    last_price: float = 0.0
    total_trades: int = 0
    wins: int = 0
    losses: int = 0
    pnl_history: list = field(default_factory=list)

    def update_on_trade(self, side: str, qty: float, price: float):
        self.total_trades += 1
        if side == "BUY":
            self.cash -= qty * price
            self.coin += qty
        elif side == "SELL":
            self.cash += qty * price
            self.coin -= qty
        self.last_price = price
        self.equity = self.cash + self.coin * price
        self.pnl_history.append(self.equity)

    def max_drawdown(self):
        if not self.pnl_history:
            return 0.0
        peaks = np.maximum.accumulate(self.pnl_history)
        drawdowns = (peaks - self.pnl_history) / peaks
        return float(np.max(drawdowns))

    def sharpe(self):
        if len(self.pnl_history) < 2:
            return 0.0
        rets = np.diff(self.pnl_history)
        if rets.std() == 0:
            return 0.0
        return float(rets.mean() / rets.std() * (len(rets) ** 0.5))

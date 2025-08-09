
from dataclasses import dataclass
from logger_setup import setup_logger
from typing import Optional, Dict, Any
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
import math

logger = setup_logger("exec")

@dataclass
class Order:
    side: str
    qty: float
    price: float
    paper: bool = True
    raw: Optional[Dict[str, Any]] = None

class Trader:
    def __init__(self, client: Optional[Client] = None, symbol: str = "BTCUSDT", paper: bool = True):
        self.paper = paper
        self.client = client
        self.symbol = symbol
        self._filters = None  # cache of symbol filters

    # --- filters & rounding helpers ---
    def _load_filters(self):
        if self._filters is not None or self.client is None:
            return
        try:
            info = self.client.get_symbol_info(self.symbol)
            if not info:
                raise RuntimeError(f"No symbol info for {self.symbol}")
            f = {flt["filterType"]: flt for flt in info["filters"]}
            self._filters = f
        except Exception as e:
            logger.error(f"Failed loading filters: {e}")
            self._filters = {}

    def _step(self, value, step):
        if step is None:
            return value
        precision = int(round(-math.log(float(step), 10), 0)) if float(step) != 0 else 8
        return math.floor(value / float(step)) * float(step)

    def _round_qty(self, qty: float) -> float:
        self._load_filters()
        lot = self._filters.get("LOT_SIZE", {})
        stepSize = lot.get("stepSize")
        minQty = float(lot.get("minQty", 0)) if lot else 0
        q = self._step(qty, stepSize) if stepSize else qty
        if q < minQty:
            q = 0.0
        return float(q)

    def _min_notional_ok(self, qty: float, price: float) -> bool:
        self._load_filters()
        mn = self._filters.get("MIN_NOTIONAL", {})
        minNotional = float(mn.get("minNotional", 0)) if mn else 0
        return (qty * price) >= minNotional if minNotional else True

    # --- public API ---
    def place_order(self, side: str, qty: float, price: float) -> Order:
        """Place MARKET order in real mode; log and simulate in paper."""
        side = side.upper()
        if side not in ("BUY", "SELL"):
            raise ValueError("side must be BUY or SELL")

        if self.paper or self.client is None:
            logger.info(f"Placing PAPER order: {side} {qty} @ {price}")
            return Order(side=side, qty=qty, price=price, paper=True)

        # real trading path
        try:
            rq = self._round_qty(qty)
            if rq <= 0:
                logger.warning("Rounded quantity is 0; skipping order.")
                return Order(side=side, qty=0, price=price, paper=False, raw={"skipped":"qty_rounded_to_zero"})

            if not self._min_notional_ok(rq, price):
                logger.warning("Below MIN_NOTIONAL; skipping order.")
                return Order(side=side, qty=rq, price=price, paper=False, raw={"skipped":"min_notional"})

            logger.info(f"Placing REAL MARKET order: {side} {rq} {self.symbol}")
            res = self.client.create_order(
                symbol=self.symbol,
                side=side,
                type="MARKET",
                quantity=float(rq)
            )
            fill_price = price
            try:
                # try to compute avg fill price from fills if provided
                if "fills" in res and res["fills"]:
                    total_qty = sum(float(f["qty"]) for f in res["fills"])
                    total_quote = sum(float(f["price"]) * float(f["qty"]) for f in res["fills"])
                    if total_qty > 0:
                        fill_price = total_quote / total_qty
            except Exception:
                pass

            return Order(side=side, qty=float(rq), price=float(fill_price), paper=False, raw=res)
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Binance order error: {e}")
            return Order(side=side, qty=0, price=price, paper=False, raw={"error":str(e)})
        except Exception as e:
            logger.error(f"Order exception: {e}")
            return Order(side=side, qty=0, price=price, paper=False, raw={"error":str(e)})


import numpy as np

def dynamic_position_size(volatility: float, base_budget_usdt: float = 50.0) -> float:
    # Reduce size when volatility is high
    if np.isnan(volatility) or volatility <= 0:
        return base_budget_usdt
    scale = 1.0 / (1.0 + 10.0 * volatility)  # simple inverse scaling
    return max(base_budget_usdt * scale, base_budget_usdt * 0.1)

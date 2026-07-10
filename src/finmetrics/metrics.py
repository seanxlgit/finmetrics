import numpy as np
from collections.abc import Sequence

# functions
def max_drawdown(prices: Sequence[float]) -> float:
    """ Max Drawdown over a price series.
        Returns the largest peak-to-trough declines as a negative fraction (0.0 if prices never fall)

    Raises:
        ValueError:  if empty list, single price, non-positive prices
    """
    if len(prices) < 2:
        raise ValueError(f"Need >= 2 prices, got {len(prices)}")
    elif any(x<=0 for x in prices):
        raise ValueError("Need positive prices. price<=0 found.")
    max_dd = 0.0
    peak = prices[0]
    for p in prices:
        peak = max(peak, p)
        max_dd = min(max_dd, (p - peak) / peak)
    return max_dd


def annualized_volatility(returns: Sequence[float], periods_per_year: int = 252) -> float:
    """ Annualized Volatility over a provided returns series
    Default periods_per_year: 252
    Calculates the annualized volatility as a non-negative decimal number (0.0 if no return changes)

    Raises:
        ValueError: if empty or single return, or periods_per_year < 2
    """
    if len(returns) < 2:
        raise ValueError(f"Need >=2 returns, got {len(returns)}")
    if periods_per_year < 2:
        raise ValueError(f"Need periods_per_year >= 2, got {periods_per_year}")
    # Calc
    return float(np.std(returns, ddof=1) * np.sqrt(periods_per_year))


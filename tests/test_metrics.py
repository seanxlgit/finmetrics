import pytest
from finmetrics import max_drawdown, annualized_volatility

@pytest.mark.parametrize("prices, expected", [
    ([1, 2, 3, 50, 30, 40, 30], -0.4),
    ([100, 60, 100], -0.4),
    ([100, 100, 110], 0.0),
])
def test_max_drawdown(prices, expected):
    assert max_drawdown(prices) == pytest.approx(expected)

def test_too_few_prices():
    with pytest.raises(ValueError, match="Need >= 2 prices, got 1"):
        max_drawdown([100])

def test_non_positive_prices():
    with pytest.raises(ValueError, match="Need positive prices. price<=0 found."):
        max_drawdown([100, 0.0, 20.5, 10.0])

@pytest.mark.parametrize("returns, periods_per_year, expected_vola", [
    ([0.15, 0.15, 0.15], 252, 0.0),
    ([0.20, 0.10, -0.10], 250, 2.415),
    ([-0.20, -0.10, 0.10], 250, 2.415),
])
def test_annualized_volatility(returns, periods_per_year, expected_vola):
    assert annualized_volatility(returns, periods_per_year) == pytest.approx(expected_vola, abs=0.001)

def test_too_few_returns():
    with pytest.raises(ValueError, match="Need >=2 returns, got 1"):
        annualized_volatility([0.1])

def test_too_small_periods():
    with pytest.raises(ValueError, match="Need periods_per_year >= 2, got 1"):
        annualized_volatility([0.15, 0.20, 0.1], 1)



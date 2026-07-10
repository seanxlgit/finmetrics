# finmetrics

A lightweight Python library for financial performance and risk metrics.

`finmetrics` provides clean, well-tested implementations of common investment performance statistics, making it easy to analyze portfolios, strategies, and backtests.

The project emphasizes:

- Simple and intuitive API
- Numerical correctness
- Extensive unit testing
- Minimal dependencies
- Well-documented implementations

---

## Features

Current and planned metrics include:

### Return Metrics

- Annualized Return (CAGR)
- Total Return
- Cumulative Return

### Risk Metrics

- Annualized Volatility
- Downside Deviation
- Maximum Drawdown
- Drawdown Duration

### Risk-Adjusted Performance

- Sharpe Ratio
- Sortino Ratio
- Calmar Ratio
- Information Ratio
- Treynor Ratio

### Benchmark Comparison

- Alpha
- Beta
- Tracking Error
- Active Return

---

## Installation

Clone the repository

```bash
git clone https://github.com/seanxlgit/finmetrics.git
cd finmetrics
```

Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
```

or

```powershell
.venv\Scripts\activate
```

Install in editable mode

```bash
pip install -e ".[dev]"
```

---

## Example

```python
import numpy as np

from finmetrics.metrics import annualized_return
from finmetrics.metrics import annualized_volatility

returns = np.array([
    0.02,
    -0.01,
    0.03,
    0.015,
    -0.005
])

r = annualized_return(returns)
v = annualized_volatility(returns)

print(r)
print(v)
```

---

## Running Tests

Run all tests

```bash
pytest
```

Run with coverage

```bash
pytest --cov=src/finmetrics
```

---

## Project Structure

```
finmetrics/
│
├── src/
│   └── finmetrics/
│
├── tests/
│
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## Development

Contributions are welcome.

Typical development workflow:

```bash
git pull
pip install -e ".[dev]"
pytest
git add .
git commit
git push
```

---

## Roadmap

- [x] Annualized Return
- [x] Annualized Volatility
- [ ] Sharpe Ratio
- [ ] Sortino Ratio
- [ ] Maximum Drawdown
- [ ] Calmar Ratio
- [ ] Information Ratio
- [ ] Beta
- [ ] Alpha
- [ ] Documentation
- [ ] CI/CD with GitHub Actions

---

## License

This project is licensed under the MIT License.

See the LICENSE file for details.


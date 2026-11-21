import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from analytics.visualizers.price_charts import plot_price, plot_rsi
from analytics.visualizers.comparison_charts import plot_leaders


def test_plot_price_creates_file():
    """plot_price должен создавать PNG-файл."""
    data = {
        "date": pd.date_range("2023-01-01", periods=50),
        "ticker": ["SBER"] * 50,
        "close": [100 + i * 0.5 for i in range(50)]
    }
    df = pd.DataFrame(data)
    df.set_index("date", inplace=True)
    
    reports_dir = Path(__file__).parent.parent / "temp_reports"
    reports_dir.mkdir(exist_ok=True)
    
    plot_price(df, "SBER", reports_dir)
    assert (reports_dir / "price_SBER.png").exists()
    
    (reports_dir / "price_SBER.png").unlink()


def test_plot_rsi_creates_file():
    """plot_rsi должен создавать PNG-файл."""
    data = {
        "date": pd.date_range("2023-01-01", periods=50),
        "ticker": ["SBER"] * 50,
        "close": [100 + i * 0.5 for i in range(50)]
    }
    df = pd.DataFrame(data)
    df.set_index("date", inplace=True)
    
    reports_dir = Path(__file__).parent.parent / "temp_reports"
    reports_dir.mkdir(exist_ok=True)
    
    plot_rsi(df, "SBER", reports_dir)
    assert (reports_dir / "rsi_SBER.png").exists()
    
    (reports_dir / "rsi_SBER.png").unlink()


def test_plot_leaders_creates_file():
    """plot_leaders должен создавать PNG-файл."""
    metrics = pd.DataFrame({
        "ticker": ["SBER", "GAZP", "LKOH"],
        "sector": ["Финансы", "Нефть", "Нефть"],
        "total": [0.1, -0.05, 0.2],
        "volatility": [0.3, 0.4, 0.35],
        "sharpe": [1.0, -0.5, 1.2],
        "max_down": [-0.2, -0.3, -0.25]
    })
    
    reports_dir = Path(__file__).parent.parent / "temp_reports"
    reports_dir.mkdir(exist_ok=True)
    
    plot_leaders(metrics, reports_dir)
    assert (reports_dir / "leaders.png").exists()
    
    (reports_dir / "leaders.png").unlink()
from pathlib import Path
from analytics.data_loader import load_market_data
from analytics.metrics.portfolio import (
    calculate_metrics,
    calculate_correlation_matrix,
    calculate_sector
)
from analytics.visualizers.price_charts import generate_price_charts
from analytics.visualizers.comparison_charts import generate_comparison_charts

def setup_dir() -> Path:
    reports_dir = Path(__file__).parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    return reports_dir


def main():
    print("Началась аналитика.")

    print("Загрузка данных")
    df, assets_meta = load_market_data()
    print(f"Загруженно: {len(df)}")
    print(f"Активов {len(assets_meta)}")

    print("метрики")
    metrics = calculate_metrics(df, assets_meta)
    corr_matrix = calculate_correlation_matrix(df)
    sector_df = calculate_sector(metrics)

    print('Графики')
    report_dir = setup_dir()
    key_tickers = ["SBER", "GAZP", "YDEX"]
    generate_price_charts(df, key_tickers, report_dir)
    generate_comparison_charts(metrics, corr_matrix, sector_df, report_dir)
    print(f"Папка для графиков: {report_dir.absolute()}")

    print('Вроде работает')

if __name__ == "__main__":
    main()
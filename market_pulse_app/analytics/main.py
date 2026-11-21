from pathlib import Path
from analytics.data_loader import load_market_data

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

    report_dir = setup_dir()
    print(f"Папка для графиков: {report_dir.absolute()}")

    print('Вроде работает')

if __name__ == "__main__":
    main()
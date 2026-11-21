import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from analytics.data_loader import load_market_data
from analytics.visualizers.price_charts import generate_all_price_charts


def main():
    print("проверка работы check_vis.py")
    df, _ = load_market_data()
    reports_dir = Path(__file__).parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    generate_all_price_charts(df, ["SBER", "GAZP", "YDEX"], reports_dir)
    
    files = list(reports_dir.glob("*.png"))
    print(f"Создано файлов: {len(files)}")
    for f in sorted(files):
        print(f"   - {f.name}")


if __name__ == "__main__":
    main()
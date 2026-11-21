import json
import pandas as pd
from pathlib import Path

def load_market_data() -> tuple[pd.DataFrame, list[dict]]:
    base_dir = Path(__file__).parent.parent
    data_file = base_dir / "data" / "dataset.json"


    with open(data_file, "r", encoding="utf-8") as file_name:
        data_json = json.load(file_name)

    df = pd.DataFrame(data_json["quotes"])
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    df = df.sort_index()

    assets_meta = data_json.get("assets", [])

    return df, assets_meta
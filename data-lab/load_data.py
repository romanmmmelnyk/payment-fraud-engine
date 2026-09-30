from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).parent / "datasets" / "synthetic_financial_data.csv"


def load_data(path=DATA_PATH):
    return pd.read_csv(path)

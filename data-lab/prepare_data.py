import pandas as pd


def prepare_data(df):
    df = df.copy()
    df["amount"] = pd.to_numeric(df["amount"])
    df["customer_age"] = pd.to_numeric(df["customer_age"])
    df["is_fraudulent"] = pd.to_numeric(df["is_fraudulent"]).astype(int)
    df["transaction_time"] = pd.to_datetime(df["transaction_time"])
    return df

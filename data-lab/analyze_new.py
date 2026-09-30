from pathlib import Path

import pandas as pd

from behavior import add_behavior_features, search_patterns, summarize_behavior
from checks import show_each, show_rate_span
from combinations import pair_span
from logistic_regression import run_logistic_regression

TRAIN_PATH = Path(__file__).parent / "datasets" / "new" / "train.csv"
RAW_FEATURES = ["amount", "hours_since_prev_txn", "channel"]
LARGE_AMOUNT = 50


def load_new(path=TRAIN_PATH):
    raw = pd.read_csv(path)
    return pd.DataFrame(
        {
            "customer_id": raw["user_id"],
            "transaction_time": pd.to_datetime(raw["timestamp"], unit="s"),
            "amount": raw["amount"],
            "merchant_id": raw["merchant_category"],
            "merchant_category": raw["merchant_category"],
            "location": raw["country"],
            "card_type": raw["device_id"],
            "channel": raw["channel"],
            "hours_since_prev_txn": raw["hours_since_prev_txn"],
            "is_fraudulent": raw["label"].astype(int),
        }
    )


def check_new(df):
    fraud = int(df["is_fraudulent"].sum())
    by_customer = df.groupby("customer_id")
    customer_rates = by_customer["is_fraudulent"].mean()
    gaps = df.sort_values(["customer_id", "transaction_time"]).groupby("customer_id")["transaction_time"].diff().dt.total_seconds().dropna()
    countries = by_customer["location"].nunique()
    devices = by_customer["card_type"].nunique()

    print("rows", len(df))
    print("fraud", fraud)
    print("not_fraud", len(df) - fraud)
    print("fraud_rate", round(fraud / len(df), 4))
    print("time_from", df["transaction_time"].min())
    print("time_to", df["transaction_time"].max())
    print("customers", int(by_customer.ngroups))
    print("gap_median_sec", round(float(gaps.median()), 1))
    print("country_not_stable", int((countries > 1).sum()))
    print("channel_not_stable", int((by_customer["channel"].nunique() > 1).sum()))
    print("device_not_stable", int((devices > 1).sum()))
    print("category_not_stable", int((by_customer["merchant_category"].nunique() > 1).sum()))
    print("countries_per_customer_avg", round(float(countries.mean()), 1))
    print("devices_per_customer_avg", round(float(devices.mean()), 1))
    print("customer_fraud_rate_min", round(float(customer_rates.min()), 3))
    print("customer_fraud_rate_max", round(float(customer_rates.max()), 3))
    print("customers_all_fraud", int((customer_rates == 1).sum()))
    print("customers_no_fraud", int((customer_rates == 0).sum()))

    amounts = df.groupby("is_fraudulent")["amount"].agg(["mean", "median"])
    print("amount_mean_not_fraud", round(float(amounts.loc[0, "mean"]), 2))
    print("amount_mean_fraud", round(float(amounts.loc[1, "mean"]), 2))
    print("amount_median_not_fraud", round(float(amounts.loc[0, "median"]), 2))
    print("amount_median_fraud", round(float(amounts.loc[1, "median"]), 2))
    gaps_given = df.groupby("is_fraudulent")["hours_since_prev_txn"].median()
    print("given_gap_median_not_fraud", round(float(gaps_given.loc[0]), 1))
    print("given_gap_median_fraud", round(float(gaps_given.loc[1]), 1))

    work = df.copy()
    work["amount_bin"] = pd.cut(
        work["amount"],
        bins=[0, 10, 20, 40, 80, 1000],
        right=False,
        labels=["0-10", "10-20", "20-40", "40-80", "80+"],
    )
    show_each(work, "channel")
    show_each(work, "merchant_category")
    show_each(work, "amount_bin")
    show_rate_span(work, "location")
    show_rate_span(work, "card_type")
    print("--- combinations ---")
    pair_span(work, ["channel", "merchant_category"])
    pair_span(work, ["channel", "amount_bin"])
    pair_span(work, ["merchant_category", "amount_bin"])


def search_hour_pattern(df):
    mask = (
        (df["amount"] >= LARGE_AMOUNT)
        & (df["hours_since_prev_txn"] <= 3600)
        & (df["location_changed"] == 1)
        & (df["card_type_changed"] == 1)
    )
    part = df[mask]
    rate = float(part["is_fraudulent"].mean()) if len(part) else 0
    print("large_within_hour_new_place", "n", int(len(part)), "fraud_rate", round(rate, 3))


def main():
    df = load_new()
    print("--- individual ---")
    check_new(df)
    df = add_behavior_features(df)
    print("--- behavior ---")
    summarize_behavior(df)
    print("--- patterns ---")
    print("large_amount", LARGE_AMOUNT)
    search_patterns(df, large_amount=LARGE_AMOUNT)
    search_hour_pattern(df)
    print("--- logistic ---")
    run_logistic_regression(df, raw_features=RAW_FEATURES)


if __name__ == "__main__":
    main()

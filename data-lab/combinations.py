import pandas as pd


def check_combinations(df):
    work = df.copy()
    work["amount_bin"] = pd.cut(
        work["amount"],
        bins=[0, 1000, 2500, 5000, 7500, 10001],
        right=False,
        labels=["0-1000", "1000-2500", "2500-5000", "5000-7500", "7500-10000"],
    )
    pair_span(work, ["card_type", "purchase_category"])
    pair_span(work, ["card_type", "amount_bin"])
    pair_span(work, ["purchase_category", "amount_bin"])


def pair_span(df, columns):
    table = df.groupby(columns, observed=True)["is_fraudulent"].agg(["count", "mean"])
    label = " x ".join(columns)
    low = table.sort_values("mean").iloc[0]
    high = table.sort_values("mean").iloc[-1]
    print(label, "cells", len(table))
    print(label, "low", low.name, "rate", round(float(low["mean"]), 3), "n", int(low["count"]))
    print(label, "high", high.name, "rate", round(float(high["mean"]), 3), "n", int(high["count"]))

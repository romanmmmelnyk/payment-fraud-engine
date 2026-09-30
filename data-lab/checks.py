import pandas as pd


def check_data(df):
    fraud = int(df["is_fraudulent"].sum())
    gaps = df["transaction_time"].sort_values().diff().dt.total_seconds().dropna()
    by_customer = df.groupby("customer_id")
    customer_rates = by_customer["is_fraudulent"].mean()
    cities = by_customer["location"].nunique()
    desc_merchant = df["transaction_description"].str.replace("Purchase at Merchant-", "", regex=False)

    print("rows", len(df))
    print("fraud", fraud)
    print("not_fraud", len(df) - fraud)
    print("time_from", df["transaction_time"].min())
    print("time_to", df["transaction_time"].max())
    print("unique_gaps_sec", sorted(gaps.unique().tolist()))
    print("customers", int(by_customer.ngroups))
    print("age_not_stable", int((by_customer["customer_age"].nunique() > 1).sum()))
    print("card_not_stable", int((by_customer["card_type"].nunique() > 1).sum()))
    print("city_not_stable", int((by_customer["location"].nunique() > 1).sum()))
    print("cities_per_customer_min", int(cities.min()))
    print("cities_per_customer_max", int(cities.max()))
    print("cities_per_customer_avg", round(float(cities.mean()), 1))
    print("customer_fraud_rate_min", round(float(customer_rates.min()), 3))
    print("customer_fraud_rate_max", round(float(customer_rates.max()), 3))
    print("customers_all_fraud", int((customer_rates == 1).sum()))
    print("customers_no_fraud", int((customer_rates == 0).sum()))
    print("description_is_merchant", bool((desc_merchant == df["merchant_id"].astype(str)).all()))

    amounts = df.groupby("is_fraudulent")["amount"].agg(["mean", "median"])
    print("amount_mean_not_fraud", round(float(amounts.loc[0, "mean"]), 2))
    print("amount_mean_fraud", round(float(amounts.loc[1, "mean"]), 2))
    print("amount_median_not_fraud", round(float(amounts.loc[0, "median"]), 2))
    print("amount_median_fraud", round(float(amounts.loc[1, "median"]), 2))

    work = df.copy()
    work["age_bin"] = (work["customer_age"] // 10) * 10
    work["amount_bin"] = pd.cut(
        work["amount"],
        bins=[0, 1000, 2500, 5000, 7500, 10001],
        right=False,
        labels=["0-1000", "1000-2500", "2500-5000", "5000-7500", "7500-10000"],
    )
    show_each(work, "card_type")
    show_each(work, "purchase_category")
    show_each(work, "age_bin")
    show_each(work, "amount_bin")
    show_rate_span(work, "location")
    show_rate_span(work, "merchant_id")


def show_each(df, column):
    table = df.groupby(column, observed=True)["is_fraudulent"].agg(["count", "mean"])
    print(column)
    for key, row in table.iterrows():
        print(key, "n", int(row["count"]), "rate", round(float(row["mean"]), 3))


def show_rate_span(df, column):
    rates = df.groupby(column)["is_fraudulent"].mean()
    print(column + "_groups", int(rates.size))
    print(column + "_fraud_rate_min", round(float(rates.min()), 3))
    print(column + "_fraud_rate_max", round(float(rates.max()), 3))

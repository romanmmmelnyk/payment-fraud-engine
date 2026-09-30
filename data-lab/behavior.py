import pandas as pd

BEHAVIOR_FEATURES = [
    "transactions_last_10s",
    "transactions_last_60s",
    "transactions_last_5min",
    "amount_last_60s",
    "average_amount",
    "amount_deviation",
    "time_since_previous_transaction",
    "unique_merchants_last_10min",
    "unique_locations_last_10min",
    "location_changed",
    "card_type_changed",
    "customer_transaction_velocity",
    "customer_fraud_history",
]


def window_indexes(times, i, seconds):
    border = times[i] - pd.Timedelta(seconds=seconds)
    return [j for j in range(i) if times[j] >= border]


def customer_features(group):
    group = group.sort_values("transaction_time").copy()
    times = group["transaction_time"].to_list()
    amounts = group["amount"].to_list()
    merchants = group["merchant_id"].to_list()
    locations = group["location"].to_list()
    cards = group["card_type"].to_list()
    frauds = group["is_fraudulent"].to_list()

    last_10s = []
    last_60s = []
    last_5min = []
    amount_60s = []
    avg_amount = []
    amount_dev = []
    since_prev = []
    merchants_10min = []
    locations_10min = []
    location_changed = []
    card_changed = []
    velocity = []
    fraud_history = []

    for i, moment in enumerate(times):
        w10 = window_indexes(times, i, 10)
        w60 = window_indexes(times, i, 60)
        w300 = window_indexes(times, i, 300)
        w600 = window_indexes(times, i, 600)
        last_10s.append(len(w10))
        last_60s.append(len(w60))
        last_5min.append(len(w300))
        amount_60s.append(sum(amounts[j] for j in w60))
        merchants_10min.append(len({merchants[j] for j in w600}))
        locations_10min.append(len({locations[j] for j in w600}))
        if i == 0:
            avg_amount.append(0)
            amount_dev.append(0)
            since_prev.append(0)
            location_changed.append(0)
            card_changed.append(0)
            velocity.append(0)
            fraud_history.append(0)
            continue
        mean_amount = sum(amounts[:i]) / i
        avg_amount.append(mean_amount)
        amount_dev.append(amounts[i] - mean_amount)
        since_prev.append((moment - times[i - 1]).total_seconds())
        location_changed.append(int(locations[i] != locations[i - 1]))
        card_changed.append(int(cards[i] != cards[i - 1]))
        minutes = (moment - times[0]).total_seconds() / 60
        velocity.append(i / minutes if minutes else 0)
        fraud_history.append(sum(frauds[:i]) / i)

    group["transactions_last_10s"] = last_10s
    group["transactions_last_60s"] = last_60s
    group["transactions_last_5min"] = last_5min
    group["amount_last_60s"] = amount_60s
    group["average_amount"] = avg_amount
    group["amount_deviation"] = amount_dev
    group["time_since_previous_transaction"] = since_prev
    group["unique_merchants_last_10min"] = merchants_10min
    group["unique_locations_last_10min"] = locations_10min
    group["location_changed"] = location_changed
    group["card_type_changed"] = card_changed
    group["customer_transaction_velocity"] = velocity
    group["customer_fraud_history"] = fraud_history
    return group


def add_behavior_features(df):
    parts = [customer_features(group) for _, group in df.groupby("customer_id", sort=False)]
    return pd.concat(parts, ignore_index=True)


def search_patterns(df, large_amount=5000):
    slices = {
        "burst_60s": df["transactions_last_60s"] >= 3,
        "large_and_burst": (df["amount"] >= large_amount) & (df["transactions_last_60s"] >= 3),
        "large_burst_new_place": (
            (df["amount"] >= large_amount)
            & (df["transactions_last_60s"] >= 3)
            & (df["location_changed"] == 1)
            & (df["card_type_changed"] == 1)
        ),
    }
    for name, mask in slices.items():
        part = df[mask]
        rate = float(part["is_fraudulent"].mean()) if len(part) else 0
        print(name, "n", int(len(part)), "fraud_rate", round(rate, 3))


def summarize_behavior(df):
    for name in BEHAVIOR_FEATURES:
        means = df.groupby("is_fraudulent")[name].mean()
        print(
            name,
            "not_fraud",
            round(float(means.loc[0]), 3),
            "fraud",
            round(float(means.loc[1]), 3),
        )

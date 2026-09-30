from pathlib import Path

import numpy as np
import pandas as pd

from logistic_regression import fit_weights, predict_proba, split_rows

TX_PATH = Path(__file__).parent / "datasets" / "train_transaction.csv"
ID_PATH = Path(__file__).parent / "datasets" / "train_identity.csv"


def load_frame():
    tx = pd.read_csv(
        TX_PATH,
        usecols=[
            "TransactionID",
            "isFraud",
            "TransactionDT",
            "TransactionAmt",
            "ProductCD",
            "card4",
            "card6",
            "P_emaildomain",
        ],
    )
    ident = pd.read_csv(
        ID_PATH,
        usecols=[
            "TransactionID",
            "id_15",
            "id_30",
            "id_31",
            "DeviceType",
            "DeviceInfo",
        ],
    )
    df = tx.merge(ident, on="TransactionID", how="left")
    df["log_amount"] = np.log1p(df["TransactionAmt"])
    df["hour"] = pd.to_datetime(df["TransactionDT"], unit="s").dt.hour
    df["day_part"] = df["hour"].map(day_part)
    df["email"] = df["P_emaildomain"].map(email_group)
    df["os"] = df["id_30"].map(os_group)
    df["browser"] = df["id_31"].map(browser_group)
    df["device_family"] = df["DeviceInfo"].map(device_family)
    df["card4"] = df["card4"].fillna("none")
    df["card6"] = df["card6"].map(card_group)
    df["DeviceType"] = df["DeviceType"].fillna("none")
    df["id_15"] = df["id_15"].fillna("none")
    df["ProductCD"] = df["ProductCD"].fillna("none")
    return df


def day_part(hour):
    if hour <= 3:
        return "night"
    if hour <= 9:
        return "early"
    if hour <= 17:
        return "day"
    return "evening"


def email_group(value):
    if pd.isna(value):
        return "none"
    text = str(value).lower()
    for name in ("proton", "anonymous", "gmail", "yahoo", "hotmail", "outlook", "aol", "icloud"):
        if name in text:
            return name
    return "other"


def os_group(value):
    if pd.isna(value):
        return "none"
    text = str(value).lower()
    if "android" in text:
        return "android"
    if "ios" in text:
        return "ios"
    if "windows" in text:
        return "windows"
    if "mac" in text:
        return "mac"
    return "other"


def browser_group(value):
    if pd.isna(value):
        return "none"
    text = str(value).lower()
    for name in ("chrome", "safari", "edge", "firefox", "samsung", "ie"):
        if name in text:
            return name
    return "other"


def device_family(value):
    if pd.isna(value):
        return "none"
    text = str(value).lower()
    if "samsung" in text:
        return "samsung"
    if "ios" in text or "iphone" in text:
        return "ios"
    if "windows" in text:
        return "windows"
    if "mac" in text:
        return "mac"
    if "huawei" in text or "redmi" in text or "moto" in text:
        return "android_other"
    return "other"


def card_group(value):
    if pd.isna(value):
        return "none"
    text = str(value).lower()
    if text in ("credit", "debit"):
        return text
    return "other"


def show_rates(df, column):
    table = df.groupby(column)["isFraud"].agg(["count", "mean"]).sort_values("mean", ascending=False)
    print(column)
    for key, row in table.iterrows():
        print(key, "n", int(row["count"]), "rate", round(float(row["mean"]), 4))


def design_matrix(df, columns):
    parts = [df[["log_amount"]]]
    for column in columns:
        parts.append(pd.get_dummies(df[column], prefix=column, drop_first=True))
    frame = pd.concat(parts, axis=1)
    return frame.astype(float)


def auc_fast(y, proba):
    order = np.argsort(proba, kind="mergesort")
    y_sorted = y[order]
    n_pos = float(y_sorted.sum())
    n_neg = float(len(y) - n_pos)
    ranks = np.arange(1, len(y) + 1)
    sum_pos = ranks[y_sorted == 1].sum()
    return float((sum_pos - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def fit_print(df, columns, name):
    x_frame = design_matrix(df, columns)
    x = x_frame.to_numpy()
    y = df["isFraud"].to_numpy(dtype=float)
    train, test = split_rows(y)
    x_train, x_test = x[train], x[test]
    y_train, y_test = y[train], y[test]
    mean = x_train.mean(axis=0)
    std = x_train.std(axis=0)
    std[std == 0] = 1
    x_train = (x_train - mean) / std
    x_test = (x_test - mean) / std
    weights = fit_weights(x_train, y_train, ridge=1e-4)
    proba = predict_proba(x_test, weights)
    print("model", name)
    print("rows", len(df))
    print("auc", round(auc_fast(y_test, proba), 3))
    order = np.argsort(proba)
    band = max(1, len(y_test) // 10)
    print("bottom_10_fraud_rate", round(float(y_test[order[:band]].mean()), 4))
    print("top_10_fraud_rate", round(float(y_test[order[-band:]].mean()), 4))
    names = list(x_frame.columns)
    pairs = sorted(zip(names, weights[1:]), key=lambda item: abs(item[1]), reverse=True)
    for feature, coef in pairs[:15]:
        print(feature, round(float(coef), 3))


def main():
    df = load_frame()
    fraud = int(df["isFraud"].sum())
    print("rows", len(df))
    print("fraud", fraud)
    print("fraud_rate", round(fraud / len(df), 4))
    print("with_identity", int(df["DeviceType"].ne("none").sum()))
    print("--- rates ---")
    for column in ("ProductCD", "card6", "card4", "DeviceType", "id_15", "day_part", "email", "os", "browser", "device_family"):
        show_rates(df, column)
    known = df[df["DeviceType"] != "none"]
    print("--- identity rows product ---")
    show_rates(known, "ProductCD")
    print("--- logistic ---")
    fit_print(df, ["ProductCD", "card6", "card4", "day_part"], "transaction")
    fit_print(df, ["DeviceType", "id_15", "os", "browser", "device_family", "email"], "identity")
    fit_print(
        df,
        ["ProductCD", "card6", "card4", "day_part", "DeviceType", "id_15", "os", "browser", "device_family", "email"],
        "both",
    )
    fit_print(known, ["ProductCD", "card6", "DeviceType", "id_15", "os", "browser", "device_family", "email", "day_part"], "identity_rows")


if __name__ == "__main__":
    main()

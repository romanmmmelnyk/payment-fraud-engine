import numpy as np

from behavior import BEHAVIOR_FEATURES

RAW_FEATURES = ["amount", "customer_age"]


def run_logistic_regression(df, raw_features=None):
    raw = RAW_FEATURES if raw_features is None else raw_features
    fit_model(df, raw, "raw")
    fit_model(df, BEHAVIOR_FEATURES, "behavior")
    fit_model(df, list(raw) + BEHAVIOR_FEATURES, "raw_and_behavior")


def fit_model(df, columns, name):
    x = df[columns].fillna(0).to_numpy(dtype=float)
    y = df["is_fraudulent"].to_numpy(dtype=float)
    train, test = split_rows(y)
    x_train, x_test = x[train], x[test]
    y_train, y_test = y[train], y[test]
    mean = x_train.mean(axis=0)
    std = x_train.std(axis=0)
    std[std == 0] = 1
    x_train = (x_train - mean) / std
    x_test = (x_test - mean) / std
    weights = fit_weights(x_train, y_train)
    proba = predict_proba(x_test, weights)
    pred = (proba >= 0.5).astype(float)
    print("model", name)
    print("accuracy", round(float((pred == y_test).mean()), 3))
    print("auc", round(auc_score(y_test, proba), 3))
    order = np.argsort(proba)
    band = max(1, len(y_test) // 10)
    print("bottom_10_fraud_rate", round(float(y_test[order[:band]].mean()), 3))
    print("top_10_fraud_rate", round(float(y_test[order[-band:]].mean()), 3))
    pairs = sorted(zip(columns, weights[1:]), key=lambda item: abs(item[1]), reverse=True)
    for feature, coef in pairs:
        print(feature, round(float(coef), 3))


def split_rows(y):
    rng = np.random.default_rng(0)
    train = []
    test = []
    for label in (0, 1):
        rows = np.flatnonzero(y == label)
        rng.shuffle(rows)
        cut = int(len(rows) * 0.75)
        train.append(rows[:cut])
        test.append(rows[cut:])
    return np.concatenate(train), np.concatenate(test)


def fit_weights(x, y):
    ones = np.ones((len(x), 1))
    design = np.column_stack([ones, x])
    weights = np.zeros(design.shape[1])
    for _ in range(25):
        scores = np.clip(design @ weights, -20, 20)
        proba = 1 / (1 + np.exp(-scores))
        variance = np.clip(proba * (1 - proba), 1e-6, None)
        gradient = design.T @ (proba - y) / len(y)
        hessian = (design.T * variance) @ design / len(y)
        weights -= np.linalg.solve(hessian, gradient)
    return weights


def predict_proba(x, weights):
    ones = np.ones((len(x), 1))
    scores = np.clip(np.column_stack([ones, x]) @ weights, -20, 20)
    return 1 / (1 + np.exp(-scores))


def auc_score(y, proba):
    positive = proba[y == 1]
    negative = proba[y == 0]
    wins = (positive[:, None] > negative[None, :]).sum()
    ties = (positive[:, None] == negative[None, :]).sum()
    return float((wins + 0.5 * ties) / (len(positive) * len(negative)))

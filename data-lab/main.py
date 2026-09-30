from behavior import add_behavior_features, search_patterns, summarize_behavior
from checks import check_data
from combinations import check_combinations
from load_data import load_data
from logistic_regression import run_logistic_regression
from prepare_data import prepare_data


def main():
    df = load_data()
    df = prepare_data(df)
    print("--- individual ---")
    check_data(df)
    print("--- combinations ---")
    check_combinations(df)
    df = add_behavior_features(df)
    print("--- behavior ---")
    summarize_behavior(df)
    print("--- patterns ---")
    search_patterns(df)
    print("--- logistic ---")
    run_logistic_regression(df)


if __name__ == "__main__":
    main()

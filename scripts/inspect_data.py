import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw/data.csv")


def load_data(path):
    return pd.read_csv(path)


def inspect_data(df):
    print('\n--- Shape ---')
    print(df.shape)

    print('\n--- Duplicate rows ---')
    print(df.duplicated().sum())

    print('\n--- Missing values ---')
    print(df.isnull().sum())


def check_column(df):
    print('\n--- Columns ---')
    print(df.columns.tolist())

    print('\n--- Top 5 rows ---')
    print(df.head())


def check_dtypes(df):
    print('\n--- Data types ---')
    print(df.dtypes)


def check_stats(df):
    print('\n--- Numeric summary (describe) ---')
    print(df.describe())


def check_categorical(df):
    print('\n--- Unique values per categorical column ---')
    cat_cols = df.select_dtypes(include='object').columns
    for col in cat_cols:
        print(f"\n{col}: {df[col].nunique()} unique values")
        print(df[col].unique()[:10])


def check_id_columns(df):
    # Helps spot which columns look like IDs (account, merchant, transaction)
    print('\n--- Possible ID / key columns ---')
    for col in df.columns:
        if 'id' in col.lower():
            print(f"{col}: {df[col].nunique()} unique values out of {len(df)} rows")


def main():
    df = load_data(DATA_PATH)

    inspect_data(df)
    check_column(df)
    check_dtypes(df)
    check_stats(df)
    check_categorical(df)
    check_id_columns(df)


if __name__ == "__main__":
    main()
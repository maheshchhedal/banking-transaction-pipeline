import pandas as pd
from pathlib import Path

DATA_PATH = Path('data/raw/data.csv')

# TODO: replace these with your real column names from df.columns
NUMERIC_COLUMNS = ['transactionamount', 'accountbalance']
TITLE_CASE_COLUMNS = ['transactiontype', 'location', 'customeroccupation']
DATE_COLUMN = 'transactiondate'


def load_data(path):
    return pd.read_csv(path)


def clean_column_names(df):
    print('\n cleaning column names (lowercase, no spaces)')
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    print(df.columns)
    return df


def fix_date_column(df):
    print('\n converting date column to datetime')
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], format='mixed')
    print(df[DATE_COLUMN].dtype)
    print('nulls after date conversion:', df[DATE_COLUMN].isnull().sum())
    return df


def fix_numeric_columns(df):
    print('\n converting numeric columns')
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            print(f'{col} nulls after conversion:', df[col].isnull().sum())
    return df


def drop_duplicate_rows(df):
    print('\n duplicates before:', df.duplicated().sum())
    df = df.drop_duplicates()
    return df


def remove_null_rows(df):
    print('\n nulls before:\n', df.isnull().sum())
    df = df.dropna()
    return df


def format_text_columns(df):
    print('\n formatting text columns to title case')
    for col in TITLE_CASE_COLUMNS:
        if col in df.columns:
            df[col] = df[col].str.title()
    return df


def main():
    df = load_data(DATA_PATH)
    df = clean_column_names(df)
    df = fix_date_column(df)
    df = fix_numeric_columns(df)
    df = drop_duplicate_rows(df)
    df = remove_null_rows(df)
    df = format_text_columns(df)

    print('\n final shape:', df.shape)
    print('\n final dtypes:\n', df.dtypes)

    return df


if __name__ == '__main__':
    main()
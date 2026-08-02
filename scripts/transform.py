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


def build_dim_account(df):
    print('\n building dim_account table')
    dim_account = df[['accountid', 'customerage', 'customeroccupation']].drop_duplicates(subset='accountid')
    dim_account = dim_account.reset_index(drop=True)
    print('dim_account shape:', dim_account.shape)
    return dim_account


def build_dim_merchant(df):
    print('\n building dim_merchant table')
    dim_merchant = df[['merchantid']].drop_duplicates(subset='merchantid')
    dim_merchant = dim_merchant.reset_index(drop=True)
    print('dim_merchant shape:', dim_merchant.shape)
    return dim_merchant


def build_fact_transactions(df):
    print('\n building fact_transactions table')
    fact_columns = [
        'transactionid', 'accountid', 'merchantid', 'transactionamount',
        'transactiondate', 'transactiontype', 'location', 'deviceid',
        'ip_address', 'channel', 'transactionduration', 'loginattempts',
        'accountbalance'
    ]
    fact_transactions = df[fact_columns].copy()
    print('fact_transactions shape:', fact_transactions.shape)
    return fact_transactions


def run_transformations(df):
    """Runs all cleaning + splitting steps on any given dataframe.
    Used by both main() (for the original CSV) and run_pipeline.py (for new incoming data).
    """
    df = clean_column_names(df)
    df = fix_date_column(df)
    df = fix_numeric_columns(df)
    df = drop_duplicate_rows(df)
    df = remove_null_rows(df)
    df = format_text_columns(df)

    print('\n final shape:', df.shape)
    print('\n final dtypes:\n', df.dtypes)

    dim_account = build_dim_account(df)
    dim_merchant = build_dim_merchant(df)
    fact_transactions = build_fact_transactions(df)

    return dim_account, dim_merchant, fact_transactions


def main():
    df = load_data(DATA_PATH)
    return run_transformations(df)


if __name__ == '__main__':
    main()
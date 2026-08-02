import yaml
from pathlib import Path
from sqlalchemy import create_engine

import sys
sys.path.append(str(Path(__file__).resolve().parent))
from transform import main as run_transform

CONFIG_PATH = Path('config/config.yaml')


def load_config(path):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config['mysql']


def get_engine(config):
    connection_string = (
        f"mysql+pymysql://{config['user']}:{config['password']}"
        f"@{config['host']}:{config['port']}/{config['database']}"
    )
    engine = create_engine(connection_string)
    return engine


import pandas as pd


def get_existing_ids(engine, table_name, id_column):
    query = f"SELECT {id_column} FROM {table_name}"
    existing = pd.read_sql(query, engine)
    return set(existing[id_column])


def load_dim_account(engine, dim_account):
    print('\n loading dim_account into MySQL')
    existing_ids = get_existing_ids(engine, 'dim_account', 'accountid')
    new_rows = dim_account[~dim_account['accountid'].isin(existing_ids)]
    if new_rows.empty:
        print('no new accounts to insert')
        return
    new_rows.to_sql('dim_account', con=engine, if_exists='append', index=False)
    print('dim_account rows loaded:', len(new_rows))


def load_dim_merchant(engine, dim_merchant):
    print('\n loading dim_merchant into MySQL')
    existing_ids = get_existing_ids(engine, 'dim_merchant', 'merchantid')
    new_rows = dim_merchant[~dim_merchant['merchantid'].isin(existing_ids)]
    if new_rows.empty:
        print('no new merchants to insert')
        return
    new_rows.to_sql('dim_merchant', con=engine, if_exists='append', index=False)
    print('dim_merchant rows loaded:', len(new_rows))


def load_fact_transactions(engine, fact_transactions):
    print('\n loading fact_transactions into MySQL')
    fact_transactions.to_sql('fact_transactions', con=engine, if_exists='append', index=False)
    print('fact_transactions rows loaded:', len(fact_transactions))


def main():
    config = load_config(CONFIG_PATH)
    engine = get_engine(config)

    dim_account, dim_merchant, fact_transactions = run_transform()

    load_dim_account(engine, dim_account)
    load_dim_merchant(engine, dim_merchant)
    load_fact_transactions(engine, fact_transactions)

    print('\n load complete')


if __name__ == '__main__':
    main()
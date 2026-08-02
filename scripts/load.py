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


def load_dim_account(engine, dim_account):
    print('\n loading dim_account into MySQL')
    dim_account.to_sql('dim_account', con=engine, if_exists='append', index=False)
    print('dim_account rows loaded:', len(dim_account))


def load_dim_merchant(engine, dim_merchant):
    print('\n loading dim_merchant into MySQL')
    dim_merchant.to_sql('dim_merchant', con=engine, if_exists='append', index=False)
    print('dim_merchant rows loaded:', len(dim_merchant))


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
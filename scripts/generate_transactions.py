import random
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker()

OUTPUT_DIR = Path('data/incoming')
NUM_ROWS = 30

TRANSACTION_TYPES = ['Debit', 'Credit']
CHANNELS = ['Online', 'ATM', 'Branch']
OCCUPATIONS = ['Engineer', 'Doctor', 'Student', 'Retired', 'Teacher', 'Manager']


def generate_row():
    return {
        'transactionid': str(uuid.uuid4())[:8],
        'accountid': f"acc_{random.randint(1000, 9999)}",
        'transactionamount': round(random.uniform(5, 2000), 2),
        'transactiondate': fake.date_time_between(start_date='-1d', end_date='now'),
        'transactiontype': random.choice(TRANSACTION_TYPES),
        'location': fake.city(),
        'deviceid': f"dev_{random.randint(100, 999)}",
        'ip_address': fake.ipv4(),
        'merchantid': f"merch_{random.randint(100, 999)}",
        'channel': random.choice(CHANNELS),
        'customerage': random.randint(18, 75),
        'customeroccupation': random.choice(OCCUPATIONS),
        'transactionduration': random.randint(10, 300),
        'loginattempts': random.randint(1, 5),
        'accountbalance': round(random.uniform(100, 20000), 2),
    }


def generate_batch(num_rows):
    rows = [generate_row() for _ in range(num_rows)]
    return pd.DataFrame(rows)


def save_batch(df, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = output_dir / filename
    df.to_csv(filepath, index=False)
    print(f"Saved {len(df)} new transactions to {filepath}")
    return filepath


def main():
    df = generate_batch(NUM_ROWS)
    save_batch(df, OUTPUT_DIR)


if __name__ == '__main__':
    main()
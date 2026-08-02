from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))

import extract
import transform
import load


def main():
    print('=' * 50)
    print('STARTING PIPELINE RUN')
    print('=' * 50)

    print('\n--- STEP 1: EXTRACT ---')
    new_data = extract.main()

    if new_data.empty:
        print('\n no new data found, pipeline run skipped')
        return

    print('\n--- STEP 2: TRANSFORM ---')
    dim_account, dim_merchant, fact_transactions = transform.run_transformations(new_data)

    print('\n--- STEP 3: LOAD ---')
    config = load.load_config(load.CONFIG_PATH)
    engine = load.get_engine(config)

    load.load_dim_account(engine, dim_account)
    load.load_dim_merchant(engine, dim_merchant)
    load.load_fact_transactions(engine, fact_transactions)

    print('\n' + '=' * 50)
    print('PIPELINE RUN COMPLETE')
    print('=' * 50)


if __name__ == '__main__':
    main()
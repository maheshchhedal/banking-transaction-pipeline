# Banking Transaction Data Pipeline

An automated ETL (Extract, Transform, Load) pipeline that processes banking transaction data, normalizes it into a relational schema, and loads it into MySQL — fully automated with Windows Task Scheduler.

## Overview

This project simulates a real-world data engineering workflow: ingesting raw transaction data, cleaning and validating it, transforming it into a proper relational (star) schema, and loading it into a database — all running automatically on a daily schedule without manual intervention.

**Tech stack:** Python, pandas, numpy, MySQL, SQLAlchemy, Faker, Windows Task Scheduler

## Architecture

```
                     ┌─────────────────────┐
                     │   Kaggle Dataset      │
                     │  (initial 50,000      │
                     │   historical rows)     │
                     └──────────┬────────────┘
                                │
                     ┌──────────▼────────────┐
                     │ generate_transactions.py│
                     │  (Faker - simulates      │
                     │   new daily transactions)│
                     └──────────┬────────────┘
                                │
                                ▼
                       data/incoming/*.csv
                                │
                     ┌──────────▼────────────┐
                     │      extract.py         │
                     │  reads new files,         │
                     │  archives after processing│
                     └──────────┬────────────┘
                                │
                     ┌──────────▼────────────┐
                     │     transform.py          │
                     │  cleans data, fixes types, │
                     │  removes nulls/duplicates, │
                     │  normalizes into 3 tables  │
                     └──────────┬────────────┘
                                │
                     ┌──────────▼────────────┐
                     │       load.py              │
                     │  inserts into MySQL,         │
                     │  skips existing records      │
                     │  (duplicate-safe upsert)      │
                     └──────────┬────────────┘
                                │
                                ▼
                         MySQL Database
                    (banking_pipeline)
                                │
                     ┌──────────▼────────────┐
                     │   Windows Task Scheduler │
                     │  runs the entire flow      │
                     │  automatically, daily       │
                     └────────────────────────┘
```

## Database Schema

The pipeline normalizes a flat CSV into a star schema with one fact table and two dimension tables:

**`dim_account`** — one row per unique account
| Column | Type |
|---|---|
| accountid (PK) | VARCHAR |
| customerage | INT |
| customeroccupation | VARCHAR |

**`dim_merchant`** — one row per unique merchant
| Column | Type |
|---|---|
| merchantid (PK) | VARCHAR |

**`fact_transactions`** — one row per transaction
| Column | Type |
|---|---|
| transactionid (PK) | VARCHAR |
| accountid (FK) | VARCHAR |
| merchantid (FK) | VARCHAR |
| transactionamount | DECIMAL |
| transactiondate | DATETIME |
| transactiontype | VARCHAR |
| location | VARCHAR |
| deviceid | VARCHAR |
| ip_address | VARCHAR |
| channel | VARCHAR |
| transactionduration | INT |
| loginattempts | INT |
| accountbalance | DECIMAL |

## Project Structure

```
banking-transaction-pipeline/
├── config/
│   └── config.yaml            # MySQL credentials (not committed to git)
├── data/
│   ├── raw/                    # original Kaggle CSV
│   ├── incoming/                # new Faker-generated batches land here
│   └── archive/                  # processed files moved here after loading
├── scripts/
│   ├── inspect_data.py           # one-time data exploration
│   ├── generate_transactions.py  # Faker script - simulates new daily transactions
│   ├── extract.py                 # picks up new files, archives after processing
│   ├── transform.py               # cleans, validates, normalizes data
│   ├── load.py                     # inserts into MySQL (duplicate-safe)
│   └── run_pipeline.py             # orchestrates extract -> transform -> load
├── sql/
│   └── schema.sql                  # CREATE TABLE statements
├── scheduler/
│   └── run_pipeline.bat             # triggered by Windows Task Scheduler
├── logs/
│   └── pipeline.log                  # output/errors from each scheduled run
├── requirements.txt
└── README.md
```

## Pipeline Steps

1. **Generate** — `generate_transactions.py` creates a batch of simulated new transactions using Faker, saved as a timestamped CSV in `data/incoming/`
2. **Extract** — `extract.py` scans `data/incoming/` for new files, reads and combines them, then moves processed files to `data/archive/`
3. **Transform** — `transform.py` cleans column names, fixes data types (dates, numeric fields), removes duplicates/nulls, standardizes text formatting, and splits the flat data into the 3 normalized tables
4. **Load** — `load.py` connects to MySQL via SQLAlchemy and inserts the cleaned tables, checking for existing `accountid`/`merchantid` values to avoid duplicate-key errors on repeated runs
5. **Automate** — `run_pipeline.bat` runs the full flow and is triggered daily via Windows Task Scheduler, with all output logged to `logs/pipeline.log`

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR-USERNAME/banking-transaction-pipeline.git
cd banking-transaction-pipeline
```

### 2. Create a virtual environment and install dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up MySQL
- Install MySQL (or use XAMPP)
- Run `sql/schema.sql` to create the `banking_pipeline` database and its tables

### 4. Configure database credentials
Create `config/config.yaml`:
```yaml
mysql:
  host: localhost
  port: 3306
  user: root
  password: ""
  database: banking_pipeline
```

### 5. Add the initial dataset
Download the [Bank Transaction Dataset for Fraud Detection](https://www.kaggle.com/datasets/valakhorasani/bank-transaction-dataset-for-fraud-detection) from Kaggle and place it at `data/raw/data.csv`

### 6. Run the pipeline manually
```bash
python scripts/transform.py
python scripts/load.py
```

### 7. Set up daily automation
Create a Windows Task Scheduler task that runs `scheduler/run_pipeline.bat` on a daily trigger.

## Key Data Engineering Concepts Demonstrated

- **ETL pipeline design** — clear separation between extract, transform, and load stages
- **Data normalization** — converting a flat/denormalized source into a proper star schema (fact + dimension tables)
- **Incremental loading** — only processing new files each run, archiving what's already been handled
- **Idempotent inserts (upsert logic)** — checking for existing records before inserting to avoid duplicate-key errors on repeated runs
- **Data quality validation** — type conversion, null handling, duplicate removal
- **Pipeline automation** — scheduled, unattended daily execution with logging for traceability

## Future Improvements

- Add anomaly/fraud detection using numpy (e.g., flagging transactions with unusual amounts or excessive login attempts)
- Add a daily reconciliation/summary report
- Add proper error handling and alerting (e.g., email on pipeline failure)
- Migrate from Windows Task Scheduler to a dedicated orchestration tool (e.g., Apache Airflow)

## Author

Built as a hands-on data engineering portfolio project.
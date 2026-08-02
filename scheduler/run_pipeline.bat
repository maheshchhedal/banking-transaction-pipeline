@echo off
cd /d E:\banking-transaction-pipeline

call venv\Scripts\activate.bat

python scripts\generate_transactions.py >> logs\pipeline.log 2>&1
python scripts\run_pipeline.py >> logs\pipeline.log 2>&1

echo Pipeline run finished at %date% %time% >> logs\pipeline.log


CREATE DATABASE IF NOT EXISTS banking_pipeline;
USE banking_pipeline;

-- ---------------------------------------
-- Table: dim_account
-- One row per unique account
-- ---------------------------------------
CREATE TABLE IF NOT EXISTS dim_account (
    accountid VARCHAR(50) PRIMARY KEY,
    customerage INT,
    customeroccupation VARCHAR(100)
);

-- ---------------------------------------
-- Table: dim_merchant
-- One row per unique merchant
-- ---------------------------------------
CREATE TABLE IF NOT EXISTS dim_merchant (
    merchantid VARCHAR(50) PRIMARY KEY
);

-- ---------------------------------------
-- Table: fact_transactions
-- One row per transaction, links back to dim_account and dim_merchant
-- ---------------------------------------
CREATE TABLE IF NOT EXISTS fact_transactions (
    transactionid VARCHAR(50) PRIMARY KEY,
    accountid VARCHAR(50),
    merchantid VARCHAR(50),
    transactionamount DECIMAL(12,2),
    transactiondate DATETIME,
    transactiontype VARCHAR(50),
    location VARCHAR(100),
    deviceid VARCHAR(100),
    ip_address VARCHAR(45),
    channel VARCHAR(50),
    transactionduration INT,
    loginattempts INT,
    accountbalance DECIMAL(12,2),

    FOREIGN KEY (accountid) REFERENCES dim_account(accountid),
    FOREIGN KEY (merchantid) REFERENCES dim_merchant(merchantid)
);
-- ============================================================================
-- CUSTOMER CHURN & REVENUE INTELLIGENCE
-- SCRIPT 01: DATABASE AND SCHEMA CREATION
-- Author: Senior Data Analyst & BI Developer
-- Target Systems: PostgreSQL / MySQL / SQLite / Snowflake / SQL Server
-- ============================================================================

-- Drop tables if they already exist (idempotent setup)
DROP TABLE IF EXISTS customer_churn_clean;
DROP TABLE IF EXISTS customer_churn_raw;

-- ----------------------------------------------------------------------------
-- 1. STAGING TABLE (RAW IMPORT)
-- Designed with flexible text columns to prevent load failures on messy data
-- ----------------------------------------------------------------------------
CREATE TABLE customer_churn_raw (
    CustomerID          VARCHAR(50),
    Gender              VARCHAR(20),
    Age                 VARCHAR(20),
    City                VARCHAR(100),
    Tenure_Months       VARCHAR(20),
    Contract_Type       VARCHAR(50),
    Subscription_Plan   VARCHAR(50),
    Monthly_Charges     VARCHAR(50),
    Total_Charges       VARCHAR(50),
    Payment_Method      VARCHAR(100),
    Internet_Service    VARCHAR(50),
    Support_Tickets     VARCHAR(20),
    Last_Login_Date     VARCHAR(50),
    Usage_Hours         VARCHAR(50),
    Discount_Applied    VARCHAR(20),
    Churn_Status        VARCHAR(20),
    Churn_Reason        VARCHAR(255),
    Signup_Date         VARCHAR(50)
);

-- ----------------------------------------------------------------------------
-- 2. PRODUCTION ANALYTICAL TABLE
-- Strongly typed schema with primary keys, constraints, and audit metrics
-- ----------------------------------------------------------------------------
CREATE TABLE customer_churn_clean (
    CustomerID          VARCHAR(20) PRIMARY KEY,
    Gender              VARCHAR(10) NOT NULL CHECK (Gender IN ('Male', 'Female')),
    Age                 INT NOT NULL CHECK (Age >= 18 AND Age <= 120),
    City                VARCHAR(50) NOT NULL,
    Tenure_Months       INT NOT NULL CHECK (Tenure_Months >= 0),
    Contract_Type       VARCHAR(30) NOT NULL CHECK (Contract_Type IN ('Month-to-Month', 'One Year', 'Two Year')),
    Subscription_Plan   VARCHAR(30) NOT NULL CHECK (Subscription_Plan IN ('Basic', 'Standard', 'Premium', 'Enterprise')),
    Monthly_Charges     DECIMAL(10,2) NOT NULL CHECK (Monthly_Charges >= 0),
    Total_Charges       DECIMAL(10,2) NOT NULL CHECK (Total_Charges >= 0),
    Payment_Method      VARCHAR(50) NOT NULL,
    Internet_Service    VARCHAR(30) NOT NULL,
    Support_Tickets     INT NOT NULL DEFAULT 0 CHECK (Support_Tickets >= 0),
    Last_Login_Date     DATE NOT NULL,
    Usage_Hours         DECIMAL(10,1) NOT NULL CHECK (Usage_Hours >= 0),
    Discount_Applied    VARCHAR(10) NOT NULL CHECK (Discount_Applied IN ('Yes', 'No')),
    Churn_Status        VARCHAR(10) NOT NULL CHECK (Churn_Status IN ('Yes', 'No')),
    Churn_Reason        VARCHAR(100) NOT NULL,
    Signup_Date         DATE NOT NULL
);

-- ----------------------------------------------------------------------------
-- 3. PERFORMANCE INDEXES
-- Optimizing query execution for filtering, joins, and aggregations
-- ----------------------------------------------------------------------------
CREATE INDEX idx_churn_status ON customer_churn_clean(Churn_Status);
CREATE INDEX idx_contract_type ON customer_churn_clean(Contract_Type);
CREATE INDEX idx_subscription_plan ON customer_churn_clean(Subscription_Plan);
CREATE INDEX idx_payment_method ON customer_churn_clean(Payment_Method);
CREATE INDEX idx_signup_date ON customer_churn_clean(Signup_Date);

-- ============================================================================
-- DATA IMPORTING INSTRUCTIONS:
--
-- [PostgreSQL]
-- \copy customer_churn_raw FROM 'dataset/customer_churn.csv' WITH (FORMAT csv, HEADER true);
--
-- [MySQL]
-- LOAD DATA INFILE '/path/to/customer_churn.csv'
-- INTO TABLE customer_churn_raw
-- FIELDS TERMINATED BY ',' ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;
--
-- [SQLite CLI]
-- .mode csv
-- .import dataset/customer_churn.csv customer_churn_raw
--
-- [Python / SQLAlchemy automation]
-- df.to_sql('customer_churn_raw', engine, if_exists='append', index=False)
-- ============================================================================

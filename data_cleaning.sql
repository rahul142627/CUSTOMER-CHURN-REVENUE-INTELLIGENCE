-- ============================================================================
-- CUSTOMER CHURN & REVENUE INTELLIGENCE
-- SCRIPT 02: DATA CLEANING & QUALITY AUDITING
-- Author: Senior Data Analyst & BI Developer
-- Business Objective: Validate data integrity, detect anomalies, resolve nulls/blanks,
--                     and prepare production-ready analytical records.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- STEP 1: PRE-CLEANING QUALITY AUDIT
-- ----------------------------------------------------------------------------

-- 1.1 Total raw records check
SELECT COUNT(*) AS total_raw_records FROM customer_churn_raw;

-- 1.2 Duplicate CustomerID detection
-- Business Question: Are there duplicated customer records skewing metrics?
SELECT 
    CustomerID, 
    COUNT(*) AS occurrence_count
FROM customer_churn_raw
GROUP BY CustomerID
HAVING COUNT(*) > 1;

-- 1.3 Audit missing values and blanks across columns
SELECT 
    SUM(CASE WHEN CustomerID IS NULL OR TRIM(CustomerID) = '' THEN 1 ELSE 0 END) AS missing_customer_id,
    SUM(CASE WHEN Monthly_Charges IS NULL OR TRIM(Monthly_Charges) = '' THEN 1 ELSE 0 END) AS missing_monthly_charges,
    SUM(CASE WHEN Total_Charges IS NULL OR TRIM(Total_Charges) = '' THEN 1 ELSE 0 END) AS blank_total_charges,
    SUM(CASE WHEN Churn_Status IS NULL OR TRIM(Churn_Status) = '' THEN 1 ELSE 0 END) AS missing_churn_status,
    SUM(CASE WHEN Internet_Service IS NULL OR TRIM(Internet_Service) = '' THEN 1 ELSE 0 END) AS missing_internet_service
FROM customer_churn_raw;

-- 1.4 Identify specific records with blank Total_Charges
-- Business Question: Why are Total_Charges blank? (Typically new customers with Tenure = 0)
SELECT 
    CustomerID, 
    Tenure_Months, 
    Monthly_Charges, 
    Total_Charges, 
    Signup_Date
FROM customer_churn_raw
WHERE Total_Charges IS NULL OR TRIM(Total_Charges) = '';

-- ----------------------------------------------------------------------------
-- STEP 2: DATA TRANSFORMATION & POPULATION INTO CLEAN TABLE
-- Imputation Strategy:
--  - Total_Charges: If blank or null, impute 0.00 (reflects new customers pending first bill).
--  - Internet_Service: If null or empty, replace with 'None'.
--  - Type Casting: Convert strings to proper INTEGER, DECIMAL, and DATE types.
--  - String Cleaning: TRIM leading/trailing whitespace.
-- ----------------------------------------------------------------------------
INSERT INTO customer_churn_clean (
    CustomerID,
    Gender,
    Age,
    City,
    Tenure_Months,
    Contract_Type,
    Subscription_Plan,
    Monthly_Charges,
    Total_Charges,
    Payment_Method,
    Internet_Service,
    Support_Tickets,
    Last_Login_Date,
    Usage_Hours,
    Discount_Applied,
    Churn_Status,
    Churn_Reason,
    Signup_Date
)
SELECT 
    TRIM(CustomerID) AS CustomerID,
    TRIM(Gender) AS Gender,
    CAST(Age AS INT) AS Age,
    TRIM(City) AS City,
    CAST(Tenure_Months AS INT) AS Tenure_Months,
    TRIM(Contract_Type) AS Contract_Type,
    TRIM(Subscription_Plan) AS Subscription_Plan,
    CAST(Monthly_Charges AS DECIMAL(10,2)) AS Monthly_Charges,
    -- Handle blank / whitespace Total_Charges gracefully
    CASE 
        WHEN Total_Charges IS NULL OR TRIM(Total_Charges) = '' THEN 0.00
        ELSE CAST(TRIM(Total_Charges) AS DECIMAL(10,2))
    END AS Total_Charges,
    TRIM(Payment_Method) AS Payment_Method,
    -- Handle missing / null Internet Service
    CASE 
        WHEN Internet_Service IS NULL OR TRIM(Internet_Service) = '' THEN 'None'
        ELSE TRIM(Internet_Service)
    END AS Internet_Service,
    CAST(COALESCE(NULLIF(TRIM(Support_Tickets), ''), '0') AS INT) AS Support_Tickets,
    CAST(TRIM(Last_Login_Date) AS DATE) AS Last_Login_Date,
    CAST(TRIM(Usage_Hours) AS DECIMAL(10,1)) AS Usage_Hours,
    TRIM(Discount_Applied) AS Discount_Applied,
    TRIM(Churn_Status) AS Churn_Status,
    TRIM(Churn_Reason) AS Churn_Reason,
    CAST(TRIM(Signup_Date) AS DATE) AS Signup_Date
FROM customer_churn_raw;

-- ----------------------------------------------------------------------------
-- STEP 3: POST-CLEANING VALIDATION
-- ----------------------------------------------------------------------------

-- Verify clean record count matches raw record count
SELECT 
    (SELECT COUNT(*) FROM customer_churn_raw) AS raw_row_count,
    (SELECT COUNT(*) FROM customer_churn_clean) AS clean_row_count,
    CASE 
        WHEN (SELECT COUNT(*) FROM customer_churn_raw) = (SELECT COUNT(*) FROM customer_churn_clean)
        THEN 'Data Cleaning Audit PASSED (100% Integrity)'
        ELSE 'Data Cleaning Audit FAILED'
    END AS reconciliation_status;

-- Verify no negative values exist in numerical columns
SELECT 
    COUNT(*) AS invalid_records
FROM customer_churn_clean
WHERE Monthly_Charges < 0 
   OR Total_Charges < 0 
   OR Tenure_Months < 0 
   OR Usage_Hours < 0;

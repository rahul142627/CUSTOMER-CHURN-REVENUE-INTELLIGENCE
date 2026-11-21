-- ============================================================================
-- CUSTOMER CHURN & REVENUE INTELLIGENCE
-- SCRIPT 03: CUSTOMER BEHAVIOR & COHORT ANALYSIS
-- Author: Senior Data Analyst & BI Developer
-- Business Objective: Profile customer demographics, evaluate tenure lifecycles,
--                     identify customer friction points, and analyze engagement.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. EXECUTIVE KPI SUMMARY: CUSTOMER COUNTS & CHURN RATE
-- Business Question: What is the company's current active customer base and churn rate?
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn_Status = 'No' THEN 1 ELSE 0 END) AS active_customers,
    SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'No' THEN 1 ELSE 0 END) / COUNT(*), 2) AS retention_rate_pct
FROM customer_churn_clean;

-- ----------------------------------------------------------------------------
-- 2. DEMOGRAPHIC SEGMENTATION: AGE BRACKET ANALYSIS
-- Business Question: Does customer age influence retention and churn propensity?
-- ----------------------------------------------------------------------------
WITH age_segments AS (
    SELECT 
        CustomerID,
        Age,
        Churn_Status,
        CASE 
            WHEN Age < 25 THEN '1. Under 25 (Young Adult)'
            WHEN Age BETWEEN 25 AND 39 THEN '2. 25-39 (Early Career)'
            WHEN Age BETWEEN 40 AND 54 THEN '3. 40-54 (Mid Career)'
            WHEN Age BETWEEN 55 AND 64 THEN '4. 55-64 (Mature)'
            ELSE '5. 65+ (Senior)'
        END AS age_group
    FROM customer_churn_clean
)
SELECT 
    age_group,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn_Status = 'No' THEN 1 ELSE 0 END) AS active_customers,
    SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customer_churn_clean), 2) AS pct_of_total_base
FROM age_segments
GROUP BY age_group
ORDER BY age_group;

-- ----------------------------------------------------------------------------
-- 3. GEOGRAPHIC DISTRIBUTION & REGIONAL CHURN
-- Business Question: Are specific metropolitan markets experiencing higher attrition?
-- ----------------------------------------------------------------------------
SELECT 
    City,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn_Status = 'No' THEN 1 ELSE 0 END) AS active_customers,
    SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(Monthly_Charges), 2) AS avg_monthly_spend,
    RANK() OVER (ORDER BY ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) DESC) AS churn_rank
FROM customer_churn_clean
GROUP BY City
ORDER BY churn_rate_pct DESC;

-- ----------------------------------------------------------------------------
-- 4. TENURE COHORT ANALYSIS (LIFECYCLE ATTRITION)
-- Business Question: At what stage of the customer lifecycle is attrition most severe?
-- ----------------------------------------------------------------------------
WITH tenure_buckets AS (
    SELECT 
        CustomerID,
        Tenure_Months,
        Churn_Status,
        Monthly_Charges,
        CASE 
            WHEN Tenure_Months <= 6 THEN '01. 0-6 Months (Onboarding Risk)'
            WHEN Tenure_Months BETWEEN 7 AND 12 THEN '02. 7-12 Months (First Year)'
            WHEN Tenure_Months BETWEEN 13 AND 24 THEN '03. 13-24 Months (Established)'
            WHEN Tenure_Months BETWEEN 25 AND 48 THEN '04. 25-48 Months (Mature)'
            ELSE '05. 49+ Months (Long-Term Loyalist)'
        END AS tenure_cohort
    FROM customer_churn_clean
)
SELECT 
    tenure_cohort,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cohort_churn_rate_pct,
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / 
          (SELECT SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) FROM customer_churn_clean), 2) AS pct_of_all_churns,
    ROUND(AVG(Monthly_Charges), 2) AS avg_monthly_charges
FROM tenure_buckets
GROUP BY tenure_cohort
ORDER BY tenure_cohort;

-- ----------------------------------------------------------------------------
-- 5. SUPPORT TICKET FRICTION & ESCALATION ANALYSIS
-- Business Question: What is the relationship between customer support escalations
--                    and churn? At what ticket threshold does churn spike?
-- ----------------------------------------------------------------------------
SELECT 
    Support_Tickets,
    COUNT(*) AS customer_count,
    SUM(CASE WHEN Churn_Status = 'No' THEN 1 ELSE 0 END) AS active_count,
    SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(Usage_Hours), 1) AS avg_usage_hours,
    ROUND(AVG(Monthly_Charges), 2) AS avg_monthly_charges
FROM customer_churn_clean
GROUP BY Support_Tickets
ORDER BY Support_Tickets ASC;

-- ----------------------------------------------------------------------------
-- 6. PLATFORM ENGAGEMENT (USAGE HOURS VS CHURN)
-- Business Question: Are disengaged users significantly more likely to cancel?
-- ----------------------------------------------------------------------------
WITH usage_segments AS (
    SELECT 
        CustomerID,
        Usage_Hours,
        Churn_Status,
        Monthly_Charges,
        CASE 
            WHEN Usage_Hours < 20 THEN '1. Dormant (<20 hrs/mo)'
            WHEN Usage_Hours BETWEEN 20 AND 59.9 THEN '2. Moderate (20-60 hrs/mo)'
            WHEN Usage_Hours BETWEEN 60 AND 119.9 THEN '3. Active (60-120 hrs/mo)'
            ELSE '4. Power User (120+ hrs/mo)'
        END AS engagement_level
    FROM customer_churn_clean
)
SELECT 
    engagement_level,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(Monthly_Charges), 2) AS avg_monthly_charges
FROM usage_segments
GROUP BY engagement_level
ORDER BY engagement_level;

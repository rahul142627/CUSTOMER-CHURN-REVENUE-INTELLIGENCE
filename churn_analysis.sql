-- ============================================================================
-- CUSTOMER CHURN & REVENUE INTELLIGENCE
-- SCRIPT 05: CHURN DRIVERS, RISK SCORING & RETENTION INTELLIGENCE
-- Author: Senior Data Analyst & BI Developer
-- Business Objective: Pinpoint root causes of attrition, identify high-value
--                     accounts at imminent risk, and quantify revenue exposure.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. CHURN DRIVERS: CONTRACT TYPE X PAYMENT METHOD INTERACTION
-- Business Question: What combination of payment method and contract carries the
--                    deadliest churn risk?
-- ----------------------------------------------------------------------------
SELECT 
    Contract_Type,
    Payment_Method,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn_Status = 'Yes' THEN Monthly_Charges ELSE 0 END), 2) AS mrr_lost,
    DENSE_RANK() OVER (ORDER BY ROUND(100.0 * SUM(CASE WHEN Churn_Status = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) DESC) AS risk_rank
FROM customer_churn_clean
GROUP BY Contract_Type, Payment_Method
ORDER BY churn_rate_pct DESC;

-- ----------------------------------------------------------------------------
-- 2. ROOT CAUSE ATTRIBUTION: CHURN REASONS & REVENUE IMPACT
-- Business Question: What are the exact stated reasons customers leave, and how
--                    much monthly revenue is lost to each specific cause?
-- ----------------------------------------------------------------------------
SELECT 
    Churn_Reason,
    COUNT(*) AS churned_customer_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customer_churn_clean WHERE Churn_Status = 'Yes'), 2) AS pct_of_total_churns,
    ROUND(SUM(Monthly_Charges), 2) AS monthly_revenue_lost,
    ROUND(SUM(Monthly_Charges) * 12, 2) AS annualized_revenue_lost,
    ROUND(AVG(Monthly_Charges), 2) AS avg_monthly_charges_lost,
    ROUND(AVG(Tenure_Months), 1) AS avg_tenure_at_exit
FROM customer_churn_clean
WHERE Churn_Status = 'Yes'
GROUP BY Churn_Reason
ORDER BY monthly_revenue_lost DESC;

-- ----------------------------------------------------------------------------
-- 3. HIGH-VALUE CUSTOMERS AT RISK (IMMEDIATE EXECUTIVE INTERVENTION LIST)
-- Business Question: Which active, high-spending VIP customers are exhibiting multiple
--                    strong churn signals right now?
-- ----------------------------------------------------------------------------
SELECT 
    CustomerID,
    City,
    Subscription_Plan,
    Contract_Type,
    Monthly_Charges,
    Total_Charges,
    Tenure_Months,
    Support_Tickets,
    Usage_Hours,
    Payment_Method,
    Last_Login_Date
FROM customer_churn_clean
WHERE Churn_Status = 'No'
  AND Monthly_Charges >= 85.00                -- High value account
  AND Contract_Type = 'Month-to-Month'         -- High flight flexibility
  AND Support_Tickets >= 3                     -- Friction indicator
  AND Usage_Hours < 50.0                       -- Low engagement indicator
ORDER BY Monthly_Charges DESC, Support_Tickets DESC;

-- ----------------------------------------------------------------------------
-- 4. MULTI-ATTRIBUTE CHURN RISK SCORING MODEL (SQL IMPLEMENTATION)
-- Business Question: How can we algorithmically categorize all active customers
--                    into Low, Medium, High, and Critical Risk tiers?
-- ----------------------------------------------------------------------------
WITH active_scored AS (
    SELECT 
        CustomerID,
        Subscription_Plan,
        Contract_Type,
        Monthly_Charges,
        Tenure_Months,
        Support_Tickets,
        Usage_Hours,
        Payment_Method,
        -- Point-based risk scoring algorithm
        (
            CASE WHEN Contract_Type = 'Month-to-Month' THEN 35 ELSE 0 END +
            CASE WHEN Support_Tickets >= 4 THEN 30 
                 WHEN Support_Tickets >= 2 THEN 15 ELSE 0 END +
            CASE WHEN Payment_Method = 'Electronic Check' THEN 15 ELSE 0 END +
            CASE WHEN Tenure_Months <= 6 THEN 15 
                 WHEN Tenure_Months <= 12 THEN 8 ELSE 0 END +
            CASE WHEN Usage_Hours < 25 THEN 15 
                 WHEN Usage_Hours < 50 THEN 8 ELSE 0 END
        ) AS risk_score
    FROM customer_churn_clean
    WHERE Churn_Status = 'No'
),
risk_categorized AS (
    SELECT 
        *,
        CASE 
            WHEN risk_score >= 70 THEN 'Critical Risk (Immediate Action)'
            WHEN risk_score >= 50 THEN 'High Risk'
            WHEN risk_score >= 30 THEN 'Medium Risk'
            ELSE 'Low Risk (Healthy)'
        END AS risk_tier
    FROM active_scored
)
SELECT 
    risk_tier,
    COUNT(*) AS customer_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM active_scored), 2) AS pct_of_active_base,
    ROUND(SUM(Monthly_Charges), 2) AS monthly_revenue_at_risk,
    ROUND(SUM(Monthly_Charges) * 12, 2) AS annualized_revenue_at_risk,
    ROUND(AVG(Monthly_Charges), 2) AS avg_monthly_charges,
    ROUND(AVG(risk_score), 1) AS avg_risk_score
FROM risk_categorized
GROUP BY risk_tier
ORDER BY avg_risk_score DESC;

-- ----------------------------------------------------------------------------
-- 5. COHORT RETENTION HEATMAP DATA GENERATION
-- Business Question: What percentage of customers acquired in each half-year cohort
--                    remain active after various tenure milestones?
-- ----------------------------------------------------------------------------
WITH cohort_base AS (
    SELECT 
        SUBSTR(Signup_Date, 1, 4) || '-H' || CASE WHEN CAST(SUBSTR(Signup_Date, 6, 2) AS INT) <= 6 THEN '1' ELSE '2' END AS signup_half_year,
        COUNT(*) AS cohort_size,
        SUM(CASE WHEN Tenure_Months >= 6 AND Churn_Status = 'No' THEN 1 ELSE 0 END) AS retained_6m,
        SUM(CASE WHEN Tenure_Months >= 12 AND Churn_Status = 'No' THEN 1 ELSE 0 END) AS retained_12m,
        SUM(CASE WHEN Tenure_Months >= 24 AND Churn_Status = 'No' THEN 1 ELSE 0 END) AS retained_24m
    FROM customer_churn_clean
    GROUP BY signup_half_year
)
SELECT 
    signup_half_year,
    cohort_size,
    retained_6m,
    ROUND(100.0 * retained_6m / cohort_size, 1) AS retention_rate_6m_pct,
    retained_12m,
    ROUND(100.0 * retained_12m / cohort_size, 1) AS retention_rate_12m_pct,
    retained_24m,
    ROUND(100.0 * retained_24m / cohort_size, 1) AS retention_rate_24m_pct
FROM cohort_base
ORDER BY signup_half_year DESC;
